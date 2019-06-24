#!/usr/bin/python3 -u

#Version2
#with contribution from cpd73 / forum.slimdevices.com 

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject as gobject

import dbus
import dbus.mainloop.glib
import os
from subprocess import Popen

dbg = False

CONFIG_FILE='bt-devices'
SQUEEZE_LITE='/usr/bin/squeezelite'
DEVNULL = open(os.devnull, 'w')

players={}
def debug(*args):
    if dbg == True:
        print(*args)
        
def connected(hci, dev, name):
    key=dev.replace(':', '_')
    if key in players:
        return

    debug("Connected %s" % name,hci,dev)
    debug(SQUEEZE_LITE, '-o', 'bluealsa:DEV=%s,PROFILE=a2dp' % ( dev), '-n', name, '-m', dev, '-f', '/dev/null')
    players[key] = Popen([SQUEEZE_LITE, '-o', 'bluealsa:DEV=%s,PROFILE=a2dp' % ( dev), '-n', name, '-m', dev , '-f', '/dev/null'], stdout=DEVNULL, stderr=DEVNULL, shell=False)

def disconnected(dev, name):
    key=dev.replace(':', '_')
    if key not in players:
        return

    debug("Disconnected %s" % name,dev)
    players[key].kill()
    os.waitpid(players[key].pid, 0)
    players.pop(key)

def getName(dev):
    with open(CONFIG_FILE) as f:
        for line in f:
            parts=line.strip().split('=')
            if 2==len(parts) and dev==parts[0]:
                return parts[1] 
    return None

def bluealsa_handler(path, *args, **kwargs):
    """Catch all handler.
    Catch and debug information about all signals.
    """ 
    dbus_interface = kwargs['dbus_interface']
    member = kwargs['member']
    dev = None
    hci = None
    if path:
        parts=path.split('/')
        if len(parts)>=4:
            hci=parts[3]
            dev=":".join(parts[4].split('_')[1:])

    name = None
    if None!=dev and None!=hci:
        name = getName(dev)

    if None==name:
        debug("Unknown device") 
    else:
        if member == "PCMRemoved" :
            disconnected(dev, name)
        elif member == "PCMAdded" :
            connected(hci, dev, name)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    bus.add_signal_receiver(bluealsa_handler, dbus_interface="org.bluealsa.Manager1", interface_keyword='dbus_interface', member_keyword='member')

    mainloop = gobject.MainLoop()
    mainloop.run()
    