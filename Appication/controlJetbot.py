import csv
import cv2
import mediapipe as mp
import pandas as pd
import joblib
from sklearn.neural_network import MLPClassifier
import pyautogui
import pydirectinput
# Load the model
# loaded_model = joblib.load('../mlp_classifier.joblib')
from websockets.sync.client import connect

def setControl(command):
    with connect("ws://192.168.50.234:8765") as websocket:
        websocket.send(command)
        message = websocket.recv()
        print(f"Received: {message}")

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
            # row['CLASS'] = 3
            # writer.writerow(row)
            predicted_y = loaded_model.predict(noomdata)
            # predictedTolist = predicted_y.tolist()
            # print(predicted_y)
            # print(predictedTolist)
            # print(type(predictedTolist))
            print(predicted_y[0])
            if predicted_y[0]==0:
                setControl(str(0))
            elif predicted_y[0]==1:
                setControl(str(1))
            elif predicted_y[0]==2:
                setControl(str(2))
            elif predicted_y[0]==3:
                setControl(str(3))
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
