#!/usr/bin/env python
import rospy
import actionlib
from tarea2.msg import LinearAction, LinearGoal, LinearResult

if __name__=="__main__":
  rospy.init_node('go_linear_client')
  client = actionlib.SimpleActionClient('linear', LinearAction)
  client.wait_for_server()
  goal = LinearGoal()
  goal.posicion_deseada = 1.0
  client.send_goal(goal)
  client.wait_for_result()
  #print('Timer elapsed: %f'%(client.get_result().time_elapsed.to_sec()))
  #print('Feedback : %f'%(client.get_result().updates_sent))