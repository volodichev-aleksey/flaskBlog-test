#!/bin/bash
time=`date +%F_%H-%M`
backup_path=../
cp -Trf $backup_path'db.latest/' ./db
