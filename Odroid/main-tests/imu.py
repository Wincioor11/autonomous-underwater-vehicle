import um7
from connectionForTesting import *
import threading
import time

IP_ADDRESS = '192.168.137.100'

class IMUClass(): #runnable :)) #java zryła banie
	
	def __init__(self, *statevars):
		name1 = 's'
		port1 = '/dev/ttySAC0'
		self.statevars = [] 		# example: ['roll', 'pitch', 'yaw'] 
		for state in statevars:
			self.statevars.append(state) 
		# All states avaible: 
		#['roll', 'pitch', 'yaw'] 
		#['health', 'roll', 'pitch', 'yaw'] #'mag_proc_x', 'mag_proc_y', 'mag_proc_z', 'mag_raw_x', 'mag_raw_y', 'mag_raw_z', #'accel_raw_x', 'accel_raw_y', 'accel_raw_z', 'accel_proc_x', 'accel_proc_y', 'accel_proc_z', 'gyro_proc_x', 'gyro_proc_y', #'gyro_proc_z', 'accel_raw_time', 'accel_proc_time', 'euler_time']

		self.s1 = um7.UM7(name1, port1, self.statevars, baud=115200)
		try:
			print('IMU initialition process:')
			#self.s1.reset_to_factory()
			print('GET_FW_REVISION=' +     '{}'.format(self.s1.get_fw_revision()))
			print('ZERO_GYROS ' + 'ok.' if self.s1.zero_gyros()      else 'failed.')
			self.s1.set_mag_reference()
			self.s1.set_home_position()
			#print('SET_MAG_REFERENCE ' + 'ok.' if self.s1.set_mag_reference()      else 'failed.')
			#print('SET_HOME_POSITION ' + 'ok.'  if self.s1.set_home_position()       else 'failed.')
			print('RESET_EKF ' + 'ok.'  if self.s1.reset_ekf()       else 'failed.')
			print('FLASH_COMMIT ' + 'ok.'  if self.s1.flash_commit()       else 'failed.')
		except:
			print('------------!ERROR occured!--------------\n')
		
		
		# readings view format:
		self.fs = ''
		self.hs = ''
		for i in self.statevars:
			self.hs += '{:>9.9s} '
			if i == 'health':
				self.fs += ' {0['+i+']:08b} '
			else:
				self.fs += '{0['+i+']:9.3f} '

		
		self.sv = ['roll', 'pitch', 'yaw']

	def catchSamples(self):
		self.s1.catchallsamples(self.sv, 1.0)
				
	def getSamples(self):
		return self.s1.state
		
	def getSample(self, sample): 
                # sample is string for instance: 'roll' , 'accel_raw_x'
		#return self.s1.state[sample]
		if(sample == 'roll' or sample == 'pitch' or sample == 'yaw'):
			#print('jest kat')
			state = self.s1.state[sample]
			#print(state)
			if(state > 180): 
				#print(str(360 - state))
				return (-360 + state)
			if(state < -180):
				#print("state < -180")
				return (360 + state)
		#print("Main return")
		return self.s1.state[sample]
	
	def printSamples(self, headerFlag):
		if headerFlag:
			print(self.hs.format(*self.statevars))
		print(self.getSample('roll'),' ', self.getSample('pitch'),' ', self.getSample('yaw'))
		
	def startSendingSamples(self, connectionObject): #without printing 
		# this method can be a target -> in Thread constructor
		#c = 0
		while True:
			#self.catchSamples()
			#self.printSamples(c % 50 == 0)
			#c += 1
			connectionObject.setDataFrame(self.s1.state)


#imu = IMUClass('roll', 'pitch', 'yaw')
#connThread = Connection(IP_ADDRESS)

#threading.Thread(target=imu.startSendingSamples, args=[connThread]).start()
#connThread.start()
