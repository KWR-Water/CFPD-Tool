import pygame
import wx
import conversion
import datetime
import math
import sys
import numpy
import supportfunctions

def drawBitmap(static_bitmap,wx_bitmap):
    static_bitmap.SetBitmap(wx_bitmap)

def drawhist(frame, hist, bounds, xl, yl, values=False):
    #print 'hist='+str(hist)

    # pygame surface
    pygame_surface=pygame.Surface([xl,yl])
    pygame_surface.fill((225,225,225))

    if values:
       barl=yl-10
    else:
       barl=yl


    if len(hist)>0:
       maxn=max(hist)
 
       dx=xl/float(len(hist))
       col=(0,0,80)
       for i in range(len(hist)):
          x=float(i)*dx
          y=barl*(1.0-float(hist[i])/float(maxn))
          lbarl=barl*float(hist[i])/float(maxn)
          pygame.draw.rect(pygame_surface,col,(x,y,dx,lbarl),0)

   
    if values:
       col=(0,0,0)
       smin='%1.2f' % (bounds[0])
       #smin=str(bounds[0])
       #print 'smin='+smin
       pygameprint(pygame_surface,smin,4,yl-10,col,8) 
       smax='%1.2f' % (bounds[-1])
       #smax=str(bounds[len(bounds)-1])
       #print 'smax='+smax
       pygameprint(pygame_surface,smax,xl-5*len(smax),yl-10,col,8) 

    # display
    image_string = pygame.image.tostring(pygame_surface, "RGB")
    imgWx = wx.Image(width=int(xl), height=int(yl))
    frame.SetClientSize((xl,yl))
    frame.SetMinSize((xl,yl))
    imgWx.SetData(image_string)
    wx_bitmap = imgWx.ConvertToBitmap()

    drawBitmap(frame,wx_bitmap)
    return wx_bitmap

def drawhistcurves(frame, curve, color, colbg, xrange, yrange, xl, yl, hist, legend=[], levels=False, fontsize=10,drawbghist=True, baselevel=0.05):

    #print 'visual.drawcurves'

    lminx=1e31; lmaxx=-1e31; lminy=1e31; lmaxy=-1e31


    icurve=-1
    #print 'curve '+str(icurve)
    x=curve[0]; y=curve[1]
    for i in range(len(x)):
       lminx=min(x[i],lminx)
       lmaxx=max(x[i],lmaxx)
       if ((xrange[0]==-1 and xrange[1]==-1) or (x[i]>=xrange[0] and x[i]<=xrange[1])):
          # when zooming in, only look at zoom range y values
          lminy=min(y[i],lminy)
          lmaxy=max(y[i],lmaxy)

    if (xrange[0]==-1):
       minx=lminx
    else:
       minx=xrange[0]
    if (xrange[1]==-1):
       maxx=lmaxx
    else:
       maxx=xrange[1]
    if (yrange[0]==-1):
       miny=lminy
    else:
       miny=yrange[0]
    if (yrange[1]==-1):
       maxy=lmaxy
    else:
       maxy=yrange[1]

    if (minx==maxx):
       minx=maxx-0.1
       maxx=maxx+0.1
    if (miny==maxy):
       miny=maxy-0.1
       maxy=maxy+0.1

    #print 'minx,maxx,miny,maxy='+str([minx,maxx,miny,maxy])

    # pygame surface
    pygame_surface=pygame.Surface([xl,yl])
    pygame_surface.fill((225,225,225))


    #print '----------------------------------------------'
    # day pattern with histogram info
    if (colbg): 
       c=1
       dx=xl/(maxx-minx)
       for ix in range(int(minx)-1, int(maxx)+2):
          date=conversion.minimalist_xldate_as_datetime(ix+0.1,0)
          datep1=conversion.minimalist_xldate_as_datetime(ix-0.9,0) # subtract one day to make week start on Monday instead of Sunday
          #datep1=conversion.minimalist_xldate_as_datetime(ix,0)
          w=int(datep1.strftime('%U'))%2
          if (ix>0):
             ds=conversion.exceldate2string(ix+0.1)
          else:
             ds='-----'

          if (w==0):
             if (c==1):
                col=(250,250,250)
                #col=(240,250,240)
             else:
                col=(240,240,240)
                #col=(210,220,210)
          else:
             if (c==1):
                col=(250,255,255)
                #col=(240,240,250)
             else:
                col=(240,250,250)
                #col=(210,210,220)
          c*=-1


          lx=(float(ix)-minx)*dx
          pygame.draw.rect(pygame_surface,col,(lx,0,dx,yl),0)

    # draw curves
    #colar=[(255,0,0,255),(0,255,0,255),(0,0,255,255), (255,255,0,255), (0,255,255,255), (255,0,255,255)]
    colar=[(255,0,0),(0,255,0),(0,0,255), (255,255,0), (0,255,255), (255,0,255)]
    try:
       lidx=1.0/(maxx-minx)
    except:
       lidx=0
    try:
       lidy=1.0/(maxy-miny)
    except:
       lidy=1

    # histograms
    lx=curve[0]
    if drawbghist:
       #print 'drawing background histograms'
       for i in range(len(hist)):
          h1=hist[i][0][0]; h2=hist[i][1][0]
          if (i==0):
             llx=xl*(lx[i]-minx)*lidx
             llx2=xl*(lx[i]-minx+0.5*(lx[i+1]-lx[i]))*lidx
          elif (i==len(hist)-1):
             llx=xl*(lx[i]-minx-0.5*(lx[i]-lx[i-1]))*lidx
             llx2=xl*(lx[i]-minx)*lidx
          else:
             llx=xl*(lx[i-1]-minx+0.5*(lx[i]-lx[i-1]))*lidx
             llx2=xl*(lx[i]+minx+0.5*(lx[i+1]-lx[i]))*lidx
          #llx=xl*(lx[i]-minx)*lidx
          m=max(h1)
          for j in range(len(h1)):
             lly=0.5*yl*float(j)/float(len(h1))
             lly2=0.5*yl*float(j+1)/float(len(h1))
             v=128.0*float(h1[j])/float(m)
             col=(127+v,127,127)
             if (llx2>0.0 and llx<xl):
                try:
                   pygame.draw.rect(pygame_surface,col,(llx,lly,llx2-llx,lly2-lly),0) 
                   #pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),1) 
                except:
                   print('1) draw error coor='+str([llx,lly,llx2,lly2]))
                   sys.exit(1)
          m=max(h2)
          for j in range(len(h2)):
             lly=0.5*yl+0.5*yl*float(j)/float(len(h2))
             lly2=0.5*yl+0.5*yl*float(j+1)/float(len(h2))
             v=128.0*float(h2[j])/float(m)
             col=(127,127+v,127)
             if (llx2>0.0 and llx<xl):
                try:
                   pygame.draw.rect(pygame_surface,col,(llx,lly,llx2-llx,lly2-lly),0) 
                   #pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),1) 
                except:
                   print('2) draw error coor='+str([llx,lly,llx2,lly2]))
                   sys.exit(1)
    #else:
       #print 'not drawing background histograms'
             
    # determine point average point spacing
    dx=[]
    for i in range(len(lx)-1):
       ldx=lx[i+1]-lx[i]
       if (ldx>0.0):
          dx.append(ldx)
    lmindx=min(dx)
    #print 'lmindx='+str(lmindx)

    # curves
    col=colar[color%len(colar)]
    ly=curve[1]
    #print 'lx='+str(lx)
    #print 'ly='+str(ly)
    if (len(lx)>0):
       for i in range(len(lx)-1):
          llx=xl*(lx[i]-minx)*lidx
          lly=yl*(1.0-(ly[i]-miny)*lidy)
          llx2=xl*(lx[i+1]-minx)*lidx
          lly2=yl*(1.0-(ly[i+1]-miny)*lidy)
          if (llx2>0.0 and llx<xl and (lx[i+1]-lx[i])<5.0*lmindx):
             try:
                pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),1) 
             except:
                print('3) draw error coor='+str([llx,lly,llx2,lly2]))
                sys.exit(1)

    # draw level lines
    if (levels and maxy>0.0):
       # orders of magnitude 
       lminy=miny; lmaxy=maxy
       maom=int(math.log(lmaxy,10))
       m=int(lmaxy/10**maom)+1
       maxlin=float(m)*10**(maom)
       #print 'maxy, maom, m,maxlin='+str([maxy, maom, m,maxlin])
       nline=5
       for iline in range(nline):
          val=(float(iline+1)/float(nline))*maxlin
          y=yl*(1.0-(val-lminy)/(lmaxy-lminy))
          #print 'y='+str(y)
          col=(180,180,180)
          pygame.draw.line(pygame_surface,col,(0,y),(xl,y),1) 
          col=(0,0,0)
          pygameprint(pygame_surface,str(val),30,y-4,col,fontsize) 

    # draw base level line
    ndash=100
    col=(255,0,0)
    y=yl*(1.0-(baselevel-miny)/(maxy-miny))
    for idash in range(ndash):
       x1=idash*xl/float(ndash)
       x2=x1+0.5*xl/float(ndash)
       pygame.draw.line(pygame_surface,col,(x1,y),(x2,y),1) 

    # draw legend
    try:
       # determine legend length
       lleg=legend
       nmax=len(lleg)
       x=xl-0.8*float(fontsize*nmax)-10
       y=10
       col=colar[color%len(colar)]          
       pygameprint(pygame_surface,lleg,x,y,col)
    except:
       # no legend
       dum=0

    # display
    image_string = pygame.image.tostring(pygame_surface, "RGB")
    imgWx = wx.Image(width=int(xl), height=int(yl))
    frame.SetClientSize((xl,yl))
    frame.SetMinSize((xl,yl))
    imgWx.SetData(image_string)
    wx_bitmap = imgWx.ConvertToBitmap()

    drawBitmap(frame,wx_bitmap)
    return wx_bitmap

