#!/usr/bin/env python
import rospy
import actionlib
from tarea2.msg import AngularAction, AngularGoal, AngularResult

if __name__=="__main__":
  rospy.init_node('go_angular_client')
  client = actionlib.SimpleActionClient('angular', AngularAction)
  client.wait_for_server()
  goal = AngularGoal()
  goal.orientacion_deseada = 0.75
  client.send_goal(goal)
  client.wait_for_result()
  #print('Timer elapsed: %f'%(client.get_result().time_elapsed.to_sec()))
  #print('Feedback : %f'%(client.get_result().updates_sent))