import Leap, sys, thread, time
class LeapMotonListener(Leap.Listener):
	finger_names=['Thumb','Index','Middle','Ring','Pinky']
	bone_names=['Metacarpal','Proximal','Intermediate','Distal']
	state_names=['STATE_INVALID','STATE_START','STATE_UPDATA','STATE_END']

	def on_init(self, controller):
		print "Initialized"
	def on_connect(self,controller):
		print "Motion Sensor Connected"

	def on_disconnect(self,controller):
		print "Motion Sensor Disconnected"

	def on_exit(self,controller):
		print "Exited"

	def on_frame(self,controller):
		hand=[]
		left=[]
		right=[]
		time=[]
		frame = controller.frame()
		for hand in frame.hands:
			handType="left" if hand.is_left else "right"
			time=str(frame.timestamp)
			timeid=str(frame.id)
			hand_x_basis = str(hand.basis.x_basis)
    		hand_y_basis = str(hand.basis.y_basis)
    		hand_z_basis = str(hand.basis.z_basis)
    		position=str(hand.palm_position)

			# normal = hand.palm_normal
			# direction = hand.direction

			# print "Pitch: " + str(direction.pitch*Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG)
			# arm = hand.arm
			# print "Arm Direction " + str(arm.direction) + " Wrist Position " + str(arm.wrist_position) + " Elbow Position " + str(arm.elbow_position)
			i=0
			for finger in hand.fingers:
				j=0
				for b in range(0,4):
					bone = finger.bone(b)
					basis = bone.basis
					print "preJoint: " + str(bone.prev_joint) + " nextJoint: " + str(bone.next_joint) + "orientation:"+str(basis.x_basis) + "," + str(basis.y_basis) + "," + str(basis.z_basis) + "type: " + str(j)
					j+=1
				print "Type: " + str(i)
				i+=1
			print "orientation:"+ hand_x_basis+ hand_y_basis+ hand_z_basis + "type:"+handType + ",position: " + position+",id:"+timeid+",time"+time
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