def drawcurves(frame, curves, colors, colbg, xrange, yrange, xl, yl, zoom, xzoom, legend=[], levels=False, fontsize=8, sd=[[],[],[],[],[],[],[],[]], vergrid=False, vergridmaxn=10, linethickness=1, checkskip=True, markers=[], markersize=1, markercols=[0,1,2,3,4,5,6,7],curvemarkers=[False,False,False,False,False,False,False,False], curvemarkersize=1, zoombands=[], ifitcurve=[-1,-1],labelgridline=True,devlinefactor=1.0,horvergridsame=False,text='', datelabels=False, markerboxes=[],levellinemultiplier=0,display=True,command='',comment='',suppressxmargin=True):

    #print 'visual.drawcurves: curves='+str(curves)
    #print 'fontsize='+str(fontsize)
    
    defaultcolors=[(0,0,0),(192,0,0),(0,192,0),(0,0,192),(128,128,128),(96,0,0),(0,96,0),(0,0,96)]

    lminx=1e31; lmaxx=-1e31; lminy=1e31; lmaxy=-1e31

    #xl*=2; yl*=2 # high res (pseudo subpixels)

    if zoom:
       minxzoom=xzoom[0]
       maxxzoom=xzoom[1]

    if command=='printcurves':
       print('printcurves:')
       print('comment='+comment)
       for curve in curves:
          print('curve:')
          for i in range(len(curve[0])):
             print(curve[0][i],', ',curve[1][i])

    icurve=-1
    for curve in curves:
       icurve+=1
       #print 'curve '+str(icurve)
       x=curve[0]; y=curve[1]
       for i in range(len(x)):
          lminx=min(x[i],lminx)
          lmaxx=max(x[i],lmaxx)
          if ((xrange[0]==-1 and xrange[1]==-1) or (x[i]>=xrange[0] and x[i]<=xrange[1])):
             # when zooming in, only look at zoom range y values
             lminy=min(y[i],lminy)
             lmaxy=max(y[i],lmaxy)

    auto=False
    if (xrange[0]==-1):
       minx=lminx
       auto=True
    else:
       minx=xrange[0]
    if (xrange[1]==-1):
       maxx=lmaxx
       auto=True
    else:
       maxx=xrange[1]
    if (yrange[0]==-1):
       miny=lminy
       auto=True
    else:
       miny=yrange[0]
    if (yrange[1]==-1):
       maxy=lmaxy
       auto=True
    else:
       maxy=yrange[1]

    if auto:
       dy=maxy-miny
       miny-=0.10*dy
       maxy+=0.10*dy
       if not suppressxmargin:
          dx=maxx-minx
          minx-=0.10*dx
          maxx+=0.10*dx
    

    if (minx==maxx):
       minx=maxx-0.1
       maxx=maxx+0.1
    if (miny==maxy):
       miny=maxy-0.1
       maxy=maxy+0.1

    #print 'minx,maxx,miny,maxy='+str([minx,maxx,miny,maxy])

    # pygame surface
    pygame_surface=pygame.Surface([xl,yl])
    pygame_surface.fill((225,225,225))


    #print '----------------------------------------------'
    # day pattern
    if (colbg): 
       c=1
       dx=xl/(maxx-minx)
       for ix in range(int(minx)-1, int(maxx)+2):
          #date=conversion.xldate_as_datetime(ix+0.1,0)
          #datep1=conversion.xldate_as_datetime(ix-0.9,0) # subtract one day to make week start on Monday instead of Sunday
          date=conversion.minimalist_xldate_as_datetime(ix+0.1,0)
          datep1=conversion.minimalist_xldate_as_datetime(ix-0.9,0) # subtract one day to make week start on Monday instead of Sunday
          w=int(datep1.strftime('%U'))%2
          if (ix>0):
             ds=conversion.exceldate2string(ix+0.1)
          else:
             ds='-----'
          #print 'date='+str(ix+0.1)+" "+ds+' week number='+date.strftime('%U')+' w='+str(w)+' datestr='+date.strftime('%Y %m %d %H %M %S')
          if (w==0):
             if (c==1):
                col=(250,250,250)
                #col=(240,250,240)
             else:
                col=(240,240,240)
                #col=(210,220,210)
          else:
             if (c==1):
                col=(250,252,255)
                #col=(240,240,250)
             else:
                col=(240,245,250)

          c*=-1
          lx=(float(ix)-minx)*dx
          #print 'lx,dx,yl='+str(lx)+' '+str(dx)+' '+str(yl)
          pygame.draw.rect(pygame_surface,col,(lx,0,dx,yl),0)
          if datelabels:
             #lfontsize=8
             lfontsize=int(dx/3)
             lfontsize=min(lfontsize,10)
             d=conversion.exceldate2string(ix+0.1).split(' ')[0].split('/')[0]
             m=conversion.exceldate2string(ix+0.1).split(' ')[0].split('/')[1]
             ltext=d+'/'+m
             
             xx=lx+0.05*dx
             yy=0.1*yl
             col=(150,150,150)
             #lprint 'text='+text+' lfontsize='+str(lfontsize)+' dx='+str(dx)
             pygameprint(pygame_surface,ltext,xx,yy,col, fontsize=lfontsize)

    # zoom bands
    if (len(zoombands)>0):
       col=(200,200,250)
       lx=xl*(zoombands[0]-minx)/float(maxx-minx)
       dx=xl*(zoombands[1]-zoombands[0])/float(maxx-minx)
       pygame.draw.rect(pygame_surface,col,(lx,0,dx,yl),0)
       ly=yl*(1.0-(zoombands[2]-miny)/float(maxy-miny))
       dy=-yl*(zoombands[3]-zoombands[2])/float(maxy-miny)
       pygame.draw.rect(pygame_surface,col,(0,ly,xl,dy),0)

    # marker boxes
    if (len(markerboxes)>0):
       for item in markerboxes:
          try:
             col=item[2]
          except:
             # no color specified -> make it blue
             col=(0,0,255)
          lx=xl*float(item[0]-minx)/(float(maxx)-float(minx))
          dx=xl*float(item[1]-item[0])/(float(maxx)-float(minx))
          pygame.draw.rect(pygame_surface,col,(lx,0,dx,yl),1)

    # zoom area
    if (zoom):
       col=(255,255,0)
       lx=xl*float(minxzoom-minx)/(float(maxx)-float(minx))
       dx=xl*float(maxxzoom-minxzoom)/(float(maxx)-float(minx))
       #print 'lx='+str(lx)+' dx='+str(dx)
       pygame.draw.rect(pygame_surface,col,(lx,0,dx,yl),1)

    # draw standard deviations and curves
    colar=[(255,0,0),(0,255,0),(0,0,255), (255,255,0), (0,255,255), (255,0,255), (128,0,0),(0,128,0),(0,0,128)]
    #colar=[(255,0,0),(0,255,0),(0,0,255), (255,255,0), (0,255,255), (255,0,255)]
    try:
       lidx=1.0/(maxx-minx)
    except:
       lidx=0
    try:
       lidy=1.0/(maxy-miny)
    except:
       lidy=1

    # standard deviations
    for icurve in range(len(curves)):
       ls=sd[icurve]
       if (len(ls)>0):
          lcol=colar[colors[icurve]%len(colar)]
          col=(lcol[0],lcol[1],lcol[2],50) # add alpha value 
          #col=(lcol[0],lcol[1],lcol[2],128) # add alpha value 
          lx=curves[icurve][0]
          ly=curves[icurve][1]
          lsurf=pygame.Surface([xl,yl], pygame.SRCALPHA)
          #lsurf.fill((0,0,0))
          #lsurf.set_alpha(255)

          # determine point average point spacing
          dx=[]
          for i in range(len(lx)-1):
             ldx=lx[i+1]-lx[i]
             if (ldx>0.0):
                dx.append(ldx)
          lmindx=min(dx)
          #print 'lmindx='+str(lmindx)

          if (len(lx)>0):
             for i in range(len(lx)-1):
                llx=xl*(lx[i]-minx)*lidx
                lly1a=yl*(1.0-(ly[i]-2.0*ls[i]-miny)*lidy)
                lly1b=yl*(1.0-(ly[i]+2.0*ls[i]-miny)*lidy)
                llx2=xl*(lx[i+1]-minx)*lidx
                lly2a=yl*(1.0-(ly[i+1]-2.0*ls[i+1]-miny)*lidy)
                lly2b=yl*(1.0-(ly[i+1]+2.0*ls[i+1]-miny)*lidy)
                pointlist=[[llx,lly1a],[llx2,lly2a],[llx2,lly2b],[llx,lly1b]]
                try:
                   #print 'pointlist='+str(pointlist)
                   if (llx2>0.0 and llx<xl and (lx[i+1]-lx[i])<5.0*lmindx):
                      pygame.draw.polygon(lsurf,col,pointlist,0) 
                except:
                   idum=0

          pygame_surface.blit(lsurf,(0,0))

    # draw lines parallel to base line for scaling
    if ifitcurve[0]>-1:
       lx=[curves[ifitcurve[0]][0][0],curves[ifitcurve[0]][0][-1]]
       ly=[curves[ifitcurve[0]][1][0],curves[ifitcurve[0]][1][-1]]

       maom=int(math.log(maxy,10))
       m=int(maxy/10**maom)+1
       lmin=-2*m
       lmax=2*m
       lstep=10**(maom-1)
       nstep=100*int(lmax/lstep)
       #print 'maom,m,lmin,lmax,lstep,nstep='+str([maom,m,lmin,lmax,lstep,nstep])
       if (nstep<5):
          nstep+=1
          nstep*=10

       #print 'devlinefactor='+str(devlinefactor)
       lnstep=nstep*2**devlinefactor
       nstep=int(lnstep)
       lstep/=2**devlinefactor
       #while nstep>20*devlinefactor:
          #oldnstep=nstep
          #nstep=int(float(nstep)/2.0)
          #if nstep<1:
             #nstep=1
             #break
          #lstep*=float(oldnstep)/float(nstep)
          #print 'lstep='+str(lstep)
        

       deltaflowlist=[]
       for i in range(1,nstep):
          val=-i*lstep
          deltaflowlist.append(val)
       for i in range(1,nstep):
          val=i*lstep
          deltaflowlist.append(val)
       #print 'deltaflowlist='+str(deltaflowlist)
       col=[160,180,160]
       if (len(lx)>0):
          for df in deltaflowlist:
             llx=xl*(lx[0]-minx)*lidx
             lly=yl*(1.0-(ly[0]+df-miny)*lidy)
             llx2=xl*(lx[1]-minx)*lidx
             lly2=yl*(1.0-(ly[1]+df-miny)*lidy)
             dl=(llx2-llx)/50.0
             sl=0.5*dl
             lstr=str(df)
             if df>0:
                lstr='+'+lstr
             drawdashedline(pygame_surface,col,(llx,lly),(llx2,lly2),yl,linethickness,lstr,dl,sl,fontsize,0.05) 
    # draw percentage lines for additions
    if ifitcurve[1]>-1:
       lx=[curves[ifitcurve[1]][0][0],curves[ifitcurve[1]][0][-1]]
       ly=[curves[ifitcurve[1]][1][0],curves[ifitcurve[1]][1][-1]]
       percentages=[]
       for i in range(-100,int(100*(ly[1]/lx[1])+50),10):
          if i!=0:
             percentages.append(i)
       col=[160,160,180]
       if (len(lx)>0):
          for perc in percentages:
             llx=xl*(lx[0]-minx)*lidx
             lly=yl*(1.0-(ly[0]*(1.0+perc/100.0)-miny)*lidy)
             llx2=xl*(lx[1]-minx)*lidx
             lly2=yl*(1.0-(ly[1]*(1.0+perc/100.0)-miny)*lidy)
             dl=(llx2-llx)/50.0
             sl=0.5*dl
             lstr=str(perc)+' %'
             if perc>0:
                lstr='+'+lstr
             drawdashedline(pygame_surface,col,(llx,lly),(llx2,lly2),yl,linethickness,lstr,dl,sl,fontsize,0.1) 

       

    # draw level lines
    amaxy=max(abs(miny),abs(maxy))
    done=False
    extrafact=1
    nloop=0
    while not done:
       if (levels and amaxy>0.0):
          # orders of magnitude 
          maom=int(math.log(amaxy,10))
          #maom=int(math.log(maxy,10))
          m=int(amaxy/10**maom)+1
          #m=int(maxy/10**maom)+1
          maxlin=float(m)*10**(maom)
          nline=int(extrafact*5*2**levellinemultiplier)
          linecount=0
          for iline in range(nline+1):
             val=(float(iline)/float(nline))*maxlin
             y=yl*(1.0-(val-miny)/(maxy-miny))
             if y>=miny and y<=maxy:
                linecount+=1
             #print 'y='+str(y)
             col=(180,180,180)
             pygame.draw.line(pygame_surface,col,(0,y),(xl,y),1) 
             if horvergridsame:
                x=xl*((val-miny)/(maxy-miny))
                #print 'x='+str(x)
                pygame.draw.line(pygame_surface,col,(x,0),(x,yl),1)
             if labelgridline:
                col=(0,0,0)
                pygameprint(pygame_surface,str(val),30,y-int(fontsize/2),col,fontsize) 
          # also for negative y:
          for iline in range(nline):
             val=-(float(iline+1)/float(nline))*maxlin
             y=yl*(1.0-(val-miny)/(maxy-miny))
             if y>=miny and y<=maxy:
                linecount+=1
             #print 'y='+str(y)
             col=(180,180,180)
             pygame.draw.line(pygame_surface,col,(0,y),(xl,y),1) 
             if horvergridsame:
                x=xl*((val-miny)/(maxy-miny))
                pygame.draw.line(pygame_surface,col,(x,0),(x,yl),1)
             if labelgridline:
                col=(0,0,0)
                pygameprint(pygame_surface,str(val),30,y-int(fontsize/2),col,fontsize) 
          if linecount>=2 or nloop>1:
             done=True
          else:
             #print 'refine nloop='+str(nloop)
             extrafact*=2
             nloop+=1
       else:
          done=True

    # draw vertical grid lines
    if (vergrid and maxx>0.0 and (not horvergridsame)):
       # orders of magnitude 
       maom=int(math.log(maxx,10))
       m=int(maxx/10**maom)+1
       maxlin=float(m)*10**(maom)
       #print 'maxy, maom, m,maxlin='+str([maxy, maom, m,maxlin])
       nline=5
       for iline in range(nline+1):
          val=(float(iline)/float(nline))*maxlin
          lx=xl*((val-minx)/(maxx-minx))
          #print 'y='+str(y)
          col=(180,180,180)
          pygame.draw.line(pygame_surface,col,(lx,0),(lx,yl),1)
          col=(0,0,0)
          if labelgridline:
             pygameprint(pygame_surface,str(val),lx-1.5*fontsize,yl-26,col,fontsize) 
       # also for negative y:
       for iline in range(nline):
          val=-(float(iline+1)/float(nline))*maxlin
          lx=xl*((val-minx)/(maxx-minx))
          #print 'y='+str(y)
          col=(180,180,180)
          pygame.draw.line(pygame_surface,col,(lx,0),(lx,yl),1)
          col=(0,0,0)
          if labelgridline:
             pygameprint(pygame_surface,str(val),lx-1.5*fontsize,yl-26,col,fontsize) 

    # curves
    for icurve in range(len(curves)):
       col=colar[colors[icurve]%len(colar)]
       lx=curves[icurve][0]
       ly=curves[icurve][1]
       #print 'lx='+str(lx)
       #print 'ly='+str(ly)

       # determine minimum point spacing
       dx=[]
       for i in range(len(lx)-1):
          ldx=lx[i+1]-lx[i]
          if (ldx>0.0):
             dx.append(ldx)
       if (len(dx)>0):
          lmindx=min(dx)
       else:
          #print 'lmindx set to 1; no data'
          lmindx=1
       #print 'lmindx='+str(lmindx)+' n='+str(len(lx))

       if (len(lx)>0):
          for i in range(len(lx)-1):
             llx=xl*(lx[i]-minx)*lidx
             lly=yl*(1.0-(ly[i]-miny)*lidy)
             llx2=xl*(lx[i+1]-minx)*lidx
             lly2=yl*(1.0-(ly[i+1]-miny)*lidy)
             #print "prepare line "+str([lx[i],ly[i],lx[i+1],ly[i+1]])
             if (llx2>=0.0 and llx<=xl and ((checkskip and (lx[i+1]-lx[i])<2.0*lmindx) or not checkskip) and llx2>=llx):
                try:
                   #print 'draw'
                   pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),linethickness) 
                except:
                   print('4) draw error coor='+str([llx,lly,llx2,lly2]))
                   print('xl,yl,i,lx[i],lx[i+1],minx,ly[i],ly[i+1],miny,lidx,lidy='+str([xl,yl,i,lx[i],lx[i+1],minx,ly[i],ly[i+1],miny,lidx,lidy]))
                   sys.exit(1)

       if (curvemarkers[icurve]):
          for i in range(len(lx)):
             llx=xl*(lx[i]-minx)*lidx
             lly=yl*(1.0-(ly[i]-miny)*lidy)

             llx1=llx-curvemarkersize*xl/300.0
             lly1=lly-curvemarkersize*xl/300.0
             #lly1=lly-curvemarkersize*yl/300.0
             llx2=llx+curvemarkersize*xl/300.0
             lly2=lly+curvemarkersize*xl/300.0
             #lly2=lly+curvemarkersize*yl/300.0
             pygame.draw.line(pygame_surface,col,(llx1,lly1),(llx2,lly2),curvemarkersize) 
             pygame.draw.line(pygame_surface,col,(llx1,lly2),(llx2,lly1),curvemarkersize) 

    # markers
    for imarker in range(len(markers)):
       llx=xl*(markers[imarker][0]-minx)*lidx
       lly=yl*(1.0-(markers[imarker][1]-miny)*lidy)

       # check if it is a tuple or a color index
       if type(markercols[imarker])==tuple:
          col=markercols[imarker]
       elif type(markercols[imarker])==int:
          col=defaultcolors[markercols[imarker]]
       else:
          print('color error')
          sys.exit(1)

       if markersize>0:
          llx1=llx-markersize*xl/300.0
          lly1=lly-markersize*yl/300.0
          llx2=llx+markersize*xl/300.0
          lly2=lly+markersize*yl/300.0

          lt=int(markersize)
          if lt<1:
             lt=1

          pygame.draw.line(pygame_surface,col,(llx1,lly1),(llx2,lly2),lt) 
          pygame.draw.line(pygame_surface,col,(llx1,lly2),(llx2,lly1),lt) 
       else:
          #print 'col,(llx,lly),-markersize)='+str([col,(llx,lly),-markersize])
          pygame.draw.circle(pygame_surface,col,(int(llx),int(lly)),-markersize,0) 
        


    # draw legend
    try:
       # determine legend length
       nmax=0
       for icurve in range(len(curves)):
          lleg=legend[icurve]
          nmax=max(nmax,len(lleg))
       x=xl-0.8*float(fontsize*nmax)-10
       for icurve in range(len(curves)):
          lleg=legend[icurve]
          y=fontsize+int(1.3*fontsize)*icurve
          col=colar[colors[icurve]%len(colar)]          
          pygameprint(pygame_surface,lleg,x,y,col,fontsize)
    except:
       # no legend
       dum=0

    if text!='':
       # print text
       items=text.split('\n')
       iitem=0
       for item in items:
          iitem+=1
          y=0.75*yl+iitem*1.2*(fontsize+2)
          pygameprint(pygame_surface,item,0.6*xl, y,col,fontsize+2) 

    # display
    image_string = pygame.image.tostring(pygame_surface, "RGB")
    imgWx = wx.Image(width=int(xl), height=int(yl))
    imgWx.SetData(image_string)
    #wx_bitmap = imgWx.Scale(xl/2,yl/2).ConvertToBitmap() # high res (pseudo subpixels)
    wx_bitmap = imgWx.ConvertToBitmap()

    if display:
       #frame.SetClientSize((xl,yl)) # nodig?
       #frame.SetMinSize((xl,yl)) # nodig?
       drawBitmap(frame,wx_bitmap)
    return wx_bitmap

