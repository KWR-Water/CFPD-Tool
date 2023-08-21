
import numpy as npy
import sys
import math
import string
import wx
import datetime
import conversion

def dp(a,b):
   u=0.0
   if (not (len(a)==len(b))):
      sys.exit(1)
   for i in range(len(a)):
      u+=a[i]*b[i]
   return u
      

def der(x,y):
   d=[]
   for i in range(len(y)):
      if (i==0):
         v=(y[1]-y[0])/(x[1]-x[0])
      elif (i==(len(y)-1)):
         v=(y[len(y)-1]-y[len(y)-2])/(x[len(y)-1]-x[len(y)-2])
      else:
         v=(y[i+1]-y[i-1])/(x[i+1]-x[i-1])
      d.append(v)

   return d
   
def plateaupoint(x,y,pv,eps):
   for i in range(len(y)):
      if (abs(pv-y[i])>eps):
         return x[i] 

   return -999

def gettrunccurves(x,y, miny, maxy, starttim, endtim, ntrunc, ipass, npass):

   count=0
   ncountshow=100
   n=5+ncountshow
   dlg = wx.ProgressDialog('Progress', 'Computing truncation statistics ('+str(ipass)+'/'+str(npass)+')', n)

   # compute statistics
   thisv=[]
   for i in range(len(x)):
      tim=x[i]%1.0
      if (tim>=starttim and tim<=endtim):
         if (y[i]>=miny and y[i]<=maxy):
            thisv.append(y[i])
   count+=1
   dlg.Update(count)

   m=npy.mean(thisv)
   s=npy.std(thisv)
   thisv.sort()

   #print "m="+str(m)
   #print "s="+str(s)

   ival=0
   vblom=[]
   vprob=[]
   for val in thisv:
      ival+=1
      vblom.append((float(ival)-0.375)/(float(len(thisv)+0.25)))
      if (ival==len(thisv)):
         vprob.append(0.99999)
      else:
         vprob.append(float(ival)/float(len(thisv)))
   maxval=max(thisv)
  
   count+=1
   dlg.Update(count)

   means=[]
   stdevs=[]
   epsilons=[]
   Qbars=[]
   sigmas=[]
   iupd=0
   lastupd=0
   if (len(thisv)>0):
      for itrunc in range(ntrunc):
         iupd=int(ncountshow*float(itrunc)/float(ntrunc))
         if (iupd>lastupd):
            count+=1
            dlg.Update(count)
            lastupd=iupd
         trunc=float(itrunc)/float(ntrunc-1)
         ar=[]
         for val in thisv:
            v=(val-maxval*trunc)
            if (v<0.0):
               v=0.0
            ar.append(v)
         means.append(npy.mean(ar))
         stdevs.append(npy.std(ar))
         epsilons.append((maxval*trunc-m)/s)
         sar=sum(ar)
         Qbars.append((1.0/(float(len(thisv))*s))*sar)
         sqa=float(len(thisv))*dp(ar,ar)-sar*sar
         #print 'sqa='+str(sqa)
         sigmas.append((1.0/(float(len(thisv))*s))*math.sqrt(sqa))

   count+=1
   dlg.Update(count)
   derQbar=der(epsilons,Qbars)
   count+=1
   dlg.Update(count)
   dersigmas=der(epsilons,sigmas)
 
   dlg.Destroy()

   return Qbars, sigmas, derQbar, dersigmas, m, s, epsilons

def subset(x,y,minx, maxx, miny, maxy, mint, maxt):
   #return subset_impl1(x,y, minx, maxx, miny, maxy, mint, maxt)
   return subset_impl2(x,y, minx, maxx, miny, maxy, mint, maxt)

def subset_impl2(x,y, minx, maxx, miny, maxy, mint, maxt):

   ox=[]; oy=[]; oi=[]
   margin=1e-6
   #margin=1e-9
   minxm=minx-margin
   maxxm=maxx+margin
   minym=miny-margin
   maxym=maxy+margin
   mintm=mint-margin 
   maxtm=maxt+margin
   for i in range(len(x)):
      if (x[i]>=minxm):
         if (x[i]<=maxxm):
            if (y[i]>=minym):
               if (y[i]<=maxym):
                  t=x[i]%1.0 
                  if (t>=mintm and t<=maxtm):
                     ox.append(x[i])
                     oy.append(y[i])
                     oi.append(i)

   return ox,oy,oi

