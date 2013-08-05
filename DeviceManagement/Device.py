#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## Device.py

import os
from AdbCommand import AdbCommand
from ViewServerCommand import ViewServerCommand
from DeviceConsole import DeviceConsole

class Device():
    '''
    Device
    '''
    
    def __init__(self, logger, device_name="emulator-5554", device_port=5554, device_address="127.0.0.1", view_server_port=4939, monkey_server_port=12345):
        self.m_logger = logger
        self.class_name = "Device"
        self.device_name = device_name
        self.device_port = device_port
        self.device_address = device_address
        self.view_server_port = view_server_port
        self.monkey_server_port = monkey_server_port
        
        self.adb_console = AdbCommand(self.m_logger, self.device_name, self.device_port)
        self.view_console = ViewServerCommand(self.m_logger, self.device_address, self.view_server_port, self.device_name, self.monkey_server_port)
        self.device_console = DeviceConsole(self.m_logger, self.device_address, self.device_port)
    
    # 3 state
    # device, offline, bootloader    
    def checkDevice(self):
        command = "adb -s %s get-state" %self.device_name
        out = os.popen(command)
        res = out.read()
        out.close()
        try:
            if (None == res) or (0 == len(res)) or ("device" != res.rstrip("\n")):
                self.adb_console.killServer()
                self.adb_console.startServer()    
                self.adb_console.forwardPort(self.view_server_port, self.view_server_port)
                self.adb_console.forwardPort(self.monkey_server_port, self.monkey_server_port)            
            return True
        except Exception, e:
            msg = "[%s] Failed to check Device state: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def hasService(self):
        ## check whether this device has IWindowServer service
        check_cmd = "adb -s %s shell getprop ro.secure" %self.device_name
        out=os.popen(check_cmd) ## return "0\r\n" or "1\r\n"
        res = out.read()
        out.close()
        if (None==res) or (0==len(res)):
            msg = "Please check whether your device or emulator is running?"
            self.m_logger.error(msg)
            return False
        
        elif '1' == res[0]:
            msg = "This is real device and it might not have android IWindowManger service!"
            self.m_logger.warn(msg)
            return True
        elif '0' == res[0]:
            msg = "Emulator or rooted-device has IWindowService!"
            return True
        else:
            self.m_logger.error("Failed to check whether device has IWindowService: other errors")
            return False
        
    def stopService(self):
        ## stop window service first
        stopWinService_cmd = "adb -s %s shell service call window 2 i32 %s" %(self.device_name, self.view_server_port)
        return_code = os.system(stopWinService_cmd)
        if 0 != return_code:
            msg = "Fail to stop IWindow Service"
            self.m_logger.error(msg)
    
    def startService(self):
        ## start window service then
        startWinService_cmd = "adb -s %s shell service call window 1 i32 %s" %(self.device_name, self.view_server_port)
        return_code = os.system(startWinService_cmd)
        if 0 != return_code:
            msg = "Fail to start IWindow Service"
            self.m_logger.error(msg)
        
    
    def setForwardPort(self):            
        ## set port forwarding
        setPortForwarding_cmd = "adb -s %s forward tcp:%s tcp:%s" %(self.device_name, self.view_server_port, self.view_server_port)
        return_code = os.system(setPortForwarding_cmd)
        if 0 == return_code:  
            return True
        else:
            return False
    
    def isServiceRunning(self):        
        viewServer_running_flag = "Result: Parcel(00000000 00000001   '........')"
        viewServer_not_running_flag = "Result: Parcel(00000000 00000000   '........')"
        
        check_command = "adb -s %s shell service call window 3 i32 %s" %(self.device_name, self.view_server_port)
        
        try:
            out = os.popen(check_command)
            res = out.read()
            res = res.rstrip(os.linesep)
            out.close()
        except Exception, e:
            self.m_logger.error("Failed to check isRunning of IWindowServer service: [%s]" %str(e))
            return False
        
        if viewServer_not_running_flag == res:
            return False
        elif viewServer_running_flag == res:
            return True
        else:
            return False
        
    def open(self):
        try:
#            if not self.checkDevice():
#                return False
                
            if not self.hasService():
                return False
            
            if not self.isServiceRunning():
                self.startService()
                
            if self.setForwardPort():
                return True
        except Exception, e:
            self.m_logger.error("Faild to open device: [%s]" %str(e))
        return False
        
    def close(self):
        if self.isServiceRunning():
            self.stopService()
            
    def isClosed(self):
        return (not self.isServiceRunning())
    
    
    def getDumpData(self, command="DUMP -1"):
        return self.view_console.getInfosByTelnet(command)
    
    
    
