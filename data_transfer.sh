#!/bin/bash
# 1st argument /dev/sda1
# 2nd argument cp or mv
# example ./data_transfer.sh /dev/sda1 mv   #for move

#mounting
sudo mount $1 /mnt/usb
sudo mkdir -p /mnt/usb/Data

sudo $2 -v /home/pi/Data/* /mnt/usb/Data/

#un-mounting
sudo umount /mnt/usb
#clear
