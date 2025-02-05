# Raspberry Pi Zero

### Router

**Plug the router into LAN2**

After turning on the router, the Raspberry Pi Zero should connect to the `smartbears` SSID. This may take 5-10 minutes. 

To check all devices on the network, connect to the wifi on your device, and go to the following link: http://192.168.1.1/status-devices.asp

### SSH

To ssh into the Raspberry Pi Zero:

```
ssh pi@192.168.1.142
```

You may get this error:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
```

If so, try running:

```
ssh-keygen -R 192.168.1.142
```

Then, try to ssh into the pi again.

### PiCam

After running `picam.py`, you should be able to see the live feed from the PiCam at: http://192.168.1.142:5000/video_feed


### Video Stream Communcation 

Run `camera_stream_client` on the raspberry Pi

Run `camera_stream_server` on your computer
