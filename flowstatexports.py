import xlrd
import xlwt
import datetime
import math
import conversion
#import docx

def exportABSToXls(parent,mata,matb,matsa,matsb,tstart,persel,dt,nperiod,datfilename,fname,analysislabel):
   wb = xlwt.Workbook()
   wsa = wb.add_sheet('Slope a')
   wssa = wb.add_sheet('StDev slope a')
   wsb = wb.add_sheet('Intercept b')
   wssb = wb.add_sheet('StDev intercept b')

   #print'mata='+str(mata)
   #print'matsa='+str(matsa)
   #print'matb='+str(matb)
   #print'matsb='+str(matsb)
   print('period selection='+str(persel))
   print('dt,nperiod='+str([dt,nperiod]))
   print('tstart='+str(tstart))
   print('datfilename='+datfilename)
   print('fname='+fname)

   font0 = xlwt.Font()
   font0.name = 'Arial'
   font0.colour_index = 0
   font0.bold = True

   font1 = xlwt.Font()
   font1.name = 'Arial'
   font1.colour_index = 0
   font1.bold = False

   style0 = xlwt.XFStyle()
   style0.font = font0

   style1 = xlwt.XFStyle()
   style1.font = font1

   style2 = xlwt.XFStyle()
   style2.font = font1
   style2.num_format_str = 'DD-MM-YYYY'
   #style2.num_format_str = 'DD-MM-YYYY h:mm:ss'

   now=str(datetime.datetime.now())

   wsa.write(0, 0, analysislabel+' - Slopes a', style0)
   wsa.write(1, 0, 'time of analysis'+now, style1)
   wsa.write(2, 0, 'data source:'+datfilename, style1)
   wssa.write(0, 0, 'Standard deviations of slopes a', style0)
   wssa.write(1, 0, 'time of analysis'+now, style1)
   wssa.write(2, 0, 'data source:'+datfilename, style1)
   wsb.write(0, 0, 'Intercepts b', style0)
   wsb.write(1, 0, 'time of analysis'+now, style1)
   wsb.write(2, 0, 'data source:'+datfilename, style1)
   wssb.write(0, 0, 'Standard deviations of intercepts b', style0)
   wssb.write(1, 0, 'time of analysis'+now, style1)
   wssb.write(2, 0, 'data source:'+datfilename, style1)

   dattimelabelsstart=[]
   dattimelabelsend=[]
   minyear,minmonth=conversion.timstr2yearmonth(conversion.exceldate2string(tstart))
   for i in range(nperiod):
      [t,te]=parent.selectperiod(persel, i, tstart,dt,minyear,minmonth)
      dattimelabelsstart.append(t)   
      dattimelabelsend.append(te)

   wsa.write(6, 0, 'start', style1)
   wsa.write(6, 1, 'end', style1)
   wssa.write(6, 0, 'start', style1)
   wssa.write(6, 1, 'end', style1)
   wsb.write(6, 0, 'start', style1)
   wsb.write(6, 1, 'end', style1)
   wssb.write(6, 0, 'start', style1)
   wssb.write(6, 1, 'end', style1)
   for irow in range(nperiod):
      wsa.write(7+irow, 0, dattimelabelsstart[irow], style2)
      wsa.write(7+irow, 1, dattimelabelsend[irow], style2)
      wssa.write(7+irow, 0, dattimelabelsstart[irow], style2)
      wssa.write(7+irow, 1, dattimelabelsend[irow], style2)
      wsb.write(7+irow, 0, dattimelabelsstart[irow], style2)
      wsb.write(7+irow, 1, dattimelabelsend[irow], style2)
      wssb.write(7+irow, 0, dattimelabelsstart[irow], style2)
      wssb.write(7+irow, 1, dattimelabelsend[irow], style2)
 
   wsa.write(4, 2, 'start', style1)
   wsa.write(5, 2, 'end', style1)
   wssa.write(4, 2, 'start', style1)
   wssa.write(5, 2, 'end', style1)
   wsb.write(4, 2, 'start', style1)
   wsb.write(5, 2, 'end', style1)
   wssb.write(4, 2, 'start', style1)
   wssb.write(5, 2, 'end', style1)
   for icol in range(nperiod):
      wsa.write(4,3+icol, dattimelabelsstart[icol], style2)
      wsa.write(5,3+icol, dattimelabelsend[icol], style2)
      wssa.write(4,3+icol, dattimelabelsstart[icol], style2)
      wssa.write(5,3+icol, dattimelabelsend[icol], style2)
      wsb.write(4,3+icol, dattimelabelsstart[icol], style2)
      wsb.write(5,3+icol, dattimelabelsend[icol], style2)
      wssb.write(4,3+icol, dattimelabelsstart[icol], style2)
      wssb.write(5,3+icol, dattimelabelsend[icol], style2)
       
   for irow in range(nperiod):
      for icol in range(irow,nperiod):
         wsa.write(7+irow, 3+icol, mata[irow][icol] , style1)
         wssa.write(7+irow, 3+icol, matsa[irow][icol], style1)
         wsb.write(7+irow, 3+icol, matb[irow][icol], style1)
         wssb.write(7+irow, 3+icol, matsb[irow][icol], style1)

   try:
      wb.save(fname)
      success=True
   except:
      success=False

   return success

