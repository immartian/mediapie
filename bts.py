import urllib, urllib2
import re
from datetime import datetime

class BTSync:
  def gettoken(self):
    timestr = urllib.quote(str(datetime.now()))
    url = 'http://localhost:8888/gui/token.html?t='+timestr
    req = urllib2.Request(url,data='this ida is passed to CGI2')
    f = urllib2.urlopen(req)
    m = f.read()
    p = re.compile(r'<.*?>')
    #private.token 
    self.token = p.sub('',m)
  def addSyncFolder(self):
  def removeSyncFolder(self):
  def generateSecret(self):


if __name__ == "__main__":
  bts= BTSync()
  bts.gettoken()  
  print bts.token
