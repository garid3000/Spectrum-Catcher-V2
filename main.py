import os, time
import curses

from Custom_Lib.devinput       import *
from Custom_Lib.button_manager import *

aboutstr = 'Spectrum Catcher V2.0\n developed by Hokkaido Uni.\n License notice: this software uses following GPL/LGPL softwares that are provided from Raspberry-OS'
#. Those softwares are ffmpeg, bash, ncurses, opencv2'

bm = None
def init():
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    bm.addTagButton(   0, 1, 3,  7, "Meas.",    tag="mb1", buttonId="a", show=True)
    bm.addTagButton(   3, 1, 3,  7, "Setup",    tag="mb2", buttonId="b", show=True)
    bm.addTagButton(   6, 1, 3,  7, "Data" ,    tag="mb3", buttonId="c", show=True)
    bm.addTagButton(   9, 1, 3,  7, "About",    tag="mb4", buttonId="d", show=True)
    bm.addTagButton(  12, 1, 3,  7, "Sys." ,    tag="mb5", buttonId="e", show=True)

    bm.addButton(1+ 1, 9, 4, 14, "Capture",     tag="mb1", buttonId="mb1_1" )
    bm.addButton(1+ 1,23, 4, 14, "Expo-calib",  tag="mb1", buttonId="mb1_1a")
    bm.addButton(1+ 5, 9, 4, 14, "M-Shot(v1)",  tag="mb1", buttonId="mb1_2" )
    bm.addButton(1+ 5,23, 4, 14, "M-Shot(v2)",  tag="mb1", buttonId="mb1_2a")
    bm.addButton(1+ 9, 9, 4, 14, "P/view cam",  tag="mb1", buttonId="mb1_3" )
    bm.addButton(1+ 9,23, 4, 14, "P/view spe",  tag="mb1", buttonId="mb1_4" )

    bm.addButton(1+ 1, 9, 4, 14, "Expo",        tag="mb2", buttonId="mb2_1")
    bm.addButton(1+ 5, 9, 4, 14, "Gain",        tag="mb2", buttonId="mb2_2")
    bm.addButton(1+ 9, 9, 4, 14, "M-shot (v1)", tag="mb2", buttonId="mb2_3")
    bm.addButton(1+ 9, 9, 4, 14, "M-shot (v2)", tag="mb2", buttonId="mb2_4")
    #bm.addButton(1+ 7, 9, 3, 14, "Timer",      tag="mb2", buttonId="mb2_3")
    #bm.addButton(1+10, 9, 3, 14, "Multi",      tag="mb2", buttonId="mb2_4")

    bm.addButton(1+ 1, 9, 4, 14, "Copy data",   tag="mb3", buttonId="mb3_1")
    bm.addButton(1+ 5, 9, 4, 14, "Move data",   tag="mb3", buttonId="mb3_2")
    bm.addButton(1+ 9, 9, 4, 14, "Del. data",   tag="mb3", buttonId="mb3_3")
    bm.addButton(1+ 1,23,12, 14, "",            tag="mb3", buttonId="mb3_4",boxshow=False)

    bm.addButton(   1, 9,13, 28, aboutstr,      tag="mb4", buttonId="mb4_1",boxshow=False)
    bm.addButton(   1,10, 3, 20, "---- System -----",
                                  tag="mb5", buttonId="mb5_1", boxshow=False)
    bm.addButton(1+ 5, 9, 4, 14, "Shutdown",    tag="mb5", buttonId="mb5_2")
    bm.addButton(1+ 5,23, 4, 14, "Reboot",      tag="mb5", buttonId="mb5_3")
    bm.addButton(1+ 9, 9, 4, 14, "Update",      tag="mb5", buttonId="mb5_4")
    bm.addButton(1+ 9,23, 4, 14, "Calibration", tag="mb5", buttonId="mb5_5")
    #bm.addButton(1+10, 9, 3, 14, "---------", tag="mb3", buttonId="mb3_4")

    bm.setCallback('mb1_1', callback_mb1_1)
    bm.setCallback('mb1_2', callback_mb1_2)
    bm.setCallback('mb1_3', callback_mb1_3)
    bm.setCallback('mb1_4', callback_mb1_4)

    bm.setCallback('mb2_1', callback_mb2_1)
    bm.setCallback('mb2_2', callback_mb2_2)

    bm.setCallback('mb3_1', callback_mb3_1)
    bm.setCallback('mb3_2', callback_mb3_2)
    bm.setCallback('mb3_3', callback_mb3_3)
    bm.setCallback('mb3_4', callback_mb3_4)

    bm.setCallback('mb5_2', callback_mb5_2)
    bm.setCallback('mb5_3', callback_mb5_3)
    bm.setCallback('mb5_3', callback_mb5_3)


