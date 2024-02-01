#!/bin/bash
time=`date +%F_%H-%M`
backup_path=../
cp -Trf ./db/ $backup_path'db.'$time
rm -f $backup_path'db.latest'
ln -s ./db.$time $backup_path'db.latest'
