#!/usr/bin/env python

from __future__ import print_function

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import traceback
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from rospy import get_param, init_node, Publisher
import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
    'i':(1,0,0,0),
    'o':(1,0,0,-1),
    'j':(0,0,0,1),
    'l':(0,0,0,-1),
    'u':(1,0,0,1),
    ',':(-1,0,0,0),
    '.':(-1,0,0,1),
    'm':(-1,0,0,-1),
    'O':(1,-1,0,0),
    'I':(1,0,0,0),
    'J':(0,1,0,0),
    'L':(0,-1,0,0),
    'U':(1,1,0,0),
    '<':(-1,0,0,0),
    '>':(-1,-1,0,0),
    'M':(-1,1,0,0),
    't':(0,0,1,0),
    'b':(0,0,-1,0),
}

resetBindings={
    'a': None,
    's': None,
    'd': None
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    pub = Publisher('cmd_vel', Twist, queue_size = 1)
    init_node('teleop_twist_keyboard')
    ns = "~"
    p_speed = get_param(ns + "speed_factor", 0.1)
    p_turn = get_param(ns + "turn_factor", 0.1)
    max_speed = get_param(ns + "max_speed", 1.0)
    min_speed = get_param(ns + "min_speed", -max_speed)
    max_turn = get_param(ns + "max_turn", 1.0)
    min_turn = get_param(ns + "min_turn", -max_turn)
    x = 1; y = 0; z = 0
    th = 1; status = 0
    speed = 0.0; turn = 0.0
    try:
        print(msg)
        print(vels(speed,turn))
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                speed += ((moveBindings[key][0] * max_speed) - speed) * p_speed
                speed = np.clip(
                    speed,
                    min_speed,
                    max_speed
                )
                turn += ((moveBindings[key][3] * max_turn) - turn) * p_turn
                turn = np.clip(
                    turn,
                    min_turn,
                    max_turn
                )
                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15 
            else:
                speed, turn = 0,0
                if (key == '\x03'):
                    break

            twist = Twist()
            twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
            pub.publish(twist)

    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
