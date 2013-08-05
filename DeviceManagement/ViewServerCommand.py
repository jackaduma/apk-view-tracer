#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## ViewServerCommand.py

import socket
import os
import telnetlib

class ViewServerCommand():
    '''
    View Server Command
    '''
    
    list_view_cmd = "LIST"
    dump_view_cmd = "DUMP"
    server_cmd = "SERVER"
    protocol_cmd = "PROTOCOL"
    get_focus_cmd = "GET_FOCUS"
    autolist_cmd = "AUTOLIST"
    
    # ViewDebug Command
    capture_cmd = "CAPTURE"
    invalidate_cmd = "INVALIDATE"
    profile_cmd = "PROFILE"
    
    def __init__(self, logger, device_ip, view_server_port, device_name, monkey_server_port):
        self.class_name = "ViewServerCommand"
        self.m_logger = logger
        
        self.device_ip = device_ip
        self.view_server_port = view_server_port
        self.device_name = device_name
        self.monkey_server_port = monkey_server_port
        
    
    #===============================================================================
    # # method 1 : send command by socket
    # # can not find the end flag  ******
    #===============================================================================
    def getInfosBySocket(self, command="DUMP -1"):   
        host = self.device_ip
        port = self.view_server_port
        ## connect the service with a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        try:
            s.connect((host,port))
        except Exception,e:
            msg = "[%s] Failed to get infos from View Server by socket [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)   
    
        s.send(command+'\n')
        self.m_logger.info("sucess to send command: [%s] " %command)
        buf_size = 65565
        data=""
        end_flag = "DONE"
        while True:
            res = s.recv(buf_size)
            data+=res
            if  0 <= res.find(end_flag, -5):
                self.m_logger.info("read the end flag: 'DONE' ")
                break            
    
        s.close()
        return data


    #===============================================================================
    # # method 2 : send command by telnet
    #===============================================================================
    def getInfosByTelnet(self, command="DUMP -1"):
        host = self.device_ip
        port = self.view_server_port
        time_out = 30

        retry_time = 5;
        tn = None
        data = None
        while retry_time>0:            
            try:
                tn = telnetlib.Telnet(host=host, port=port, timeout=time_out) # this telnetlib is from python lib
#               tn = telnetlib.Telnet(host=host, port=port) # this telnetlib is from jython.jar lib
                tn.write(command + "\n")
                data = tn.read_until("DONE", timeout=60)
                tn.close()
                if None == data or 0==len(data):
                    retry_time -= 1
                    continue
                
                if (command.startswith("DUMP")) and (not data.endswith("DONE")):
                    self.m_logger.error("The dump data not end with 'DONE', continue this dump loop")
                    retry_time -= 1  
                    continue
                break
            except Exception, e:
                msg = "[%s] Failed to get infos from View Server by Telnet: [%s]" %(self.class_name, str(e))                
                self.m_logger.error(msg)
                if isinstance(tn, telnetlib.Telnet) and tn.sock:
                    tn.close()
                os.system("adb kill-server")
                os.system("adb start-server")
                os.system("adb -s %s forward tcp:%s tcp%s" %(self.device_name, self.view_server_port, self.view_server_port))
                os.system("adb -s %s forward tcp:%s tcp%s" %(self.device_name, self.monkey_server_port, self.monkey_server_port))
                retry_time -= 1                          
        
        if None==data or 0==len(data):
            self.m_logger.error("Fail to dump data!")
        else:
            if (command.startswith("DUMP")) and (not data.endswith("DONE")):
                data = None
            
        return data
    
    #===========================================================================
    # # ViewServer Command
    #===========================================================================
    
    # get ViewServer server version
    def getServerInfo(self):
        return self.getInfosByTelnet(ViewServerCommand.server_cmd)
    
    # get ViewServer protocol version
    def getProtocolInfo(self):
        return self.getInfosByTelnet(ViewServerCommand.protocol_cmd)
    
    # get View Info of Current Focused Window
    # 4080e650 com.android.calculator2/com.android.calculator2.Calculator  
    def getFocusViewInfo(self):
        return self.getInfosByTelnet(ViewServerCommand.get_focus_cmd)
    
    def getFocusViewHashCode(self):
        info = self.getFocusViewInfo()
        focusView = info.split("\n")[0]
        hash_code = focusView.split(" ")[0]
        return hash_code
    
    def getFocusViewClassName(self):
        info = self.getFocusViewInfo()
        focusView = info.split("\n")[0]
        l = focusView.split(" ")
        if None==l or 2>len(l):
            return None
          
        name = l[1]
        
        class_name = name.split(r"/")[-1]
        return class_name
        
    def getFocusViewPackageName(self):
        info = self.getFocusViewInfo() 
        focusView = info.split("\n")[0]
        name = focusView.split(" ")[1]
        
        package_name = name.split(r"/")[0]
        return package_name        
    
    def getViewListInfo(self):
        return self.getInfosByTelnet(ViewServerCommand.list_view_cmd)
    
    # current view is focused view
    def getCurrentViewInfo(self):
        dump_command = ViewServerCommand.dump_view_cmd + " -1"
        return self.getInfosByTelnet(dump_command)

    def dumpViewInfosByHashCode(self, hash_code="-1"):
        dump_command = ViewServerCommand.dump_view_cmd + " " + str(hash_code)
        try:
            return self.getInfosByTelnet(dump_command)
        except Exception, e:
            msg = "[%s]: Failed to Dump this view. The ID might be invalid! [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    # this method might have problem
    def getAutoListInfo(self):
        return self.getInfosByTelnet(ViewServerCommand.autolist_cmd)


#------------------------------------------------------------------------------ 
    #===========================================================================
    # # ViewDebug Command; they are retained for testing 
    #===========================================================================
    
    def captureInfoByHashCode(self, hash_code):
        capture_command = ViewServerCommand.capture_cmd + " " + str(hash_code)
        try:
            return self.getInfosByTelnet(capture_command)
        except Exception,e:
            msg = "[ERROR]:" + "Failed to Capture this view. The ID might be invalid! [%s]" %str(e)
            self.m_logger.error(msg)
            return None
        
    def invalidateInfoByID(self, strID):
        invalidate_command = ViewServerCommand.invalidate_cmd + " " + str(strID)
        try:
            return self.getInfosByTelnet(invalidate_command)
        except Exception,e:
            msg = "[ERROR]:" + "Failed to Invalidate this view. The ID might be invalid! [%s]" %str(e)
            self.m_logger.error(msg)
            return None
        
    def profileInfoByID(self, strID):
        profile_command = ViewServerCommand.profile_cmd + " " + str(strID)
        try:
            return self.getInfosByTelnet(profile_command)
        except Exception,e:
            msg = "[ERROR]:" + "Failed to Profile this view. The ID might be invalid! [%s]" %str(e)
            self.m_logger.error(msg)
            return None
#------------------------------------------------------------------------------ 

if __name__ == "__main__":
    deviceCmd = ViewServerCommand()
#    deviceCmd.getViewListInfo()
    deviceCmd.captureInfoByID("406a4c68")
    deviceCmd.invalidateInfoByID("406a4c68")
    deviceCmd.profileInfoByID("406a4c68")
    
    