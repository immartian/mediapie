#! /usr/bin/env python

# This is the player class to match a channel-based environment
# Sharism Licence, 2013
# by @isaac Mao

import pexpect
import re

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _FILEPROP_REXP = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'

    paused = False
    # KRT turn subtitles off as a command option is used
    subtitles_visible = False

    #****** KenT added argument to control dictionary generation
    def __init__(self, mediafile, args=None, start_playback=False, do_dict=False):
        if not args:
            args = ""
        #******* KenT signals to tell the gui playing has started and ended
        self.start_play_signal = False
        self.end_play_signal=False
        cmd = self._LAUNCH_CMD % (mediafile, args)
        self._process = pexpect.spawn(cmd)
        # fout= file('logfile.txt','w')
        # self._process.logfile_send = sys.stdout
        
        # ******* KenT dictionary generation moved to a function so it can be omitted.
        if do_dict:
            self.make_dict()
            
        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()
        if not start_playback:
            self.toggle_pause()
        # don't use toggle as it seems to have a delay
        # self.toggle_subtitles()


    def _get_position(self):
    
        # ***** KenT added signals to allow polling for end by a gui event loop and also to check if a track is playing before
        # sending a command to omxplayer
        self.start_play_signal = True  

        # **** KenT Added self.position=0. Required if dictionary creation is commented out. Possibly best to leave it in even if not
        #         commented out in case gui reads position before it is first written.
        self.position=-100.0
        
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if index == 1: continue
            elif index in (2, 3):
                # ******* KenT added
                self.end_play_signal=True
                break
            else:
                self.position = float(self._process.match.group(1))                
            sleep(0.05)



    def make_dict(self):
        self.video = dict()
        self.audio = dict()

        #******* KenT add exception handling to make code resilient.
        
        # Get file properties
        try:
            file_props = self._FILEPROP_REXP.match(self._process.readline()).groups()
        except AttributeError:
            return False        
        (self.audio['streams'], self.video['streams'],
        self.chapters, self.subtitles) = [int(x) for x in file_props]
        
        # Get video properties        
        try:
            video_props = self._VIDEOPROP_REXP.match(self._process.readline()).groups()
        except AttributeError:
            return False
        self.video['decoder'] = video_props[0]
        self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
        self.video['profile'] = int(video_props[3])
        self.video['fps'] = float(video_props[4])
                        
        # Get audio properties
        try:
            audio_props = self._AUDIOPROP_REXP.match(self._process.readline()).groups()
        except AttributeError:
            return False       
        self.audio['decoder'] = audio_props[0]
        (self.audio['channels'], self.audio['rate'],
         self.audio['bps']) = [int(x) for x in audio_props[1:]]

        if self.audio['streams'] > 0:
            self.current_audio_stream = 1
            self.current_volume = 0.0



# ******* KenT added basic command sending function
    def send_command(self,command):
        self._process.send(command)
        return True


# ******* KenT added test of whether _process is running (not certain this is necessary)
    def is_running(self):
        return self._process.isalive()

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible
            
    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError


#from pyomxplayer import OMXPlayer


import os, os.path

channelpath = "channels"

class channelPlayer():
		
	def __init__(self, channel=None):
		if channel is None:
			channel = "mychannel"
		self.currentChannel = channel
		self.filelist = []
		
  	def readAll(self):
		fullpath = os.path.abspath('..') + "/"+ channelpath
		dirtocheck = fullpath+ "/" +self.currentChannel
		print dirtocheck
			
		for root, _, files in os.walk(dirtocheck):
    			for f in files:
				#check file type here
				if self.checkfiletype(f):				
        				fullpath = os.path.join(root, f)
					print fullpath
					self.filelist.append(fullpath)	
		

	# play a MP3 or MIDI music file using module pygame
	def checkfiletype(self,fn):
		ext = os.path.splitext(fn)[-1].lower()
		# Now we can simply use == to check for equality, no need for wildcards.
		if ext == ".mp3":
			self #haha
		elif ext == ".mp4":
			self #ha
		else:
			return False
		return True




if __name__ == "__main__":

	#player= channelPlayer(channel= "RCXOVNLNVK56GBQK2OCWR3GLY2DENRZG4")
	#player.playAll()
	omx = OMXPlayer('../channels/RCXOVNLNVK56GBQK2OCWR3GLY2DENRZG4/09 - The Syncopated Clock.mp3')
        
