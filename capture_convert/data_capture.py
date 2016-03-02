import Leap, sys, thread, time
import os
class LeapMotonListener(Leap.Listener):
	finger_names=['Thumb','Index','Middle','Ring','Pinky']
	bone_names=['Metacarpal','Proximal','Intermediate','Distal']
	state_names=['STATE_INVALID','STATE_START','STATE_UPDATA','STATE_END']
	def open_file(self):
		global file
		file=open('data.txt','w')

	def write_file(self,a):
		file.write(a)
	def close_file(self):
		file.close()

	def convertData(self,a):
		a=str(a)
		a=a[1:-1]
		a=a.replace(" ", "")
		a='['+a+']'
		return a

	def convert_3x3(self,a):
		temp='['
		i=0
		while i<3:
			temp=temp+str(a.pop(0))+','
			i+=1
		temp=temp[0:-1]
		temp=temp+']'
		return temp
	def convert_4x4(self,a):
		temp='['
		i=0
		while i<3:
			temp=temp+str(a.pop(0))+','
			i+=1
		a.pop(0)
		temp=temp[0:-1]
		temp=temp+']'
		return temp

	def on_init(self, controller):
		print "Initialized"
	def on_connect(self,controller):
		print "Motion Sensor Connected"
		self.open_file()
		print "??????????"
		self.write_file('{"clients":[{"frames":[')

	def on_disconnect(self,controller):
		print "Motion Sensor Disconnected"

	def on_exit(self,controller):
		print "Exited"
		self.close_file()
		with open('data.txt', 'a+') as file:
			file.seek(-1, os.SEEK_END)
			file.truncate()
		file.close()
		file=open('data.txt','a')
		file.write('],"id":-1}]}')
		file.close
		pre, ext = os.path.splitext('data.txt')
		os.rename('data.txt', pre + '.json')

	def on_frame(self,controller):
		frame = controller.frame()
		index=0
		if len(frame.hands)!=0:
			time=str(frame.timestamp)
			timeid=str(frame.id)
			self.write_file('{"hands":[')
		for hand in frame.hands:
			handType="left" if hand.is_left else "right"
			position=hand.palm_position
			hand_x_basis = hand.basis.x_basis
			hand_y_basis = hand.basis.y_basis
			hand_z_basis = hand.basis.z_basis
			matrix_hand = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, position)
			matrix_hand=matrix_hand.to_array_4x4()
			# inverse_hand=matrix.rigid_inverse
			self.write_file('{"fingers":[')
			i=0
			for finger in hand.fingers:
				self.write_file('{"bones":[')
				j=0
				for b in range(0,4):
					bone = finger.bone(b)
					basis = bone.basis
					x_basis = basis.x_basis
					y_basis = basis.y_basis
					z_basis = basis.z_basis
					origin = basis.origin
					matrix = Leap.Matrix(x_basis, y_basis, z_basis, origin)
					inverse=matrix.rigid_inverse()
					inverse=inverse.to_array_3x3()
					print("*****inverse"+str(inverse))
					print("*****"+str(matrix))
					self.write_file('{"nextJoint":')
					temp=self.convertData(bone.next_joint)
			 		self.write_file(temp+',"orientation":[')
			 		temp=self.convert_3x3(inverse)
					self.write_file(temp+",")
			 		temp=self.convert_3x3(inverse)
			 		self.write_file(temp+",")
			 		temp=self.convert_3x3(inverse)
			 		self.write_file(temp+'],"preJoint":')
			 		temp=self.convertData(bone.prev_joint)
			 		self.write_file(temp)
					if j !=3:
						self.write_file(',"type":'+str(j)+'},')
					else:
						self.write_file(',"type":'+str(j)+'}],')
					print ",nextJoint:" + str(bone.next_joint) +  ",orientation:"+str(basis.x_basis) + "," + str(basis.y_basis) + "," + str(basis.z_basis) + "preJoint:" + str(bone.prev_joint) + "type: " + str(j)
					j+=1
				if i !=4:
					self.write_file('"type":'+str(i)+"},")
				else:
					self.write_file('"type":'+str(i)+"}],")
				print "Type: " + str(i)
				i+=1
			self.write_file('"orientation":[')
			temp=self.convert_4x4(matrix_hand)
			self.write_file(temp+",")
			temp=self.convert_4x4(matrix_hand)
			self.write_file(temp+",")
			temp=self.convert_4x4(matrix_hand)
			self.write_file(temp+'],"position":')
			temp=self.convert_4x4(matrix_hand)
			self.write_file(temp)
			if index==0 and len(frame.hands)==2:
				self.write_file(',"type":'+'"'+handType+'"'+"},")
			elif index==1 and len(frame.hands)==2:
				self.write_file(',"type":'+'"'+handType+'"'+'}')
			elif index==0 and len(frame.hands)==1:
				self.write_file(',"type":'+'"'+handType+'"'+'}')
			index+=1
		if len(frame.hands)!=0:
			self.write_file('],"id":'+timeid+',"timestamp":'+time+"},")
		    #print "orientation:"+hand_x_basis+hand_y_basis+hand_z_basis+",type:"+handType + ",position:" + position+",id:"+timeid+",timestamp:"+time
def main():
	listener=LeapMotonListener();
	controller=Leap.Controller();

	controller.add_listener(listener)
	print "Press enter to quit"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally: 
		controller.remove_listener(listener)
if __name__=="__main__":
	main()