# squeezelite-bluetooth

The following steps describes how to connect a bluetooth-speaker to a ***Raspberry Pi 3B+ and a squeezelight player***.
The bluetooth-speaker should automaticly connect to the headless raspberry pi and squeezelite should play
music without touching the raspberry pi.

One Problem was, if the BT-speaker disconnects, squeezelite didnt recognize this, create errors and the service stops.
Another problem was the automaticly reconnection of the BT-speaker. In this solution i created a service to track the connection state of bluetooth-speaker devices and start/stop the squeezelite service.

This guide describe the sound-output for alsa. I have previously tried it unsuccessfully with pulseaudio.

The 2.version of this guide was enhanced with input from 
* cpd73 forum.slimdevices.com
* paul- forum.slimdevices.com
The 3. version of this guide was improved with input from
* Eric https://github.com/coissac

## Basic installation part

### 1. Check/Install Bluetooth on the raspberry

```bash
sudo apt-get install pi-bluetooth
```

### 2. Check/Install squeezelite on the squeezelite

```bash
sudo apt-get install squeezelite
```
Normaly you get here an older version. After installation you can download an replace (/usr/bin/squeezelite) the squeezelite executable from the author of squeezelite
[Sourceforge squeezelite/Linux](https://sourceforge.net/projects/lmsclients/files/squeezelite/linux/). For raspberry use the arm6f-archives

### 3. Build and install bluez-alsa
This library is used for the transport of sound-data from bluetooth to the alsa sound-system

Install dependencies
```bash
sudo apt-get update
sudo apt-get install -y libasound2-dev dh-autoreconf libortp-dev \
          bluez pi-bluetooth bluez-tools libbluetooth-dev \
          libusb-dev libglib2.0-dev libudev-dev libical-dev \
          libreadline-dev libsbc1 libsbc-dev \
          libdbus-glib-1-dev python3-pip
```

Download and build the library
```bash
cd ~
git clone https://github.com/Arkq/bluez-alsa.git
cd bluez-alsa
autoreconf --install
mkdir build && cd build
../configure --disable-hcitop --with-alsaplugindir=/usr/lib/arm-linux-gnueabihf/alsa-lib
make && sudo make install
```

### 4. Install dbus-python libraries for python3
This library is used to track the connection-status of a BT-speaker and start/stop the squeezelite service. 

```bash
sudo pip3 install dbus-python
```

if the installation of dbus-python fails in case of missing DBUS-1, then you have to install the following library and try again

```bash
sudo apt-get install libdbus-glib-1-dev
```

### 5. reboot your raspberry

### 6. copy the following files (from /src of this git) to your filesystem

```bash
/etc/pyserver/btspeaker-monitor.py
/etc/pyserver/bt-devices
/etc/systemd/system/btspeaker-monitor.service
/etc/systemd/system/bluezalsa.service
```

### 7. change owner of files to root and create a user lms and add user to group

```bash
adduser --disabled-login \
        --no-create-home \
        --system  lms
```

```bash
addgroup lms audio
```


```bash
sudo chown root:root /etc/pyserver/btspeaker-monitor.py
sudo chown root:root /etc/pyserver/bt-devices
sudo chown root:root /etc/systemd/system/btspeaker-monitor.service
sudo chown root:root /etc/systemd/system/bluezalsa.service
```

### 8. change execution flag

```bash
sudo chmod +x /etc/pyserver/btspeaker-monitor.py
```

### 9. enable the services

```bash
sudo systemctl daemon-reload
sudo systemctl enable bluezalsa.service
sudo systemctl enable btspeaker-monitor.service
sudo systemctl start bluezalsa.service
sudo systemctl start btspeaker-monitor.service
```

---

## Connect and register your BT-speaker for the first time

### 1. Turn on your BT-speaker, change to pairing-mode and start the bluetooth-utility

```bash
sudo bluetoothctl 
```

```bash
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
```

After that new recognized devices are listed, you maybe have to wait some time. if your devices is not recognized, then check the pairing mode of your device.
If your BT-speaker is listed, note the Device-ID as follows 00:00:00:00:00:00
Then you register your device. please replace all 00:00:00:00:00:00 with your device id

```bash
[bluetooth]# scan off
[bluetooth]# pair 00:00:00:00:00:00
[bluetooth]# trust 00:00:00:00:00:00
[bluetooth]# connect 00:00:00:00:00:00
[bluetooth]# exit
```
if there was no error, your device is now connected, trusted and can connect next time without interaction

### 2. register your BT-speaker and define a nice name
Edit the following bt-devices and replace 00:00:00:00:00:00 with your device id of the BT-speaker and
define a nice name after the equal sign. if you have more BT-speaker add more rows

```bash
sudo nano /etc/pyserver/bt-devices
```

### 3. reboot your raspberry

---

## Normal use

### 1. Turn BT-speaker on

The squeezelite can be seen in the LMS-server.
If the player is in a synchonized group the music starts playing.
if this didnt happen then turn the BT-speaker off and enable again 

### 2. Turn BT-speaker off

The squeezelite-player disappears in the LMS-server.
Wait up to one minute to turn the BT-speaker again.
the squeezelite-service needs some time to stop


