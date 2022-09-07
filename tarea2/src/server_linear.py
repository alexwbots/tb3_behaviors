#!/usr/bin/env python
import rospy
import time
import actionlib
from tarea2.msg import LinearAction, LinearGoal, LinearResult
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

global posicion_actual, posicion_intermedia, flag1
posicion_actual = 0
#posicion_deseada = 1.5
flag1 = True
posicion_intermedia = 0


def odometrycb(msg):
  global posicion_actual, posicion_intermedia, flag1
  posicion_actual = msg.pose.pose.position.x
  if flag1:
    posicion_intermedia = msg.pose.pose.position.x
    flag1 = False


def do_linear(goal):

  global posicion_actual, posicion_intermedia, flag1

  rospy.Subscriber('/odom', Odometry, odometrycb)
  vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
  velocidad = Twist()

  posicion_deseada = goal.posicion_deseada

  print("Accion recibida, posicion deseada: "+str(goal.posicion_deseada))

  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    posicion_relativa = posicion_deseada + posicion_intermedia
    error = posicion_relativa - posicion_actual
    kp = 0.6
    if(error>=0.01):
      velocidad.linear.x = kp*error
    else:
      velocidad.linear.x = 0.0
      vel_pub.publish(velocidad)
      result = LinearResult()
      result.posicion_resultante = posicion_actual
      print("Resultado de la accion: "+str(posicion_actual))
      server.set_succeeded(result)
      flag1 = True
      break

    vel_pub.publish(velocidad)
    rate.sleep()


if __name__=="__main__":
  rospy.init_node('go_linear_server')
  server = actionlib.SimpleActionServer('linear', LinearAction, do_linear, False)
  server.start()
  print("Action Server has started")
  rospy.spin()