def exportMinMaxTableToXls(minmaxarray,datfilename,fname):
   wb = xlwt.Workbook()
   wsa = wb.add_sheet('Value ranges per period')

   print('datfilename='+datfilename)
   print('fname='+fname)

   font0 = xlwt.Font()
   font0.name = 'Arial'
   font0.colour_index = 0
   font0.bold = True

   font1 = xlwt.Font()
   font1.name = 'Arial'
   font1.colour_index = 0
   font1.bold = False

   style0 = xlwt.XFStyle()
   style0.font = font0

   style1 = xlwt.XFStyle()
   style1.font = font1

   style2 = xlwt.XFStyle()
   style2.font = font1
   style2.num_format_str = 'DD-MM-YYYY'
   #style2.num_format_str = 'DD-MM-YYYY h:mm:ss'

   now=str(datetime.datetime.now())

   wsa.write(0, 0, 'Value ranges of parameters a and b and their standard deviations per analysis period', style0)
   wsa.write(1, 0, 'time of analysis'+now, style1)
   wsa.write(2, 0, 'data source:'+datfilename, style1)

   wsa.write(4, 0, 'period', style1)
   wsa.write(4, 1, 'a', style1)
   wsa.write(4, 3, 'b', style1)
   wsa.write(4, 5, 'stdev a', style1)
   wsa.write(4, 6, 'stdev b', style1)
   wsa.write(5, 1, 'min', style1)
   wsa.write(5, 2, 'max', style1)
   wsa.write(5, 3, 'min', style1)
   wsa.write(5, 4, 'max', style1)
   wsa.write(5, 5, 'max', style1)
   wsa.write(5, 6, 'max', style1)
   for irow in range(len(minmaxarray)):
      wsa.write(6+irow, 0, irow+1, style1)
      for jcol in range(6):
         wsa.write(6+irow, jcol+1, minmaxarray[irow][jcol], style1)
 

   try:
      wb.save(fname)
      success=True
   except:
      success=False

   return success

#def createDocxWithBlockTables(parent,fname,images,npertab):
#
   #fname=fname.replace('.docx','').replace('.DOCX','')+'.docx'
#
   #nimage=len(images)
   #ntab=int(math.ceil(float(nimage)/float(npertab)))
#
   ## Default set of relationshipships - these are the minimum components of a document
   #relationships = docx.relationshiplist()
#
   ## Make a new document tree - this is the main part of a Word document
   #document = docx.newdocument()
#
   ## This xpath location is where most interesting content lives 
   #docbody = document.xpath('/w:document/w:body', namespaces=docx.nsprefixes)[0]
#
   #labels=['a) ','b) ','c) ','d) ','e) ','f) ','g) ']
   #for itab in range(ntab):
     #
      #table=[['','','','']] # first row should not contain pictures
