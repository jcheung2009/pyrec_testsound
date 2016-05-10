#! /usr/bin/env python

import wave
import audioop
import platform
import sys
import time
import math
import pdb
import ConfigParser
import numpy as np
import multiprocessing as mp

sys.path.append("/home/brad/src/behavior_controller")
import lib.soundout_tools as so
from collections import deque

uname = platform.uname()[0]
if uname=='Linux': # this allows for development on non-linux systems
    import alsaaudio as aa
else:
    import pyaudio as pa

class AudioRecord:
    def __init__(self):
        self.event_queue = None
        self.recording_queue = None

        self.params = {}
        self.params['birdname'] = None
        self.params['chunk'] = 1024
        if uname == 'Linux':
            self.params['format'] = aa.PCM_FORMAT_S16_LE
            self.pcm = None
        else:
            self.params['format'] = pa.paInt16
            self.pcm = 0
        self.params['channels'] = 1
        self.params['rate'] = 44100
        self.params['threshold'] = None
        self.params['silence_limit'] = None
        self.params['prev_audio'] = None
        self.params['min_dur'] = None
        self.params['outdir'] = None

    def test_config(self):
        self.params['chunk'] = 256
        if uname == 'Linux':
            self.params['format'] = aa.PCM_FORMAT_S16_LE
            self.pcm = 'hw:CARD=usbaudio_2,DEV=0'
        else:
            self.params['format'] = pa.paInt16
            self.pcm = 0
        self.params['channels'] = 1
        self.params['rate'] = 44100
        self.params['silence_limit'] = 0.5
        self.params['prev_audio'] = 1
        self.params['min_dur'] = 1
        self.params['outdir'] = "."

    def init_config(self, config_file):
#        pdb.set_trace()
        if config_file is None:
            self.test_config()
            return
        config = ConfigParser.ConfigParser() 
        config.read(config_file)
        #pdb.set_trace()
        for option in config.options('record_params'):
            if option == "sound_card":
                attr = config.get('record_params', option)
                self.set_sound_card(attr)
            elif option in ["outdir", "bird"]:
                attr = config.get('record_params', option)
                self.params[option] = attr
            elif option == "chunk":
                attr = config.getint('record_params', option)
                self.params[option] = attr
            else:
                attr = config.getfloat('record_params', option)
                self.params[option] = attr

        if not os.path.exists(self.params['outdir']):
            os.makedirs(self.params['outdir'])

    def set_sound_card(self, attr):
        if uname == 'Linux':
            self.pcm = "hw:CARD=%s,DEV=0" % attr
        else:
            self.pcm = int(attr)

    def list_sound_cards(self):
        return so.list_sound_cards()

    def audio_int(self, num_samples=64):
        """ Gets max audio intensity for a bunch of chunks of data. Useful for setting threshold.
        """
        print "Getting intensity values from mic."
        values = None
        if uname == "Linux":
        #stream = aa.PCM(aa.PCM_CAPTURE,aa.PCM_NORMAL, INPUT)
            stream = aa.PCM(aa.PCM_CAPTURE,aa.PCM_NORMAL, device=self.pcm)
            stream.setchannels(self.params['channels'])
            stream.setrate(self.params['rate'])
            stream.setformat(self.params['format'])
            stream.setperiodsize(self.params['chunk'])
            values = [math.sqrt(abs(audioop.max(stream.read()[1], 4)))for x in range(num_samples)]
        else:
            p = pa.PyAudio()
            stream = p.open(rate=self.params['rate'],
                             input_device_index=self.pcm,
                             format=self.params['format'],
                             channels=self.params['channels'],
                             frames_per_buffer=self.params['chunk'],
                             input=True)
            values = [math.sqrt(abs(audioop.max(stream.read(self.params['chunk']), 4)))for x in range(num_samples)]

        #values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print "Finished"
        print "max audio intensity is", values
        stream.close()
        return r

    def set_threshold(self):
        values = self.audio_int()
        values_thresh = np.max(values) * 1.1
        print "threshold set to: " + str(values_thresh)
        self.threshold = values_thresh
        return values_thresh

    def start(self):
        self.event_queue = mp.Queue()
        self.proc = mp.Process(target = start_recording, args= (self.event_queue,
                                                                self.pcm,
                                                                self.params['birdname'],
                                                                self.params['channels'],
                                                                self.params['rate'],
                                                                self.params['format'],
                                                                self.params['chunk'],
                                                                self.params['silence_limit'],
                                                                self.params['prev_audio'],
                                                                self.params['min_dur'],
                                                                self.params['threshold'],
                                                                self.params['outdir']))
        self.proc.start()

    def start_return_data(self):
        self.event_queue = mp.Queue()
        self.recording_queue = mp.Queue()
        error_queue = mp.Queue()
        self.proc = mp.Process(target = start_recording_return_data, args= (self.event_queue,
                                                                self.recording_queue,
                                                                            error_queue,
                                                                self.pcm,
                                                                self.params['channels'],
                                                                self.params['rate'],
                                                                self.params['format'],
                                                                self.params['chunk']))


        self.proc.start()

        ### Check if mic connection good ###
        current_time = time.time()
        max_time = 1
        while (time.time() - current_time) < max_time:
            if not error_queue.empty():
                raise Exception

    def stop(self):
        self.event_queue.put(1)

