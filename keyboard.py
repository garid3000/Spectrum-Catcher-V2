import os, time
import curses

from Custom_Lib.devinput       import *
from Custom_Lib.button_manager import *
bm = None

class Keyboard():
    def __init__(self):
        #bm.addTagButton(   0, 1, 2,  7, " ↑↑ ",    tag="cap", buttonId="a", show=True)
        #bm.addTagButton(   0, 9, 2,  7, "?123",    tag="123", buttonId="b", show=True)
        #bm.addTagButton(   0,18, 2,  7, " ↓↓ ",    tag="low", buttonId="b", show=True)
        bm.addButton(  1  , 2, 3, 28, "    ",    tag="norm", buttonId="d", show=True)

        bm.addButton( 13  , 1, 3,  7, " ↑↑ ",    tag="norm", buttonId="a", show=True)
        bm.addButton( 13  , 8, 3,  7, " ↓↓ ",    tag="norm", buttonId="c", show=True)
        bm.addButton( 13  ,15, 3,  7, " "   ,    tag="norm", buttonId=" ", show=True)
        bm.addButton( 13  ,22, 3,  7, "?123",    tag="norm", buttonId="b", show=True)


        bm.setCallback('a', self.change2capital)
        bm.setCallback('b', self.change2number)
        bm.setCallback('c', self.change2lower)

        self.l1 = ['q','w','e','r','t','y','u','i','o','p']
        self.l2 = ['a','s','d','f','g','h','j','k','l',';']
        self.l3 = ['z','x','c','v','b','n','m',',','.',' ']

        self.L1 = ['Q','W','E','R','T','Y','U','I','O','P']
        self.L2 = ['A','S','D','F','G','H','J','K','L',';']
        self.L3 = ['Z','X','C','V','B','N','M',',','.',' ']

        self.n1 = ['1','2','3','4','5','6','7','8','9','0']
        self.n2 = ['!','@','#','$','%','^','&','*','(',')']
        self.n3 = ['~','`','_','-','=','+','?','/','<','>']

        xs = [i*3 +1 for i  in range(10)]
        ys = [4, 7, 10]

        #x = [None] * 10
        for i in range(10):
            bm.addButton( ys[0], xs[i], 3, 3, self.l1[i],
                        tag = 'norm',
                        buttonId = "b{}{}".format(0,i), show=True)
            time.sleep(.01)
            bm.refresh(-1,-1)

        for i in range(10):
            bm.addButton( ys[1], xs[i], 3, 3, self.l2[i],
                        tag = 'norm',
                        buttonId = "b{}{}".format(1,i), show=True)
            time.sleep(.01)
            bm.refresh(-1,-1)

        for i in range(10):
            bm.addButton( ys[2], xs[i], 3, 3, self.l3[i],
                        tag = 'norm',
                        buttonId = "b{}{}".format(2,i), show=True)
            time.sleep(.01)
            bm.refresh(-1,-1)
        return

    def change2capital(self):
        for i in range(10): bm.setLabel("b{}{}".format(0,i), self.L1[i]);
        for i in range(10): bm.setLabel("b{}{}".format(1,i), self.L2[i]);
        for i in range(10): bm.setLabel("b{}{}".format(2,i), self.L3[i]);
        bm.refresh(-1,-1)
    def change2lower(self):
        for i in range(10): bm.setLabel("b{}{}".format(0,i), self.l1[i]);
        for i in range(10): bm.setLabel("b{}{}".format(1,i), self.l2[i]);
        for i in range(10): bm.setLabel("b{}{}".format(2,i), self.l3[i]);
        bm.refresh(-1,-1)
    def change2number(self):
        for i in range(10): bm.setLabel("b{}{}".format(0,i), self.n1[i]);
        for i in range(10): bm.setLabel("b{}{}".format(1,i), self.n2[i]);
        for i in range(10): bm.setLabel("b{}{}".format(2,i), self.n3[i]);
        bm.refresh(-1,-1)





def init():
    kbd = Keyboard()
    return


def main(stdscr):
    global bm
    bm = Buttons_manager(stdscr)

    textstr = ""

    init()
    bm.refresh(-1,-1)
    while 1:
        y,x = getTouch()
        #:bm.setLabel('d', "{}-{}".format(y,x))
        x = bm.refresh(y,x)
        if x is not None and len(x) ==1:
            textstr += x
            bm.setLabel('d', textstr)
            bm.refresh(-1,-1)

        #stdscr.addstr(y,x, "{}{}".format(y,x))
        #stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
