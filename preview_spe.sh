#rm ~/spe.bmp
#rm ~/cam.bmp
#ffmpeg -hide_banner -loglevel error -i /dev/video2 -t 3 -vf drawbox=200:200:300:300 -pix_fmt bgra -f fbdev /dev/fb0
ffmpeg -hide_banner -loglevel error -i /dev/video0 -t 3 -pix_fmt bgra -f fbdev /dev/fb0

#ffmpeg -hide_banner -loglevel error -f video4linux2 -i /dev/video0 -vframes 1 ~/spe.bmp
#ffmpeg -hide_banner -loglevel error -f video4linux2 -i /dev/video2 -vframes 1 ~/cam.bmp
#printf '[3J'
clear
