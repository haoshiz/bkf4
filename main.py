

import Leap, sys, thread, time, pynput
import Tkinter as tk
import math
import time
import serial


class SampleListener(Leap.Listener):
    velocity_x = 0
    velocity_y = 0
    velocity_z = 0
    flag = 0

    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            '''print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)'''

            position = hand.palm_position
            velocity = hand.palm_velocity
            #print "Hand velocity matrix: %s " % velocity
            self.velocity_x = velocity.x
            self.velocity_y = velocity.y
            self.velocity_z = velocity.z
            self.position_z = position.z
            if abs(velocity.x) < 50 and abs(velocity.y) < 50:
                self.flag = 0
                self.velocity_x = 0
                self.velocity_y = 0
            else:
                self.flag = 1




            #print(type(x))


            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction







def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    ser = serial.Serial('/dev/cu.usbserial-A9Y15J7R')


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    window = tk.Tk()

    canvas = tk.Canvas(window, width=600, height=600)

    oval = canvas.create_oval(400, 400, 430, 430, fill='green')

    button_label = canvas.create_text(300, 300, text='Button', font=('Helvetica', 36), fill='white')

    button_shape = canvas.create_rectangle(220, 260, 380, 340, fill='red')
    #canvas.tag_raise(button_label)
    canvas.tag_lower(button_shape)

    window.title('my app')

    window.geometry('600x600')


    text_content = tk.StringVar()


    main.y = 0
    main.signal_flag_b = True
    main.signal_flag_a = True
    main.signal_flag_c = True
    main.signal_flag_off = True

    def collision():
        a = canvas.find_overlapping(220, 260, 380, 340)
        zz = listener.velocity_z

        #state = "state2"
        if len(a) == 3 and main.y == 0:
            main.signal_flag_off = True
            text_content.set('Hover')
            canvas.itemconfig(button_shape, fill='pink')
            #send b
            if main.signal_flag_b:
                ser.write('b')
                print 'b'
                main.signal_flag_b = False
            if zz < -80 and listener.position_z < 0:


                main.y = 1

        if len(a) == 3 and main.y == 1:

            text_content.set('Pressed')
            canvas.itemconfig(button_shape, fill='blue')

            #send a
            if main.signal_flag_a:
                ser.write('a')
                print 'a'
                main.signal_flag_a = False
            if zz > 150 and listener.position_z > 0:
                main.y = 2

        if len(a) == 3 and main.y == 2:
            #send c


            text_content.set('Release')
            canvas.itemconfig(button_shape, fill='yellow')
            if main.signal_flag_c:
                ser.write('c')
                print 'c'
                main.signal_flag_c = False
        if len(a) != 3:
            if main.signal_flag_off:
                ser.write('c')
                print 'c'
                main.signal_flag_off = False
            text_content.set('Not detected')
            main.y = 0
            canvas.itemconfig(button_shape, fill='red')
            main.signal_flag_b = True
            main.signal_flag_a = True
            main.signal_flag_c = True

    def move():
        speed = 5
        #print listener.velocity_x
        theta = math.atan2(-listener.velocity_y, listener.velocity_x)
        #print "theta %f" % theta
        movex = speed*math.cos(theta)

        #print "x %f" % movex
        movey = speed*math.sin(theta)
        #print "y %f" % movey
        if listener.flag == 1:
            canvas.move(oval, movex, movey)
            listener.flag = 0
    label = tk.Label(window, textvariable=text_content, text="This is TK", font=('Times', 24), width=15, height=2)

    label.pack()
    canvas.pack()
    # Keep this process running until Enter is pressed
    #print "Press Enter to quit..."

    while True:

        move()
        collision()
        window.update_idletasks()
        window.update()



if __name__ == "__main__":

    main()
