import numpy as np
import evdev

def touch_event_identifier(save = False):
    path  = '/proc/bus/input/devices'
    path1 = '~/Spectrum-Catcher-V2/touchscreen'

    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    #print(lines)


    s, devent =  None,None
    for line in lines:
        if "ADS7846 Touchscreen" in line:
            s = True
        if s:
            if "Sysfs" in line:
                tmp = int(''.join(filter(str.isdigit,line.split('/')[-1])))
                devent = '/dev/input/event{}'.format(tmp)
                #print(devent)
                break
    if save:
        f = open(path1, 'w')
        f.write(devent)
        f.close()

    return devent

#click_state = 1
tcalx = np.load('~/Spectrum-Catcher-V2/touch_calib_x.npy')
tcaly = np.load('~/Spectrum-Catcher-V2/touch_calib_y.npy')

def getTouch():
    dev = evdev.InputDevice(touch_event_identifier())
    #global tx, ty
    tx, ty = 0, 0
    for event in dev.read_loop():
        if event.type == 1:
            if event.code == 330:
                if event.value == 0:  #up
                    click_state = 1
                    charx = round(float(tcalx[0]*tx + tcalx[1]))-1
                    chary = round(float(tcaly[0]*ty + tcaly[1]))-1
                    return chary, charx
        elif event.type == 3:
            if event.code == 0:
                ty = event.value
            elif event.code == 1:
                tx = event.value
if __name__ == '__main__':
    print(touch_event_identifier(True))
