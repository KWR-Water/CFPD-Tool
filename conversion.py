import datetime

def minimalist_xldate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    dt=(
        #datetime.datetime(1899, 12, 30)
        datetime.datetime(1899, 12, 31)
        + datetime.timedelta(days=xldate-1 + 1462 * datemode)
        )
    #print 'minimalist_xldate_as_datetime: '+str(xldate)+' ->  '+dt.isoformat()
    return dt

##
# Convert an Excel number (presumed to represent a date, a datetime or a time) into
# a Python datetime.datetime
# @param xldate The Excel number
# @param datemode 0: 1900-based, 1: 1904-based.
# <br>WARNING: when using this function to
# interpret the contents of a workbook, you should pass in the Book.datemode
# attribute of that workbook. Whether
# the workbook has ever been anywhere near a Macintosh is irrelevant.
# @return a datetime.datetime object, to the nearest_second.
# <br>Special case: if 0.0 <= xldate < 1.0, it is assumed to represent a time;
# a datetime.time object will be returned.
# <br>Note: 1904-01-01 is not regarded as a valid date in the datemode 1 system; its "serial number"
# is zero.
# @throws XLDateNegative xldate < 0.00
# @throws XLDateAmbiguous The 1900 leap-year problem (datemode == 0 and 1.0 <= xldate < 61.0)
# @throws XLDateTooLarge Gregorian year 10000 or later
# @throws XLDateBadDatemode datemode arg is neither 0 nor 1
# @throws XLDateError Covers the 4 specific errors

def xldate_as_datetime(xldate, datemode):
    if datemode not in (0, 1):
        raise XLDateBadDatemode(datemode)
    if xldate == 0.00:
        return datetime.time(0, 0, 0)
    if xldate < 0.00:
        raise XLDateNegative(xldate)
    xldays = int(xldate)
    frac = xldate - xldays
    seconds = int(round(frac * 86400.0))
    assert 0 <= seconds <= 86400
    if seconds == 86400:
        seconds = 0
        xldays += 1
    #if xldays >= _XLDAYS_TOO_LARGE[datemode]:
        #raise XLDateTooLarge(xldate)

    if xldays == 0:
        # second = seconds % 60; minutes = seconds // 60
        minutes, second = divmod(seconds, 60)
        # minute = minutes % 60; hour    = minutes // 60
        hour, minute = divmod(minutes, 60)
        return datetime.time(hour, minute, second)

    #if xldays < 61 and datemode == 0:
        #raise XLDateAmbiguous(xldate)

    return (
        datetime.datetime.fromordinal(xldays + 693594 + 1462 * datemode)
        + datetime.timedelta(seconds=seconds)
        )

def date2exceldate(date):

    d1=datetime.datetime(1900,1,1)
    d=(date-d1).days+1
    s=(date-d1).seconds
    return float(d)+1.0+float(s)/86400.0

def exceldate2string(date):
       #print 'date='+str(date)
    #try:
       dt=xldate_as_datetime(date,0)
       tim=dt.strftime("%d/%m/%Y %H:%M:%S")
       #print 'exceldate2string "'+str(date)+'" = '+tim
    #except:
       #raise Exception
       return tim

def exceldate2stringd(date):
    dt=xldate_as_datetime(date,0)
    tim=dt.strftime("%d-%m-%Y")
    return tim

def string2exceldate(str):
    dat=str.split(' ')[0]
    tim=str.split(' ')[1]
    y=int(dat.split('/')[2])
    mo=int(dat.split('/')[1])
    d=int(dat.split('/')[0])
    h=int(tim.split(':')[0])
    mi=int(tim.split(':')[1])
    try:
       s=int(tim.split(':')[2])
    except:
       s=0
    dt=datetime.datetime(y,mo,d,h,mi,s)
    ed=date2exceldate(dt)
    return ed

def string2exceldated(dat):
    y=int(dat.split('/')[2])
    mo=int(dat.split('/')[1])
    d=int(dat.split('/')[0])
    h=0
    mi=0
    s=0
    dt=datetime.datetime(y,mo,d,h,mi,s)
    ed=date2exceldate(dt)
    return ed

def excelDate2YearMonthDay(ed):
    dt=xldate_as_datetime(ed,0)
    y=int(dt.strftime("%Y"))
    m=int(dt.strftime("%m"))
    d=int(dt.strftime("%d"))
    return y,m,d

def timstr2num(tim):
    #try:
       h=int(tim.split(':')[0])
       mi=int(tim.split(':')[1])
       s=int(tim.split(':')[2])
    #except:
       #raise Exception
   
       return float(h)/24.0+float(mi)/1440.0+float(s)/86400.0

def timstr2yearmonth(dattim):
    #print 'timstr2yearmonth: dattim='+dattim
    m=int(dattim.split(" ")[0].split("/")[1])
    y=int(dattim.split(" ")[0].split("/")[2])
    #print 'y.m='+str([y,m])
    return y,m

def getrefdat():
   refday=datetime.datetime(2011,5,2) # May 2, 2011 is a Monday
   #refday=datetime.datetime(2011,5,1) # May 2, 2011 is a Monday
   irefday=date2exceldate(refday)
   return irefday

def xldateweekday(iday):
   dt=xldate_as_datetime(iday,0) 
   #print 'iday,dt='+str([iday,dt])
   return datetime.date.weekday(dt)

def cleanupstring(lstr):
   allowedchars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','-','_','.',',',';',':','"','/','\\',' ']
   ostr=''
   for letter in lstr: 
      try:
         test=allowedchars.index(letter)
         ostr+=letter
      except:
         ostr+='*'
   return ostr 
