#! /usr/bin/env python

# This is the player class to match a channel-based environment
# Sharism Licence, 2013
# by @isaac Mao

from pyomxplayer import OMXPlayer
import os, os.path
from random import shuffle

channelpath = "channels"

class channelManager():
		
	def __init__(self, channel=None):
		if channel is None:
			channel = "mychannel"
		self.currentChannel = channel
		self.filelist = []
		
  	def readAll(self):
		fullpath = os.path.abspath('..') + "/"+ channelpath
		dirtocheck = fullpath+ "/" +self.currentChannel
		#print dirtocheck
			
		for root, _, files in os.walk(dirtocheck):
    			for f in files:
				#check file type here
				if self.checkfiletype(f):				
        				fullpath = os.path.join(root, f)
					#print fullpath
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

	manager= channelManager(channel= "RCXOVNLNVK56GBQK2OCWR3GLY2DENRZG4")
	manager.readAll()
	shuffle(manager.filelist)
	for f in manager.filelist:
		print f
		omx = OMXPlayer(f)
		while omx.is_running():
			pass
			

       
