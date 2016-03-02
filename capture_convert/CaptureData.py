import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class LeapMotonListener(Leap.Listener):
	finger_names=['Thumb','Index','Middle','Ring','Pinky']
	bone_names=['Metacarpal','Proximal','Intermediate','Distal']
	state_names=['STATE_INVALID','STATE_START','STATE_UPDATA','STATE_END']

	def on_init(self, controller):
		print "Initialized"
	def on_connect(self,controller):
		print "Motion Sensor Connected"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self,controller):
		print "Motion Sensor Disconnected"

	def on_exit(self,controller):
		print "Exited"

	def on_frame(self,controller):
		frame = controller.frame()

		# print "Frame ID " + str(frame.id)\
		# 	  + "Timestamp " + str(frame.timestamp)\
		# 	  + "# of Hands " + str(len(frame.hands))\
		# 	  + "# of Fingers " + str(len(frame.fingers))\
		# 	  + "# of Tools " + str(len(frame.tools))\
		# 	  + "# of Gesture" + str(len(frame.gestures()))

		for hand in frame.hands:
			handType="Left Hand" if hand.is_left else "Right Hand"

			print handType + "Hand ID: " + str(hand.id) + "Palm Position: " + str(hand.palm_position)

			normal = hand.palm_normal
			direction = hand.direction
			hand_x_basis = hand.basis.x_basis
			hand_y_basis = hand.basis.y_basis
			hand_z_basis = hand.basis.z_basis
			hand_origin = hand.palm_position
			hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
			print str(hand_transform)

			hand_transform = hand_transform.rigid_inverse()

			print "Pitch: " + str(direction.pitch) + " Roll: " + str(normal.roll) + " Yaw: " + str(direction.yaw)
			print str(hand_transform)
			arm = hand.arm
			array_matrix = hand_transform.to_array_3x3()
			print("??????????"+str(array_matrix))
			# print "Arm Direction " + str(arm.direction) + " Wrist Position " + str(arm.wrist_position) + " Elbow Position " + str(arm.elbow_position)
			for finger in hand.fingers:
			# 	print "Type: " + self.finger_names[finger.type] + " ID: " + str(finger.id) + " Length (mm): " + str(finger.length) + " Width (mm): " + str(finger.width)

				for b in range(0,4):
					bone = finger.bone(b)
					basis = bone.basis
					direction = bone.direction
					print "Bone: " + self.bone_names[bone.type] + " X: "+str(basis.x_basis) + " Y: " + str(basis.y_basis) + " Z: " + str(basis.z_basis) + " Start " + str(bone.prev_joint) + " End: " + str(bone.next_joint) + " Direction: " + str(bone.direction) 
					x_basis = basis.x_basis
					y_basis = basis.y_basis
					z_basis = basis.z_basis
					matrix = Leap.Matrix(x_basis, y_basis, z_basis)
					direction = Leap.Vector(bone.direction)
					transformed = matrix.transform_direction(direction)
					print (str(transformed))
		# for tool in frame.tools:
		# 	print "Tool ID: " + str(tool.id) + " Tip Position: " + str(tool.tip_position) + " Direction: " + str(tool.direction)
		# for gesture in frame.gestures():
		# 	if gesture.type==Leap.Gesture.TYPE_CIRCLE:
		# 		circle= CircleGesture(gesture)
		# 		if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
		# 			clockwiseness="clockwise"
		# 		else:
		# 			clockwiseness="count-clockwise"
		# 		swept_angle=0
		# 		if circle.state != Leap.Gesture.STATE_START:
		# 			previous = CircleGesture(controller.frame(1).gesture(circle.id))
		# 			swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
		# 		print "ID: " + str(circle.id) + " Progress: " + str(circle.progress) + " Radius: " + str(circle.radius) + " Swept_Angle: " + str(swept_angle * Leap.RAD_TO_DEG) + " " + clockwiseness
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
