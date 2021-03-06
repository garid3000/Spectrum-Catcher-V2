import os, time, sys
import curses
from Custom_Lib.devinput import *
from Custom_Lib.button_manager import *
from Custom_Lib.pyv4l2 import Py_v4l2

#spe camera
dev = '/dev/video{}'.format(0)
v4l2 = Py_v4l2(dev)


bm = None
def init():
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    #bm.addTagButton(   1, 1, 3,  7, "Meas.", tag="mb1", buttonId="a", show=True)
    #bm.addTagButton(   4, 1, 3,  7, "Setup", tag="mb2", buttonId="b", show=True)
    #bm.addTagButton(   7, 1, 3,  7, "Data" , tag="mb3", buttonId="c", show=True)
    #bm.addTagButton(  10, 1, 3,  7, "About", tag="mb4", buttonId="d", show=True)

    currentExpo = 'Gain: {:4d}'.format(v4l2.get_gain())

    bm.addButton(1, 9, 3, 14, "Setting Expo", tag="mb1", buttonId="mb1_1", show=True)
    bm.addButton(4, 9, 3, 10, "+ gain",       tag="mb1", buttonId="mb1_2", show=True)
    bm.addButton(4, 19,3, 10, "- gain",       tag="mb1", buttonId="mb1_3", show=True)
    bm.addButton(7, 9, 3, 14, currentExpo,    tag="mb1", buttonId="mb1_4", show=True)
    bm.addButton(10,9, 3, 10, "Done",         tag="mb1", buttonId="mb1_5", show=True)

    bm.setCallback('mb1_5', exit)
    bm.setCallback('mb1_2', callback_expo_up)
    bm.setCallback('mb1_3', callback_expo_down)
    #bm.setCallback('mb1_3', callback_mb1_3)
    #bm.setCallback('mb1_4', callback_mb1_4)
    #bm.setCallback('mb2_1', callback_mb2_1)


def exit():
    #global exitflag
    #exitflag = True
    #time.sleep(1)
    sys.exit(0)


def callback_expo_up():
    v4l2.set_gain(v4l2.gain + 1)
    i= v4l2.get_gain()
    bm.setLabel('mb1_4', 'Gain: {:4d}'.format(i))

def callback_expo_down():
    v4l2.set_gain(v4l2.gain - 1)
    i= v4l2.get_gain()
    bm.setLabel('mb1_4', 'Gain: {:4d}'.format(i))




def main(stdscr):
    global bm, exitflag
    bm = Buttons_manager(stdscr, cac=False)

    stdscr.box()
    stdscr.refresh()
    init()
    bm.refresh(1,1)
    while 1:
        y,x = getTouch()
        bm.refresh(y, x)
        #js= chr(stdscr.getch())
        #stdscr.addstr(10, 10, s)
        #if s == 'q':
        #    break
        #if exitflag:
        #    break

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.start_color()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    main(stdscr)

    curses.endwin()
    #curses.wrapper(main)
