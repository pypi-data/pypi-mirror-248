# -*- coding: utf-8 -*-
import numpy, tempfile, copy
# import ffmpeg, pathlib, os
import ffmpeg
from loguru import logger
import sox
from pathlib import Path
from rich import print
from itertools import groupby
# import opentimelineio as otio
from datetime import timedelta
import pprint, shutil, os

from inspect import currentframe, getframeinfo
try:
    from . import yaltc
except:
    import yaltc

CLUSTER_GAP = 0.5 # secs between multicam clusters

# utility for accessing pathnames
def _pathname(tempfile_or_path):
    if isinstance(tempfile_or_path, str):
        return tempfile_or_path
    if isinstance(tempfile_or_path, yaltc.Recording):
        return str(tempfile_or_path.AVpath)
    if isinstance(tempfile_or_path, Path):
        return str(tempfile_or_path)
    if isinstance(tempfile_or_path, tempfile._TemporaryFileWrapper):
        return tempfile_or_path.name
    else:
        raise Exception('%s should be Path or tempfile...'%tempfile_or_path)


# utility for changing path suffix to wav
# def _make_ISO_path(path):
#     parts = path.parts
#     parents = parts[:-1]
#     base = parts[-1]
#     base_WO_suffix = base.split('.')[0]
#     return Path().joinpath(*parents, base_WO_suffix + '.iso')

# utility for extracting one audio channel
def _extr_channel(source, dest, channel):
    # int channel = 1 for first channel
    # print(dest.name)
    if dest.name == 'none.wav':
        return
    sox_transform = sox.Transformer()
    mix_dict = {1:[channel]}
    logger.debug('sox args %s %s %s'%(source, dest, mix_dict))    
    sox_transform.remix(mix_dict)
    # sox_transform.remix(mix_dict, num_output_channels=1)
    # sox_transform.set_output_format(channels=1)
    logger.debug('sox transform %s'%str(sox_transform))
    status = sox_transform.build(str(source), str(dest))
    logger.debug('sox status %s'%status)

# def _split_channels(source, destinations=None):
#     # split all chnnels to distinations filename
#     nchan = sox.file_info.channels(str(source))
#     if not destinations:
#         for n in range(nchan):
#             _extr_channel(source, 'chan_%i.wav'%n, n+1)

# utility for printing groupby results
def print_grby(grby):
    for key, keylist in grby:
        print('\ngrouped by %s:'%key)
        for e in keylist:
            print(' ', e)

# deltatime utility
def from_midnight(a_datetime):
    # returns a deltatime from a datetime, skipping the date
    return(timedelta(hours=a_datetime.hour, minutes=a_datetime.minute,
                     seconds=a_datetime.second,
                     microseconds=a_datetime.microsecond))

