import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
	finger = ['t','i','m','r','p']
	bone = ['m','p','i','d']
	status = ['INVALID','START','UPDATE','END']

	def on_init(self, controller):
		print("initiallized")

	def on_connect(self, controller):
		print("connected")
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print("disconnect")

	def on_exit(self,controller):
		print("exited")

	def on_frame(self,controller):
		pass



def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()

	controller.add_listener(listener)
	print("enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__=="__main__":
	main()

