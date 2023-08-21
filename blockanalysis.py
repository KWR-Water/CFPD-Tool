import math
import numpy

import sys


def determineclusters(parent,xdat,ydat,nclust,minclustsize,verbose=False):
   # from a CFPD curve, determine clusters of points which are most consistent

   # generate two-node clusters (or more nodes when they coincide)
   n=len(xdat) # number of datapoints
   alist=[]; blist=[]; nodelist=[]
   finished=False
   i=0
   while not finished:
      i2=n-1
      for j in range(i+1,n):
         if not (xdat[j]==xdat[i] and ydat[j]==ydat[i]):
            # not coinciding -> suitable as end point
            #print 'not the same: coor='+str([xdat[j],xdat[i],ydat[j],ydat[i]])
            i2=j
            break
         #else:
            #print 'the same: coor='+str([xdat[j],xdat[i],ydat[j],ydat[i]])
      dy=ydat[i2]-ydat[i]
      dx=xdat[i2]-xdat[i]
      if dx==0.0:
         a=1e9 # very large
         b=-1e9 # very large
      else:
         a=dy/dx
         b=ydat[i]-xdat[i]*a
      alist.append(a)
      blist.append(b)
      nodelist.append([i,i2])
      if i2==n-1:
         finished=True   
      else:
         i=i2

   #print 'nodelist='+str(nodelist)
   n=len(alist) # number of remaining clusters

   # merge clusters until we have nclust left
   while n>nclust:
      # find two adjacent clusters which are closest in (a,b)-space and merge them

      if verbose:
         print('================================================')
         print('nclust='+str(nclust))
         for i in range(len(alist)):
            print(str(alist[i])+', '+str(blist[i]))

      # get distance between adjacent clusters in (a,b)-space
      dist=[]
      mina=min(alist); maxa=max(alist)
      minb=min(blist); maxb=max(blist)
      for i in range(n-1):
         # scale differences to value range
         da=(alist[i]-alist[i+1])/(maxa-mina) 
         db=(blist[i]-blist[i+1])/(maxb-minb) 
         d=math.sqrt(da*da+db*db)
         dist.append(d)

      # smallest distance
      mind=min(dist)
      # cluster index
      idx=dist.index(mind)

      # merge cluster idx to cluster idx+1
      nodelist[idx][1]=nodelist[idx+1][1] # update end node
      alist.pop(idx+1) # remove second cluster
      blist.pop(idx+1) # remove second cluster
      nodelist.pop(idx+1) # remove second cluster
      i1=nodelist[idx][0] # start node of new cluster
      i2=nodelist[idx][1] # end node of new cluster
      dx=xdat[i2]-xdat[i1]
      dy=ydat[i2]-ydat[i1]
      if dx==0.0:
         alist[idx]=1e9 # very large
         blist[idx]=-1e9 # very large
      else:
         alist[idx]=(ydat[i2]-ydat[i1])/(xdat[i2]-xdat[i1])
         blist[idx]=ydat[i1]-xdat[i1]*alist[idx]
     
      # update number of clusters
      n-=1

   # return result
   return nodelist




def printmat(mat):
   m=len(mat)
   n=len(mat[0])
   for i in range(m):
      lstr=''
      for j in range(n): 
         lstr+=' %5.2f ' % mat[i][j]
      lstr+='\n'
      sys.stdout.write(lstr)



def plateautemplates(apf,nrowcol):
   templates=[]
   for pf in apf:
      template=numpy.zeros((nrowcol,nrowcol))
      x1=pf[0]; x2=pf[1]; 

      jrow=numpy.arange(0,x1)
      template[jrow,x1:x2]=[1.0]*(x2-x1)
      jrow=numpy.arange(x1,x2)
      template[jrow,x2:]=[-1.0]*(nrowcol-x2)

      #print 'template=\n'+str(template)

      templates.append(template)

   return templates 


def weekendtemplates(nrowcol,firstsaturday):
   weekendmask1=numpy.zeros((nrowcol,nrowcol))
   weekendmask2=numpy.zeros((nrowcol,nrowcol))
   idxs=list(range(firstsaturday,nrowcol,7))+list(range(firstsaturday+1,nrowcol,7))
   if firstsaturday==6: 
      idxs.append(0) # add the first Sunday explicitly
   idxs.sort()
   for i in idxs:
      # rows
      weekendmask1[i][i+1:]=[1.0]*(nrowcol-i-1)
      # columns
      j=numpy.arange(i)
      weekendmask2[j,i]=1.0

   # explicitly reset weekend-weekend blocks to 0
   for i in idxs:
      for j in idxs:
         weekendmask1[i][j]=0.0
         weekendmask2[i][j]=0.0

   #print 'weekendmask1:' 
   #print str(weekendmask1)
   #print 'weekendmask2:' 
   #print str(weekendmask2)


   return [weekendmask1,weekendmask2]
   