def subset_impl1(x,y, minx, maxx, miny, maxy, mint, maxt):

   ox=[]; oy=[]; oi=[]
   margin=1e-9
   for i in range(len(x)):
      if (x[i]>=minx-margin):
         if (x[i]<=maxx+margin):
            if (y[i]>=miny-margin):
               if (y[i]<=maxy+margin):
                  t=x[i]%1.0 
                  if (t>=mint-margin and t<=maxt+margin):
                     ox.append(x[i])
                     oy.append(y[i])
                     oi.append(i)

   return ox,oy,oi

def basepattern(choice, nsample, mean, sd, minx,maxx,mint, maxt, trunc):

   ox=[]; oy=[]; ot=[]
   if (choice=="normal"):
      dlg = wx.ProgressDialog('Progress', 'Generating baseline sample set', 1)

      oy=[]
      for isample in range(nsample):
         loy=npy.random.normal(mean,sd)
         if (loy>=trunc):
            oy.append(loy)
         else:
            oy.append(trunc)
      #for i in range(nsample):
          #x=mint+i*(maxt-mint)/float(nsample-1)
          #t=x
          #ox.append(x+7.0)
          #ot.append(t+7.0)
      nday=int(maxx-minx)
      nperday=int(nsample/nday)+1
      ntot=0
      for iday in range(nday):
         for jsam in range(nperday):
            ntot+=1
            if ntot>nsample:
               break
            t=mint+jsam*(maxt-mint)/float(nperday)
            x=float(int(minx)+iday)+t
            ox.append(x)
            ot.append(t)
            

      dlg.Update(1)
      dlg.Destroy()
   else:
      print('mystat.basepattern error choice='+str(choice))
      sys.exit(1)

   return ox,oy,ot
 
def dates2weekdays(x):
   # reference day: May 2, 2011 is a Monday
   ox=[]
   for i in range(len(x)):
      d=conversion.xldate_as_datetime(x[i],0) 
      wd=d.weekday()
      ox.append(conversion.date2exceldate(datetime.datetime(2011,5,2+wd,d.hour,d.minute,d.second)))

   print('dates2weekdays: min,max='+str([min(ox),max(ox)]))

   return ox

def getstats(x,y,dt):
   # dt in days
   #print '============== getstats ========================'

   nframe=int(7.0/dt)

   irefday=conversion.getrefdat()
   #print 'irefday='+str(irefday)

   ox=[]
   omean=[]
   osd=[]

   #print 'fstart='+str(irefday)
   for iframe in range(nframe):
      fstart=irefday+float(iframe)*dt
      fend  =irefday+float(iframe+1)*dt

      dat=[]
      for i in range (len(x)): 
         if (x[i]>=fstart and x[i]<fend):
            # inside frame
            dat.append(y[i]) 
      if (len(dat)>0):
         ox.append(0.5*(fstart+fend))
         m=npy.mean(dat)
         s=npy.std(dat)
         #print str(fstart)+' - '+str(fend)+' : '+str(dat)+' m='+str(m)+' s='+str(s)
         omean.append(m)
         osd.append(s)
   #print 'fend='+str(fend)

   #print 'ox='+str(ox)

   return ox, omean, osd

def getttest(x1,y1,x2,y2,dt):

   # perform student's t-test to determine wether two sets of samples (x1,y1) 
   # and (x2,y2) belong to the same population (assuming a single population
   # variance). 

   nframe=int(7.0/dt)
   print('nframe='+str(nframe))

   irefday=conversion.getrefdat()

   ox=[]
   ot=[]
   op=[]
   oh=[]

   dat1={}
   li1=[]
   for i in range(len(x1)):
      li=int((x1[i]-float(irefday))/dt)
      lis=str(li)
      li1.append(li)
      if (li>=0 and li<nframe):
         try:
            dat1[lis].append(y1[i])
         except:
            dat1[lis]=[y1[i]]

   dat2={}
   li2=[]
   for i in range(len(x2)):
      li=int((x2[i]-float(irefday))/dt)
      lis=str(li)
      li2.append(li)
      if (li>=0 and li<nframe):
         try:
            dat2[lis].append(y2[i])
         except:
            dat2[lis]=[y2[i]]
      
   #print '============================'
   #print 'dat1='+str(dat1)
   #print '----------------------------'
   #print 'dat2='+str(dat2)
   #print '----------------------------'
   #print 'li1='+str(li1)
   #print '----------------------------'
   #print 'li2='+str(li2)
   #print '============================'


   for iframe in range(nframe):
      fstart=float(irefday)+float(iframe)*dt
      fend  =float(irefday)+float(iframe+1)*dt

      #dat1=[]
      #for i in range (len(x1)):
         #if (x1[i]>=fstart and x1[i]<fend):
            ## inside frame
            #dat1.append(y1[i])
      #dat2=[]
      #for i in range (len(x2)):
         #if (x2[i]>=fstart and x2[i]<fend):
            ## inside frame
            #dat2.append(y2[i])
      lis=str(iframe)
      try:
         n1=len(dat1[lis])
         n2=len(dat2[lis])
      except:
         n1=0
         n2=0
      if (n1>1 and n2>1):
         #print 'dat1='+str(dat1[lis])
         #print 'dat2='+str(dat2[lis])
         ox.append(0.5*(fstart+fend))
         [t,p]=stats.ttest_ind(dat1[lis],dat2[lis],axis=0)
         ot.append(t)
         op.append(p)
         ln1=int(math.sqrt(n1))
         h1=npy.histogram(dat1[lis])
         ln2=int(math.sqrt(n2))
         h2=npy.histogram(dat2[lis])
         oh.append([h1,h2])

   #print 'ox='+str(ox)
   #print 'op='+str(op)

   return ox, ot, op, oh

      
