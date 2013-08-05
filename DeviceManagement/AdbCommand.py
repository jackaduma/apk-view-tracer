#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## AdbCommand.py

import os

class AdbCommand():
    '''
    Adb Command : it use adb command
    '''
    __ClassName = "CommandConsole"
    
    def __init__(self, logger, device_name, device_port):
        self.device_port = device_port
        self.device_name = device_name
        self.m_logger = logger
        
    def executeCommand(self, cmd, bNeedResult=False):
        try:
            if bNeedResult:
                out = os.popen(cmd)
                res = out.read()
                out.close()
                return res
            else:
                return_code = os.system(cmd)
                if 0 == return_code:
                    return True
                else:
                    return False
        except Exception, e:
            msg = "[%s] Failed execute cmd [%s]: [%s]" %(self.class_name, cmd, str(e))
            self.m_logger.error(msg)
            if bNeedResult:
                return None
            else:
                return False
        
    def killServer(self):
        killCommand = "adb -s %s kill-server" %self.device_name
        return self.executeCommand(killCommand)
    
    def startServer(self):
        startCommand = "adb -s %s start-server" %self.device_name
        return self.executeCommand(startCommand)
    
    def forwardPort(self, source_port, target_port):
        forwardCommand = "adb -s %s forward tcp:%s tcp:%s" %(source_port, target_port)
        return self.executeCommand(forwardCommand)
        
    def installPkg(self, package_name):
        # 安装 package的时候就不需要判断之前有没有安装package 
        # 参数 -r 
        installPkgCmd = "adb -s %s install -r %s" %(self.device_name, package_name) 
        return self.executeCommand(installPkgCmd)
    
    def removePkg(self, package_name):
        removePkgCmd = "adb -s %s uninstall %s" %(self.device_name, package_name)
        return self.executeCommand(removePkgCmd)
    
    def shell(self, command, bNeedResult=False):
        shell_command = "adb -s %s shell %s" %(self.device_name, command)
        return self.executeCommand(shell_command, bNeedResult)

    #===========================================================================
    #  start an Activity: am start [-D] [-W] <INTENT>
    # -D: enable debugging
    # -W: wait for launch to complete
    # <INTENT> specifications include these flags:
    # [-a <ACTION>] [-d <DATA_URI>] [-t <MIME_TYPE>]
    # [-c <CATEGORY> [-c <CATEGORY>] ...]
    # [-e|--es <EXTRA_KEY> <EXTRA_STRING_VALUE> ...]
    # [--esn <EXTRA_KEY> ...]
    # [--ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE> ...]
    # [-e|--ei <EXTRA_KEY> <EXTRA_INT_VALUE> ...]
    # [-n <COMPONENT>] [-f <FLAGS>]
    # [--grant-read-uri-permission] [--grant-write-uri-permission]
    # [--debug-log-resolution]
    # [--activity-brought-to-front] [--activity-clear-top]
    # [--activity-clear-when-task-reset] [--activity-exclude-from-recents]
    # [--activity-launched-from-history] [--activity-multiple-task]
    # [--activity-no-animation] [--activity-no-history]
    # [--activity-no-user-action] [--activity-previous-is-top]
    # [--activity-reorder-to-front] [--activity-reset-task-if-needed]
    # [--activity-single-top]
    # [--receiver-registered-only] [--receiver-replace-pending]
    # [<URI>]
    #===========================================================================
    def startActivity(self, uri, action, data, mimetype, categories_list, component, flags_list=None, extras_list=None):
        startActivityCmd = "adb -s %s shell am start -W " %self.device_name            
        
        if None!=action and 0!=len(action):
            startActivityCmd += "-a %s " %action
            if None!=data and 0!=len(data):
                startActivityCmd += "-d %s " %data
            if None!=mimetype and 0!=len(mimetype):
                startActivityCmd += "-t %s " %mimetype
        
        if None!=categories_list and 0!=len(categories_list):
            for category in categories_list:
                if None!=category and 0!=len(category):
                    startActivityCmd += "-c %s " %category
                    
        if None!=extras_list and 0!=len(extras_list):
            for extra in extras_list:
                if None!=extra and 0!=len(extra):
                    startActivityCmd += "-e %s " %extra
                
        if None!=component and 0!=len(component):
            startActivityCmd += "-n %s " %component
            if None!=flags_list and 0!=len(flags_list):
                for flag in flags_list:
                    if None!=flag and 0!=len(flag):
                        startActivityCmd += "-f %s " %flag
                        
        if None!=uri and 0!=len(uri):
            startActivityCmd += uri
        
        return self.executeCommand(startActivityCmd)  

    ## for example:
    ## To start the Settings application: # am start -n com.android.settings/.Settings
    ##                                    # am start -n com.android.settings/com.android.settings.Settings
    ## To start the Browser: # am start -n com.android.browser/.BrowserActivity
    ##                       # am start -n com.android.browser/com.android.browser.BrowserActivity
    ## To start the Calculator # am start -n com.android.calculator2/.Calculator
    ##                         # am start -n com.android.calculator2/com.android.calculator2.Calculator    
    def startActivity2(self, package_name, activity_name, url=None):
        # -W must be before -n
        # -W is "start" command option, and -n is <INTENT> option
        if None==url:
            startActivityCmd = "adb -s %s shell am start -W -n %s/%s" %(self.device_name, package_name, activity_name)
        else:
            startActivityCmd = "adb -s %s shell am start -W -n %s/%s %s" %(self.device_name, package_name, activity_name, url)
        return self.executeCommand(startActivityCmd)
    
    ## To start the phone dialer: # am start tel:210-385-0098
    def startPhoneDialer(self, phone_number):
        startPhoneDialerCmd = "adb -s %s shell am start tel:%s" %(self.device_name, str(phone_number))
        return self.executeCommand(startPhoneDialerCmd)
    
    def startService(self, service_name):
        startServiceCmd = "adb -s %s shell am startservice %s" %(self.device_name, service_name)
        return self.executeCommand(startServiceCmd)
        
    def sendBroadcastIntent(self, broadcast_name):
        sendIntentCmd = "adb -s %s shell am broadcast %s" %(self.device_name, broadcast_name)
        return self.executeCommand(sendIntentCmd)
    
    def startInstrumentation(self, component_name):
        startInstrumentationCmd = "adb -s %s shell am instrument -w %s" %(self.device_name, component_name)
        return self.executeCommand(startInstrumentationCmd)
    
    def pushFile(self, local_path, emulator_path):
        pushFileCmd = "adb -s %s push %s %s" %(self.device_name, local_path, emulator_path)
        return self.executeCommand(pushFileCmd)
    
    def pullFile(self, emulator_path, local_path):
        pullFileCmd = "adb -s %s pull %s %s" %(self.device_name, emulator_path, local_path)
        return self.executeCommand(pullFileCmd)
        
    def phoneCall(self):
        pass
    
    def sendSMS(self):
        pass
    
    def browseWebPage(self):
        pass
    
    