def pygameprint(surf,text,xx,yy,color, fontsize=10,angle=0):
   font = pygame.font.SysFont("Helvetica",int(fontsize))
   #font = pygame.font.SysFont("Courier New",fontsize)
   ren = font.render(text,1,color)
   rotate = pygame.transform.rotate
   rren=rotate(ren,angle) # note: angle in degrees ROTATION DOES NOT APPEAR TO WORK
   surf.blit(rren, (xx,yy))

def drawdashedline(pygame_surface,col, xxx_todo_changeme, xxx_todo_changeme1,maxy,linethickness,label, dashlength, skiplength,fontsize,placementfactor):

   (llx,lly) = xxx_todo_changeme
   (llx2,lly2) = xxx_todo_changeme1
   alpha=math.atan2((lly2-lly),(llx2-llx))
   dx=dashlength*math.cos(alpha)
   dy=dashlength*math.sin(alpha)
   dx2=skiplength*math.cos(alpha)
   dy2=skiplength*math.sin(alpha)
   lx=llx
   ly=lly
   # draw dashed line
   while (lx<=llx2): 
      pygame.draw.line(pygame_surface,col,(lx,ly),(lx+dx,ly+dy),linethickness)
      lx+=dx+dx2
      ly+=dy+dy2

   # draw label
   xx=llx+(1.0-placementfactor)*(llx2-llx)-2*0.67*fontsize
   yy=lly+(1.0-placementfactor)*(lly2-lly)
   if yy<0:
      xx=llx+placementfactor*(llx2-llx)-2*0.67*fontsize
      yy=lly+placementfactor*(lly2-lly)
   #print 'alpha,xx,yy='+str([alpha,xx,yy])
   angle=-alpha*math.pi/180.0
   pygameprint(pygame_surface,label,xx,yy,col,fontsize,angle)

