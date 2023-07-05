import csv
import cv2
import mediapipe as mp
import pandas as pd
import joblib
from sklearn.neural_network import MLPClassifier
import pyautogui
import os
import ctypes
import win32api

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
   _fields_ = [("wVk", ctypes.c_ushort),
               ("wScan", ctypes.c_ushort),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
   _fields_ = [("uMsg", ctypes.c_ulong),
               ("wParamL", ctypes.c_short),
               ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
   _fields_ = [("dx", ctypes.c_long),
               ("dy", ctypes.c_long),
               ("mouseData", ctypes.c_ulong),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
   _fields_ = [("ki", KeyBdInput),
               ("mi", MouseInput),
               ("hi", HardwareInput)]


class Input(ctypes.Structure):
   _fields_ = [("type", ctypes.c_ulong),
("ii", Input_I)]

def press_key(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008 | 0x0002

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
# import pydirectinput
# Load the model
# loaded_model = joblib.load('../mlp_classifier.joblib')
loaded_model = joblib.load('C:\\Users\\Mr.Noom\\Documents\\Hand-detection-using-python-and-cvzone\\Ann\\mlp_classifier.joblib')
# Create a VideoCapture object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FPS, 30)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# Initialize the hand detection model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

fingers = [
    'THUMB',
    'INDEX_FINGER',
    'MIDDLE_FINGER',
    'RING_FINGER',
    'PINKY'
]

thumb_parts = ['CMC', 'MCP', 'IP', 'TIP']
other_finger_parts = ['MCP', 'PIP', 'DIP', 'TIP']
parts = [thumb_parts if finger == 'THUMB' else other_finger_parts for finger in fingers]

fieldnames = [f'{finger}_{part}_{coordinate}' for finger, finger_parts in zip(fingers, parts) for part in finger_parts for coordinate in ['X', 'Y', 'Z']]
print(type(fieldnames))
fieldnames.append("CLASS")
# Open a CSV file for writing
# with open('landmarks.csv', 'a', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the BGR image to RGB before processing
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and draw the hand landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            row = {}
            for finger, finger_parts in zip(fingers, parts):
                for part in finger_parts:
                    landmark = hand_landmarks.landmark[getattr(mp_hands.HandLandmark, f'{finger}_{part}')]
                    # print(f"{finger} {part}: x={landmark.x}, y={landmark.y}, z={landmark.z}")
                    for coordinate in ['X', 'Y', 'Z']:
                        row[f'{finger}_{part}_{coordinate}'] = getattr(landmark, coordinate.lower())
            noomdata = pd.DataFrame([row])
            predicted_y = loaded_model.predict(noomdata)
            print(predicted_y[0])
            if predicted_y[0]==0:
                press_key(0x23);release_key(0x11); # w
                # print("OK")
            elif predicted_y[0]==1:
                press_key(0x39);release_key(0x39); # SPACE  
                
            elif predicted_y[0]==2:                                      
                press_key(0x1E);release_key(0x1E); # a
                
            elif predicted_y[0]==3:
               press_key(0x20);release_key(0x20); # g
               

            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the capture object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
