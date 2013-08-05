#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## TreeType.py

#===============================================================================
# # data structures
#===============================================================================
class CRect(object):
    mLeft = 0
    mRight = 0
    mTop = 0
    mBottom = 0
    
class CPoint():
    x = 0
    y = 0

class CTreeNode(object):
    mClassName = "mClassName"
    mHashCode = "fffff"
    mId = "mId"
    mText = "mText"
    mAbsoluteRect=CRect()
    mRect = CRect()
    mLocation = CPoint() 
    mElement = "element_data" ## just init, it was string data which was dumped from telnet
    mParentNode = {} ## just init, but it also was CTreeNode object
    mChildNodes = []
    mDepth = 0
    mTreeDepth = 0 ## its depth in this view tree
    mActive = False ## currently, I get this value from (DRAWN, Visiable, Clickable)
    mVisible = False
    mScrollX = 0
    mScrollY = 0
    mClickable = False