class AudioStitcherVideoMerger:
    """
    Typically each found video is associated with an AudioStitcherVideoMerger
    instance. AudioStitcherVideoMerger does the actual audio-video file
    processing of merging self.ref_recording (gen. a video) with all audio
    files in  self.matched_audio_recordings as determined by the Matcher
    object (it instanciates and manages AudioStitcherVideoMerger objects).

    All audio file edits are done using pysox and video+audio merging with
    ffmpeg. When necessary, clock drift is corrected for all overlapping audio
    devices to match the precise clock value of the ref recording (to a few
    ppm), using sox tempo transform.

    N.B.: A audio_stitch doesn't extend beyond the corresponding ref_recording
    video start and end times: it is not a audio montage for the whole movie
    project.


    Attributes:

        ref_recording : a Recording instance
            The video (or designated main sound) audio files are synced to

        matched_audio_recordings : list

            audio recordings that intersect ref_recording in time, set by
            Timeline.scan_audio_for_each_ref_rec() in AudioStitcherVideoMerger.add_matched_audio

        edited_audio : dict {Recording : path}

            keys are elements of matched_audio_recordings of class Recording
            and the value stores the Pathlib path of the eventual edited
            audio (trimmed , padded or time stretched). Before building the
            audio_montage, path points to the initial
            Recording.media_without_YaLTC


    """

    def __init__(self, reference_recording):
        self.ref_recording = reference_recording
        self.matched_audio_recordings = []
        self.edited_audio = {}
        # self.result_video_file = None
        logger.debug('instantiating AudioStitcherVideoMerger for %s'%reference_recording)

    def add_matched_audio(self, audio_rec):
        # if the recording has been previously edited in another AudioStitcherVideoMerger
        # reset its edited_version
        # audio_rec.edited_version = audio_rec.media_without_YaLTC
        self.edited_audio[audio_rec] = audio_rec.media_without_YaLTC
        self.matched_audio_recordings.append(audio_rec)

    def _get_audio_devices(self):
        # ex {'RCR_A', 'RCR_B', 'RCR_C'} if multisound
        return set([r.device for r in self.matched_audio_recordings])

    def _get_all_recordings_for(self, device):
        # return recordings for a particular device, sorted by time
        recs = [a for a in self.matched_audio_recordings if a.device == device]
        recs.sort(key=lambda r: r.start_time)
        return recs

    def _dedrift_rec(self, rec):
        # first_audio_p = rec.AVpath
        initial_duration = sox.file_info.duration(
            _pathname(rec.media_without_YaLTC))
        sox_transform = sox.Transformer()
        # tempo_scale_factor = rec.device_relative_speed
        tempo_scale_factor = rec.device_relative_speed
        print('rec %s needs to be time stretched: speed %f'%(rec,
            tempo_scale_factor))
        if tempo_scale_factor > 1:
            print('device clock too fast (rel to ref):file too long')
        else:
           print('device clock too slow (rel to ref):file too short')             
        sox_transform.tempo(tempo_scale_factor)
        # scaled_file = self._get_soxed_file(rec, sox_transform)
        logger.debug('sox_transform %s'%sox_transform.effects)
        self._edit_audio_file(rec, sox_transform)
        scaled_file_name = _pathname(self.edited_audio[rec])
        new_duration = sox.file_info.duration(scaled_file_name)
        # goal_duration = rec.get_corrected_duration()
        logger.debug('initial_duration %f new_duration %f ratio:%f'%(
            initial_duration, new_duration, initial_duration/new_duration))

    def _get_concatenated_audiofile_for(self, device):

        """
        return a handle for the final audio file formed by all detected
        overlapping recordings, produced by the same specified device.
        
        """
        logger.debug('concatenating device %s'%str(device))
        recordings = self._get_all_recordings_for(device)
        # [TODO here] Check if all unidentified device files are not
        # overlapping because they are considered produced by the same
        # device. If some overlap then necessarily they're from different
        # ones. List the files and warn the user there is a risk of error if
        # they're not from the same device.

        logger.debug('%i audio files for reference rec %s:'%(len(recordings),
            self.ref_recording))
        for r in recordings:
            logger.debug('  %s'%r)
        speeds = numpy.array([rec.get_speed_ratio(self.ref_recording)
                                    for rec in recordings])
        mean_speed = numpy.mean(speeds)
        for r in recordings:
            r.device_relative_speed = mean_speed
            # r.device_relative_speed = 0.9
            logger.debug('set device_relative_speed for %s'%r)
            logger.debug(' value: %f'%r.device_relative_speed)
            r.set_time_position_to(self.ref_recording)
            logger.debug('time_position for %s: %fs relative to %s'%(r,
                r.time_position, self.ref_recording))

        # st_dev_speeds just to check for anomalous situation
        st_dev_speeds = numpy.std(speeds)
        logger.debug('mean speed for %s: %.6f std dev: %.0e'%(device,
                                                    mean_speed,
                                                    st_dev_speeds))
        if st_dev_speeds > 1.0e-5:
            logger.error('too much variation for device speeds')
            quit()
        # Because of length
        # transformations with pysox.tempo, it is not the sum of REC durations
        #
        #         ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        #         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ref
        #           ┏━━━━┓   ┏━━━━┓
        #         ┣━┻━━━━┻━━━┻━━━━┛ growing_file
        #
        #         ├───────────────┤
        #                      end_time
        #


        # process first element 'by hand' outside the loop
        # first_audio is a Recording, not a path nor filehandle
        first_audio = recordings[0]
        needs_dedrift, delta = first_audio.needs_dedrifting()
        logger.debug('first audio is %s'%first_audio)
        logger.debug('checking drift, first audio: delta of %0.2f ms'%(
            delta*1e3))
        if needs_dedrift:
            self._dedrift_rec(first_audio)
        else:
            logger.debug('no time stretch for 1st audio')        
        self._pad_or_trim_first_audio(first_audio)
        # loop for the other files
        # growing_file = first_audio.edited_version
        growing_file = self.edited_audio[first_audio]
        for i, rec in enumerate(recordings[1:]):
            logger.debug('Padding and joining for %s'%rec)
            needs_dedrift, delta = rec.needs_dedrifting()
            logger.debug('next audio is %s'%rec)
            logger.debug('checking drift for next audio, delta of %0.2f ms'%(
                delta*1e3))
            if needs_dedrift:
                # logger.debug('dedrifting too...delta of %0.2f ms'%(delta*1e3))
                self._dedrift_rec(rec)
            else:
                logger.debug('no dedrifting')        
            end_time = sox.file_info.duration(growing_file.name)
            logger.debug('  growing_file %s'%(growing_file.name))
            logger.debug('  growing_file duration %.2f'%(end_time))
            logger.debug('  rec.time_position  for next audio %s %.2f'%(rec,
                rec.time_position))
            # TODO check if rec.needs_dedrifting() before padding
            pad_duration = rec.time_position - end_time
            self._pad_file(rec, pad_duration)
            # new_file = rec.edited_version
            new_file = self.edited_audio[rec]
            growing_file = self._concatenate_audio_files(growing_file, new_file)
        end_time = sox.file_info.duration(growing_file.name)
        logger.debug('total edited audio duration  %.2f s'%end_time)
        return growing_file

    def _pad_or_trim_first_audio(self, first_rec):
        """
        TODO: check if first_rec is a Recording or tempfile (maybe a tempfile if dedrifted)
        NO: will change tempo after trimming/padding

        Store (into Recording.edited_audio dict) the handle  of the sox processed
        first recording, padded or chopped according to AudioStitcherVideoMerger.ref_recording
        starting time. Length of the written file can differ from length of the
        submitted Recording object if drift is corrected with sox tempo
        transform, so check it with sox.file_info.duration()
        """
        logger.debug(' editing %s'%first_rec)
        audio_start  = first_rec.get_start_time()
        ref_start = self.ref_recording.get_start_time()
        if ref_start < audio_start: # padding
            logger.debug('padding')
            pad_duration  = (audio_start-ref_start).total_seconds()
            """padding first_file:
                    ┏━━━━━━━━━━━━━━━┓
                    ┗━━━━━━━━━━━━━━━┛ref
                      ┏━━━━━━┓
                    ┣━┻━━━━━━┛
            """
            self._pad_file(first_rec, pad_duration)
        else:
            logger.debug('trimming')
            length = (ref_start-audio_start).total_seconds()
            """chopping first_file:
                    ┏━━━━━━━━━━━━━━━┓
                    ┗━━━━━━━━━━━━━━━┛ref
                  ┏━╋━━━━┓
                  ┗━┻━━━━┛
            """
            self._chop_file(first_rec, length)
        return

    def _concatenate_audio_files(self, f1, f2):
        # return a tmp file object resulting in f1 f2 concatenation
        # on exit f1 and f2 are closed()
        cbn = sox.Combiner()
        out_file = tempfile.NamedTemporaryFile(suffix='.wav',  delete=True)
        out_file_name = out_file.name
        status = cbn.build(
            [f1.name, f2.name],
            out_file_name,
            combine_type='concatenate',
            )
        logger.debug('sox.build exit code %s'%str(status))
        f1.close()
        f2.close()
        return out_file

    def _pad_file(self, recording, pad_duration):
        # set recording.edited_version to the handle file a sox padded audio
        sox_transform = sox.Transformer()
        sox_transform.pad(pad_duration)
        logger.debug('sox_transform.pad arg: %f secs'%pad_duration)
        self._edit_audio_file(recording, sox_transform)

    def _chop_file(self, recording, length):
        # set recording.edited_version to the handle file a sox chopped audio
        sox_transform = sox.Transformer()
        sox_transform.trim(length)
        logger.debug('sox_transform.trim arg: %f secs'%length)
        self._edit_audio_file(recording, sox_transform)

    def _edit_audio_file(self, audio_rec, sox_transform):
        """
        Apply the specified sox_transform onto the audio_rec and update
        self.edited_audio dict with the result (with audio_rec as the key)
        """
        output_fh = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        logger.debug('transform: %s'%sox_transform.effects)
        recording_path = self.edited_audio[audio_rec]
        input_file = _pathname(recording_path)
        out_file = _pathname(output_fh)
        logger.debug('sox in and out files: %s %s'%(input_file, out_file))
        status = sox_transform.build(input_file, out_file, return_output=True )
        logger.debug('sox.build exit code %s'%str(status))
        # audio_rec.edited_version = output_fh
        self.edited_audio[audio_rec] = output_fh

    def _parse_track_values(self, tracks_file):
        file=open(tracks_file,"r")
        # tracks = 
        # tracks = [l for l in tracks.splitlines() ]
        tracks_lines = [l for l in file.read().splitlines() if len(l) > 0 and l[0] != '#']
        track_names = [l.split()[0] for l in tracks_lines if l != 'ttc']
        return track_names

    def build_audio_and_write_video(self, top_dir, IO_structure):
        """
        IO_structure is either: loose | strict

        For each audio devices found, pad, trim or stretch audio files
        overlapping self.ref_recording,
        calling _get_concatenated_audiofile_for(), and put them in
        merged_audio_files_by_device. More than one audio recorder can be
        used for a shot: that's why merged_audio_files_by_device is a list

        Returns nothing

        Sets self.final_synced_file on completion
        """
        match IO_structure:
            case 'strict':
                tictacsynced_dir = Path(top_dir)/'SyncedClips'
                tictacsynced_dir.mkdir(exist_ok=True)
                output_dir = tictacsynced_dir/Path(self.ref_recording.device.name)
                output_dir.mkdir(exist_ok=True)
            case 'loose':
                output_dir = Path(top_dir)
        output_path = output_dir/Path(self.ref_recording.new_rec_name).name
        logger.debug('editing files for %s'%output_path)
        merged_audio_files_by_device = [
                            (d, self._get_concatenated_audiofile_for(d)) 
                            for d in self._get_audio_devices()]
        if len(merged_audio_files_by_device) > 1:
            logger.error('more than one audio device... not yet implemented')
            quit()
        if len(merged_audio_files_by_device) == 0:
            # no audio file overlaps for this one
            return
        device, joined_audio = merged_audio_files_by_device[0] # [TO DO] multi audio recorders
        logger.debug('device, joined_audio %s %s'%(device, joined_audio))
        joined_audio = joined_audio.name # [TO DO] multi audio recorders
        if IO_structure == 'strict':
            # generates ISOs too
            # ISOdir = _make_ISO_path(output_path)
            audio_folder = device.folder
            tracks_file = audio_folder/'tracks.txt'
            track_names = False
            if os.path.isfile(tracks_file):
                track_names = self._parse_track_values(tracks_file)
                # print(track_names)
            video_stem_WO_suffix = output_path.stem.split('.')[0]
            ISOdir = Path(top_dir)/'ISOs'
            ISOdir.mkdir(exist_ok=True)
            ISOdir = Path(top_dir)/'ISOs'/video_stem_WO_suffix
            ISOdir.mkdir(exist_ok=True)            # audio_name = output_path.stem + '.wav'
            ISO_multi_chan = ISOdir / 'all.wav'
            logger.debug('will split audio to %s'%(ISOdir))
            shutil.copy(joined_audio, ISO_multi_chan)
            # audio_name = Path(os.getcwd())/audio_name
            nchan = sox.file_info.channels(str(ISO_multi_chan))
            if track_names and nchan != len(track_names):
                print('error parsing %s content'%tracks_file)
                print('incoherent number of tracks, quitting\n')
                quit()
            for n in range(nchan):
                if track_names:
                    iso_destination = ISOdir / (track_names[n]+'.wav')
                else:
                    iso_destination = ISOdir / ('chan_%i.wav'%n)
                logger.debug('iso_destination %s'%iso_destination)
                _extr_channel(ISO_multi_chan, iso_destination, n+1)
            os.remove(ISO_multi_chan)
        video_path = self.ref_recording.AVpath
        logger.debug('will merge with %s'%(joined_audio))
        self._merge_audio_and_video(joined_audio, output_path)
        self.ref_recording.final_synced_file = output_path # relative

    def _keep_VIDEO_only(self, video_path):
        # return file handle to a temp video file formed from the video_path
        # stripped of its sound
        in1 = ffmpeg.input(_pathname(video_path))
        video_extension = video_path.suffix
        silenced_opts = ["-loglevel", "quiet", "-nostats", "-hide_banner"]
        file_handle = tempfile.NamedTemporaryFile(suffix=video_extension,
            delete=False)
        out1 = in1.output(file_handle.name, map='0:v', vcodec='copy')
        ffmpeg.run([out1.global_args(*silenced_opts)], overwrite_output=True)
        return file_handle
        # os.path.split audio channels if more than one

    def _merge_audio_and_video(self, audio_path, output_path):
        # call ffmpeg to join audio and video

        video_path = self.ref_recording.AVpath
        timecode = self.ref_recording.get_timecode()
        self.ref_recording.synced_audio = audio_path
        vid_only_handle = self._keep_VIDEO_only(video_path)
        a_n = str(audio_path)
        v_n = str(vid_only_handle.name)
        out_n = str(output_path)
        logger.debug('Merging: \n\t %s + %s = %s\n'%(
                        audio_path,
                        video_path,
                        output_path
                        ))
        # building args for debug purpose only:
        ffmpeg_args = (
            ffmpeg
            .input(v_n)
            .output(out_n, shortest=None, vcodec='copy', acodec='copy',
                timecode=timecode)
            .global_args('-i', a_n, "-hide_banner")
            .overwrite_output()
            .get_args()
        )
        logger.debug('ffmpeg args: %s'%' '.join(ffmpeg_args))
        try: # for real now
            _, out = (
            ffmpeg
            .input(v_n)
            .output(out_n, shortest=None, vcodec='copy', acodec='copy',
                # metadata='reel_name=foo', not all container support gen MD
                timecode=timecode,
                )
            .global_args('-i', a_n, "-hide_banner")
            .overwrite_output()
            .run(capture_stderr=True)
            )
            logger.debug('ffmpeg output')
            for l in out.decode("utf-8").split('\n'):
                logger.debug(l)
        except ffmpeg.Error as e:
            logger.error('ffmpeg.run error')
            logger.error(e)
            logger.error(e.stderr)


