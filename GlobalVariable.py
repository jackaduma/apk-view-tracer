#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## GlobalVariable.py

class Global():
    ## global variables for store
    g_bReDump = False  ## re-dump view if it was True
    g_sPreFocusedViewHashCode = "0"  ## set this value 
    g_sCurFocusedViewHashCode = "0"  ## set this value after dump
    g_lsPreViewsList = []   ## set this value 
    g_lsCurViewsList = []   ## set this value