def drawMatrix(frame, mat, use, minx, miny, xl, yl, logscale=False,region='A',zerov=0, markers=[], mark=[],bw=False, bounds=[-1,-1], legend='none',display=True,printvaluerange=False,nprior=0,start=1,singledays=False,markercols=[],markerbox=[],label='',suppressscalebar=False, vertlines=[]):

   #print 'drawmatrix: mat='+str(mat)

   if len(mat)==2:
      # two matrices with standard deviations for a and b
      lmat1=mat[0]
      lmat2=mat[1]
      twomat=True
      try:
         zerov1=zerov[0]
         zerov2=zerov[1]
      except:
         zerov1=0.0
         zerov2=0.0
   else:
      # only one matrix
      lmat1=mat
      twomat=False

   nx=lmat1.shape[1]
   ny=lmat1.shape[0]

   if legend=='none':
      dx=float(xl)/float(nx)
      dy=float(yl-20)/float(ny)
      xskip=0
      yskip=0
   elif legend=='monthly' or legend=='numbers' or legend=='datedays':
      dx=float(xl)/float(nx+1)
      dy=float(yl-20)/float(ny+1)
      xskip=dx
      yskip=dy
      monthleg=['J','F','M','A','M','J','J','A','S','O','N','D']


   if (logscale):
      print("not implemented")
      sys.exit(1)
      #if not twomat:
         #lm=[]
         #for iy in range(ny):
            #for ix in range(nx):
               #if (lmat1[iy][ix]>0.0):
                  #lm.append(lmat1[iy][ix])
         #minv=math.log(min(lm),10)
         #maxv=math.log(max(lm),10)
      #else:
         #lm1=[]
         #lm2=[]
         #for iy in range(ny):
            #for ix in range(nx):
               #if (lmat1[iy][ix]>0.0):
                  #lm1.append(lmat1[iy][ix])
               #if (lmat2[iy][ix]>0.0):
                  #lm2.append(lmat2[iy][ix])
         #minv=min(math.log(min(lm1),10),math.log(min(lm2),10))
         #maxv=min(math.log(max(lm1),10),math.log(max(lm2),10))

   else:
      if twomat:
         try:
            minv1=lmat1.min()
            maxv1=lmat1.max()
            minv2=lmat2.min()
            maxv2=lmat2.max()
         except:
            minv1=min(lmat1)
            maxv1=max(lmat1)
            minv2=min(lmat2)
            maxv2=max(lmat2)
         if (minv1==maxv1):
            minv1-=1e-3
            maxv1+=1e-3
         if (minv2==maxv2):
            minv2-=1e-3
            maxv2+=1e-3
         uminv=[minv1,minv2]; umaxv=[maxv1,maxv2]
      else:
         try:
            minv=lmat1.min()
            maxv=lmat1.max()
         except:
            try:
               minv=min(lmat1)
               maxv=max(lmat1)
            except:
               minv=-1e-3
               maxv=1e-3
         if (minv==maxv):
            minv-=1e-3
            maxv+=1e-3
         uminv=minv; umaxv=maxv

   if not twomat:
      if bounds[0]!=-1:
         minv=bounds[0]
      if bounds[1]!=-1:
         maxv=bounds[1]

   pygame_surface=pygame.Surface([xl,yl])
   pygame_surface.fill((255,255,255))
   #pygame_surface.fill((255,255,255,255))
   if not bw:
      pygame.draw.rect(pygame_surface, (235,235,235), (0,0,xl,(ny+1)*dy), 0)
      #pygame.draw.rect(pygame_surface, (235,235,235), (0,0,xl,ny*dy), 0)


   for iy in range(ny):
      y=math.floor(miny+iy*dy)+yskip
      if region=='A':
         ixstart=0
         ixend=nx
      elif region=='U':
         ixstart=iy
         ixend=nx
      for ix in range(ixstart,ixend):
         if use[iy][ix]==1:
            x=math.floor(minx+ix*dx)+xskip
            if (logscale):
               print('error logscale not implemented')
               sys.exit(1)
            else:
               if not twomat:
                  if bw:
                     col=getColbw(minv, zerov,maxv, lmat1[iy][ix])
                  else:
                     col=getCol(minv, zerov,maxv, lmat1[iy][ix])
                  pygame.draw.rect(pygame_surface, col, (x,y,math.ceil(dx),math.ceil(dy)), 0)
                  if bw:
                     # add sign
                     icol=col[0]-128
                     lposx=0.3*dx
                     lposy=0
                     lsize=int(0.9*dx)
                     if icol<0:
                        icol+=255
                     if lmat1[iy][ix]>zerov:
                        pygameprint(pygame_surface,'+',x+lposx,y+lposy,(icol,icol,icol),lsize)
                     elif lmat1[iy][ix]<zerov:
                        pygameprint(pygame_surface,'-',x+lposx,y+lposy,(icol,icol,icol),lsize)
                     else:
                        pygameprint(pygame_surface,'=',x+lposx,y+lposy,(icol,icol,icol),lsize)
               else:
                  if bw:
                     col1=getColbw(minv1, zerov1,maxv1, lmat1[iy][ix])
                     col2=getColbw(minv2, zerov2,maxv2, lmat2[iy][ix])
                  else:
                     col1=getCol(minv1, zerov1,maxv1, lmat1[iy][ix])
                     col2=getCol(minv2, zerov2,maxv2, lmat2[iy][ix])
                  #pygame.draw.rect(pygame_surface, col, (x,y,math.ceil(dx),math.ceil(dy)), 0)
                  polygon1=[[x+dx,y],[x,y],[x,y+dy]]
                  #polygon1=[[x,y],[x+dx,y],[x,y+dy]]
                  polygon2=[[x+dx,y+dy],[x+dx,y],[x,y+dy]]
                  pygame.draw.polygon(pygame_surface,col1,polygon1)
                  pygame.draw.polygon(pygame_surface,col2,polygon2)

   # period indicators
   if not legend=='none':
      if legend=='monthly' or ny<10:
         lsize=int(0.7*dx)
      else:
         lsize=int(0.55*dx)
      # vertical
      x=minx
      for iy in range(ny):
         y=math.floor(miny+iy*dy)+yskip
         if legend=='monthly' or ny<10:
            lposx=0.3*dx
            lposy=0
         else:
            lposx=0.2*dx
            lposy=0.2*dy
         if legend=='monthly':
            jy=iy%12
            pygameprint(pygame_surface,monthleg[jy],x+lposx,y+lposy,(0,0,0),lsize)
         elif legend=='numbers':
            num=iy+1-nprior
            if num<1:
               num-=1 # everything below 1 should be -1, -2, -3 etc. 0 is skipped
            col=(0,0,0)
            iday=start+iy-nprior
            if singledays and conversion.xldateweekday(iday)>=5:
               # weekend days
               col=(0,0,255)
            pygameprint(pygame_surface,str(num),x+lposx,y+lposy,col,lsize)
         elif legend=='datedays':
            iday=start+iy-nprior
            year,month,day=conversion.excelDate2YearMonthDay(iday)
            col=(0,0,0)
            if singledays and conversion.xldateweekday(iday)>=5:
               # weekend days
               col=(0,0,255)
            pygameprint(pygame_surface,str(day),x+lposx,y+lposy,col,lsize)
      # horizontal
      y=miny
      for ix in range(nx):
         x=math.floor(minx+ix*dx)+xskip
         if legend=='monthly' or ny<10:
            lposx=0.3*dx
            lposy=0
         else:
            if (ix<9): # shown number is ix+1, so <9 instead of <10
               lposx=0.4*dx
            else:
               lposx=0.2*dx
            lposy=0.2*dy
         if legend=='monthly':
            jx=ix%12
            pygameprint(pygame_surface,monthleg[jx],x+lposx,y+lposy,(0,0,0),lsize)
         elif legend=='numbers':
            num=ix+1-nprior
            if num<1:
               num-=1 # everything below 1 should be -1, -2, -3 etc. 0 is skipped
            iday=start+ix-nprior
            #iday=start+num-1
            #iday=start-nprior+num-1
            col=(0,0,0)
            if singledays and conversion.xldateweekday(iday)>=5:
               # weekend days
               col=(0,0,255)
            pygameprint(pygame_surface,str(num),x+lposx,y+lposy,col,lsize)
         elif legend=='datedays':
            iday=start+ix-nprior
            year,month,day=conversion.excelDate2YearMonthDay(iday)
            col=(0,0,0)
            if singledays and conversion.xldateweekday(iday)>=5:
               # weekend days
               col=(0,0,255)
            pygameprint(pygame_surface,str(day),x+lposx,y+lposy,col,lsize)

   # draw vertical marker lines
   for vertline in vertlines[:-1]: # last entry is not used
      col=(60,60,60)
      lx=vertline
      llx=math.floor(minx+lx*dx)+xskip
      lly=0
      lly2=math.floor(miny+lx*dy)+yskip
      pygame.draw.line(pygame_surface,col,(llx,lly),(llx,lly2),3) 

   # markers
   if not twomat:
      if len(markers)>0:
         #print 'markers='+str(markers)
         for imarker in range(len(markers)):
            marker=markers[imarker]
            [ix,iy]=marker
            if len(markercols)==0:
               col=(0,0,192)
            else:
               col=markercols[imarker]
            y=math.floor(miny+(iy+1)*dy)
            x=math.floor(minx+(ix+1)*dx)
            pygame.draw.rect(pygame_surface, col, (x,y,math.ceil(dx),math.ceil(dy)), 2)

   # mark clusters
   if not twomat:
      if len(mark)>0:
         #print 'mark='+str(mark)
         for marker in mark:
            [ix,iy]=marker
            y=math.floor(miny+(iy+1.05)*dy)
            x=math.floor(minx+(ix+1.05)*dx)
            pygame.draw.rect(pygame_surface, (0,255,255), (x,y,math.ceil(0.9*dx),math.ceil(0.9*dy)), 1)

   # marker box
   if len(markerbox)>0:
      transp_surface=pygame.Surface([xl,yl],flags=pygame.SRCALPHA)
      basealpha=25
      layercol=(0,0,0,basealpha)
      transp_surface.fill(layercol)
      [ix1,iy1,ix2,iy2]=markerbox
      x1=math.floor(minx+(ix1+1)*dx)
      y1=math.floor(miny+(iy1+1)*dy)
      x2=math.floor(minx+(ix2+1)*dx)
      y2=math.floor(miny+(iy2+(ix2-ix1)+1)*dy)
      xw=math.floor((ix2-ix1)*dx)-1
      xw2=math.floor((nx-ix2)*dx)-1
      yh=math.floor((iy2-iy1)*dy)-1
      pygame.draw.rect(transp_surface, (0,0,0,0), (x1+1,y1+1,xw-2,yh-2), 0)
      pygame.draw.rect(transp_surface, (0,0,0,0), (x2+1,y1+yh+1,xw2-2,xw-2), 0)
      nwidth=15
      for iring in range(nwidth):
         a=255-int(float(iring)**0.5/float(nwidth-1)**0.5*(255-basealpha))
         col=(layercol[0],layercol[1],layercol[2],a)

         pointlist=[(x1-iring,y1-iring),\
                    (x2+iring-1,y1-iring),\
                    (x2+iring-1,y1+yh-iring),\
                    (x2+xw2+iring,y1+yh-iring),\
                    (x2+xw2+iring,y1+yh+xw+iring),\
                    (x2-iring-1,y1+yh+xw+iring),\
                    (x2-iring-1,y1+yh+iring),\
                    (x1-iring,y1+yh+iring),\
                    (x1-iring,y1-iring)]
                   
         pygame.draw.polygon(transp_surface,col,pointlist,1)
         #pygame.draw.rect(transp_surface, col, (x1-iring,y1-iring,xw+2*iring,yh+2*iring), 1)
         #if not (ix2==nx):
            #pygame.draw.rect(transp_surface, col, (x2-iring,y1+yh-iring,xw2+2*iring,xw+2*iring), 1)
      # clear centers
      #pygame.draw.rect(transp_surface, (0,0,0,0), (x1+1,y1+1,xw-2,yh-2), 0)
      #pygame.draw.rect(transp_surface, (0,0,0,0), (x2+1,y1+yh+1,xw2-2,xw-2), 0)
      pygame_surface.blit(transp_surface,(0,0))

   # print value range
   if printvaluerange:
      iy=ny-2
      #iy=ny-1
      y=math.floor(miny+iy*dy)+yskip
      ix=1
      x=math.floor(minx+ix*dx)+xskip
      #print 'type(uminv)='+str(type(uminv))
      if type(uminv)==tuple or type(uminv)==list:
         lstr='value ranges %2.2f - %2.2f and %2.2f - %2.2f' % (uminv[0],umaxv[0],uminv[1],umaxv[1])
         lsize=0.04*xl
         #lsize=int(0.5*dx)
         y+=int(0.2*dy)
      else:
         lstr='value range %2.2f - %2.2f' % (uminv,umaxv)
         lsize=0.05*xl
         #lsize=int(0.7*dx)
      pygameprint(pygame_surface,lstr,x,y,(0,0,0),lsize)

   # print label
   if not label=='':
      if ny<10:
         lposx=0.3*dx
         lposy=0
      else:
         lposx=0.2*dx
         lposy=0.2*dy
      iy=ny-2
      y=math.floor(miny+iy*dy)+yskip
      ix=1
      x=math.floor(minx+ix*dx)+xskip
      pygameprint(pygame_surface,label,x+lposx,y+lposy,(0,0,0),lsize)
     

   # scale bar(s)
   if not suppressscalebar:
      if not twomat:
         nsub=100
         sbwidth=xl
         sbheight=15
         py1=miny+yl-sbheight+5
         pdx=sbwidth/float(nsub)
         pdy=sbheight
         for isub in range(nsub):
            px1=minx+float(isub)*pdx
            v=minv+float(isub)*(maxv-minv)/float(nsub)
            if bw:
               col=getColbw(minv, zerov,maxv, v)
            else:
               col=getCol(minv, zerov,maxv, v)
            pygame_surface.fill(col, (px1,py1,pdx,pdy))
      else:
         nsub=50
         sbwidth=xl/2.0-10
         sbheight=15
         py1=miny+yl-sbheight+5
         pdx=sbwidth/float(nsub)
         pdy=sbheight
         for isub in range(nsub):
            px1=minx+float(isub)*pdx
            v=minv1+float(isub)*(maxv1-minv1)/float(nsub)
            if bw:
               col=getColbw(minv1, zerov1,maxv1, v)
            else:
               col=getCol(minv1, zerov1,maxv1, v)
            pygame_surface.fill(col, (px1,py1,pdx,pdy))
         for isub in range(nsub):
            px1=minx+xl/2+10+float(isub)*pdx
            v=minv2+float(isub)*(maxv2-minv2)/float(nsub)
            if bw:
               col=getColbw(minv2, zerov2,maxv2, v)
            else:
               col=getCol(minv2, zerov2,maxv2, v)
            pygame_surface.fill(col, (px1,py1,pdx,pdy))
     

   # display
   image_string = pygame.image.tostring(pygame_surface, "RGB")
   imgWx = wx.Image(width=int(xl), height=int(yl))
   imgWx.SetData(image_string)
   wx_bitmap = imgWx.ConvertToBitmap()

   if display:
      drawBitmap(frame,wx_bitmap)

   return uminv,umaxv,wx_bitmap

