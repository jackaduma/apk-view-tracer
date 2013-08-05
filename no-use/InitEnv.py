#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## InitEnv.py

import os
from Utility import getToolsDir,getPlatformToolsDir

class InitEnvironment():
    def __init__(self, logger):
        self.m_logger = logger
        self.current_dir = os.getcwd()
    
    ## check dir
    def checkDir(self):
        dir_list = os.listdir(os.getcwd())       
        if "tools" not in dir_list:
            msg = "It needs android sdk tools dir here! "
            print msg
            self.m_logger.error(msg)
            return False        
        if "platform-tools" not in dir_list:
            msg = "It needs android sdk platform-tools dir here! "
            print msg
            self.m_logger.error(msg)
            return False

        return True

    ## check file
    def checkFile(self):
        android_tool_file_list = os.listdir(getToolsDir())
        if (None==android_tool_file_list) or (0==len(android_tool_file_list)):
            msg = "There is no files in android sdk tools dir! "
            print msg
            self.m_logger.error(msg)
            return False
        
        android_platform_tools_file_list = os.listdir(getPlatformToolsDir())
        if (None==android_platform_tools_file_list) or (0==len(android_platform_tools_file_list)):
            msg = "There is no files in android sdk platform-tools dir! "
            print msg
            self.m_logger.error(msg)
            return False               
        return True
        
    def run(self):
        if self.checkDir() and self.checkFile():
            msg = "Sucess to init enviroment! "
            print msg
            self.m_logger.info(msg)
        else:
            return False        
        return True
    
if __name__=="__main__":
    InitEnv = InitEnvironment()
    InitEnv.run()
