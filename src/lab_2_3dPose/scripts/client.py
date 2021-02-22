#!/usr/bin/env python

from __future__ import print_function

import sys
import tf
import rospy
from lab_2_3dPose.srv import *

def euler_to_quarternion_client(a, b, c, format):
    #rospy.init_node('euler_to_quarternion_client')
    rospy.wait_for_service('euler_to_quarternion')

    try:
        convert = rospy.ServiceProxy('euler_to_quarternion', angles)
        resp1 = convert(a, b, c, format)
        return [resp1.qx, resp1.qy, resp1.qz, resp1.qw]

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":

    input_angles = [(0.00, 0.00, 0.00, "xyz"),
        (1.57, 1.57, 1.57, "xyz"),
        (1.57, 0.00, 0.00, "xyz"),
        (0.00, 1.57, 0.00, "xyz"),
        (0.00, 0.00, 1.57, "xyz"),
        (3.14, 0.00, 0.00, "xyz"),
        (0.00, 3.14, 0.00, "xyz"),
        (0.00, 0.00, 3.14, "xyz"),
        (-1.57, 0.00, 0.00, "xyz"),
        (0.00, -1.57, 0.00, "xyz"),
        (0.00, 0.00, -1.57, "xyz"),
        (1.57, 1.57, 0.00, "xyz"),
        (1.57, 0.00, 1.57, "xyz"),
        (0.00, 1.57, 1.57, "xyz"),
        (1.57, 1.57, 0.00, "yxz"),
        (0.00, 1.57, 1.57, "yxz"),
        (0.00, 1.57, 1.57, "yxz"),
        (1.57, 1.57, 0.00, "zyx"),
        (1.57, 0.00, 1.57, "zyx"),
        (0.00, 1.57, 1.57, "zyx")
            ]

    for angle in input_angles:
        a = angle[0]
        b = angle[1]
        c = angle[2]
        format = angle[3]

        print("Euler angle: \t\t %s, %s, %s, %s" %(a, b, c, format))
        result = euler_to_quarternion_client(a, b, c, format)
        print("Quaternion form: \t %s, %s, %s, %s \n" %(result[0], result[1], result[2], result[3]))