def getCol(minv, zerov,maxv, v):
   # first limb 0-127: blue-white

   if v==None:
      return 255,255,0
   elif v==float('NaN') or v==float('Inf') or v==float('-Inf'):
      return 255,255,0

   if v<zerov:
      l=(v-minv)/(zerov-minv)
      if l<0.0:
         l=0.0
      elif l>1.0:
         l=1.0
      try:
         r=int(255.0*l)
      except ValueError:
         return 255,255,0
      #r=int(255.0*(v-minv)/(zerov-minv))
      col=r,r,255
   elif v==zerov:
      col=255,255,255
   else:
      l=(v-zerov)/(maxv-zerov)
      if l<0.0:
         l=0.0
      elif l>1.0:
         l=1.0
      try:
         r=int(255.0*l)
      except ValueError:
         return 255,255,0
      #r=int(255.0*(v-zerov)/(maxv-zerov))
      col=255,255-r,255-r

   #print 'col='+str(col)
   return col

def getColbw(minv, zerov,maxv, v):
   # first limb 0-127: blue-white

   mmv=max(abs(zerov-minv),abs(maxv-zerov))

   if v==zerov:
      r=0
   else:
      r=int(255.0*abs(zerov-v)/mmv)

   if r<0: 
      r=0
   if r>255:
      r=255

   col=255-r,255-r,255-r

   #if r>255:
      #print 'getColbw:'
      #print 'v,zerov,minv,maxv,mmv,r='+str([v,zerov,minv,maxv,mmv,r]) 

   #print 'col='+str(col)
   return col

