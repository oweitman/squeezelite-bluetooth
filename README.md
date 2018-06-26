# squeeze-bluetooth

The following steps describes how to connect a bluetooth-speaker to a Raspberry Pi 3B+ 
and a squeezelight player.
The bluetooth-speaker should automaticly connect to the headless raspberry pi and squeezelite should play
music without touching the raspberry pi.

One Poblem was, if the BT-speaker disconnects, squeezelite didnt recognize this, create errors and the service stops.
Another problem was the automaticly reconnection of the BT-speaker.

This guide describe the sound-output for alsa. I have previously tried it unsuccessfully with pulseaudio.

##Basic installation part

1. Check/Install Bluetooth on the raspberry

```bash
sudo apt-get install pi-bluetooth
```

2. Check/Install squeezelite on the squeezelite

```bash
sudo apt-get install pi-squeezelite
```

Normaly you get here an older version. After installation you can download an replace (/usr/bin/squeezelite) the squeezelite executable from the author of squeezelite
[Sourceforge squeezelite/Linux](https://sourceforge.net/projects/lmsclients/files/squeezelite/linux/)

3. Install dbus-python libraries for python3
This library is used to track the connection-status of a BT-speaker. 

```bash
sudo pip3 install dbus-python
```

if the installation of dbus-python fails in case of missing DBUS-1 then you have to unstall another library and try again

```bash
sudo apt-get install libdbus-glib-1-dev
```

4. reboot your raspberry

5. copy the following files to your filesystem

```bash
/etc/asound.conf
/etc/pyserver/btspeaker-monitor.py
/etc/systemd/system/btspeaker-monitor.service
```

6. change owner of files to root

```bash
sudo chown root:root /etc/asound.conf
sudo chown root:root /etc/pyserver/btspeaker-monitor.py
sudo chown root:root /etc/systemd/system/btspeaker-monitor.service
```

7. change execution flag

```bash
sudo chmod +x /etc/pyserver/btspeaker-monitor.py
```

8. enable the btspeaker-monitor.service

```bash
sudo systemctl daemon-reload
sudo systemctl enable btspeaker-monitor.service
sudo systemctl start btspeaker-monitor.service
```

---
##Connect and register your BT-speaker for the first time

1. Turn on your BT-speaker, change to pairing-mode and start the bluetooth-utility

```bash
sudo bluetoothctl 
```

```bash
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
```

After that new recognized devices are listed. maybe you have to wait some time. if not check the pairing mode of your device.
If your BT-speaker is listet, note the Device-ID as follows 00:00:00:00:00:00
Then you register your device. all 00:00:00:00:00:00 pleas replace with your device id

```bash
[bluetooth]# scan off
[bluetooth]# pair 00:00:00:00:00:00
[bluetooth]# trus 00:00:00:00:00:00
[bluetooth]# connect 00:00:00:00:00:00
[bluetooth]# exit
```
if there was no error, your device is now connected, trusted and can connected next time without interaction

2. connect the alsa-sound-system to your BT-speaker
Edit the following asound.conf and rerplace 00:00:00:00:00:00 with your device id of the BT-speaker

```bash
sudo nano /etc/asound.conf
```
and restart the alsa-sound-system

```bash
sudo alsactl restore
```

3. reboot your raspberry