#
      #for irow in range(npertab):
          #iset=itab*npertab+irow
          #try:
             #limages=images[iset]
          #except IndexError:
             ## no more images -> end
             #break
          #print 'limages='+str(limages)
          #relationships,picpara1 = docx.picture(relationships,limages[4],'a,b-diagram',iset*4+1,pixelwidth=28)
          #relationships,picpara2 = docx.picture(relationships,limages[1],'a,b-diagram',iset*4+2,pixelwidth=28)
          #relationships,picpara3 = docx.picture(relationships,limages[2],'a,b-diagram',iset*4+3,pixelwidth=28)
          #relationships,picpara4 = docx.picture(relationships,limages[3],'a,b-diagram',iset*4+4,pixelwidth=28)
          #table.append([labels[irow]+limages[0],'','',''])
          #table.append([picpara1,picpara2,picpara3,picpara4])
#
      ## Append a table
      #docbody.append(docx.table(table))
#
   ## Create our properties, contenttypes, and other support files
   #coreprops = docx.coreproperties(title='Flowstat CFPD block analysis output',subject='',creator=parent.appname,keywords=['CFPD'])
   #appprops = docx.appproperties()
   #contenttypes = docx.contenttypes()
   #websettings = docx.websettings()
   #wordrelationships = docx.wordrelationships(relationships)
#
   ## Save our document
   #docx.savedocx(document,coreprops,appprops,contenttypes,websettings,wordrelationships,fname)
#
def createHtmlWithBlockTables(parent,fname,images,npertab,analysislabel):

   fname=fname.replace('.html','').replace('.HTML','')+'.html'

   nimage=len(images)
   ntab=int(math.ceil(float(nimage)/float(npertab)))

   f=open(fname,'w')

   labels=['a) ','b) ','c) ','d) ','e) ','f) ','g) ']
   for itab in range(ntab):
     
      perstart=images[itab*npertab]["periodlabel"]
      try:
         perend=images[itab*npertab+npertab-1]["periodlabel"] # last set of table
      except:
         perend=images[-1]["periodlabel"] # table is not full length -> take last available
      f.write('VLPV-blokanalyseresultaten voor '+analysislabel+' voor de periode '+perstart+' t/m '+perend+'. Van links naar rechts zijn weergegeven a,b-diagrammen, hellingen, intercepts en standaarddeviaties. Tussen haakjes is de determinatieco&euml;ffici&euml;nt van het a,b-diagram voor een lineaire fit weergegeven.\n') 
      f.write('<table style="border:1px solid black;border-collapse:collapse;">\n')

      npix=142 #132
     
      for irow in range(npertab):

          iset=itab*npertab+irow
          try:
             limages=images[iset]
          except IndexError:
             # no more images -> end
             break
          if len(limages)<6:
             # something is wrong
             print('error: limages='+str(limages))
             print('aborting table creation')
             break
          f.write('<tr>\n') 
          R2form="%1.3f" % limages["abcurveR2"]
          f.write('<td style="border:1px solid black;" >'+labels[irow]+limages["periodlabel"]+' (R<sup>2</sup>='+R2form+')</td>\n')
          f.write('</tr>\n') 
          f.write('\n') 
          f.write('<tr>\n') 
          f.write('<td style="border:1px solid black;" >\n')
          f.write('<br />\n') 
          f.write('&nbsp;\n') 
          abfile=limages["abfile"].replace('\\','/').split('/')[-1] # remove path
          slopefile=limages["slopefile"].replace('\\','/').split('/')[-1] # remove path
          interceptfile=limages["interceptfile"].replace('\\','/').split('/')[-1] # remove path
          varfile=limages["stdevfile"].replace('\\','/').split('/')[-1] # remove path
          f.write('<img src="'+abfile+'" width='+str(npix)+' > &nbsp;\n') 
          f.write('<img src="'+slopefile+'" width='+str(npix)+' > &nbsp;\n') 
          f.write('<img src="'+interceptfile+'" width='+str(npix)+' > &nbsp;\n') 
          f.write('<img src="'+varfile+'" width='+str(npix)+' > &nbsp;\n') 
          f.write('&nbsp;\n') 
          f.write('<br />\n') 
          f.write('</tr>\n') 
          f.write('\n') 
      f.write('</table>\n') 
      f.write('<br />\n') 
      f.write('<br />\n') 
      f.write('\n') 

   f.close()

