#!/usr/bin/env python

from __future__ import print_function

import rospy 
import tf
import time

from open_manipulator_msgs.srv import *
from open_manipulator_msgs.msg import *

kinematics_pose = KinematicsPose()

def callback(data):
    kinematics_pose = data.pose    

def move_in_task_space(x, y, z, path_time):

    rospy.wait_for_service('goal_task_space_path')
    rospy.Subscriber("kinematics_pose", KinematicsPose, callback)

    try:
        setJointPath = rospy.ServiceProxy('goal_task_space_path', SetKinematicsPose)

        request =  SetKinematicsPoseRequest()

        request.end_effector_name = "gripper"

        request.kinematics_pose.pose.position.x = x
        request.kinematics_pose.pose.position.y = y
        request.kinematics_pose.pose.position.z = z

        request.kinematics_pose.pose.orientation.x = kinematics_pose.pose.orientation.x
        request.kinematics_pose.pose.orientation.y = kinematics_pose.pose.orientation.y
        request.kinematics_pose.pose.orientation.z = kinematics_pose.pose.orientation.z
        request.kinematics_pose.pose.orientation.w = kinematics_pose.pose.orientation.w

        request.path_time = path_time

        response = setJointPath(request)

        return response.is_planned

    except rospy.ServiceException as e:

        print("Service call failed: %s"%e)


def activate_actuators(state):

    rospy.wait_for_service('set_actuator_state')

    try:

        activate = rospy.ServiceProxy('set_actuator_state', SetActuatorState)
        
        request = SetActuatorStateRequest()

        request.set_actuator_state = state

        response =  activate(request)

        return response.is_planned

    except rospy.ServiceException as e:

        print("Service call failed: %s"%e)

if __name__ == "__main__":

    positions = [[0.134, 0.134, 0.241, 2.0], [0.0, 0.134, 0.241, 2.0], [0.134, 0.200, 0.241, 2.0], [0.200, 0.200, 0.200, 2.0]]

    for i, pos in enumerate(positions):
                
        print("moving to position ", i)

        if activate_actuators(True):
            print("Activation completed")
        else:
            print("Activation failed")

        if move_in_task_space(pos[0], pos[1], pos[2], pos[3]):
            print("Successfully moved")
        else:
            print("Failed to move")

        time.sleep(3.0)

        if activate_actuators(False):
            print("Deactivation completed")
        else:
            print("Deactivation failed")

        time.sleep(1.0)
