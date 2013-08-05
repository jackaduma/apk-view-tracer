#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## ParseView.py

from InitDevice import init_service
from GetConfigInfo import GetViewServerInfo
from ParseElement import ParseElement
import telnetlib

class ParseView():
    
    def __init__(self):
        self.element_parser = ParseElement()
    
    #406c1d58 com.android.internal.service.wallpaper.ImageWallpaper
    #4054bf40 com.android.launcher/com.android.launcher2.Launcher
    #4073dcd8 com.example.android.apis/com.example.android.apis.ApiDemos
    #406a7510 TrackingView
    #405ec120 StatusBarExpanded
    #40632908 StatusBar
    #4067b9e8 Keyguard
    #DONE
    def isSystemView(self, view_detail):
        if "com.android.internal.service.wallpaper.ImageWallpaper" == view_detail:
            return True
        elif "com.android.launcher/com.android.launcher2.Launcher" == view_detail:
            return True
        elif "TrackingView" == view_detail:
            return True
        elif "StatusBarExpanded" ==  view_detail:
            return True
        elif "StatusBar" == view_detail:
            return True
        elif "Keyguard" == view_detail:
            return True
        else:
            return False
    
    def getViewListData(self, view_list_data):
        viewListHashCode_List = []
        viewListHashCode_Dict = {}
        lines_list = view_list_data.split("\n")
        if '' in lines_list:
            lines_list.remove('')
        if 'DONE' in lines_list:
            lines_list.remove('DONE')
        for line in lines_list:
            temp = line.split(" ")
            hashcode = temp[0]
            detail_info = temp[1]
            # clear the views of android system default services or applications
            # ImageWallpaper,Launcher,TrackingView,StatusBarExpanded,StatusBar,Keyguard
            if not self.isSystemView(detail_info):
                viewListHashCode_List.append(hashcode)
                viewListHashCode_Dict[hashcode] = detail_info

        return viewListHashCode_List, viewListHashCode_Dict
    
    
    # parse view data by dump, then get the view text list
    def getViewTextList(self, view_dump_data):
        view_text_list = []
        element_list = self.element_parser.getStructure(view_dump_data)[0]
        for element in element_list:
            text = self.element_parser.getText(element)
            view_text_list.append(text)       
        
        return view_text_list
    
    def isEqualTextList(self, view_dump_data1, view_dump_data2):
        text_list1 = self.getViewTextList(view_dump_data1)     
        text_list2 = self.getViewTextList(view_dump_data2) 
        
        return (text_list1 == text_list2)       

def DiffCheck_Views():
    # List View and get Current Focus
    if False == init_service():
        print "failed to init service!"
        return False
        #return None
    config = GetViewServerInfo()
    host = config.getServerHost()
    port = config.getServerPort()
    time_out = config.getServerTimeOut()
    tn = telnetlib.Telnet(host, port, time_out)
    tn.write("GET_FOCUS\n")
    CurView_Data = tn.read_until("DONE")
    tn.close()
    tn = telnetlib.Telnet(host, port, time_out)
    tn.write("LIST\n")
    ViewList_Data = tn.read_until("DONE")
    tn.close()
    print "Current Focused Window:"    
    view_parser = ParseView()
    print CurView_Data
    view_parser.getViewListData(CurView_Data)
    print "Current Windows List:"
    print ViewList_Data
    view_parser.getViewListData(ViewList_Data)
    
    return CurView_Data, ViewList_Data

if __name__=="__main__":
    DiffCheck_Views()
    
