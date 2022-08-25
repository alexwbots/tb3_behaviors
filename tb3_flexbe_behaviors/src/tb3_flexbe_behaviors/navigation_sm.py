#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from tb3_flexbe_behaviors.go_to_goal_sm import Go_to_goalSM
from tb3_flexbe_states.Go_nav import MoveBaseState as tb3_flexbe_states__MoveBaseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Dec 01 2021
@author: Alexander Lopez
'''
class NavigationSM(Behavior):
	'''
	Navigation of a mobile robot
	'''


	def __init__(self):
		super(NavigationSM, self).__init__()
		self.name = 'Navigation'

		# parameters of this behavior
		self.add_parameter('x_des', 1.0)
		self.add_parameter('y_des', 1.0)
		self.add_parameter('tetha_des', 0.75)

		# references to used behaviors
		self.add_behavior(Go_to_goalSM, 'Go_to_goal')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:618 y:86, x:285 y:307
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:106 y:92
			OperatableStateMachine.add('go_nav',
										tb3_flexbe_states__MoveBaseState(x_deseado=self.x_des, y_deseado=self.y_des, theta_deseado=self.tetha_des),
										transitions={'arrived': 'Go_to_goal', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off})

			# x:364 y:75
			OperatableStateMachine.add('Go_to_goal',
										self.use_behavior(Go_to_goalSM, 'Go_to_goal'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