def getsynthcurves(n,m,s):
   Es=[]
   Ss=[]
   epsilon=[]
   for i in range(1,n+1):
      rank=(float(i)-0.375)/(float(n)+0.25)
      zvalue=norm.ppf(rank,0.0,1.0)
      if (i<n):
         prob=float(i)/float(n)
      else:
         prob=0.9999
      pat=norm.ppf(prob,m,s)
      eps=(pat-m)/s
      Evalue=norm.pdf(eps,0,1)-eps*norm.cdf(-1.0*eps,0,1)
      Svalue=math.sqrt((1.0+2.0*eps*norm.pdf(eps,0,1)+eps*eps*norm.cdf(eps,0,1))*norm.cdf(-1*eps,0,1)-(eps+norm.pdf(eps,0,1))*norm.pdf(eps,0,1))
      epsilon.append(eps)
      Es.append(Evalue)
      Ss.append(Svalue)

   derE=der(epsilon,Es)
   derS=der(epsilon,Ss)


   return epsilon,Es,Ss,derE,derS

def normalprobabilityplotdata(dat):
   # following the NormalProbabilityPlot.xls spreadsheet
   zvalue=[]

   dat.sort()

   n=len(dat)

   for i in range(n):
      rank=i+1
      proportion=float(rank)/float(n+1)
      zvalue.append(norm.ppf(proportion)) # invnorm function

   return [dat,zvalue]
      
def resample(dat,n):

   ndat=len(dat)

   outdat=[]
   for i in range(n):
      j=i*float(ndat)/float(n)
      j1=int(math.floor(j)); j2=int(math.floor(j)+1)
      # linear interpolation
      if j2>=ndat:
         v=dat[j1]
      else:
         v=dat[j1]+(j-float(j1))*(dat[j2]-dat[j1])
      outdat.append(v)
  
   return outdat

def aggregate(x,y,t,blocklen):
   print('blocklen='+str(blocklen))
   x0=min(x); x1=max(x)
   n=int((x1-x0)/blocklen+1)
   px=[]
   py=[]
   pt=[]
   for i in range(n):
      px.append([])
      py.append([])
      pt.append([])
   #print 'px='+str(px)
   #print 'py='+str(py)
   #print 'pt='+str(pt)
   for i in range(len(x)):
      j=int((x[i]-x0)/blocklen)
      #print 'i,j='+str([i,j])
      #print 'add '+str(x[i])+' to '+str(px[j])
      px[j].append(x[i])
      py[j].append(y[i])
      pt[j].append(t[i])
   #print 'pt='+str(pt)
       
   #print 'px='+str(px)
   #print 'py='+str(py)
   #print 'pt='+str(pt)
   ox=[]; oy=[]; ot=[]
   for i in range(n):
      #print 'i='+str(i)+'/'+str(n)
      if len(px[i])>0:
         ox.append(x0+i*blocklen)
         ot.append(min(pt[i])) 
         oy.append(npy.mean(py[i]))

   #print 'ox='+str(ox)
   #print 'oy='+str(oy)
   #print 'ot='+str(ot)

   #print 'input range:'
   #print 'x:'+str([min(x),max(x)])
   #print 'y:'+str([min(y),max(y)])
   #print 't:'+str([min(t),max(t)])
   #print 'n='+str(len(x))
   #print 'output range:'
   #print 'x:'+str([min(ox),max(ox)])
   #print 'y:'+str([min(oy),max(oy)])
   #print 't:'+str([min(ot),max(ot)])
   #print 'n='+str(len(ox))
   mindx=1e33
   for i in range(len(ox)-1):
      dx=ox[i+1]-ox[i]
      mindx=min(mindx,dx)
   #print 'min dx='+str(mindx)


   return ox,oy,ot
