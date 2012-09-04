#!/bin/bash

stats=`hostname`'-> CPU idle: '`iostat|gawk '{if (NR==4) print $6 }'`' '`uptime |gawk '{print $4 " "$5" Load:"$8}'`' / usage: '`df -h|gawk '{if (NR==2) print $5}'`', Free memory: '`vmstat -S M|gawk '{if (NR==3) print $4}'`'M'
echo $stats
