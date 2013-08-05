#! python2.7
## -*- coding: utf-8 -*-

import telnetlib
import os

os.system("adb shell service call window 1 i32 4939")
os.system("adb forward tcp:4939 tcp:4939")

tn = telnetlib.Telnet("localhost", 4939)
tn.write("DUMP -1\n")
print tn.read_until("DONE")
tn.close()