import cv2
import numpy as np
import subprocess


width = 640
height = 480


command = ['ffmpeg',
           #'-rtsp_flags', 'listen',  # The "listening" feature is not working (probably because the stream is from the web)
           #'-rtsp_transport', 'tcp',  # Force TCP (for testing)
           #'-max_delay', '30000000',  # 30 seconds (sometimes needed because the stream is from the web).
           #'-i', in_stream,
           '-i', '/dev/video0',
           '-f', 'image2pipe',
           '-pix_fmt', 'bgr24',
           #'-framerate', '10',
           #'-video_size', '640x480',
           '-vcodec', 'rawvideo', '-an', '-'
           ]
           #'-vcodec', 'rawvideo', '-an', '-']

# Open sub-process that gets in_stream as input and uses stdout as an output PIPE.
p1 = subprocess.Popen(command, stdout=subprocess.PIPE)


while True:
    # read width*height*3 bytes from stdout (1 frame)
    raw_frame = p1.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # Convert the bytes read into a NumPy array, and reshape it to video frame dimensions
    frame = np.fromstring(raw_frame, np.uint8)
    frame = frame.reshape((height, width, 3))

    # Show video frame
    cv2.imshow('image', frame)
    cv2.waitKey(1)

# Wait one more second and terminate the sub-process
try:
    p1.wait(1)
except (sp.TimeoutExpired):
    p1.terminate()

cv2.destroyAllWindows()
