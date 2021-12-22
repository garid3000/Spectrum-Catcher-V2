import time, sys, os                # system libraries
import getopt                       # for parsing user arguments
import subprocess                   # for getting pipe-d (image data) from ffmpeg
from threading  import Thread       # parallel processing
from queue import Queue, Empty      # from reading parallel process

import numpy as np                  # data array manipulation
from PIL import Image               # for saving as bmp
import plotext as plt               # for plotting on text screen

from Custom_Lib.pyv4l2 import Py_v4l2 # for changing v4l2-ctl camera expo




longopts = ["verbose",
            "device=",           #device
            "output=",           #output directory name      ifnot nosave
            "datatype=",         #bmp,csv,npy,dat            ifnot npy
            "optimize=",         #all, no, once, normal      ifnot no optimization
            "engine=",           #ffmpeg, cv2                ifnot ffmpeg
            "number=",           #number of shots            ifnot 1
            "timer=",            #1sec between               ifnot 5 sec
            "pov=",              #number of pov divides      ifnot 1
            "show",              #show                       ifnot yes
            "optupper=",         #optimization upper         ifnot 230
            "optlower=",         #optimization upper         ifnot 100
            "nametag=",
            "help",
            "showfb"
            ]


shortopts = "vD:o:d:O:e:n:t:p:sM:m:N:hS"

argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, shortopts, longopts)
except:
    #print("Usage: python3 filename.py -o outFolder -ft bmp,csv,npy,dat -e ffmpeg")
    print("python3 spectra_text.py -s --output=some/folder/name --datatype=bmp,csv,mat,npy --optimize=normal --engine=ffmpeg --number=10 --timer=4 --nametag=testname")

alldatatypes = ['bmp', 'csv', 'npy', 'mat', 'plotpic']
v = False
outdir   = None
datatypes= ['bmp']
opt      = None
device   = '/dev/video0'
eng      = 'ffmpeg'
num      = 1
timersec = 0
pov      = 1
show     = False
optupper = 230
optlower = 100
tag      = 'shot'
showfb   = False

#print(options)
############################################################################
for name, value in options:
    if v:
        print(name, value)
        #if name in ['-v', '--verbose']:
        v = True
    elif name in ['-D', '--device']:
        if os.path.exists(value) and '/dev/video' in value:  #explicitly linux
            device = value
        else:
            print("Error: {} cam device not found".format(value))
            sys.exit(1)
    elif name in ['-o', '--output']:
        outdir = value#create that folder
        if os.path.isdir(value):
            pass
        else:
            os.makedirs(value)
    elif name in ['-d', '--datatype']:
        datatypes = [i for i in value.split(',') if i in alldatatypes]
        if v:
            print(datatypes)
        if 'mat' in datatypes:
            from scipy.io import savemat
        if 'plotpic' in datatypes:
            import matplotlib.pyplot as matplt

    elif name in ['-O', '--optimize']:
        opt = 'all'    *(value == 'all')
        opt+= 'no'     *(value == 'no')
        opt+= 'once'   *(value == 'once')
        opt+= 'normal' *(value == 'normal')
        if v:
            print(opt)
    elif name in ['-e', '--engine']:
        if value == "cv2":
            eng = 'cv2'
            try:
                import cv2
            except:
                print("Error: it seems OpenCV isn't installed")
                sys.exit(1)
        elif value == "ffmpeg":
            eng = 'ffmpeg'
        else:
            print("wrong engine specified, choose ffmpeg or cv2")
        if v:
            print(value)
    elif name in ['-n', '--number']:
        if value.isdigit():
            num = int(value)
        if v:
            print(num)
    elif name in ['-t', '--timer']:
        if value.replace('.', '', 1).isdigit():
            print(value)
            timersec = float(value)
            if timersec < 3:
                print('lower timer may results error')
        if v:
            print(timersec)
    elif name in ['-p', '--pov']:
        if value.isdigit():
            pov = int(value)
            if 0 < pov < 100:
                pass
            else:
                pov = 1
        if v:
            print('pov', pov)
    elif name in ['-s', '--show']:
        show = True #(value == 'yes')
        print('show', show)

    elif name in ['-M', '--optupper']:
        if value.isdigit():
            optupper = int(value)
        if v:
            print('optup', optupper)

    elif name in ['-m', '--optlower']:
        if value.isdigit():
            optlower = int(value)
        if v:
            print('optlow', optlower)
    elif name in ['-N', '--nametag']:
        tag = value

    elif name in ['-h', '--help']:
        if name in ['-h']:
            os.system('cat ~/Spectrum-Catcher-V2/spectra_h.txt')
        if name in ['--help']:
            os.system('cat ~/Spectrum-Catcher-V2/spectra_help.txt')
        sys.exit(0)
    elif name in ['-S', '--showfb']:
        showfb = True
        if v:
            print('optup', optupper)

##############################################################################
width = 640
height = 480
stop_threads = False