class Matcher:
    """
    Matcher looks for any video in self.recordings and for each one finds out
    all audio recordings (again in self.recordings) that time overlap
    (or against any designated 'main sound', see below). It then spawns
    AudioStitcherVideoMerger objects that do the actual file manipulations. Each video
    (and main sound) will have its AudioStitcherVideoMerger instance.

    All videos are de facto reference recording and matching audio files are
    looked up for each one of them.

    The Matcher doesn't keep neither set any editing information in itself: the
    in and out time values (UTC times) used are those kept inside each Recording
    instances.

    [NOT YET IMPLEMENTED]: When shooting is done with multiple audio recorders,
    ONE audio device can be designated as 'main sound' and used as reference
    recording; then all audio tracks are synced together against this main
    sound audio file, keeping the YaLTC track alongside for syncing against
    their video counterpart(in a second pass and after a mixdown editing).
    [/NOT YET IMPLEMENTED]

    Attributes:

        recordings : list of Recording instances
            all the scanned recordings with valid YaLTC, set in __init__()

        video_mergers : list
            of AudioStitcherVideoMerger Class instances, built by
            scan_audio_for_each_ref_rec(); each video has a corresponding
            AudioStitcherVideoMerger object. An audio_stitch doesn't extend
            beyond the corresponding video start and end times.

    """

    def __init__(self, recordings_list, IO_structure):
        """        
        At this point in the program, all recordings in recordings_list should
        have a valid Recording.start_time attribute and one of its channels
        containing a YaLTC signal (which the start_time has been demodulated
        from)
        
        """
        self.recordings = recordings_list
        self.video_mergers = []
        self._rename_all_recs(IO_structure)


    def _rename_all_recs(self, IO_structure):
        """
        Add _synced to filenames of synced video files. Change stored name only:
        files have yet to be written to.
        """
        match IO_structure:
            case 'strict':
                for rec in self.recordings:
                    rec_extension = rec.AVpath.suffix
                    rel_path_new_name = '%s%s'%(rec.AVpath.stem, rec_extension)
                    rec.new_rec_name = Path(rel_path_new_name)
                    logger.debug('for %s new name: %s'%(
                        _pathname(rec.AVpath),
                        _pathname(rec.new_rec_name)))
            case 'loose':
                for rec in self.recordings:
                    rec_extension = rec.AVpath.suffix
                    rel_path_new_name = '%s%s%s'%('ttsd_',rec.AVpath.stem, rec_extension)
                    rec.new_rec_name = Path(rel_path_new_name)
                    logger.debug('for %s new name: %s'%(
                        _pathname(rec.AVpath),
                        _pathname(rec.new_rec_name)))

    def scan_audio_for_each_ref_rec(self):
        """
        For each video (and for the Main Sound) in self.recordings, this finds
        any audio that has overlapping times and instantiates a
        AudioStitcherVideoMerger object.

        V1 checked against A1, A2, A3, A4
        V2 checked against A1, A2, A3, A4
        V3 checked against    ...
        Main Sound checked against A1, A2, A3, A4
        """
        refeference_recordings = [r for r in self.recordings if r.is_video()
                                                            or r.is_reference]
        audio_recs = [r for r in self.recordings if r.is_audio()
                                                and not r.is_reference]
        if not audio_recs:
            print('\nNo audio recording found, syncing of videos only not implemented yet, exiting...\n')
            quit()
        for ref_rec in refeference_recordings:
            reference_tag = 'video' if ref_rec.is_video() else 'audio'
            logger.debug('Looking for overlaps with %s %s'%(
                                                        reference_tag,
                                                        ref_rec))
            audio_stitch = AudioStitcherVideoMerger(ref_rec)
            for audio in audio_recs:
                if self._does_overlap(ref_rec, audio):
                    audio_stitch.add_matched_audio(audio)
                    logger.debug('recording %s overlaps,'%(audio))
                    # print('  recording [gold1]%s[/gold1] overlaps,'%(audio))
            if len(audio_stitch.matched_audio_recordings) > 0:
                self.video_mergers.append(audio_stitch)
            else:
                logger.debug('\n  nothing\n')
                print('No overlap found for %s'%ref_rec.AVpath.name)
                del audio_stitch
        logger.debug('%i video_mergers created'%len(self.video_mergers))

    def _does_overlap(self, ref_rec, audio_rec):
        A1, A2 = audio_rec.get_start_time(), audio_rec.get_end_time()
        R1, R2 = ref_rec.get_start_time(), ref_rec.get_end_time()
        no_overlap = (A2 < R1) or (A1 > R2)
        return not no_overlap

    def shrink_gaps_between_takes(self, with_gap=CLUSTER_GAP):
        """
        for single cam shootings this simply sets the gap between takes,
        tweaking each vid timecode metadata to distribute them next to each
        other along NLE timeline. For multicam takes, shifts are computed so
        video clusters are near but dont overlap, ex: 

        Cluster 1           Cluster 2
        1111111111111        2222222222 (cam A)
           11111111111[...]222222222 (cam B)

        or
        1111111111111    222222 (cam A)
          1111111     22222 (cam B)

        Returns nothing, changes are done in the video files metadata
        (each referenced by Recording.final_synced_file)
        """
        vids = [m.ref_recording for m in self.video_mergers]
        # INs_and_OUTs contains (time, direction, video) for each video,
        # where direction is 'in|out' and video an instance of Recording
        INs_and_OUTs = [(vid.get_start_time(), 'in', vid) for vid in vids]
        for vid in vids:
            INs_and_OUTs.append((vid.get_end_time(), 'out', vid))
        INs_and_OUTs = sorted(INs_and_OUTs, key=lambda vtuple: vtuple[0])
        logger.debug('INs_and_OUTs: %s'%INs_and_OUTs)
        new_cluster = True
        current_cluster = {'vids':[]}
        N_in, N_out = (0, 0)
        # clusters is a list of  {'end': t1, 'start': t2, 'vids': [r1,r3]}
        clusters = []
        for t, direction, video in INs_and_OUTs:
            if new_cluster and direction == 'out':
                logger.error('cant begin a cluster with a out time %s'%video)
                quit()
            if new_cluster:
                current_cluster['start'] = t
                new_cluster = False
            if direction == 'in':
                N_in += 1
                current_cluster['vids'].append(video)
            else:
                N_out += 1
            N_currently_open = N_in - N_out
            if N_currently_open == 0:
                # print(t,direction,video)
                current_cluster['end'] = t
                clusters.append(current_cluster)
                new_cluster = True
                current_cluster = {'vids':[]}
                N_in, N_out = (0, 0)
        logger.debug('clusters: %s'%pprint.pformat(clusters))
        # if there are N clusters, there are N-1 gaps to evaluate and shorten
        # (lengthen?) to a value of with_gap seconds
        gaps = [c2['start'] - c1['end'] for c1, c2
                                    in zip(clusters, clusters[1:])]
        logger.debug('gaps between clusters %s'%[g.total_seconds()
            for g in gaps])
        logger.debug('desired gap is %f'%with_gap)
        # if gap is 3.5s and goal is 2s (the with_gap parameter), clip has to
        # move 1.5s *to the left* ie towards negative axis of time, so the
        # offset should be negative too
        offsets = [timedelta(seconds=with_gap) - gap for gap in gaps]
        logger.debug('gap difference: %s'%[o.total_seconds() for o in offsets])
        zero = [timedelta(seconds=0)] # for the first cluster
        cummulative_offsets = zero + list(numpy.cumsum(offsets))
        # for now on, offsets are in secs, not timedeltas
        cummulative_offsets = [td.total_seconds() for td in cummulative_offsets]
        logger.debug('cummulative_offsets: %s'%cummulative_offsets)
        time_of_first = clusters[0]['start']
        offset_for_all_clips = - from_midnight(time_of_first).total_seconds()
        logger.debug('time_of_first: %s'%time_of_first)
        logger.debug('offset_for_all_clips: %s'%offset_for_all_clips)
        for cluster, offset in zip(clusters, cummulative_offsets):
            total_offset = offset + offset_for_all_clips
            logger.debug('for %s offset in sec: %f'%(cluster['vids'],
                    total_offset))
            for vid in cluster['vids']:
                tc = vid.get_timecode(with_offset=total_offset)
                logger.debug('for %s old tc: %s new tc %s'%(vid,
                    vid.get_timecode(), tc))
                vid.write_file_timecode(tc)
        return


















