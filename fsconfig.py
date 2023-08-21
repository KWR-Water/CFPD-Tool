import os
import sys

def loadconfig():

   [succes,homedir]=gethomedir()
   if not succes:
      return [False,[]]
   try:
      f=open(homedir+'/.flowstat/flowstat.conf','r')
      lines=f.readlines()
      f.close()
      path=lines[0].replace('\r','').replace('\n','').replace(' ','\ ')
      appsize=lines[1].replace('\r','').replace('\n','').replace(' ','\ ')
      print('path='+str(path))
      print('appsize='+str(appsize))
      return [True,[path,appsize]]
   except:
      return [False,[]]

def saveconfig(vrs):
   [succes,homedir]=gethomedir()
   if not succes:
      return False
   if not os.path.exists(homedir+'/.flowstat'):
      # config directory does not exist -> create
      try:
         os.mkdir(homedir+'/.flowstat')
      except:
         return False
   try:
      f=open(homedir+'/.flowstat/flowstat.conf','w')
      for var in vrs:
         f.write(str(var)+'\n')
      f.close()
      return True
   except:
      return False
   
def gethomedir():
   if os.name=='posix':
      homedir=os.environ['HOME']
      return [True,homedir]
   else:
      return [False,'']

def strippath(path):
   # strip filename from path
   components=path.split('/')
   opath=''
   for i in range(len(components)-1):
      opath+='/'+components[i]
   return opath
