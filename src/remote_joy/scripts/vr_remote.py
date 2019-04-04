#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Header
from rospy import get_param, Time, logdebug, loginfo
# from rospy.
# from genpy.message import 
from evdev import InputDevice, categorize, ecodes

# key_map = {
#     115: "FRWD",
#     114: "BKWD",
#     165: "LEFT",
#     163: "RIGHT",
#     164: "BTN_A",
#     304: "SUPER_UP",
#     305: "SUPER_DOWN",
# }

key_map = {
    115: 10,
    114: 11,
    165: 12,
    163: 13,
    164: 0,
    304: 5,
    305: 4,
}

class VRRemote(object):
    NS = "~"
    def __init__(self ,nh=None):
        topic = get_param(self.NS + "joy_topic", "joy")
        self._axes_count = get_param(self.NS + "axes_count",0)
        self._button_count = get_param(self.NS + "button_count",15)
        device = get_param(self.NS + "device_path", "/dev/input/event2")
        self._pub = rospy.Publisher(topic, Joy, queue_size=10)

        self._device = InputDevice(device)
        loginfo("Device : {}".format(self._device))
    
    def publish(self, active_keys):
        logdebug("Publishing!")
        # in_event = self._device.read_one()
        # while in_event is None:
        # #     rospy.sleep(0.1)
        #     in_event = self._device.read_one()
        #     if in_event is None:
        #         continue
        #     if in_event.type == ecodes.EV_KEY:
        #         break
        #     else:
        #         in_event = None
        # if in_event is None:
        #     return
        # if in_event.type == ecodes.EV_KEY:
        msg = Joy(header=Header(stamp=Time.now()))
        msg.axes = [0.0] * self._axes_count
        msg.buttons = [0] * self._button_count
        # active_keys = self._device.active_keys(verbose=False)
        loginfo("active_keys : {}".format(active_keys))
        for k in active_keys:
            msg.buttons[key_map[k]] = 1
        loginfo("msg.buttons : {}".format(msg.buttons))
        self._pub.publish(msg)
            

def main():
    rospy.init_node('vr_remote', anonymous=False)
    nh = None
    vr_remote = VRRemote(nh)
    if nh is not None:
            vr_remote.NS = nh + "/"
    # rate_freq = get_param(vr_remote.NS + "publish_rate", 10)
    # rate = rospy.Rate(rate_freq) # 10hz
    for in_event in vr_remote._device.read_loop():
        if in_event.type == ecodes.EV_KEY:
            vr_remote.publish(vr_remote._device.active_keys(verbose=False))
        if rospy.is_shutdown():
            break
        # rate.sleep()
    
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass