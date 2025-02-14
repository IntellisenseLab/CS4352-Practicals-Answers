#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
import time

from open_manipulator_msgs.srv import *
from open_manipulator_msgs.msg import *

def move_in_joint_space(joint1, joint2, joint3, joint4, path_time):

    rospy.wait_for_service('goal_joint_space_path_custom')

    try:
        setJointPath = rospy.ServiceProxy('goal_joint_space_path_custom', SetJointPosition)

        request =  SetJointPositionRequest()

        request.joint_position.joint_name = ["joint1", "joint2", "joint3", "joint4"]
        request.joint_position.position = [joint1, joint2, joint3, joint4]
        request.path_time = path_time

        response = setJointPath(request)

        return response.is_planned

    except rospy.ServiceException as e:

        print("Service call failed: %s"%e)

def activate_actuators(state):

    rospy.wait_for_service('set_actuator_state')

    try:

        activate = rospy.ServiceProxy('set_actuator_state', SetActuatorState)
        
        srv = SetActuatorStateRequest()

        srv.set_actuator_state = state

        response =  activate(srv)

        return response.is_planned

    except rospy.ServiceException as e:

        print("Service call failed: %s"%e)

if __name__ == "__main__":

    positions = [[0,0,0,0,5], [-0.2,0,0,0,5], [-0.2,0.4,0,0,5], [0.2,-0.2,-0.4,0,5], [-0.4,0.2,0.2,0.2,5]]
    for i, pos in enumerate(positions):

        if activate_actuators(True):
            print("Activation completed")
        else:
            print("Activation failed")

        if move_in_joint_space(pos[0], pos[1], pos[2], pos[3], pos[4]):
            print("Successfully moved")
        else:
            print("Failed to move")

        time.sleep(6.0)

        if activate_actuators(False):
            print("Deactivation completed")
        else:
            print("Deactivation failed")