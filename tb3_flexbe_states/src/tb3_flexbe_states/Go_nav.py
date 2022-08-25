#!/usr/bin/env python
import rospy
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from tf.transformations import quaternion_from_euler

class MoveBaseState(EventState):
    """
    Navigates a robot to a desired position and orientation using move_base.

    -- x_deseado 	    float	Amount of time to wait in seconds.
    -- y_deseado 	    float	Amount of time to wait in seconds.
    -- theta_deseado 	float	Amount of time to wait in seconds.

    <= arrived                  Navigation to target pose succeeded.
    <= failed                   Navigation to target pose failed.
    """

    def __init__(self, x_deseado, y_deseado, theta_deseado):
        """Constructor"""

        super(MoveBaseState, self).__init__(outcomes = ['arrived', 'failed'])
        self._x_deseado = x_deseado
        self._y_deseado = y_deseado
        self._theta_deseado = theta_deseado
        self._action_topic = "/move_base"
        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self._arrived = False
        self._failed = False


    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if self._arrived:
            return 'arrived'
        if self._failed:
            return 'failed'

        if self._client.has_result(self._action_topic):
            status = self._client.get_state(self._action_topic)
            if status == GoalStatus.SUCCEEDED:
                self._arrived = True
                return 'arrived'
            elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
                            GoalStatus.RECALLED, GoalStatus.ABORTED]:
                Logger.logwarn('Navigation failed: %s' % str(status))
                self._failed = True
                return 'failed'


    def on_enter(self, userdata):
        """Create and send action goal"""

        self._arrived = False
        self._failed = False

        # Create and populate action goal
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self._x_deseado
        goal.target_pose.pose.position.y = self._y_deseado
        (qx,qy,qz,qw) = quaternion_from_euler(0,0,self._theta_deseado)
        goal.target_pose.pose.orientation.x = qx
        goal.target_pose.pose.orientation.y = qy
        goal.target_pose.pose.orientation.z = qz
        goal.target_pose.pose.orientation.w = qw

        # goal.target_pose.header.stamp.secs = 5.0

        # Send the action goal for execution
        try:
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True
            
    def cancel_active_goals(self):
        if self._client.is_available(self._action_topic):
            if self._client.is_active(self._action_topic):
                if not self._client.has_result(self._action_topic):
                    self._client.cancel(self._action_topic)
                    Logger.loginfo('Cancelled move_base active action goal.')

    def on_exit(self, userdata):
        self.cancel_active_goals()

    def on_stop(self):
        self.cancel_active_goals()
