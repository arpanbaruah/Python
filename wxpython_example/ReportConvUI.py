#!/usr/bin/env python

import wx
import os
import time
import shutil
from  main import reportMain

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Github Version")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
    
class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, 
                 style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                                wx.RESIZE_BOX | 
                                                wx.MAXIMIZE_BOX),
                 name="MyFrame",
                 size = ( 700,250)):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)
        # Attributes
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.RED)
        
        sb1 = wx.StaticBox(self.panel, size = (550,65), pos = (110,15))
        boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)
        sb2 = wx.StaticBox(self.panel, size = (550,65), pos = (110,75))
        boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        
        src_button = wx.Button(self.panel, label = "Source Folder", pos = (500,35), size = (150,35))
        src_button.Bind(wx.EVT_BUTTON, self.sourceOnDir)
        src_button.SetBackgroundColour(wx.WHITE)
        
        des_button = wx.Button(self.panel, label = "Destination Folder", pos = (500,95), size = (150,35))
        des_button.Bind(wx.EVT_BUTTON, self.destOnDir)
        des_button.SetBackgroundColour(wx.WHITE)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.sourceCtrl = wx.TextCtrl(self.panel, -1, "", pos=(130, 37), size = (350,30),style = wx.TE_READONLY)
        self.destCtrl = wx.TextCtrl(self.panel, -1, "", pos=(130, 97), size = (350,30),style = wx.TE_READONLY)
        
        # Add a logo in this location or whereever you want the logo
        path = os.path.abspath(".\\img\\icon\\logo.png")
        icon = wx.Icon(path,wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
        
        
        ok_button = wx.Button(self.panel, label = "Execute", pos = (310,160) , size = (100,25))
        ok_button.Bind(wx.EVT_BUTTON, self.onExecute)
        
        Cancel_button = wx.Button(self.panel, label = "Cancel", pos = (430,160) , size = (100,25))
        Cancel_button.Bind(wx.EVT_BUTTON, self.onClose)
        Help_button = wx.Button(self.panel, label = "Help", pos = (550,160) , size = (100,25))
        Help_button.Bind(wx.EVT_BUTTON, self.onHelp)

   
        #----------------------------------------------------------------------
    def sourceOnDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        srcdlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if srcdlg.ShowModal() == wx.ID_OK:
            self.srcpath = srcdlg.GetPath()
            self.sourceCtrl.SetValue("%s" % (self.srcpath))
        srcdlg.Destroy()
        
        
    def destOnDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        desdlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if desdlg.ShowModal() == wx.ID_OK:
            self.destpath = desdlg.GetPath()
            self.destCtrl.SetValue("%s" % (self.destpath))
        desdlg.Destroy()
    
    
    def onHelp(self, event):
        
        filename = 'README.txt'
        os.system("start "+filename)
    
    def onExecute(self, event):
        
        try:
            if  not self.srcpath == ''  or not  self.destpath == '' :
                #files = [f for f in os.listdir(self.srcpath) if f.endswith('.xml')]   
                bopath = os.path.join(self.destpath, 'boreport')
                if not os.path.exists(bopath):
                    os.mkdir(bopath)
                    os.chmod(bopath, 0o777)
    
                obieepath = os.path.join(self.destpath, 'obieereport')
                if not os.path.exists(obieepath):
                    os.mkdir(obieepath)
                    os.chmod(obieepath, 0o777)
            
                files = [f for f in os.listdir(self.srcpath) if f.endswith('.xml')]
                for filename in files:
                    shutil.copy(os.path.join(self.srcpath,filename), os.path.join(bopath,filename))
        
        
                msg = "Please wait while we process your request..."
                busyDlg = wx.BusyInfo(msg) 
                #test = reportMain(self.destpath+'\\')
                #status = test.main()
                time.sleep(2)
                if status == 1:
                    busyDlg = None
                    dlg = wx.MessageDialog(self,"Conversion is complete","Confirm Exit", wx.OK)
                    result = dlg.ShowModal()
                    dlg.Destroy()
                    if result == wx.ID_OK:
                        self.sourceCtrl.SetValue("")
                        self.destCtrl.SetValue("")
                        foldername = os.path.join(self.destpath,'obieereport')
                        os.startfile(foldername)
        
        except:

            dlg = wx.MessageDialog(self,"Either source or destination folder is empty","Confirm Exit", wx.ICON_ERROR)
            result = dlg.ShowModal()
            dlg.Destroy()
            
     
    def onClose(self, event):
        dlg = wx.MessageDialog(self,"Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()   
        
if_name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