def callback_mb3_1():
    os.system('bash ~/Spectrum-Catcher-V2/data_transfer.sh $(ls /dev/sda* | tail -n 1) cp')
    os.system('clear')
def callback_mb3_2():
    os.system('bash ~/Spectrum-Catcher-V2/data_transfer.sh $(ls /dev/sda* | tail -n 1) mv')
    os.system('clear')
def callback_mb3_3():
    os.system('rm -v /home/pi/Data*')
    os.system('clear')

def callback_mb3_4():
    files = os.listdir('/home/pi/Data')
    nfiles = len(files)
    nbmp = len([i for i in files if "bmp" in i])
    ncsv = len([i for i in files if "csv" in i])
    nnpy = len([i for i in files if "npy" in i])
    nmat = len([i for i in files if "mat" in i])
    npng = len([i for i in files if "png" in i])

    listoffiles = ' file: {}\n'.format(nfiles)
    listoffiles+= '   -bmp: {}\n'.format(nbmp)
    listoffiles+= '   -csv: {}\n'.format(ncsv)
    listoffiles+= '   -npy: {}\n'.format(nnpy)
    listoffiles+= '   -mat: {}\n'.format(nmat)
    listoffiles+= '   -png: {}\n'.format(npng)

    listoffiles+= '   last file:\n  '
    if nfiles:
        listoffiles+= files[-1]


    bm.setLabel('mb3_4', listoffiles)
    #os.system('bash /home/pi/shells/shot1.sh')
    #curses.curs_set(False)

def callback_mb1_1():
    #os.system('bash /home/pi/shells/shot1.sh')
    os.system('bash ~/Spectrum-Catcher-V2/shot1.sh')
    curses.curs_set(False)


def  callback_mb1_2():
    #os.system("bash clear;sudo setfont /etc/console-setup/cached_Uni2-TerminusBold16.psf.gz;cd /home/pi/Spectrum-Catcher-V2;python3 spectra_text2.py -D $(cat pm/device) -o $(cat pm/output) -d $(cat pm/datatype) -O $(cat pm/optimize) -e $(cat pm/engine) -n $(cat pm/number) -t $(cat pm/timer) -p $(cat pm/pov) -s -M $(cat pm/optupper) -m $(cat pm/optlower) -N $(date '+%b-%d_%H%M%S');clear;sudo setfont /etc/console-setup/cached_Uni2-Terminus32x16.psf.gz")
    curses.nocbreak()
    #stdscr.keypad(False)
    curses.echo()

    os.system("bash shower.sh")
    curses.curs_set(False)

def callback_mb1_3():
    os.system('bash ~/Spectrum-Catcher-V2/preview_cam.sh')
    #os.system('bash /home/pi/shells/preview_cam.sh')
    curses.curs_set(False)
    bm.refresh(1, 1)

def callback_mb1_4():
    curses.endwin()
    #os.system('bash /home/pi/shells/preview_spe.sh')
    #os.system('bash /home/pi/main2/shower.sh')
    #os.system('bash ~/Spectrum-Catcher-V2/shower.sh')
    os.system('bash ~/Spectrum-Catcher-V2/preview_spe.sh')
    bm.stdscr.keypad(False)
    curses.echo()
    curses.curs_set(False)
    bm.refresh(1, 1)

def callback_mb2_1():
    #os.system('python3 /home/pi/main2/setup_expo.py')
    os.system('python3 ~/Spectrum-Catcher-V2/setup_expo.py')
    curses.nocbreak()
    bm.stdscr.keypad(False)
    curses.echo()
    curses.curs_set(False)
def callback_mb2_2():
    #os.system('python3 /home/pi/main2/setup_gain.py')
    os.system('python3 ~/Spectrum-Catcher-V2/setup_gain.py')
    curses.nocbreak()
    bm.stdscr.keypad(False)
    curses.echo()
    curses.curs_set(False)

def callback_mb5_2():
    os.system('sudo shutdown 0')
def callback_mb5_3():
    os.system('sudo reboot')
def callback_mb5_4():
    os.system('bash ~/Spectrum-Catcher-V2/update.sh')

def main(stdscr):
    global bm
    bm = Buttons_manager(stdscr)

    init()
    bm.refresh(1,1)
    while 1:
        y,x = getTouch()
        bm.refresh(y,x)
        #stdscr.addstr(y,x, "{}{}".format(y,x))
        #stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
