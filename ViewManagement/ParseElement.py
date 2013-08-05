#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracking
## ParseElement.py

from DeviceManagement.Device import Device
from TreeType import CRect
from Utility import str2int

class ParseElement():
    def __init__(self, element_data):
        self.class_name = ""
        self.hash_code = ""
        self.properties_dict = {}
        self.element_data = element_data.lstrip(" ")
    
    def getInt(self, string, integer):
        try:
            return int(self.properties_dict[string])
        except:
            return integer
        
    def getBoolean(self, string, boolean):
        try:
            if "false" == self.properties_dict[string]:
                return False
            elif "true" == self.properties_dict[string]:
                return True
            else:
                return boolean
        except:
            return boolean
    
    def loadProperties(self, data):
        i = 0
        data_length =len(data)
        
        while True:
            if i >= data_length:
                break
            key_sep_index = data.index("=", i)
            
            key = data[i : key_sep_index]
            
            value_length_sep_index = data.index(",", key_sep_index+1)
            value_length = int(data[key_sep_index+1 : value_length_sep_index])
            
            i = value_length_sep_index + 1 + value_length
            
            value = data[value_length_sep_index+1 : value_length_sep_index+1+value_length]

            self.properties_dict[key] = value
            
            i += 1
                
        self.id = self.properties_dict["mID"]
        
        if "mLeft" in self.properties_dict.keys():
            self.left = self.getInt("mLeft", 0)
        else:
            self.left = self.getInt("layout:mLeft", 0)
            
        if "mRight" in self.properties_dict.keys():
            self.right = self.getInt("mRight", 0)
        else:
            self.right = self.getInt("layout:mRight", 0)
        
        if "mTop" in self.properties_dict.keys():
            self.top = self.getInt("mTop", 0)
        else:
            self.top = self.getInt("layout:mTop", 0)
        
        if "mBottom" in self.properties_dict.keys():
            self.bottom = self.getInt("mBottom", 0)
        else:
            self.bottom = self.getInt("layout:mBottom", 0)
        
        if "getWidth()" in self.properties_dict.keys():
            self.width = self.getInt("getWidth()", 0)
        else:
            self.width = self.getInt("layout:getWidth()", 0)
            
        if "getHeight()" in self.properties_dict.keys():
            self.height = self.getInt("getHeight()", 0)
        else:
            self.height = self.getInt("layout:getHeight()", 0)
            
        if "mScrollX" in self.properties_dict.keys():
            self.scrollX = self.getInt("mScrollX", 0)
        else:
            self.scrollX = self.getInt("scrolling:mScrollX", 0)
            
        if "mScrollY" in self.properties_dict.keys():
            self.scrollY = self.getInt("mScrollY", 0)
        else:
            self.scrollY = self.getInt("scrolling:mScrollY", 0)
            
        if "mPaddingLeft" in self.properties_dict.keys():
            self.paddingLeft = self.getInt("mPaddingLeft", 0)
        else:
            self.paddingLeft = self.getInt("padding:mPaddingLeft", 0)
            
        if "mPaddingRight" in self.properties_dict.keys():
            self.paddingRight = self.getInt("mPaddingRight", 0)
        else:
            self.paddingRight = self.getInt("padding:mPaddingRight", 0)
            
        if "mPaddingTop" in self.properties_dict.keys():
            self.paddingTop = self.getInt("mPaddingTop", 0)
        else:
            self.paddingTop = self.getInt("padding:mPaddingTop", 0)
            
        if "mPaddingBottom" in self.properties_dict.keys():
            self.paddingBottom = self.getInt("mPaddingBottom", 0)
        else:
            self.paddingBottom = self.getInt("padding:mPaddingBottom", 0)
        
        if "layout_leftMargin" in self.properties_dict.keys():
            self.marginLeft = self.getInt("layout_leftMargin", -2147483648)
        else:
            self.marginLeft = self.getInt("layout:layout_leftMargin", -2147483648)
            
        if "layout_rightMargin" in self.properties_dict.keys():
            self.marginRight = self.getInt("layout_rightMargin", -2147483648)
        else:
            self.marginRight = self.getInt("layout:layout_rightMargin", -2147483648)    
            
        if "layout_topMargin" in self.properties_dict.keys():
            self.marginTop = self.getInt("layout_topMargin", -2147483648)
        else:
            self.marginTop = self.getInt("layout:layout_topMargin", -2147483648)
            
        if "layout_bottomMargin" in self.properties_dict.keys():
            self.marginBottom = self.getInt("layout_bottomMargin", -2147483648)
        else:
            self.marginBottom = self.getInt("layout:layout_bottomMargin", -2147483648)
            
        if "getBaseline()" in self.properties_dict.keys():
            self.baseline = self.getInt("getBaseline()", 0)
        else:
            self.baseline = self.getInt("layout:getBaseline()", 0)
            
        if "willNotDraw()" in self.properties_dict.keys():
            self.willNotDraw = self.getBoolean("willNotDraw()", False)
        else:
            self.willNotDraw = self.getBoolean("drawing:willNotDraw()", False)
            
        if "hasFocus()" in self.properties_dict.keys():
            self.hasFocus = self.getBoolean("hasFocus()", False)
        else:
            self.hasFocus = self.getBoolean("focus:hasFocus()", False)
            
        if "isClickable()" in self.properties_dict.keys():
            self.isClickable = self.getBoolean("isClickable()", False)
            
        if "isEnabled()" in self.properties_dict.keys():
            self.isEnabled = self.getBoolean("isEnabled()", False)

        self.hasMargins = ((self.marginLeft != -2147483648) and (self.marginRight != -2147483648)  
                       and (self.marginTop != -2147483648) and (self.marginBottom != -2147483648))
    
    
    def parseElmentData(self):
        data = self.element_data.lstrip(" ")
        
        sep_index = data.index("@")
        self.class_name = data[0 : sep_index]
        
        sub_string = data[sep_index+1 : ]
        
        sep_index = sub_string.index(" ")
        self.hash_code = sub_string[0 : sep_index]
        
        sub_string = sub_string[sep_index+1 : ]
        
        self.loadProperties(sub_string)
        

    #===============================================================================
    # # get Class Name of View and its Instance Storage Address's Hash Code
    # # android.widget.ListView@44ed6480
    # # android.widget.TextView@44ed7e08
    #===============================================================================
    def getClassName(self,):
        return self.class_name
    
    #===========================================================================
    # # get Hash Code
    #===========================================================================
    def getHashCode(self):
        return self.hash_code
                    

    #===============================================================================
    # # etc. mID=7,id/sqrt
    # # etc. mID=14,id/panelswitch
    #===============================================================================
    def getID(self):
        return self.id
    
    #===============================================================================
    # # getVisibility()=n, xxx
    # # three states: VISIBLE, GONE, 
    #===============================================================================
    def getVisible(self):
        if "getVisibility()" in self.properties_dict.keys():            
            res = self.properties_dict["getVisibility()"]
            if "VISIBLE" == res:
                return True
            elif "GONE" == res:
                return False
            elif "INVISIBLE" == res:
                return False
            else:
                print "current visibility state: [%s]" %res
                return False
        else:
            return None

    #===============================================================================
    # # isClickable()=4,true
    # # isClickable()=5,false
    #===============================================================================
    def getClickable(self):
        if "isClickable()" in self.properties_dict.keys():
            return self.isClickable
        else:
            return None

    #===============================================================================
    # # isEnabled()=4,true
    #===============================================================================
    def getEnable(self):
        if "isEnabled()" in self.properties_dict.keys():
            return self.properties_dict["isEnabled()"]
        else:
            return None

    #===============================================================================
    # # willNotDraw()=5,false
    # # willNotDraw()=4,true
    #===============================================================================
    def getWillNotDraw(self):
        if "willNotDraw()" in self.properties_dict.keys():
            return self.properties_dict["willNotDraw()"]
        else:
            return None


    #===============================================================================
    # #  mPrivateFlags_NOT_DRAWN=3,0x0   false
    # #  mPrivateFlags_DRAWN=4,0x20      true
    #===============================================================================
    def getDRAWN(self):
        if "mPrivateFlags_DRAWN" in self.properties_dict.keys():
            res = self.properties_dict["mPrivateFlags_DRAWN"]
            if "0x20" == res:
                return True
            else:
                return None
        elif "mPrivateFlags_NOT_DRAWN" in self.properties_dict.keys():
            res = self.properties_dict["mPrivateFlags_NOT_DRAWN"]
            if "0x0" == res:
                return False
            else:
                return None
        else:
            return None
    
    #===============================================================================
    # # etc. mText=3,log
    # # etc. mText=1,√
    #===============================================================================
    def getText(self):                
        if "mText" in self.properties_dict.keys():
            return self.properties_dict["mText"]
        elif "text:mText" in self.properties_dict.keys():
            return self.properties_dict["text:mText"]
        else:
            return None   
    
    def getRectArea(self):
        rect = CRect()
        rect.mTop = self.top
        rect.mBottom = self.bottom
        rect.mLeft = self.left
        rect.mRight = self.right
        return rect


    #===============================================================================
    # # this method has not used yet.
    #===============================================================================
    def getRectMidPoint(self, element):
        mid_point = {"x": None,
                     "y": None}
    
        rect = {"left": None,
                "right": None,
                "top": None,
                "bottom": None}
        tag_list = element.split(" ")
        for tag in tag_list:
            if "mTop=" in tag:
                l = tag.split(",")
                rect["top"] = l[1]
            elif "mBottom=" in tag:
                l = tag.split(",")
                rect["bottom"] = l[1]
            elif "mLeft=" in tag:
                l = tag.split(",")
                rect["left"] = l[1]
            elif "mRight" in tag:
                l = tag.split(",")
                rect["right"] = l[1]
    
        if (rect["top"]!=None) and (rect["bottom"]!=None) and (rect["left"]!=None) and (rect["right"]!=None):
            mid_point["x"] = (str2int(rect["right"])-str2int(rect["left"]))/2.0
            mid_point["y"] = (str2int(rect["bottom"])-str2int(rect["top"]))/2.0
    
        return mid_point


if __name__=="__main__":
    device = Device()
    data = device.getInfosByTelnet("DUMP -1")
    element_parser = ParseElement()
    element_parser.getStructure(data)