def drawGaussCurves(frame,vals,sds,xl,yl,cols=[],showlabels=True,histdata=[]):

   pygame_surface=pygame.Surface([xl,yl])
   pygame_surface.fill((255,255,255))
   if len(vals)>0:

      if len(cols)==0:
         d=int(255.0/float(len(vals)))
         for i in range(len(vals)):
            r=i; g=255-i; b=127+i/2 
            cols.append((r,g,b))

      minv=min(vals); maxv=max(vals)
      maxsd=max(sds)

      minx=minv-3.0*maxsd; maxx=maxv+3.0*maxsd
      xscalefact=float(xl)/(maxx-minx)

      maxy=0.0
      for i in range(len(vals)):
         maxy=max(maxy,gaussfunc(vals[i],vals[i],sds[i]))

      yscalefact=float(yl)/maxy

      # draw histogram for selected block
      if len(histdata)>0:

         # first generate histogram out of data
         nbin=int(len(vals)/10)
         if nbin<20:
            nbin=20
         if nbin>100:
            nbin=100
         hist,binedges=numpy.histogram(histdata,bins=nbin,range=(minx,maxx))

         maxn=max(hist)
 
         dx=xl/float(len(hist))
         col=(200,255,200)
         for i in range(len(hist)):
            lx=0.5*(binedges[i]+binedges[i+1])
            x=xscalefact*(lx-minx)
            y=yl*(1.0-float(hist[i])/float(maxn))
            lbarl=yl*float(hist[i])/float(maxn)
            pygame.draw.rect(pygame_surface,col,(x,y,dx,lbarl),0)

      if showlabels:
         # draw level lines
         gridlinelocations=getgridlinelocations(minx,maxx,1.0,0.0,1.0)
         col=(127,127,127)
         colt=(127,127,180)
         for gridlinelocation in gridlinelocations:
            x1=xscalefact*(gridlinelocation-minx)
            x2=xscalefact*(gridlinelocation-minx)
            y1=0
            y2=yl
            pygame.draw.line(pygame_surface, col, [x1,y1], [x2,y2], 1)
            
            lstr='%2.2f' % gridlinelocation
            pygameprint(pygame_surface,lstr,x1-4,0.1*yl,colt,8) 

      # draw gauss curves on top
      nseg=100
      #for i in range(len(vals)-1,-1,-1): # draw in reverse order
      for i in range(len(vals)):
         if (sds[i]>0):
            for iseg in range(nseg):
               dx=6*sds[i]/float(nseg)
               lx1=vals[i]-3.0*sds[i]+iseg*dx
               lx2=vals[i]-3.0*sds[i]+(iseg+1)*dx
               ly1=gaussfunc(lx1,vals[i],sds[i])
               ly2=gaussfunc(lx2,vals[i],sds[i])

               x1=xscalefact*(lx1-minx)
               x2=xscalefact*(lx2-minx)
               y1=yl-yscalefact*ly1
               y2=yl-yscalefact*ly2
               pygame.draw.line(pygame_surface, cols[i], [x1,y1], [x2,y2], 2)

   # display
   image_string = pygame.image.tostring(pygame_surface, "RGB")
   imgWx = wx.Image(width=int(xl), height=int(yl))
   frame.SetClientSize((xl,yl))
   frame.SetMinSize((xl,yl))
   imgWx.SetData(image_string)
   wx_bitmap = imgWx.ConvertToBitmap()

   drawBitmap(frame,wx_bitmap)
   return wx_bitmap

