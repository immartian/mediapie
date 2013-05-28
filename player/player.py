# This is the player class to match a channel-based environment
# Sharism Licence, 2013
# by @isaac Mao

import os, os.path
import pygame

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

	def play_music(music_file):
	    """
	    stream music with mixer.music module in blocking manner
	    this will stream the sound from disk while playing
	    """
	    clock = pygame.time.Clock()
	    try:
		pygame.mixer.music.load(music_file)
		print "Music file %s loaded!" % music_file
	    except pygame.error:
		print "File %s not found! (%s)" % (music_file, pygame.get_error())
		return
	    pygame.mixer.music.play()
	    while pygame.mixer.music.get_busy():
		# check if playback has finished
		clock.tick(30)
	
	def playAll(self):
		# set up the mixer
		freq = 44100     # audio CD quality
		bitsize = -16    # unsigned 16 bit
		channels = 2     # 1 is mono, 2 is stereo
		buffer = 2048    # number of samples (experiment to get right sound)
		pygame.mixer.init(freq, bitsize, channels, buffer)
		# optional volume 0 to 1.0
		pygame.mixer.music.set_volume(0.75)

		track = 0
		breaker = 0
		clock = pygame.time.Clock()

		while breaker == 0:
			self.readAll()
			print self.filelist[track]
			pygame.mixer.music.load(self.filelist[track])
			pygame.mixer.music.play()
			#    pygame.mixer.music.pause()

			# check if playback has finished
			while pygame.mixer.music.get_busy():
				clock.tick(30)
			#      if pygame.event.get(pygame.KEYDOWN) == pygame.K_b:
			#         pygame.mixer.music.pause()
			#      if event.key == pygame.K_n:
			#         pygame.mixer.music.stop()
			#      if event.key == pygame.K_v:
			#         track = track - 2

			track = track + 1
			if track < 0:
				track = len(self.filelist) + track
			if track > len(self.filelist) - 1:
				track = 0
			


if __name__ == "__main__":

	player= channelPlayer(channel= "RCXOVNLNVK56GBQK2OCWR3GLY2DENRZG4")
	player.playAll()