#width = 1280
#height = 720
#device = '/dev/video{}'.format(0)
if eng == 'ffmpeg':       #from ffmpeg
    command = ['ffmpeg',
               '-hide_banner',  '-loglevel', 'error',
               '-i', device, #'-i', '/dev/video2',
               '-f', 'image2pipe',
               '-pix_fmt', 'bgr24',
               '-r', '5',  #'-video_size', '1280x720', '-video_size', '480x640',
               '-vcodec', 'rawvideo',
               '-an', '-sn',
               '-' #'-map', '0',  '-', #'-map', '1',  '/dev/fb0'
               ]

    command2 = ['ffmpeg',
               '-hide_banner',  '-loglevel', 'error', #'-i', device,
               '-i', '/dev/video2',
               '-f', 'image2pipe',
               '-pix_fmt', 'bgra',
               '-r', '5', #'-video_size', '1280x720',#'-video_size', '480x640',
               '-vcodec', 'rawvideo',
               '-an', '-sn',
               '-' #'-map', '0',  '-', #'-map', '1',  '/dev/fb0'
               ]
    #p1 = subprocess.Popen(command,  stdout=subprocess.PIPE)
    #if showfb:
    #   p2 = subprocess.Popen(command2, stdout=subprocess.PIPE)
    #   p2 = subprocess.Popen(command1)


    def readFrame():
        p1.stdout.flush()
        raw_frame = p1.stdout.read(width * height * 3)
        #raw_frame, err = p1.communicate(width * height * 3)
        #frame = np.fromstring(raw_frame, np.uint8)
        frame = np.frombuffer(raw_frame, np.uint8)
        frame = frame.reshape((height, width, 3))
        #print(frame.shape, time.ctime())
        return frame

    def readFrame2():
        w = 1024
        h = 768

        raw_frame = p2.stdout.read(w * h * 4)
        #raw_frame, err = p1.communicate(width * height * 3)
        #frame = np.fromstring(raw_frame, np.uint8)
        frame = np.frombuffer(raw_frame, np.uint8)
        frame = frame.reshape((h, w, 4))
        #frame1 = frame[:480, :640, :3]
        #frame1 = frame[:480, :640, 4]
        #np.save('/home/pi/s.npy', frame[:480,:640,4])
        #print(frame.shape, time.ctime())
        return np.ascontiguousarray(frame[:480,:640,:])

    def paralel1(out, queue1):
        global stop_threads

        while 1:
            #out.flush()
            raw_frame = out.read(width * height * 3)
            frame = np.frombuffer(raw_frame, np.uint8)
            frame = frame.reshape((height, width, 3))
            queue1.put(frame)
            if stop_threads:
                break

    def paralel2(out, queue2):
        global stop_threads
        w, h = 1024, 768
        while 1:
            raw_frame = out.read(w * h * 4)
            frame = np.frombuffer(raw_frame, np.uint8)
            frame = frame.reshape((h, w, 4))
            f2 = np.ascontiguousarray(frame[:480,:640,:])
            #queue2.put(np.ascontiguousarray(frame[:480,:640,:]))
            queue2.put(f2)
            if stop_threads:
                break

            if showfb:
                with open('/dev/fb0', 'rb+') as buf:
                    buf.write(f2)

    ON_POSIX = 'posix' in sys.builtin_module_names
    p1 = subprocess.Popen(command,  stdout=subprocess.PIPE, close_fds=ON_POSIX)
    p2 = subprocess.Popen(command2, stdout=subprocess.PIPE, close_fds=ON_POSIX)

    q1 = Queue()
    q2 = Queue()

    t1 = Thread(target=paralel1, args=(p1.stdout, q1))
    t1.daemon = True # thread dies with the program
    t1.start()

    t2 = Thread(target=paralel2, args=(p2.stdout, q2))
    t2.daemon = True # thread dies with the program
    t2.start()

elif eng == 'cv2':          #from ffmpeg
    def readFrame():
        devnum = int(device.replace('/dev/video', ''))
        cap = cv2.VideoCapture(devnum)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        while 1:
            ret, frame = cap.read()
            if ret:
                return frame


v4l2 = Py_v4l2(device,
        optimize_every=3,
        upperBorder=optupper,
        lowerBorder=optlower)



if show:
    print('\033c')
    print('\x1bc')
time_init = time.time()


