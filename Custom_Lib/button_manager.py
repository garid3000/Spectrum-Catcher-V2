import os, time
import curses

class Button():
    def __init__(self, y,x, sizey, sizex, label,#scr,
            callback = None, show = True, tag = None, buttonId=None, boxshow=True):

        self.y    , self.x      = y    , x
        self.sizey, self.sizex  = sizey, sizex
        self.win  = curses.newwin(sizey, sizex, y, x)
        self.label  = label
        self.show = show
        self.buttonId = buttonId
        self.tag = tag
        self.boxshow = boxshow
        #self.scr = scr
        if callback is None:
            self.callback = self.nothing
        else:
            self.callback = callback


    def nothing(self):
        pass

    def drawBox(self):
        if self.boxshow:
            self.win.box()
    def writeLabel(self):
        #self.win.addstr(1 + (self.sizey-2)//2,
        #                1,
        #                self.label)
        self.win.addstr(1,
                        1,
                        self.label)


    def refresh(self, ty=None, tx=None):
        tmp = False
        if self.show:
            if (ty is not None) and (tx is not None):
                tmp = self.check(ty, tx)
                if tmp:
                    self.win.bkgd(' ', curses.color_pair(1))
                    #self.callback()
                    #self.drawBox()
                    #self.writeLabel()
                    #self.win.refresh()
                    #return True # meaning tried to run ccall
                else:
                    self.win.bkgd(' ', curses.color_pair(0))

            self.drawBox()
            self.writeLabel()
            self.win.refresh()
        return tmp # meaning tried to run ccall

    def check(self, ty, tx):
        if self.show == True:
            if self.y <= ty <= self.y+self.sizey-1:
                if self.x <= tx <= self.x+self.sizex-1:
                    return True
        return False

    def setLabel(self, lbl):
        self.label = lbl

    def setShow(self, tmp):
        self.show = tmp




class Buttons_manager():
    def __init__(self, stdscr, cac = True):
        self.stdscr = stdscr
        self.buttons = {}
        self.tagButtons = {}
        self.clearAfterClick = cac

    def addButton(self, starty, startx,
                  sizey, sizex, label, tag='None',
                  buttonId = 'None', show = False, boxshow=True):
        tmp = Button(starty, startx, sizey, sizex, label,
                     show = show, tag=tag, buttonId=buttonId, boxshow=boxshow)
        self.buttons[label] = tmp

    def addTagButton(self, starty, startx,
                  sizey, sizex, label, tag='None',
                  buttonId = 'None', show = False, boxshow=True):
        tmp = Button(starty, startx, sizey, sizex, label,
                     show = show, tag=tag, buttonId=buttonId, boxshow=boxshow)
        self.tagButtons[label] = tmp

    def refresh(self, ty = -1, tx = -1):
        #check Tag buttons
        tagPush = 0
        for eachtagbutton in self.tagButtons.values():
            #tmp = eachtagbutton.refresh(ty, tx)
            tmp = eachtagbutton.check(ty, tx)
            tagPush += tmp
            if tmp:
                for eachbutton in self.buttons.values():
                    eachbutton.setShow(eachbutton.tag == eachtagbutton.tag)
        if tagPush:
            if self.clearAfterClick:
                self.stdscr.clear()
                self.stdscr.refresh()
                #time.sleep(2)

        for eachtagbutton in self.tagButtons.values():
            tmp = eachtagbutton.refresh(ty, tx)
            #return


        ##############################################



        #check normal buttons
        tmp = 0
        for eachbutton in self.buttons.values():
            tmp1 = eachbutton.refresh(ty, tx)
            tmp+=tmp1
            if tmp1:
                time.sleep(.05)
                eachbutton.callback()
                return eachbutton.label


        if tmp: #i.e. clicked on button
                #we need to re-refresh
            if self.clearAfterClick:
                self.stdscr.clear()
                self.stdscr.refresh()
            self.refresh(-1, -1)
        #pass

    def setCallback(self, buttonId, callback):
        for eachbutton in self.buttons.values():
            if eachbutton.buttonId == buttonId:
                eachbutton.callback = callback
                return

    def setLabel(self, buttonId, newlabel):
        for eachbutton in self.buttons.values():
            if eachbutton.buttonId == buttonId:
                eachbutton.setLabel(newlabel)
                return

#
