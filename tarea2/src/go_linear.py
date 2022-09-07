#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

global posicion_actual
posicion_actual = 0
posicion_deseada = 1.5
global posicion_intermedia, flag1
flag1 = True
posicion_intermedia = 0


def odometrycb(msg):
  global posicion_actual
  global posicion_intermedia, flag1
  posicion_actual = msg.pose.pose.position.x
  if flag1:
    posicion_intermedia = msg.pose.pose.position.x
    flag1 = False

if __name__ == "__main__":
  
  rospy.init_node('go_lineal')
  
  rospy.Subscriber('/odom', Odometry, odometrycb)
  vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
  velocidad = Twist()

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

    rate.sleep()