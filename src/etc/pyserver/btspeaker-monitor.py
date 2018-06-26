#!/usr/bin/python3 -u

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject as gobject

import dbus
import dbus.mainloop.glib
import os

dbg = False

def debug(*args):
    if dbg == True:
        print(*args)
        
def connected():
    print("Connected")
    os.system("sudo /etc/init.d/squeezelite restart")

def disconnected():
    print("Disconnected")
    os.system("sudo /etc/init.d/squeezelite stop")

def catchall_handler(name, attr, *args, **kwargs):
    """Catch all handler.
    Catch and debug information about all singals.
    """
    debug('---- Caught signal ----')
    debug('name:', name)
    debug('kwargs:', len(kwargs))
    for key,val in kwargs.items():
        debug("* {} = {}".format(key, val))

    debug("\n")
    debug('Arguments:')
    for arg in args:
        debug('* %s ' % (str(arg)))

    debug("\n")
    if name != "org.bluez.MediaControl1" :
        return
    debug("attr[Connected]=",attr["Connected"])
    if attr["Connected"] == 0 :
        disconnected()
    if attr["Connected"] == 1 :
        connected()

if __name__ == '__main__':
    
   
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    bus.add_signal_receiver(catchall_handler, bus_name="org.bluez", interface_keyword='dbus_interface', member_keyword='member', path_keyword='path')

    mainloop = gobject.MainLoop()
    mainloop.run()
    