def start_recording(queue, pcm, bird, channels, rate, format, chunk,
                    silence_limit, prev_audio_time, min_dur, threshold, outdir):
    stream = None
    if uname == "Linux":
        stream = aa.PCM(aa.PCM_CAPTURE,aa.PCM_NORMAL, device=pcm)
        stream.setchannels(channels)
        stream.setrate(rate)
        stream.setformat(format)
        stream.setperiodsize(chunk)
    else:
        p = pa.PyAudio()
        stream = p.open(rate=rate,
                         input_device_index=pcm,
                         format=format,
                         channels=channels,
                         frames_per_buffer=chunk,
                         input=True)

    print "listening..."
    audio2send = []
    cur_data = '' # current chunk of audio data
    rel = rate/chunk
    slid_win = deque(maxlen=silence_limit * rel) #amplitude threshold running buffer
    prev_audio = deque(maxlen=prev_audio_time * rel) #prepend audio running buffer
    started = False

    if uname == "Linux":
        cur_data=stream.read()[1]
    else:
        cur_data=stream.read(chunk)
    slid_win.append(math.sqrt(abs(audioop.max(cur_data, 4))))

    while queue.empty():
        #if len(slid_win)>0:
        #    print max(slid_win) #uncomment if you want to print intensity values
        if uname == "Linux":
            cur_data=stream.read()[1]
        else:
            cur_data=stream.read(chunk)

        try:
            slid_win.append(math.sqrt(abs(audioop.max(cur_data, 4))))
        except audioop.error:
            print "invalid number of blocks for threshold calculation, but continuing"

        if(sum([x > threshold for x in slid_win]) > 0):
            if(not started):
                # start recording
                sys.stdout.write(bird + ", ")
                sys.stdout.write(time.ctime() + ": ")
                sys.stdout.write("recording ... ")
                sys.stdout.flush()
                started = True
            audio2send.append(cur_data)
        elif (started is True and len(audio2send)>min_dur*rel):
            # write out
            print "writing to file"
            filename = save_audio(list(prev_audio) + audio2send, outdir, rate)
            started = False
            slid_win = deque(maxlen=silence_limit * rel)
            prev_audio = deque(maxlen=prev_audio_time * rel)
            print "listening ..."
            audio2send=[]
        elif (started is True):
            print "duration criterion not met"
            started = False
            slid_win = deque(maxlen=silence_limit * rel)
            prev_audio = deque(maxlen=prev_audio_time * rel)
            audio2send=[]
            print "listening ..."
        else:
            prev_audio.append(cur_data)
    else:
        #print "done recording"
        stream.close()
        return

def start_recording_return_data(event_queue, recording_queue, error_queue, pcm, channels, rate, format, chunk):
    stream = None
    if uname == "Linux":
        try:
            stream = aa.PCM(aa.PCM_CAPTURE,aa.PCM_NORMAL, device=pcm)
            stream.setchannels(channels)
            stream.setrate(rate)
            stream.setformat(format)
            stream.setperiodsize(chunk)
        except:
            print "here2"
            error_queue.put(1)
            return
            #error_queue.put(1)
            #raise aa.ALSAAudioError
            #raise
            #print "recording2"
            #return
    else:
        p = pa.PyAudio()
        stream = p.open(rate=rate,
                        input_device_index=pcm,
                         format=format,
                         channels=channels,
                         frames_per_buffer=chunk,
                         input=True)

    print "listening..."
    audio2send = []
    cur_data = '' # current chunk of audio data
    rel = rate/chunk
    started = False

    if uname == "Linux":
        cur_data=stream.read()[1]
        recording_queue.put(cur_data)
    else:
        cur_data=stream.read(chunk)

    while event_queue.empty():
#            if len(slid_win)>0:
#                print max(slid_win) #uncomment if you want to print intensity values
        if uname == "Linux":
            cur_data=stream.read()[1]
            recording_queue.put(cur_data)
        else:
            cur_data=stream.read(chunk)
    else:
        stream.close()
        return

def save_audio(data, outdir, rate):
    """ Saves mic data to  WAV file. Returns filename of saved file """
    filname = "/".join([str(outdir), 'output_'+str(int(time.time()))])
    # writes data to WAV file
    data = ''.join(data)
    wavout = wave.open(filname + '.wav', 'wb')
    wavout.setnchannels(1)
    wavout.setsampwidth(4)
    wavout.setframerate(rate)
    wavout.writeframes(data)
    wavout.close()
    return filname + '.wav'

def get_audio_power(data):
    return math.sqrt(abs(audioop.max(data, 4)))

def main(argv):
    recorder = AudioRecord()
    if len(argv) > 1:
        recorder.init_config(argv[1])
    else:
        recorder.test_config()
    recorder.start()

if(__name__ == '__main__'):
    main(sys.argv)
