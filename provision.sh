#! /bin/bash

USER='tablut'
PASSWD='tablut'
IP='192.168.20.2'


sshpass -p $PASSWD ssh $USER@$IP rm -vr /tablut/*
echo '[+] Removed old files'

sshpass -p $PASSWD scp ./src/* $USER@$IP:/tablut
echo '[+] Copied new files'
