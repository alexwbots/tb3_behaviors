#!/usr/bin/env python
import rospy
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
import actionlib
from actionlib_msgs.msg import GoalStatus
from tarea2.msg import AngularAction, AngularGoal, AngularResult

class Go_angular(EventState):
    '''
    This state work with the action server angular

    -- orientacion_deseada 	float	Amount of time to wait in seconds.

    <= arrived					    Indicates when the robot arrive to the goal.
    <= failed					    Indicates when the robot couldn't get to the goal.
    '''

    def __init__(self, orientacion_deseada):
        super(Go_angular, self).__init__(outcomes=['arrived','failed'])
        self._orientacion_deseada = orientacion_deseada
        self._action_topic = "/angular"
        self._client = ProxyActionClient({self._action_topic: AngularAction})

        self._arrived = False
        self._failed = False

    def execute(self, userdata):
        if self._failed:
            return 'failed'

        if self._arrived:
            return 'arrived'
            
        if self._client.has_result(self._action_topic):
            status = self._client.get_state(self._action_topic)
            if status == GoalStatus.SUCCEEDED:
                self._arrived = True
                return 'arrived'

    def on_enter(self, userdata):
        '''Upon entering the state, save the current time and start waiting.'''
        goal = AngularGoal()
        goal.orientacion_deseada = 1.0
        self._start_time = rospy.get_rostime()

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
                    Logger.loginfo('Cancelled Go Angular active action goal.')

    def on_exit(self, userdata):
        self.cancel_active_goals()

    def on_stop(self):
        self.cancel_active_goals()