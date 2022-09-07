#!/usr/bin/env python
import rospy
import time
import actionlib
from tarea2.msg import AngularAction, AngularGoal, AngularResult
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

global orientacion_actual, orientacion_intermedia, flag1
orientacion_actual = 0
#orientacion_deseada = 1.5708
flag1 = True
orientacion_intermedia = 0


def odometrycb(msg):
  global orientacion_actual, orientacion_intermedia, flag1
  qx = msg.pose.pose.orientation.x
  qy = msg.pose.pose.orientation.y
  qz = msg.pose.pose.orientation.z
  qw = msg.pose.pose.orientation.w
  roll, pitch, yaw = euler_from_quaternion([qx,qy,qz,qw])
  orientacion_actual = yaw
  if flag1:
    orientacion_intermedia = yaw
    flag1 = False

def do_angular(goal):

  global orientacion_actual, orientacion_intermedia, flag1

  rospy.Subscriber('/odom', Odometry, odometrycb)
  vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
  velocidad = Twist()

  orientacion_deseada = goal.orientacion_deseada

  print("Accion recibida, orientacion deseada: "+str(goal.orientacion_deseada))

  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    orientacion_relativa = orientacion_deseada + orientacion_intermedia
    error = orientacion_relativa - orientacion_actual
    kp = 0.3
    if(error>=0.01):
      velocidad.angular.z = kp*error
    else:
      velocidad.angular.z = 0.0
      vel_pub.publish(velocidad)
      result = AngularResult()
      result.orientacion_resultante = orientacion_actual
      print("Resultado de la accion: "+str(orientacion_actual))
      server.set_succeeded(result)
      velocidad.angular.z = 0.0
      vel_pub.publish(velocidad)
      flag1 = True
      break

    vel_pub.publish(velocidad)
    rate.sleep()


if __name__=="__main__":
  rospy.init_node('go_angular_server')
  server = actionlib.SimpleActionServer('angular', AngularAction, do_angular, False)
  server.start()
  print("Action Server has started")
  rospy.spin()