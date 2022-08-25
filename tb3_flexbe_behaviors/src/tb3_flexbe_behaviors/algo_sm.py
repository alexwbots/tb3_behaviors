#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from tb3_flexbe_states.Go_angular import Go_angular
from tb3_flexbe_states.Go_angular import Go_lineal as tb3_flexbe_states__Go_lineal
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Dec 01 2021
@author: assdasd
'''
class AlgoSM(Behavior):
	'''
	asdfas
	'''


	def __init__(self):
		super(AlgoSM, self).__init__()
		self.name = 'Algo'

		# parameters of this behavior
		self.add_parameter('value', 1.0)
		self.add_parameter('value2', 0.75)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:589 y:70, x:396 y:280
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:146 y:70
			OperatableStateMachine.add('go_lineal',
										tb3_flexbe_states__Go_lineal(posicion_deseada=self.value),
										transitions={'arrived': 'go_angular', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off})

			# x:372 y:69
			OperatableStateMachine.add('go_angular',
										Go_angular(posicion_deseada=self.value2),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
