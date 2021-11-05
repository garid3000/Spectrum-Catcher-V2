#import time
#import numpy as np
#import cv2
#
#cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

import numpy as np
import subprocess
import time
import plotext as plt
#import curses


width = 640
height = 480

command = ['ffmpeg',
           '-hide_banner',
           '-loglevel', 'quiet',
           '-i', '/dev/video0',
           '-f', 'image2pipe',
           '-pix_fmt', 'bgr24',
           '-r', '1',
           #'-pix_fmt', 'yuv420p',
           #'-framerate', '10',
           #'-video_size', '640x480',
           '-vcodec', 'rawvideo', '-an', '-']

p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
count = 1
try:
    while 1:
    #for i in range(100):
        #ret, frame = cap.read()
        raw_frame = p1.stdout.read(width*height*3)
        #print(len(raw_frame))

        if len(raw_frame) == (width*height*3):# i.e. ret
            #print('fooog')
            #break
            frame = np.fromstring(raw_frame, np.uint8)
            frame = frame.reshape((height, width, 3))

            #print(frame.shape)
            #if ret:
            segment = frame[:,250:280,0]
            spectra = np.mean(segment, axis = 1)
            segment = frame[:,350:380,0]
            spectra1 = np.mean(segment, axis = 1)
            plt.clf()
            plt.ylim(0, 255)
            tmp = "\033[%d;%dH" % (0, 0)

            print(tmp)
            print(count)
            plt.plotsize(75, 25)
            #plt.canvas_color("none")
            #plt.axes_color("none")
            #plt.ticks_color("white")
            plt.colorless()
            #plt.plot(spectra)
            #plt.plot(spectra1)
            plt.scatter(spectra , marker="small")
            plt.scatter(spectra1, marker="small")
            #plt.show()
            plt.show(hide=1)
            canvas = plt.get_canvas()

            count -=1
            if count<0:
                break


except KeyboardInterrupt:
    print('ending')
    pass


#p1.stdout.close()
#el p1
 #


p1.send_signal(subprocess.signal.SIGINT)
