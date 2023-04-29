import random
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from Kalman import KalmanAngle
import smbus
import time
import math

import numpy as np
import RPi.GPIO as GPIO
from encoder import Encoder

GPIO.setmode(GPIO.BCM)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # create input fields and labels
        self.create_input_fields()

        # create number pad
        self.create_number_pad()

    def create_input_fields(self):
        self.input_fields = []
        self.labels = []

        label_names = ["Largeur de la cible", 
                       "IBO", 
                       "Distance de flexion", 
                       "Poids supp. sur la corde", 
                       "Force de tension", 
                       "Poids de la flèche"]
        for i in range(6):
            label = tk.Label(self, text=label_names[i])
            label.grid(row=i, column=0, padx=5, pady=5)
            self.labels.append(label)

            input_field = tk.Entry(self)
            input_field.grid(row=i, column=1, padx=5, pady=5)
            self.input_fields.append(input_field)

    def create_number_pad(self):
        self.number_pad = tk.Frame(self)
        self.number_pad.grid(row=0, column=2, rowspan=8, padx=5, pady=5)

        # create number buttons
        for i in range(9):
            button = tk.Button(self.number_pad, text=str(i+1), width=5, height=2, command=lambda num=i+1: self.insert_number(num))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)

        # create zero button
        button_zero = tk.Button(self.number_pad, text="0", width=5, height=2, command=lambda num=0: self.insert_number(num))
        button_zero.grid(row=3, column=1, padx=5, pady=5)

        # create clear, submit, and delete buttons
        button_clear = tk.Button(self.number_pad, text="C", width=5, height=2, command=self.clear_input_fields)
        button_clear.grid(row=4, column=0, padx=5, pady=5)

        button_submit = tk.Button(self.number_pad, text="Submit", width=5, height=2, command=self.submit)
        button_submit.grid(row=4, column=1, padx=5, pady=5)

        button_delete = tk.Button(self.number_pad, text="DEL", width=5, height=2, command=self.delete_from_input_field)
        button_delete.grid(row=4, column=2, padx=5, pady=5)

    def insert_number(self, num):
        # find which input field has focus
        focus_index = None
        for i in range(8):
            if self.input_fields[i] == self.master.focus_get():
                focus_index = i
                break

        # insert number into focused input field
        if focus_index is not None:
            current_text = self.input_fields[focus_index].get()
            self.input_fields[focus_index].delete(0, tk.END)
            self.input_fields[focus_index].insert(0, current_text + str(num))

    def clear_input_fields(self):
        # clear all input fields
        for i in range(8):
            self.input_fields[i].delete(0, tk.END)

    def delete_from_input_field(self):
        # find which input field has focus
        focus_index = None
        for i in range(8):
            if self.input_fields[i] == self.master.focus_get():
                focus_index = i
                break

        # delete last character from focused input field
        if focus_index is not None:
            current_text = self.input_fields[focus_index].get()
            if len(current_text) > 0:
                self.input_fields[focus_index].delete(len(current_text) - 1)

    def submit(self):
        kalmanX = KalmanAngle()
        kalmanY = KalmanAngle()

        RestrictPitch = True	#Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
        radToDeg = 57.2957786
        kalAngleX = 0
        kalAngleY = 0
        #some MPU6050 Registers and their Address
        PWR_MGMT_1   = 0x6B
        SMPLRT_DIV   = 0x19
        CONFIG       = 0x1A
        GYRO_CONFIG  = 0x1B
        INT_ENABLE   = 0x38
        ACCEL_XOUT_H = 0x3B
        ACCEL_YOUT_H = 0x3D
        ACCEL_ZOUT_H = 0x3F
        GYRO_XOUT_H  = 0x43
        GYRO_YOUT_H  = 0x45
        GYRO_ZOUT_H  = 0x47

        # create new window
        top = tk.Toplevel(self)
        top.title("Camera Feed")

        # create video capture object
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Define circle parameters
        self.circle_color = (0, 0, 255)  # Red color
        self.circle_radius = 10
        self.circle_thickness = -1  # Filled circle
        self.circle_position = [340, 240]  # Start at the center of the screen

        # Define line parameters
        self.y1 = 240 - 25 # 215
        self.y2 = 240 + 25 # 265
        line_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 5
        x1 = int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) - line_width) // 2)
        x2 = int(x1 + line_width)
        self.multiplier = 0

        def MPU_Init():
            bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
            bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
            bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))
            bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
            bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

        def read_raw_data(addr):
            high = bus.read_byte_data(DeviceAddress, addr)
            low = bus.read_byte_data(DeviceAddress, addr+1)
            value = ((high << 8) | low)
            if(value > 32768):
                    value = value - 65536
            return value

        bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
        DeviceAddress = 0x68   # MPU6050 device address
        MPU_Init()

        time.sleep(1)
        #Read Accelerometer raw value
        accX = read_raw_data(ACCEL_XOUT_H)
        accY = read_raw_data(ACCEL_YOUT_H)
        accZ = read_raw_data(ACCEL_ZOUT_H)
        print(roll)
        kalmanX.setAngle(roll)
        kalmanY.setAngle(pitch)
        gyroXAngle = roll;
        gyroYAngle = pitch;
        compAngleX = roll;
        compAngleY = pitch;

        timer = time.time()
        flag = 0

        #print(accX,accY,accZ)
        #print(math.sqrt((accY**2)+(accZ**2)))
        if (RestrictPitch):
            roll = math.atan2(accY,accZ) * radToDeg
            pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
        else:
            roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
            pitch = math.atan2(-accX,accZ) * radToDeg

        def valueChanged(value, direction):
            if direction == "L":
                self.y1 -= 2.5
                self.y2 += 2.5

                self.circle_position[0] -= random.randint(0, 10)
                self.circle_position[0] = max(self.circle_position[0], 300)
                if self.y2 <= 165:
                    self.circle_position[0] = 300         
            elif direction == "R":
                self.y1 += 2.5
                self.y2 -= 2.5

                if self.y2 <= 250:
                    self.circle_position[0] += random.randint(0, 10)
                if self.y2 <= 165:
                    self.circle_position[0] = 300

        e1 = Encoder(17, 18, valueChanged)

        # create canvas to display video feed
        canvas = tk.Canvas(top, width=640, height=480)
        canvas.pack()
        canvas.focus_set()

        # update video feed every 15 milliseconds
        def update():
            ret, frame = cap.read()
            if ret:
                #Read Accelerometer raw value
                accX = read_raw_data(ACCEL_XOUT_H)
                accY = read_raw_data(ACCEL_YOUT_H)
                accZ = read_raw_data(ACCEL_ZOUT_H)

                #Read Gyroscope raw value
                gyroX = read_raw_data(GYRO_XOUT_H)
                gyroY = read_raw_data(GYRO_YOUT_H)
                gyroZ = read_raw_data(GYRO_ZOUT_H)

                dt = time.time() - timer
                timer = time.time()

                if (RestrictPitch):
                    roll = math.atan2(accY,accZ) * radToDeg
                    pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
                else:
                    roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
                    pitch = math.atan2(-accX,accZ) * radToDeg

                gyroXRate = gyroX/131
                gyroYRate = gyroY/131

                if (RestrictPitch):

                    if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
                        kalmanX.setAngle(roll)
                        complAngleX = roll
                        kalAngleX   = roll
                        gyroXAngle  = roll
                    else:
                        kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

                    if(abs(kalAngleX)>90):
                        gyroYRate  = -gyroYRate
                        kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
                else:

                    if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
                        kalmanY.setAngle(pitch)
                        complAngleY = pitch
                        kalAngleY   = pitch
                        gyroYAngle  = pitch
                    else:
                        kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

                    if(abs(kalAngleY)>90):
                        gyroXRate  = -gyroXRate
                        kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

                #angle = (rate of change of angle) * change in time
                gyroXAngle = gyroXRate * dt
                gyroYAngle = gyroYAngle * dt

                #compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
                compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
                compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

                if ((gyroXAngle < -180) or (gyroXAngle > 180)):
                    gyroXAngle = kalAngleX
                if ((gyroYAngle < -180) or (gyroYAngle > 180)):
                    gyroYAngle = kalAngleY

                print("Angle X: " + str(kalAngleX)+"   " +"Angle Y: " + str(kalAngleY))
                #print(str(roll)+"  "+str(gyroXAngle)+"  "+str(compAngleX)+"  "+str(kalAngleX)+"  "+str(pitch)+"  "+str(gyroYAngle)+"  "+str(compAngleY)+"  "+str(kalAngleY))
                time.sleep(0.005)

                # Draw the circle
                cv2.circle(frame, (self.circle_position[0], self.circle_position[1]), self.circle_radius, self.circle_color, self.circle_thickness)

                # Move the circle randomly on the x-axis
                self.circle_position[0] += random.randint(-2, 2)
                self.circle_position[0] = max(self.circle_position[0], self.circle_radius)
                self.circle_position[0] = min(self.circle_position[0], frame.shape[1] - self.circle_radius)

                #self.circle_position[0] = self.circle_position self.multiplier

                # Update line coordinates
                x1 = int((frame.shape[1] - line_width) // 2)
                x2 = int(x1 + line_width)

                # Draw two horizontal lines spaced 100 pixels apart and 1/3 the width of the screen
                cv2.line(frame, (x1, int(self.y1)), (x2, int(self.y1)), (0, 255, 0), 2)
                cv2.line(frame, (x1, int(self.y2)), (x2, int(self.y2)), (0, 255, 0), 2)

                # convert frame to PIL Image format
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = PIL.Image.fromarray(img)

                # resize image to fit canvas
                img = img.resize((640, 480), PIL.Image.ANTIALIAS)

                # display image on canvas
                photo = PIL.ImageTk.PhotoImage(image=img)
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                canvas.photo = photo

            # schedule next update
            canvas.after(15, update)

        # start video feed update loop
        update()

        # set function to release video capture object when window is closed
        def on_closing():
            cap.release()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_closing)

root = tk.Tk()
app = Application(master=root)
app.mainloop()