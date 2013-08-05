#!/bin/bash

REPORTROOT=./reports

# remove old report files
echo "Removing old output report files..."
rm $REPORTROOT

# make dir for new report files
echo "Output reports will be stored in $REPORTROOT..."
mkdir $REPORTROOT

# run monkey on the entire system
echo "Running Monkey on entire system..."
adb -e shell monkey -v -v -v 500 > $REPORTROOT/monkey_sys.txt
# pull the log file from device?

# run monkey on particular packages
# packages here...

# create composite report
echo "Running reports..."
grep -A 5 -h -r CRASH $REPORTROOT > $REPORTROOT/crash_report.txt
