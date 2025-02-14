#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
import time
import numpy as np

from open_manipulator_msgs.srv import *
from open_manipulator_msgs.msg import *
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

a1= 0
b1= 0
c1= 0
d1= 0
e1= 0
f1= 0
a2= 0
b2= 0
c2= 0
d2= 0
e2= 0
f2= 0
a3= 0
b3= 0
c3= 0
d3= 0
e3= 0
f3= 0
a4= 0
b4= 0
c4= 0
d4= 0
e4= 0
f4= 0

cjoint1=0
cjoint2=0 
cjoint3=0 
cjoint4=0

timePlan = 0
planned = False

def callback(msg):
    global cjoint1, cjoint2, cjoint3, cjoint4

    nameArray = msg.name
    posiArray = msg.position

    for posi in range(len(nameArray)):
        if nameArray[posi] == "joint1":
            cjoint1 = posiArray[posi]

        if nameArray[posi] == "joint2":
            cjoint2 = posiArray[posi]

        if nameArray[posi] == "joint3":
            cjoint3 = posiArray[posi]

        if nameArray[posi] == "joint4":
            cjoint4 = posiArray[posi]


def calculatePath(startPos, endPos, startVec, endVec, startAcc, endAcc, time):

    #
    # Assuming y=m.x shape fr matrix for solving quintic polynomial
    #

    matY = np.array([[startPos], [endPos], [startVec], [endVec], [startAcc], [endAcc]])
    matM = np.array([[           0,            0,          0,            0,       0,      1], 
                     [     time**5,      time**4,    time**3,      time**2, time**1,      1], 
                     [           0,            0,          0,            0,       1,      0], 
                     [ 5*(time**4),  4*(time**3), 3*(time**2), 2*(time**1),       1,      0], 
                     [           0,            0,          0,            2,       0,      0], 
                     [20*(time**3), 12*(time**2), 6*(time**1),           2,       0,      0]])
    #
    # y = m.x
    # inv(m).y = inv(m).m.x
    # inv(m).y = x
    #

    matX = np.matmul(np.linalg.inv(matM), matY)

    return matX[0][0], matX[1][0], matX[2][0], matX[3][0], matX[4][0], matX[5][0]

def calculateTrajectory(request):
    global a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, a3, b3, c3, d3, e3, f3, a4, b4, c4, d4, e4, f4, planned
    global cjoint1, cjoint2, cjoint3, cjoint4
    global timePlan

    tjoint1=0
    tjoint2=0 
    tjoint3=0 
    tjoint4=0

    nameArray = request.joint_position.joint_name
    posiArray = request.joint_position.position
    timePlan = request.path_time

    for posi in range(len(nameArray)):
        if nameArray[posi] == "joint1":
            tjoint1 = posiArray[posi]

        if nameArray[posi] == "joint2":
            tjoint2 = posiArray[posi]

        if nameArray[posi] == "joint3":
            tjoint3 = posiArray[posi]

        if nameArray[posi] == "joint4":
            tjoint4 = posiArray[posi]
    
    a1, b1, c1, d1, e1, f1  = calculatePath(cjoint1, tjoint1, 0, 0, 0, 0, timePlan)
    a2, b2, c2, d2, e2, f2  = calculatePath(cjoint2, tjoint2, 0, 0, 0, 0, timePlan)
    a3, b3, c3, d3, e3, f3  = calculatePath(cjoint3, tjoint3, 0, 0, 0, 0, timePlan)
    a4, b4, c4, d4, e4, f4  = calculatePath(cjoint4, tjoint4, 0, 0, 0, 0, timePlan)

    print("\npolynomial coefficients")
    print(a1,"t^5 +\n", b1,"t^4 +\n", c1,"t^3 +\n", d1,"t^2 +\n", e1,"t +\n", f1)
    print(a2,"t^5 +\n", b2,"t^4 +\n", c2,"t^3 +\n", d2,"t^2 +\n", e2,"t +\n", f2)
    print(a3,"t^5 +\n", b3,"t^4 +\n", c3,"t^3 +\n", d3,"t^2 +\n", e3,"t +\n", f3)
    print(a4,"t^5 +\n", b4,"t^4 +\n", c4,"t^3 +\n", d4,"t^2 +\n", e4,"t +\n", f4)

    planned = True

    return SetJointPositionResponse(planned)


rospy.init_node('jointSpaceControllerServer')

server = rospy.Service('goal_joint_space_path_custom', SetJointPosition, calculateTrajectory)

j1_pub = rospy.Publisher('joint1_position/command', Float64, queue_size=1)
j2_pub = rospy.Publisher('joint2_position/command', Float64, queue_size=1)
j3_pub = rospy.Publisher('joint3_position/command', Float64, queue_size=1)
j4_pub = rospy.Publisher('joint4_position/command', Float64, queue_size=1)

jo_sub = rospy.Subscriber('joint_states', JointState, callback)
    
rate = rospy.Rate(100)
    
while not rospy.is_shutdown():
    timeStr = time.time()
    timeEnd = timeStr + timePlan

    while (planned and (timeEnd >= time.time())):
        t = time.time() - timeStr
        
        j1_pub.publish(a1*(t**5) + b1*(t**4) + c1*(t**3) + d1*(t**2) + e1*t + f1)
        j2_pub.publish(a2*(t**5) + b2*(t**4) + c2*(t**3) + d2*(t**2) + e2*t + f2)
        j3_pub.publish(a3*(t**5) + b3*(t**4) + c3*(t**3) + d3*(t**2) + e3*t + f3)
        j4_pub.publish(a4*(t**5) + b4*(t**4) + c4*(t**3) + d4*(t**2) + e4*t + f4)

        rate.sleep()
    
    planned = False