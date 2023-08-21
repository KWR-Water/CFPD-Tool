# python modules
import datetime
import math
import sys
import wx
import numpy

# flowstat modules
import conversion

def getDateTimeSelections(xdat):
   # produce a list of default start and end dates/times based on dataset
   minx=min(xdat)
   maxx=max(xdat)
   startx=math.floor(minx)

   # definitions
   onesec=1.0/86400.0
  
   miny,minm,mind=conversion.excelDate2YearMonthDay(minx)
   maxy,maxm,maxd=conversion.excelDate2YearMonthDay(maxx)

   print('miny,minm,mind='+str([miny,minm,mind]))
   print('maxy,maxm,maxd='+str([maxy,maxm,maxd]))

   nday=int(math.floor(maxx)-math.floor(minx)+1)

   optionliststart=[]; optionlistend=[]
   if nday<=31:
      # individual days
      for i in range(nday):
         optionliststart.append(conversion.exceldate2string(startx+i) )
         optionlistend.append(conversion.exceldate2string(startx+i+1-onesec) )
   elif nday<=92:
      # weeks
      nweek=int(math.ceil(nday/7.0))
      for i in range(nweek):
         optionliststart.append(conversion.exceldate2string(startx+7*i) )
         optionlistend.append(conversion.exceldate2string(startx+7*(i+1)-onesec) )
   elif nday<=750:
      # months
      nmon=maxm-minm+1+12*(maxy-miny)
      y=miny
      #print 'minm,maxm,miny,maxy,nmon='+str([minm,maxm,miny,maxy,nmon])
      for i in range(nmon):
         m=minm+i
         y=int(miny+math.floor(float(m)/12.0))
         m=m%12.0
         if m==0:
            m=12
            y-=1
         dts=datetime.datetime(int(y),int(m),1,0,0,0)
         edts=conversion.date2exceldate(dts)
         optionliststart.append(conversion.exceldate2string(edts) )
         m=minm+i+1
         y=int(miny+math.floor(float(m)/12.0))
         m=m%12.0
         if m==0:
            m=12
            y-=1
         dte=datetime.datetime(int(y),int(m),1,0,0,0)
         edte=conversion.date2exceldate(dte)
         edte-=onesec
         optionlistend.append(conversion.exceldate2string(edte))
   else:
      # years
      nyear=maxy-miny+1
      for i in range(nyear):
         y=miny+i
         dts=datetime.datetime(int(y),1,1,0,0,0)
         edts=conversion.date2exceldate(dts)
         optionliststart.append(conversion.exceldate2string(edts) )
         y=miny+i+1
         dte=datetime.datetime(y,1,1,0,0,0)
         edte=conversion.date2exceldate(dte)
         edte-=onesec
         optionlistend.append(conversion.exceldate2string(edte))

   return optionliststart,optionlistend


def blockAnalysisFilterControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):

    # controls
    x=x0; y=y0
    x=int(x)
    y=int(y)    
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl)

    # data filtering control
    # options
    label=wx.StaticText(window,-1,'Data filtering:',pos=(x,y))
    label.SetFont(parent.textfont)
    x1=int(margin1); x2=int(x1+xbs); x3=int(x2+2*xbs); x4=int(x3+7.5*xbs)
    y+=ybs+margin1
    parent.filteringrb_none=wx.RadioButton(window, -1, 'none', (x1,y), style=wx.RB_GROUP)
    parent.filteringrb_none.SetFont(parent.textfont)
    parent.filteringrb_dev=wx.RadioButton(window, -1, 'Deviating nodes', (x2,y))
    parent.filteringrb_dev.SetFont(parent.textfont)
    parent.filteringrb_clust=wx.RadioButton(window, -1, 'Consistent clusters', (x3,y))
    parent.filteringrb_clust.SetFont(parent.textfont)
    parent.filteringrb_time=wx.RadioButton(window, -1, 'Timing combo', (x4,y))
    parent.filteringrb_time.SetFont(parent.textfont)
    parent.filteringrb_none.SetValue(True)

    # consistent fraction
    x=x2; y+=ybs+margin1
    mcfulabel=wx.StaticText(window,-1,'fraction used:',pos=(x,y))
    mcfulabel.SetFont(parent.textfont)
    x+=xbs; y-=4
    parent.consistentfractionspin=wx.SpinCtrl(window, -1, value=str(parent.consistentfraction), pos=(x, y), size=(50,ybs), min=10, max=100)
    parent.consistentfractionspin.SetFont(parent.textfont)
    x+=55; y+=4
    mcfu2label=wx.StaticText(window,-1,'%',pos=(x,y))
    mcfu2label.SetFont(parent.textfont)

    # cluster analysis
    x=x3
    nuslabel=wx.StaticText(window,-1,'number of sections:',pos=(x,y))
    nuslabel.SetFont(parent.textfont)
    x+=1.4*xbs; y-=4
    parent.numberofsectionsspin=wx.SpinCtrl(window, -1, value=str(parent.numberofsections), pos=(x, y), size=(50,ybs), min=4, max=100)
    parent.numberofsectionsspin.SetFont(parent.textfont)
    x+=60; y+=4
    subdilabel=wx.StaticText(window,-1,'subdivision:',pos=(x,y))
    subdilabel.SetFont(parent.textfont)
    x+=int(0.9*xbs); y-=4
    vals=["optimal","equal size"]
    parent.subdivisionmethodcombo=wx.ComboBox(window, -1, value=parent.subdivisionmethod, pos=(x, y), size=(1.2*xbs,ybs),choices=vals)
    parent.subdivisionmethodcombo.SetToolTip(wx.ToolTip('Determines how node sections are created.'))
    parent.subdivisionmethodcombo.SetFont(parent.textfont)
    x+=int(1.3*xbs); y+=4
    keeplabel=wx.StaticText(window,-1,'keep:',pos=(x,y))
    keeplabel.SetFont(parent.textfont)
    x+=int(0.5*xbs); y-=4
    parent.numberofsectionskeepspin=wx.SpinCtrl(window, -1, value=str(parent.numberofsectionskeep), pos=(x, y), size=(40,ybs), min=1, max=100)
    parent.numberofsectionskeepspin.SetFont(parent.textfont)
    x+=50; y+=4
    critlabel=wx.StaticText(window,-1,'criterion:',pos=(x,y))
    critlabel.SetFont(parent.textfont)
    x+=int(0.7*xbs); y-=4
    vals=["median a","linear fit"]
    parent.clustercriterioncombo=wx.ComboBox(window, -1, value=parent.clustercriterion, pos=(x, y), size=(1.2*xbs,ybs),choices=vals)
    parent.clustercriterioncombo.SetToolTip(wx.ToolTip('Determines how node sections are rated. "Median a" discards sections with an a value deviating most from the median a. "Linear fit" discards sections which deviate most from the linear best fit of a,b values for all sections.'))
    parent.clustercriterioncombo.SetFont(parent.textfont)

    # timing combo filtering
    x=x4; y+=4
    timingcombolabel=wx.StaticText(window,-1,'fraction used:',pos=(x,y))
    timingcombolabel.SetFont(parent.textfont)
    x+=xbs; y-=4
    parent.timingcombofractionspin=wx.SpinCtrl(window, -1, value=str(parent.timingcombofraction), pos=(x, y), size=(50,ybs), min=1, max=100)
    parent.timingcombofractionspin.SetFont(parent.textfont)
    x+=55; y+=4
    timingcombolabel2=wx.StaticText(window,-1,'%',pos=(x,y))
    timingcombolabel2.SetFont(parent.textfont)

    y+=ybs+margin1
  
    return y

def blockAnalysisPeriodControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):
    # controls
    x=x0; y=y0
    
    x=int(x)
    y=int(y)
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl)    

    parent.setperiodrb=wx.RadioButton(window,id=-1,label='Set period length (days)',pos=(x,y),style=wx.RB_GROUP)
    parent.setperiodrb.SetFont(parent.textfont)
    x+=int(2.2*xbs)
    parent.periodspin=wx.SpinCtrl(window, -1, value=str(parent.crosstabnday), pos=(x, y), size=(50,20), min=1, max=365)
    parent.periodspin.SetFont(parent.textfont)
    x+=int(1.3*xbs)
    parent.monperiodrb=wx.RadioButton(window,id=-1,label='Month basis',pos=(x,y))
    parent.monperiodrb.SetFont(parent.textfont)
    x+=int(1.3*xbs)
    parent.yearperiodrb=wx.RadioButton(window,id=-1,label='Year basis',pos=(x,y))
    parent.yearperiodrb.SetFont(parent.textfont)
    x+=int(1.3*xbs)
    priorperlab=wx.StaticText(window,-1,"Prior periods:",pos=(x,y+4))
    priorperlab.SetFont(parent.textfont)
    x+=xbs
    parent.priorperiodspin=wx.SpinCtrl(window,value="0", pos=(x,y), size=(0.5*xbs,ybs), min=0,max=1000)
    parent.priorperiodspin.SetFont(parent.textfont)

    if parent.persel=="manual":
       parent.setperiodrb.SetValue(True)
       parent.monperiodrb.SetValue(False)
       parent.yearperiodrb.SetValue(False)
    elif parent.persel=="month":
       parent.setperiodrb.SetValue(False)
       parent.monperiodrb.SetValue(True)
       parent.yearperiodrb.SetValue(False)
    elif parent.persel=="year":
       parent.setperiodrb.SetValue(False)
       parent.monperiodrb.SetValue(False)
       parent.yearperiodrb.SetValue(True)

    y+=ybs+margin1
  
    return y

def blockAnalysisClusterControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):
    x=0; y=y0
    
    x=int(x)
    y=int(y)
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl)     
    
    clustlab=wx.StaticText(window,-1,"Cluster:",pos=(x,y+4))
    clustlab.SetFont(parent.textfont)
    x+=xbs
    parent.clusterspin1=wx.SpinCtrl(window,value="-1", pos=(x,y), size=(xbs,ybs), min=-1,max=-1)
    parent.clusterspin1.SetFont(parent.textfont)

    x=margin1+xl+margin2+margin1
    clust2lab=wx.StaticText(window,-1,"Cluster:",pos=(x,y+4))
    clust2lab.SetFont(parent.textfont)
    x+=xbs
    parent.clusterspin2=wx.SpinCtrl(window,value="-1", pos=(x,y), size=(xbs,ybs), min=-1,max=-1)
    parent.clusterspin2.SetFont(parent.textfont)
 
    x=margin1; y+=ybs
    autofindblocksbutton=wx.Button(window, id=-1, label='Analyze', pos=(x, y), size=(xbs,ybs))
    autofindblocksbutton.SetFont(parent.textfont)
    autofindblocksbutton.Bind(wx.EVT_BUTTON, parent.autofindblocks)
    autofindblocksbutton.SetToolTip(wx.ToolTip("Automatically find significant features."))

    parent.analyzerankingmode='stdev'
    x+=xbs
    vals=['mean','mean/stdev','stdev','stdev/n','mean/n_stdev', 'block size', 'n_mean/stdev']
    parent.analyzerankingmodecombo=wx.ComboBox(window, -1, value=parent.analyzerankingmode, pos=(x, y), size=(xbs,ybs),choices=vals)
    parent.analyzerankingmodecombo.SetToolTip(wx.ToolTip('Determines how detected block clusters are ranked.'))
    parent.analyzerankingmodecombo.Bind(wx.EVT_COMBOBOX, parent.resetanalyzerankingmode)
    parent.analyzerankingmodecombo.SetFont(parent.textfont)
    parent.analyzerankingmodecombo.SetEditable(False)

    x+=xbs
    lab=wx.StaticText(window,-1,"min.blocksize x:",pos=(x,y+4))
    lab.SetFont(parent.textfont)
    x+=xbs
    parent.autofindblocksminbsxspin=wx.SpinCtrl(window,value="2", pos=(x,y), size=(xbs,ybs), min=1,max=100)
    parent.autofindblocksminbsxspin.SetFont(parent.textfont)

    x+=xbs
    lab=wx.StaticText(window,-1,"show # blocks:",pos=(x,y+4))
    lab.SetFont(parent.textfont)
    x+=xbs
    parent.autofindblocksshownumberspin=wx.SpinCtrl(window,value="10", pos=(x,y), size=(xbs,ybs), min=1,max=100)
    parent.autofindblocksshownumberspin.SetFont(parent.textfont)


    y+=ybs+margin1
  
    return y

def blockAnalysisRangeControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):

    x=x0; y=y0
    
    x=int(x)
    y=int(y)
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl) 

    mmlabel=wx.StaticText(window,-1,'Set fixed min/max values:',pos=(x,y))
    mmlabel.SetFont(parent.textfont)
    x+=160; y-=4
    parent.ctwminvala=wx.TextCtrl(window,pos=(x,y),size=(xbs,ybs))
    parent.ctwminvala.SetValue('0.9')
    parent.ctwminvala.SetFont(parent.textfont)
    x+=xbs+margin1
    parent.ctwmaxvala=wx.TextCtrl(window,pos=(x,y),size=(xbs,ybs))
    parent.ctwmaxvala.SetValue('1.1')
    parent.ctwmaxvala.SetFont(parent.textfont)
    x+=xbs+margin1
    parent.ctwminvalb=wx.TextCtrl(window,pos=(x,y),size=(xbs,ybs))
    parent.ctwminvalb.SetValue('-10')
    parent.ctwminvalb.SetFont(parent.textfont)
    x+=xbs+margin1
    parent.ctwmaxvalb=wx.TextCtrl(window,pos=(x,y),size=(xbs,ybs))
    parent.ctwmaxvalb.SetValue('10')
    parent.ctwmaxvalb.SetFont(parent.textfont)
    x+=xbs+margin1
    parent.ctwfixedbounds=wx.CheckBox(window,id=-1,label='Use fixed bounds',pos=(x,y))
    parent.ctwfixedbounds.SetValue(False)
    parent.ctwfixedbounds.SetFont(parent.textfont)

    x+=2*xbs+margin1
    parent.ctwblackwhite=wx.CheckBox(window,id=-1,label='Black/White',pos=(x,y))
    parent.ctwblackwhite.SetValue(False)
    parent.ctwblackwhite.SetFont(parent.textfont)

#    x+=2*xbs+margin1
#    parent.showsteplines=wx.CheckBox(window,id=-1,label='Step lines',pos=(x,y))
#    parent.showsteplines.SetValue(False)
#    parent.showsteplines.SetFont(parent.textfont)


    y+=ybs+margin1
  
    return y
    
   
def determineBlockAnalysisDefaults(parent,iset):
    if iset==1:
       nday=parent.maxxzoom-parent.minxzoom
    else:
       nday=parent.maxxzoom2-parent.minxzoom2
    if nday>366:
       # yearly basis for long series
       persel="year"
       crosstabnday=91 # spincontrol needs a value anyway
    elif nday>131:
       # monthly basis by default
       persel="month"
       crosstabnday=7 # spincontrol needs a value anyway
    elif nday>31:
       # weekly basis 
       persel="manual"
       crosstabnday=7
    else:
       # daily basis
       crosstabnday=1
       persel="manual"

    return persel, crosstabnday

def getPriorStartTimestamp(start,persel,manualperselnday,nprior):
   
   if persel=='manual':
      ostart=start-nprior*manualperselnday   
   elif persel=='month':
      y,m,d=conversion.excelDate2YearMonthDay(start)
      m-=nprior
      if m<1:
         m+=12
         y-=1
      dt=datetime.datetime(y,m,d,0,0,0)
      ostart=conversion.date2exceldate(dt) 
   elif persel=='year':
      y,m,d=conversion.excelDate2YearMonthDay(start)
      y-=1
      dt=datetime.datetime(y,m,d,0,0,0)
      ostart=conversion.date2exceldate(dt) 
   else:
      print('getPriorStartTimestamp error')
      sys.exit(1)

   print('start '+str(start)+' -> '+str(ostart))
   
   return ostart

def getcolor(colorscale,minv,maxv,v):
   if colorscale=='blue-white-red':
      # first limb 0-127: blue-white
      r=int(int(511.0*(float(v) - float(minv))/float(maxv-minv)))
      if (r<0):
         r=0
      if (r>511):
         r=511
      if (r<256):
         sc=r
         col=sc,sc,255
      else:
         sc=255-(r-256)
         col=255,sc,sc
   elif colorscale=='blue-yellow-red':
      # first limb 0-127: blue-yellow
      r=int(int(511.0*(float(v) - float(minv))/float(maxv-minv)))
      r2=int(int(429.0*(float(v) - float(minv))/float(maxv-minv)))
      if (r<0):
         r=0
      if (r>511):
         r=511
      if (r<256):
         sc=r
         col=sc,sc,215
      else:
         sc=255-(r-256)
         sc2=215-(r2-215)
         col=255,sc,sc2
   else:
      print('undefined color scale "'+colorscale+'"')
      sys.exit(1)

   return col

