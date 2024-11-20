Run this command on the Raspberry Pi to start the GStreamer pipeline that sends the video stream to the browser:

libcamera-vid -t 0 -n --width 1280 --height 720 --framerate 25 --bitrate 2000000 --codec h264 -o - | \
gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! \
udpsink host=127.0.0.1 port=5000
