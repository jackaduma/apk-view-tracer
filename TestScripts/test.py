#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## test.py

import telnetlib
from ViewManagement.ParseView import ParseView
from InitDevice import init_service
from GetConfigInfo import GetViewServerInfo


def GetMoreInfos():
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
    view_parser.parseViewListData(CurView_Data)
    print "Current Windows List:"
    print ViewList_Data
    view_parser.parseViewListData(ViewList_Data)
    
    return CurView_Data, ViewList_Data

#===========================================================================
# # these two files are same, (sha1 are same)
# # so "dump -1" means "dump %s" %focused_view_hashcode
#===========================================================================
def testDumpFile():
    config = GetViewServerInfo()
    host = config.getServerHost()
    port = config.getServerPort()
    time_out = config.getServerTimeOut()
    
    tn = telnetlib.Telnet(host, port, time_out)
    tn.write("DUMP -1\n")
    default_dump_data = tn.read_until("DONE")
    tn.close()
    f=open("default_dump_data", "w")
    f.write(default_dump_data)
    f.close()
    
    t = GetMoreInfos()[0]
    parser = ParseView()
    ViewHashCode = parser.parseViewListData(t)[0][0]  ## focused view hash code
    tn = telnetlib.Telnet(host, port, time_out)
    tn.write("DUMP %s\n" %ViewHashCode)
    assign_dump_data = tn.read_until("DONE")
    tn.close()
    f=open("assign_dump_data", "w")
    f.write(assign_dump_data)
    f.close()
    