def array2min(dat,use=[]):
    lmin=1e33
    for i in range(len(dat)):
      for j in range(len(dat[0])):
         if len(use)==0 or use[i][j]:
            lmin=min(lmin,dat[i][j])
    return lmin

def array2max(dat,use=[]):
    lmax=-1e33
    for i in range(len(dat)):
      for j in range(len(dat[0])):
         if len(use)==0 or use[i][j]:
            lmax=max(lmax,dat[i][j])
    return lmax

def nowstring():
    dt=datetime.datetime.now()
    return dt.strftime("%d/%m/%Y %H:%M:%S")
      
def computeMontielCurve(indatx, indaty):
    datx=[]; daty=[]
    odatx=[]; odata=[]; odatb=[]
    finished=False
    # put input data (nested lists) in local lists datx and daty
    for i in range(len(indatx)):
       for val in indatx[i]:
          datx.append(val)
       for val in indaty[i]:
          daty.append(val)
    # determine data range and step size
    dv=max(max(datx),max(daty))-min(min(datx),min(daty))
    dx=2e-2*dv 
    while not finished:
       ldatx=[]; ldaty=[]
       for i in range(len(datx)):
          vx=int(datx[i]/dx)*dx # truncated value for x
          vy=int(daty[i]/dx)*dx # truncated value for y
          ldatx.append(vx)  # store in list
          ldaty.append(vy)  # store in list

       if (max(ldatx)-min(ldatx))==0.0 or (max(ldaty)-min(ldaty))==0.0:
          # all values fall in single bin -> it is time to stop
          break
       else:
          # sufficient different values to perform fit
          [fit,residuals, rank, singular_values, rcond]=numpy.polyfit(ldatx,ldaty,1,full=True) # linear fit
          a=fit[0] # slope
          b=fit[1] # intercept
          # put a and b values in output lists
          odatx.append(dx) # for visual.drawcurves
          odata.append(a) # for visual.drawcurves
          odatb.append(b) # for visual.drawcurves
          #odatx.append([dx]) # for visual.drawsimplepointcloud
          #odata.append([a]) # for visual.drawsimplepointcloud
          #odatb.append([b]) # for visual.drawsimplepointcloud
       dx+=2 # next point on curve
          
    return odatx,odata,odatb

def blockAnalysisEMClusterAnalysisControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):
    # controls
    x=x0; y=y0
    
    x=int(x)
    y=int(y)
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl) 

    performEMClusterAnalysisButton=wx.Button(window, id=-1, label='EM Cluster', pos=(x, y), size=(xbs,ybs))
    performEMClusterAnalysisButton.SetFont(parent.textfont)
    performEMClusterAnalysisButton.Bind(wx.EVT_BUTTON, lambda event: blockanalysis.EMClusterAnalysis(parent,event))
    performEMClusterAnalysisButton.SetToolTip(wx.ToolTip("Perform Expectation Maximization cluster analysis."))
    x+=int(1.3*xbs); y+=4
    label=wx.StaticText(window,-1,'number of clusters:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(1.2*xbs); y-=4
    parent.EMnumberofclustersspin=wx.SpinCtrl(window, -1, value=str(3), pos=(x, y), size=(40,ybs), min=1, max=50)
    parent.EMnumberofclustersspin.SetFont(parent.textfont)

    x+=int(1.3*xbs); y+=4
    label=wx.StaticText(window,-1,'numb. random iter.:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(1.2*xbs); y-=4
    parent.EMnumberofrandomiterationsspin=wx.SpinCtrl(window, -1, value=str(10), pos=(x, y), size=(40,ybs), min=1, max=99)
    parent.EMnumberofrandomiterationsspin.SetFont(parent.textfont)

    x+=int(1.3*xbs); y+=4
    label=wx.StaticText(window,-1,'data scale fact:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(1.2*xbs); y-=4
    parent.EMdatascalefactorspin=wx.SpinCtrl(window, -1, value=str(1), pos=(x, y), size=(40,ybs), min=1, max=100)
    parent.EMdatascalefactorspin.SetFont(parent.textfont)

    y+=ybs+margin1
  
    return y

def blockAnalysisStepAnalysisControlSet(parent,window,x0,y0,margin1,margin2,xbs,ybs,yts,xl,yl):
    # controls
    x=x0; y=y0
    
    x=int(x)
    y=int(y)
    xbs=int(xbs)
    ybs=int(ybs)
    margin1=int(margin1)
    margin2=int(margin2)
    xl=int(xl)
    yl=int(yl) 


    label=wx.StaticText(window,-1,'number of clusters:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(1.2*xbs); y-=4
    nstep=max(3,int(float(len(parent.slopedat))/4.0))
    nclust=3
    #nclust=nstep/2+1
    parent.stepanalysisnumberofclustersspin=wx.SpinCtrl(window, -1, value=str(nclust), pos=(x, y), size=(40,ybs), min=1, max=50)
    parent.stepanalysisnumberofclustersspin.SetFont(parent.textfont)

    x+=50; y+=4
    label=wx.StaticText(window,-1,'min width:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=0.7*xbs; y-=4
    parent.stepanalysisminblockwidtspin=wx.SpinCtrl(window, -1, value=str(2), pos=(x, y), size=(40,ybs), min=1, max=500)
    parent.stepanalysisminblockwidtspin.SetFont(parent.textfont)

    x+=50; y+=4
    label=wx.StaticText(window,-1,'opt. method:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(0.9*xbs); y-=4
    vals=['par_BFGS','par_downhill_simplex','par_CG', 'par_Powell']
    parent.stepanalysisoptimizercombo=wx.ComboBox(window, -1, value='par_BFGS', pos=(x, y), size=(1.2*xbs,ybs),choices=vals)
    parent.stepanalysisoptimizercombo.SetToolTip(wx.ToolTip('Select optimization algorithm.'))
    parent.stepanalysisoptimizercombo.SetFont(parent.textfont)

    x+=int(1.3*xbs); y+=4
    label=wx.StaticText(window,-1,'threshold fact.:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=xbs; y-=4
    parent.stepanalysisthreshold=wx.TextCtrl(window,pos=(x,y),size=(0.5*xbs,ybs))
    parent.stepanalysisthreshold.SetValue('0.01')
    parent.stepanalysisthreshold.SetFont(parent.textfont)
    parent.stepanalysisthreshold.SetToolTip(wx.ToolTip('Fraction of total value range acting as threshold for step detection and block function acceptance'))

    x+=int(.55*xbns); y+=4
    label=wx.StaticText(window,-1,'max # steps:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(0.8*xbs); y-=4
    parent.stepanalysismaxnumberofsteps=wx.SpinCtrl(window, -1, value=str(nstep), pos=(x, y), size=(40,ybs), min=1, max=100)
    parent.stepanalysismaxnumberofsteps.SetFont(parent.textfont)

    x+=45; y+=4
    label=wx.StaticText(window,-1,'Lx norm:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(0.7*xbs); y-=4
    parent.bonormexponent=wx.TextCtrl(window,pos=(x,y),size=(0.5*xbs,ybs))
    parent.bonormexponent.SetValue('0.5')
    parent.bonormexponent.SetFont(parent.textfont)

    x+=45; y+=4
    label=wx.StaticText(window,-1,'Penalties:',pos=(x,y))
    label.SetFont(parent.textfont)
    x+=int(0.7*xbs); y-=4
    parent.bonumberpenalty=wx.TextCtrl(window,pos=(x,y),size=(0.5*xbs,ybs))
    parent.bonumberpenalty.SetValue('0.33')
    parent.bonumberpenalty.SetFont(parent.textfont)
    parent.bonumberpenalty.SetToolTip(wx.ToolTip('Penalty factor for number of block functions used.'))
    x+=int(0.52*xbs)
    parent.booverlappenalty=wx.TextCtrl(window,pos=(x,y),size=(0.5*xbs,ybs))
    parent.booverlappenalty.SetValue('0.33')
    parent.booverlappenalty.SetFont(parent.textfont)
    parent.booverlappenalty.SetToolTip(wx.ToolTip('Penalty factor for the amount of overlap between block functions.'))




    y+=ybs+margin1
  
    return y

def getdistinctcolor(icol,ncol):
    basecolors=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
    basecol=basecolors[icol%len(basecolors)]
    return basecol

def checkvalues(ar):
    lpass=True
    for item in ar:
       if str(item)=='nan':
          lpass=False
          break
       elif str(item)=='inf':
          lpass=False
          break
       elif str(item)=='-inf':
          lpass=False
          break
       #else:
          #print 'check '+str(item)
    #print 'check '+str(item)+ ' pass '+str(lpass)
    return lpass
