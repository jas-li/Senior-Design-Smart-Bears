# Senior-Design-Smart-Bears

### Team 29 - Smart Bears
Shamir Legaspi\
David Li\
Jason Li\
Lukas Chin\
Jake Lee

## Smart System for the Visually Impaired

![Smart_System](./images/smart_system.png)

## Objective

The goal of the Smart System for Visually Impaired is to improve its users’ abilities to navigate safely. 

The first way it achieves this goal is by providing users with more visual context about their surroundings through other mediums. Visual context is transformed into text descriptions in audio and semantic haptic feedback. 

A binary assessment of whether the current surroundings are navigationally safe or unsafe is quickly transmitted to the user through haptic feedback. This way, users can quickly make a decision to not proceed before knowing the full description of their surroundings which would take much longer to propagate than a simple buzzing signal. 

The system also illuminates the user’s wrist in dark light conditions. Though this does not directly help the user navigate, it helps others navigate around the user. 

In its current state, the system achieves all of these goals, but its performance in terms of latency, accuracy, and over helpfulness can always be improved. Each aspect of the system comes with a few things to keep in mind while developing them.

## Overview
* Stereo vision-based depth mapping and object recognition
* Real-time haptic (vibration) and auditory (speech) feedback
* One-button user interface on wrist-wearable
* Intelligent visibility system (LEDs for low-light)
* Wireless connectivity (WiFi and Bluetooth)
* Designed for expandability and compliance with accessibility and safety standards

## Quick Start

### Hardware Setup
1. Mount Cameras:
Attach the dual USB stereo cameras to the Smart Cap and connect to the Raspberry Pi’s USB ports.

2. Raspberry Pi:
Place the Raspberry Pi 5 in a weather-protected case. Power it with a 5V portable battery.

3. Wrist-Wearable:
Secure the wrist module to the user’s wrist, ensuring the photoresistor is unobstructed and the button is accessible.

4. Networking:
Connect both the ESP32 (in the wrist-wearable) and the Raspberry Pi to the same WiFi network.

5. Audio Output:
Pair the bone conduction headset to the Raspberry Pi via Bluetooth.

### Software Setup
1. Access Raspberry Pi:
SSH into the Pi or use a monitor and keyboard.

2. Project Directory:
Navigate to the project root directory.

3. Run Main Script:
Execute pi.py to start the main pipeline (waits for wrist-wearable trigger, handles image capture, depth mapping, LLM query, and feedback).

4. ESP32 Firmware:
Ensure the ESP32 is flashed with the provided firmware and has open UDP ports.
Run esp.py to handle communication for the buzzer and LEDs.

5. System Test:
Press the wrist-wearable button to initiate a query.
Confirm system activation by checking for audio (speech) and haptic (vibration) feedback.
### Operation
* Normal Use:
The user points their head, presses the wrist button, and receives a spoken description of the environment plus haptic alerts for nearby obstacles. LEDs activate in low-light conditions.
* Troubleshooting:
If feedback is missing, check WiFi/Bluetooth connections.
Restart ESP32 or Raspberry Pi if communication is lost.
For persistent issues, review setup logs and ensure all scripts are running.
### System Architecture
* Smart Cap:
Dual 2MP USB cameras, Raspberry Pi 5 (16GB RAM), portable battery, wireless connectivity.
* Wrist-Wearable:
ESP32 microcontroller, vibration motor, button, LEDs, photoresistor, adjustable strap.
* Audio Output:
Bone conduction Bluetooth headset.
* Communication:
UDP over WiFi (ESP32 ↔ Raspberry Pi)
Bluetooth audio (Raspberry Pi ↔ headset)

## Network
- We are currently using a router to connect to the Raspberry Pi 5 and the TinyPICO ESP 32.
  - SSID: `smartbears`
  - Password: ` `

## Raspberry Pi

We utilized a combiantion of SSH + RealVNC Viewer for faster development. To do so connect to the Pi at `192.168.1.141`
- user: `pi`
- password: `smartbears`


### Bluetooth

We have set up a bluetooth device to enable speaker output to the wireless headset.

To set up bluetooth with the Raspberry Pi, run `sudo bluetoothctl` to start the bluetooth control tool.

Find your device and its respective address. Then, pair and trust the bluetooth device:

```
pair 41:42:D4:02:07:00
trust 41:42:D4:02:07:00
```

You can now exit bluetoothctl with `exit`. You only need to do this once.

Run this command any time you want to reconnect the headset:
```
bluetoothctl connect 41:42:D4:02:07:00
```

## Final Hardware Diagram
![Smart System Diagram](./images/Smart_System_Diagram.png)


