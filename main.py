"""
Waits for the Phidget InterfaceKit 8/8/8 to be attached.
Once attached, a sensor changed event handler is further attached,
and on change, the system volume is set to a percentage of that
value. On any input, the program is closed.
"""
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.InterfaceKit import InterfaceKit
import subprocess

def run():  
    kit = InterfaceKit()
    try:
        try:
            kit.openPhidget()
            kit.setOnAttachHandler(attached)
            kit.setOnDetachHandler(detached)
            if not kit.isAttached():
                print "Please attach the interface kit!"
            raw_input()
        except PhidgetException as e:
            print ("Phidget exception %i: %s" % (e.code,e.detail))
    except RuntimeError as e:
        print ("Runtime error: %s" % e.message)
    except Exception as e:
        print ("Unknown error: %s" % (e.message))
        
    stop(kit)
 
def stop(kit):
    kit.closePhidget()
 
def attached(e):
    kit = e.device
    print ("Attached to interface kit %s" % (kit.getSerialNum()))    
    kit.setOnSensorChangeHandler(sensor_changed)
    print "Listening for changes... press any key to quit."
    
def detached(e):
    stop(e.device)
            
def sensor_changed(e):
    """
    Expects a phidget 60mm slider sensor, and uses its value as a
    percentage to set the system volume. 
    Requires nircmd.exe (http://www.nirsoft.net/utils/nircmd.html).
    """
    if e.index == 0:
        SYS_VOL_MAX = 65535
        val_pcnt = e.value / float(1000)
        sys_vol = SYS_VOL_MAX * val_pcnt
        print ("Adjusting system volume to %%%i" % (val_pcnt*100))
        subprocess.call(["nircmd.exe","setsysvolume","%i"%(sys_vol)])
    
if __name__ == "__main__":
    run()