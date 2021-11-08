import os

def usbstorage():
    alldev = os.listdir('/dev')
    sda_s = [i for i in alldev if 'sda' in i]
    sdb_s = [i for i in alldev if 'sdb' in i]
    sdc_s = [i for i in alldev if 'sdc' in i]
    sdd_s = [i for i in alldev if 'sdd' in i]

    print('sda_s', sda_s)