try:
    for iii in range(num):
        time_fori = time_init + iii * timersec
        #print(time_fori)
        #if showfb:
        #if False:
        #    f2 = q2.get(timeout=1)
        #    while 1:
        #        if q2.empty():
        #            break
        #        f2 = q2.get(timeout = 1)
        #    with open('/dev/fb0', 'rb+') as buf:
        #        #f2 = readFrame2()
        #        buf.write(f2)
        #        time.sleep(.1)

        while time.time() <= time_fori:
            #print(time.time(), time_fori, q1.qsize(), q2.qsize())
            #time.sleep(.1)
            try:
                line = q2.get(timeout = .1)
            except Empty:
                pass #print()
            else:
                pass





        #reading cam and getting spectrum
        if opt == 'no':
            #frame = readFrame()
            frame = q1.get(timeout = 1)
            segment = frame[:,250:280,0]
            spectra = np.mean(segment, axis = 1)
            segment = frame[:,350:380,0]
            spectra1 = np.mean(segment, axis = 1)


        elif opt == 'all':
            while 1:
                #frame = readFrame()
                frame = q1.get(timeout = 1)
                segment = frame[:,250:280,0]
                spectra = np.mean(segment, axis = 1)
                segment = frame[:,350:380,0]
                spectra1 = np.mean(segment, axis = 1)

                # get max data
                m = max(np.max(spectra),
                        np.max(spectra1))
                state = v4l2.optimize_expo(m)
                if state == 'steady':
                    break
                elif state == 'max':
                    break
                elif state == 'min':
                    break
        elif opt == 'once':
            while 1:
                #frame = readFrame()
                frame = q1.get(timeout = 1)
                segment = frame[:,250:280,0]
                spectra = np.mean(segment, axis = 1)
                segment = frame[:,350:380,0]
                spectra1 = np.mean(segment, axis = 1)

                # get max data
                m = max(np.max(spectra),
                        np.max(spectra1))
                state = v4l2.optimize_expo(m)
                if state == 'steady':
                    break
                elif state == 'max':
                    break
                elif state == 'min':
                    break
            opt = 'no'  #after once, no optimization on next loop
        elif opt == 'normal':
            #frame = readFrame()
            frame = q1.get(timeout = 1)
            segment = frame[:,250:280,0]
            spectra = np.mean(segment, axis = 1)
            segment = frame[:,350:380,0]
            spectra1 = np.mean(segment, axis = 1)
            m = max(np.max(spectra),
                    np.max(spectra1))
            state = v4l2.optimize_expo(m)




        #plotting
        if show:
            plt.clf()
            plt.ylim(0, 255)
            plt.plotsize(75, 25)
            plt.colorless()
            plt.ylabel("Digital Val")
            plt.xlabel("Wavelength")
            #    plt.cld()
            plt.plot(spectra , label="POV", marker='big')
            plt.plot(spectra1, label="REF", marker='big')
            plt.title("({} of {})   Exposure {}, Gain:{}, Spectrum:".format(
                iii+1, num,
                v4l2.possible_expos[v4l2.expo_i],
                v4l2.gain))
            #print('\033c')
            #print('\x1bc')
            print("\033[%d;%dH" % (0, 0))
            plt.show()
            #time.sleep(1)



        # saving
        fnametag = '{}/{}_{:04d}_s{:05d}'.format(outdir, tag, iii+1, int(time.time() - time_init))
        if outdir != None: #meaning it should save
            #if 'jpg' in datatypes:
            #    im = Image.fromarray(f2)
            #    im.save('{}.jpg'.format(fnametag))
            if 'bmp' in datatypes:
                im = Image.fromarray(frame)
                im.save('{}.bmp'.format(fnametag))
            if 'npy' in datatypes:
                np.save('{}.npy'.format(fnametag), frame)

            if 'mat' in datatypes:
                savingDict = {  'pov':spectra,
                                'ref':spectra1,
                             }
                savemat('{}.mat'.format(fnametag),
                        savingDict)
            if 'csv' in datatypes:
                savingArray = np.empty((480, 2), dtype='uint8')
                savingArray[:,0] = spectra
                savingArray[:,1] = spectra1
                np.savetxt('{}.csv'.format(fnametag),
                        savingArray, delimiter = ',', header='POV,REF', comments=''
                        )
                if 'plotpic' in datatypes:
                    os.system('gnuplot -e \"ifname=\'{}.csv\'\" -e \"ofname=\'{}.png\'\" plotpic.gp'.format(fnametag,fnametag))

                # matplotlib took wayyy tooo much CPU resources, till 100%
                #matplt.clf()
                #matplt.plot(spectra , label='POV')
                #matplt.plot(spectra1, label='REF')
                #matplt.ylabel("Digital Val")
                #matplt.ylim(0, 255)
                #matplt.xlabel("Wavelength")
                #matplt.title("({} of {})   Exposure {}, Gain:{}, Spectrum:".format(
                #    iii+1, num,
                #    v4l2.possible_expos[v4l2.expo_i],
                #    v4l2.gain))
                #matplt.legend()
                #matplt.savefig('{}.png'.format(fnametag))





except KeyboardInterrupt:
    print("User exitted, via ctl+v")

#except:
#    print("Error: unknown error in main loop")


if eng == 'ffmpeg':
    stop_threads = True
    time.sleep(1)
    #p1.terminate()

    #p2.terminate()
    p1.kill()
    p2.kill()
    #p2.kill()
    time.sleep(1)

##################################################