def gaussfunc(x,mu,sigma):
   res=(1.0/(math.sqrt(2.0*math.pi*sigma*sigma)))*math.exp(-(x-mu)**2/(2.0*sigma*sigma))
   return res

def drawsimplepointcloud(frame, x,y, xrange, yrange, xl, yl,markercols=[],display=True, colorbyindex=False,circlemarkerindices=[],drawonetooneline=False,markersize=2,drawpath=False,textlabels=[],labelsize=10,sdcontourdata=[],remark='', remarkpos=[-1,-1], remarkfontsize=12):
    # every item in both x and y is a list of x- or y-coordinates

    lminx=1e33; lmaxx=-1e33
    lminy=1e33; lmaxy=-1e33
    for lx in x:
       lminx=min(lminx,min(lx))
       lmaxx=max(lmaxx,min(lx))
    for ly in y:
       lminy=min(lminy,min(ly))
       lmaxy=max(lmaxy,min(ly))

    #print 'drawsimplepointcloud: lminx,lmaxx,lminy,lmaxy='+str([lminx,lmaxx,lminy,lmaxy])

    auto=False
    if (xrange[0]==-1):
       minx=lminx
       auto=True
    else:
       minx=xrange[0]
    if (xrange[1]==-1):
       maxx=lmaxx
       auto=True
    else:
       maxx=xrange[1]
    if (yrange[0]==-1):
       miny=lminy
       auto=True
    else:
       miny=yrange[0]
    if (yrange[1]==-1):
       maxy=lmaxy
       auto=True
    else:
       maxy=yrange[1]

    if auto:
       dy=maxy-miny
       miny-=0.05*dy
       maxy+=0.05*dy
    

    if (minx==maxx):
       minx=maxx-0.1
       maxx=maxx+0.1
    if (miny==maxy):
       miny=maxy-0.1
       maxy=maxy+0.1

    try:
       lidx=1.0/(maxx-minx)
    except:
       lidx=0
    try:
       lidy=1.0/(maxy-miny)
    except:
       lidy=1

    # pygame surface
    pygame_surface=pygame.Surface([xl,yl])
    pygame_surface.fill((255,255,255))
    #pygame_surface.fill((225,225,225))

    if drawonetooneline:
       # draw 1:1 line
       col=(0,128,0)
       lmin=min(minx,miny)
       lmax=min(maxx,maxy)
       x1=xl*(lmin-minx)*lidx
       y1=yl*(1.0-(lmin-miny)*lidy)
       x2=xl*(lmax-minx)*lidx
       y2=yl*(1.0-(lmax-miny)*lidy)
       pygame.draw.line(pygame_surface,col,(x1,y1),(x2,y2),1) 

    # draw standard deviation contours for point clouds
    if len(sdcontourdata)>0:
       means=sdcontourdata[0]
       pcav1=sdcontourdata[1]
       pcav2=sdcontourdata[2]
       rotatedsds=sdcontourdata[3]

       # number of ellipses required
       nellips=int(math.sqrt((xl*lidx)**2+(yl*lidy)**2)/min(rotatedsds))
       nellips=min(nellips,20) # maximize number
 
       # plot
       col=(128,0,128)
       for iellips in range(nellips):
          nseg=100
          dseg=2.0*math.pi/float(nseg)
          for iseg in range(nseg):
             alpha0=float(iseg)*dseg 
             alpha1=float(iseg+1)*dseg 

             odx1=rotatedsds[0]*float(iellips+1)*math.cos(alpha0)
             ody1=rotatedsds[1]*float(iellips+1)*math.sin(alpha0)
             odx2=rotatedsds[0]*float(iellips+1)*math.cos(alpha1)
             ody2=rotatedsds[1]*float(iellips+1)*math.sin(alpha1)

             x1=means[0]+pcav1[0]*odx1+pcav2[0]*ody1
             y1=means[1]-pcav1[1]*odx1-pcav2[1]*ody1
             x2=means[0]+pcav1[0]*odx2+pcav2[0]*ody2
             y2=means[1]-pcav1[1]*odx2-pcav2[1]*ody2

             #x1=means[0]+pcav1[0]*rotatedsds[0]*float(iellips+1)*math.cos(alpha0) \
                        #+pcav2[0]*rotatedsds[1]*float(iellips+1)*math.sin(alpha0)
             #y1=means[1]-pcav1[1]*rotatedsds[0]*float(iellips+1)*math.sin(alpha0) \
                        #-pcav2[1]*rotatedsds[1]*float(iellips+1)*math.cos(alpha0)
             #x2=means[0]+pcav1[0]*rotatedsds[0]*float(iellips+1)*math.cos(alpha1) \
                        #+pcav2[0]*rotatedsds[1]*float(iellips+1)*math.sin(alpha1)
             #y2=means[1]-pcav1[1]*rotatedsds[0]*float(iellips+1)*math.sin(alpha1) \
                        #-pcav2[1]*rotatedsds[1]*float(iellips+1)*math.cos(alpha1)
             lx1=xl*(x1-minx)*lidx
             ly1=yl*(1.0-(y1-miny)*lidy)
             lx2=xl*(x2-minx)*lidx
             ly2=yl*(1.0-(y2-miny)*lidy)
             pygame.draw.line(pygame_surface,col,(lx1,ly1),(lx2,ly2),1) 

    # draw paths
    collist=[(0,0,0),(0,192,0),(192,0,0)]
    if drawpath:
       for i in range(len(x)-1):
          if colorbyindex:
             col=supportfunctions.getcolor('blue-yellow-red',0,len(x)-1,i)
          elif len(markercols)==0:
             col=(0,0,0)
          else:
             if type(markercols[0])==tuple:
                col=markercols[i]
             elif type(markercols[0])==int:
                col=collist[markercols[i]]
             else:
                print('error: marker color definition type')
                sys.exit(1)
          lx=x[i][0]
          ly=y[i][0]
          llx=xl*(lx-minx)*lidx
          lly=yl*(1.0-(ly-miny)*lidy)
          lx2=x[i+1][0]
          ly2=y[i+1][0]
          llx2=xl*(lx2-minx)*lidx
          lly2=yl*(1.0-(ly2-miny)*lidy)
          pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),1) 
          kx=(llx+llx2)/2.0; ky=(lly+lly2)/2.0
          drawarrow(pygame_surface,kx,ky,col,3,[llx2-llx,lly2-lly],False)

    # draw points
    for i in range(len(x)):
       if colorbyindex:
          col=supportfunctions.getcolor('blue-yellow-red',0,len(x)-1,i)
       elif len(markercols)==0:
          col=(0,0,0)
       else:
          if type(markercols[0])==tuple:
             col=markercols[i]
          elif type(markercols[0])==int:
             col=collist[markercols[i]]
          else:
             print('error: marker color definition type')
             sys.exit(1)
       for lx in x[i]:
          for ly in y[i]:
             llx=xl*(lx-minx)*lidx
             lly=yl*(1.0-(ly-miny)*lidy)
             try:
                pygame.draw.circle(pygame_surface,col,(int(llx),int(lly)),markersize,0) 
             except ValueError:
                idum=0

    # draw circle markers
    for i in circlemarkerindices:
       if i>-1:
          #print 'circle marker:'+str(i)
          col=(0,0,0)
          for lx in x[i]:
             for ly in y[i]:
                llx=xl*(lx-minx)*lidx
                lly=yl*(1.0-(ly-miny)*lidy)
                pygame.draw.circle(pygame_surface,col,(int(llx),int(lly)),4*markersize,2) 

    # draw text labels
    for textlabel in textlabels:
       coor=textlabel[0]
       label=textlabel[1]
       col=(0,0,0)
       llx=xl*(coor[0]-minx)*lidx
       lly=yl*(1.0-(coor[1]-miny)*lidy)
       pygame.draw.circle(pygame_surface,col,(int(llx),int(lly)),int(0.5*float(labelsize)),1) 
       pygameprint(pygame_surface,label,llx+int(0.7*float(labelsize)),lly-int(0.5*float(labelsize)),col,labelsize) 

    # draw remark
    if not remark=='':
       llx=xl*remarkpos[0] 
       lly=yl*remarkpos[1] 
       col=(0,0,0)
       pygameprint(pygame_surface,remark,llx,lly,col,remarkfontsize) 
        
    # display
    image_string = pygame.image.tostring(pygame_surface, "RGB")
    imgWx = wx.Image(width=int(xl), height=int(yl))
    #if display: # do we need this code?
       #frame.SetClientSize((xl,yl))
       #frame.SetMinSize((xl,yl))
    imgWx.SetData(image_string)
    wx_bitmap = imgWx.ConvertToBitmap()

    if display:
       drawBitmap(frame,wx_bitmap)
    return wx_bitmap,[minx,maxx,miny,maxy]