def createHtmlWithMarkedBlockTables(parent,fname,images,ncolumn,analysislabel):

   fname=fname.replace('.html','').replace('.HTML','')+'.html'

   ntab=len(images)

   f=open(fname,'w')

   labels=['a) ','b) ','c) ','d) ','e) ','f) ','g) ']
   for itab in range(ntab):
      limages=images[itab]
     
      perlabel=images[itab]["periodlabel"]
      f.write('VLPV-blokanalyseresultaten voor '+analysislabel+' - '+perlabel+ ': meest significante afwijkingen in hellingen\n')
      f.write('<br />\n') 
      f.write('<br />\n') 
      f.write('<table style="border:1px solid black;border-collapse:collapse;">\n')

      npix=800/ncolumn
      #npix=458/ncolumn
     
      f.write('<tr>\n') 
      f.write('<td style="border:1px solid black;" colspan = "'+str(ncolumn)+'" >Hellingen </td>\n')
      f.write('</tr>\n') 
      f.write('\n') 
      f.write('<tr>\n') 

      nblocka=limages["slopefile_blocks"]['n']
      for iblocka in range(nblocka):
         ifile=limages["slopefile_blocks"]['imagefile'+str(iblocka)]
         amplitude=limages["slopefile_blocks"]['amplitudes'+str(iblocka)]
         pfa=limages["slopefile_blocks"]['pfa'+str(iblocka)]
         startdate=limages["slopefile_blocks"]['blockstart'+str(iblocka)]
         enddate=limages["slopefile_blocks"]['blockend'+str(iblocka)]
         f.write('<td style="border:1px solid black;" >\n')
         f.write('amplitude=%6.3f\n' % amplitude ) 
         f.write('<br />\n') 
         f.write(conversion.exceldate2stringd(startdate)+' - '+conversion.exceldate2stringd(enddate)+'\n')
         f.write('<br />\n') 
         f.write('<img src="'+ifile+'" width='+str(npix)+' > &nbsp;\n') 
         f.write('&nbsp;\n') 
         f.write('</td>\n') 

         if (iblocka+1)%ncolumn==0:
            # new line
            f.write('</tr>\n') 
            f.write('<tr>\n') 

      f.write('<br />\n') 
      f.write('</tr>\n') 
      f.write('\n') 

      f.write('</table>\n') 
      f.write('<br />\n') 
      f.write('<br />\n') 
      f.write('\n') 

   for itab in range(ntab):
      limages=images[itab]
     
      perlabel=images[itab]["periodlabel"]
      f.write('VLPV-blokanalyseresultaten voor '+analysislabel+' - '+perlabel+ ': meest significante afwijkingen in y-asafsnedes\n')
      f.write('<br />\n') 
      f.write('<br />\n') 
      f.write('<table style="border:1px solid black;border-collapse:collapse;">\n')

      npix=800/ncolumn
      #npix=142 #132
     
      f.write('<tr>\n') 
      f.write('<td style="border:1px solid black;" colspan = "'+str(ncolumn)+'" >Intercepts </td>\n')
      f.write('</tr>\n') 
      f.write('\n') 
      f.write('<tr>\n') 

      nblockb=limages["interceptfile_blocks"]['n']
      for iblockb in range(nblockb):
         ifile=limages["interceptfile_blocks"]['imagefile'+str(iblockb)]
         amplitude=limages["interceptfile_blocks"]['amplitudes'+str(iblockb)]
         pfa=limages["interceptfile_blocks"]['pfa'+str(iblockb)]
         startdate=limages["interceptfile_blocks"]['blockstart'+str(iblockb)]
         enddate=limages["interceptfile_blocks"]['blockend'+str(iblockb)]
         f.write('<td style="border:1px solid black;" >\n')
         f.write('amplitude=%6.3f\n' % amplitude ) 
         f.write('<br />\n') 
         f.write(conversion.exceldate2stringd(startdate)+' - '+conversion.exceldate2stringd(enddate)+'\n')
         f.write('<br />\n') 
         f.write('<img src="'+ifile+'" width='+str(npix)+' > &nbsp;\n') 
         f.write('&nbsp;\n') 
         f.write('</td>\n') 

         if (iblockb+1)%ncolumn==0:
            # new line
            f.write('</tr>\n') 
            f.write('<tr>\n') 

      f.write('<br />\n') 
      f.write('</tr>\n') 
      f.write('\n') 

      f.write('</table>\n') 
      f.write('<br />\n') 
      f.write('<br />\n') 
      f.write('\n') 

   f.close()


   f.close()

