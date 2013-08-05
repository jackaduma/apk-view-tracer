#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## ApkViewTracer.py

import platform,sys,os
import logging
import Logger

class ApkViewTracer():
    '''
    ApkViewTracer class is the main entry.
    '''
    
    __ClassName = "ApkViewTracer"
    
    def __init__(self):
        self.curDir = os.getcwd() + os.sep
        script_file_name="TestScripts/testMonkeyRunnerImpl.py"
        script_file_name="TestScripts/testNotification.py"
        script_file_name="TestScripts/testHome.py"
        script_file_name="TestScripts/testMenu.py"
        self.script_file = self.curDir + script_file_name
        self.m_logger = Logger.InitLog("apk-view-tracer.log", logging.getLogger("apk-view-tracer.thread"))
        
    def run(self, script_file):       
        curOS=platform.system()
        if "Windows" == curOS:
            self.m_logger.info("current OS is Windows!")
            os.system(self.curDir + "Run.bat %s" %script_file)
        elif "Linux" == curOS:
            self.m_logger.info("current OS is Linux!")
            os.system(self.curDir + "Run.sh %s" %script_file)
        else:
            self.m_logger.error("Current OS is not Windows or Linux!")
            raise Exception

def main():    
    apk_view_tracer = ApkViewTracer()
    
    script_file=""
    if None == sys.argv or 2>len(sys.argv):
        script_file = apk_view_tracer.script_file
        #print "It must have a script as input argument!"
        #return
    else:
        script_file = sys.argv[1]
        
    apk_view_tracer.run(script_file)

if __name__=="__main__":    
    main()
    
