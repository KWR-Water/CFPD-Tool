# from http://www.blog.pythonlibrary.org/2010/04/16/how-to-take-a-screenshot-of-your-wxpython-app-and-print-it/
# mod PvT 20010803

import wx
import sys


def onTakeScreenShot(self,event,window,xsize,ysize,fname):
        """ Takes a screenshot of the screen at give pos & size (rect). """
        #print 'Taking screenshot...'

        window.Raise()
        window.SetFocus()

        rect = window.GetRect()
        # see http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3575899
        # created by Andrea Gavana
 
        # adjust widths for Linux (figured out by John Torres 
        # http://article.gmane.org/gmane.comp.python.wxpython/67327)
        #if sys.platform == 'linux2':
            #client_x, client_y = window.ClientToScreen((0, 0))
            #border_width = client_x - rect.x
            #title_bar_height = client_y - rect.y
            #rect.width += (border_width * 2)
            #rect.height += title_bar_height + border_width

        # do not save window borders
        if sys.platform == 'linux2':
            client_x, client_y = window.ClientToScreen((0, 0))
            rect.x=client_x
            rect.y=client_y
            rect.width=xsize
            rect.height=ysize
 
        #Create a DC for the whole screen area
        dcScreen = wx.ScreenDC()
 
        #Create a Bitmap that will hold the screenshot image later on
        #Note that the Bitmap must have a size big enough to hold the screenshot
        #-1 means using the current default colour depth
        bmp = wx.EmptyBitmap(rect.width, rect.height)
 
        #Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()
 
        #Tell the memory DC to use our Bitmap
        #all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)
 
        #Blit (in this case copy) the actual screen on the memory DC
        #and thus the Bitmap
        memDC.Blit( 0, #Copy to this X coordinate
                    0, #Copy to this Y coordinate
                    rect.width, #Copy this width
                    rect.height, #Copy this height
                    dcScreen, #From where do we copy?
                    rect.x, #What's the X offset in the original DC?
                    rect.y  #What's the Y offset in the original DC?
                    )
 
        #Select the Bitmap out of the memory DC by selecting a new
        #uninitialized Bitmap
        memDC.SelectObject(wx.NullBitmap)

        if fname=='':
           dlg = wx.FileDialog(window,message='Save screenshot', defaultDir=self.cwd, wildcard='*.png', style=wx.FD_SAVE)
           if dlg.ShowModal() == wx.ID_OK:
              fname=dlg.GetPath()
              self.cwd=dlg.GetDirectory()
           dlg.Destroy()
 
        img = bmp.ConvertToImage()
        img.SaveFile(fname, wx.BITMAP_TYPE_PNG)
        print('saving '+fname)

def savebitmap(img,fname):
        img.SaveFile(fname, wx.BITMAP_TYPE_PNG)

def savebitmapdlg(parent,img):
        dlg = wx.FileDialog(parent,message='Save image', wildcard='*.png', style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
           fname=dlg.GetPath()
        dlg.Destroy()
        if not fname=='':
           img.SaveFile(fname, wx.BITMAP_TYPE_PNG)
