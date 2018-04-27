#!/bin/bash
DIR=/home/deployuser/logs
LOGDIR="${DIR}"
sourcelogpath="${DIR}/access.log"
touchfile="${DIR}/touchforlogrotate"
DATE=`date -d yesterday +%Y%m%d`
destlogpath="${LOGDIR}/access.${DATE}.log"
mv $sourcelogpath $destlogpath
touch $touchfile