def getgridlinelocations(minval,maxval,l,mincoor,maxcoor):
    done=False
    absmaxval=max(abs(minval),abs(maxval))
    #print 'absmaxval='+str(absmaxval)
    extrafact=1
    nloop=0
    while not done:
       coors=[]
       if absmaxval>0.0:
           # orders of magnitude 
           maom=int(math.log(absmaxval,10))
           m=int(absmaxval/10**maom)+1
           maxlin=float(m)*10**(maom)
           nline=extrafact*10
           #print 'maom,m,maxlin,nline='+str([maom,m,maxlin,nline])
           linecount=0
           for iline in range(nline+1):
              val=(float(iline)/float(nline))*maxlin
              y=l*(1.0-(val-minval)/(maxval-minval))
              if y>=mincoor and y<=maxcoor:
                 linecount+=1
                 coors.append(val)
           # also for negative y:
           for iline in range(nline):
              val=-(float(iline+1)/float(nline))*maxlin
              y=l*(1.0-(val-minval)/(maxval-minval))
              if y>=mincoor and y<=maxcoor:
                 linecount+=1
                 coors.append(val)
           if linecount>=3 or nloop>1:
              done=True
           else:
              #print 'refine nloop='+str(nloop)
              extrafact*=2
              nloop+=1
       else:
           done=True

    #print 'coors='+str(coors)
    return coors

def drawarrow(pygame_surface,x,y,col,size,vec,invertarrow):
   dirvec=normvec(vec) # make length 1
   if invertarrow:
      dirvec[0]*=-1.0
      dirvec[1]*=-1.0
   perpvec=[dirvec[1],-dirvec[0]]
   #print 'dirvec='+str(dirvec)+'  perpvec='+str(perpvec)

   x1=float(x)-float(size)*dirvec[0]+float(size)*perpvec[0]
   y1=float(y)-float(size)*dirvec[1]+float(size)*perpvec[1]
   x2=float(x)-float(size)*dirvec[0]-float(size)*perpvec[0]
   y2=float(y)-float(size)*dirvec[1]-float(size)*perpvec[1]

   pygame.draw.line(pygame_surface,col,(x1,y1),(x,y),1)
   pygame.draw.line(pygame_surface,col,(x2,y2),(x,y),1)

def normvec(vec):
   v=0.0
   for val in vec:
      v+=float(val)*float(val)
   outvec=[]
   if v>0.0:
      sqv=math.sqrt(v)
   else:
      sqv=1.0
   for val in vec:
      outvec.append(float(val)/sqv)
   return outvec

def drawsimplecurves(frame, curves, colors, linethicknesses, xl, yl, levels=False, fontsize=8,display=True,vertlines=[]):
    lminx=1e31; lmaxx=-1e31; lminy=1e31; lmaxy=-1e31

    #print 'drawsimplecurves: curves='+str(curves)

    #xl*=2; yl*=2 # high res (pseudo subpixels)

    icurve=-1
    for curve in curves:
       icurve+=1
       #print 'curve '+str(icurve)
       x=curve[0]; y=curve[1]
       for i in range(len(x)):
          lminx=min(x[i],lminx)
          lmaxx=max(x[i],lmaxx)
          lminy=min(y[i],lminy)
          lmaxy=max(y[i],lmaxy)

    minx=lminx
    maxx=lmaxx
    miny=lminy
    maxy=lmaxy

    dy=maxy-miny
    miny-=0.10*dy
    maxy+=0.10*dy

    if (minx==maxx):
       minx=maxx-0.1
       maxx=maxx+0.1
    if (miny==maxy):
       miny=maxy-0.1
       maxy=maxy+0.1

    #print 'drawsimplecurves: minx,maxx,miny,maxy,dy='+str([minx,maxx,miny,maxy,dy])

    # pygame surface
    pygame_surface=pygame.Surface([xl,yl])
    pygame_surface.fill((255,255,255))

    try:
       lidx=1.0/(maxx-minx)
    except:
       lidx=0
    try:
       lidy=1.0/(maxy-miny)
    except:
       lidy=1

    # draw level lines
    amaxy=max(abs(miny),abs(maxy))
    done=False
    extrafact=1.0
    nloop=0
    if miny>-1e10 and maxy<1e10 and len(curves)>0:
       while not done:
          if (levels and amaxy>0.0):
             # orders of magnitude 
             maom=int(math.log(amaxy,10))
             #maom=int(math.log(maxy,10))
             m=int(amaxy/10**maom)+1
             #m=int(maxy/10**maom)+1
             maxlin=float(m)*10**(maom)
             nline=int(extrafact*5)
             #print 'maxlin,nline='+str([maxlin,nline])
             linecount=0
             for iline in range(nline+1):
                val=(float(iline)/float(nline))*maxlin
                y=yl*(1.0-(val-miny)/(maxy-miny))
                #print 'y,miny,maxy='+str([y,miny,maxy])
                if val>=miny and val<=maxy:
                   linecount+=1
                #print 'y='+str(y)
                col=(180,180,180)
                pygame.draw.line(pygame_surface,col,(0,y),(xl,y),1) 
                col=(0,0,0)
                pygameprint(pygame_surface,str(val),30,y-int(fontsize/2),col,fontsize) 
             # also for negative y:
             for iline in range(nline):
                val=-(float(iline+1)/float(nline))*maxlin
                y=yl*(1.0-(val-miny)/(maxy-miny))
                if val>=miny and val<=maxy:
                   linecount+=1
                #print 'y='+str(y)
                col=(180,180,180)
                pygame.draw.line(pygame_surface,col,(0,y),(xl,y),1) 
                col=(0,0,0)
                pygameprint(pygame_surface,str(val),30,y-int(fontsize/2),col,fontsize) 
             if linecount>=2 and linecount<=6 or nloop>5:
                done=True
             elif linecount<2 :
                #print 'refine nloop='+str(nloop)
                extrafact*=2
                nloop+=1
             else:
                extrafact*=0.5
                nloop+=1
                pygame_surface.fill((255,255,255)) # remove old lines
             #print 'linecount,extrafact,nloop,done='+str([linecount,extrafact,nloop,done])
          else:
             done=True

    # draw vertical marker lines
    for vertline in vertlines:
       col=(60,60,60)
       lx=vertline
       llx=xl*(lx-minx)*lidx
       lly=0
       lly2=yl
       pygame.draw.line(pygame_surface,col,(llx,lly),(llx,lly2),1) 

    # curves
    for icurve in range(len(curves)):
       col=colors[icurve]
       lx=curves[icurve][0]
       ly=curves[icurve][1]
       lt=linethicknesses[icurve]

       if (len(lx)>0):
          for i in range(len(lx)-1):
             llx=xl*(lx[i]-minx)*lidx
             lly=yl*(1.0-(ly[i]-miny)*lidy)
             llx2=xl*(lx[i+1]-minx)*lidx
             lly2=yl*(1.0-(ly[i+1]-miny)*lidy)
             pygame.draw.line(pygame_surface,col,(llx,lly),(llx2,lly2),lt) 

    # display
    image_string = pygame.image.tostring(pygame_surface, "RGB")
    imgWx = wx.Image(width=int(xl), height=int(yl))
    imgWx.SetData(image_string)
    #wx_bitmap = imgWx.Scale(xl/2,yl/2).ConvertToBitmap() # high res (pseudo subpixels)
    wx_bitmap = imgWx.ConvertToBitmap()

    if display:
       drawBitmap(frame,wx_bitmap)
    return wx_bitmap

