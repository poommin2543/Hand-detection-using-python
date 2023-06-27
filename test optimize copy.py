import csv
import cv2
import mediapipe as mp

# Create a VideoCapture object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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

# Open a CSV file for writing
with open('landmarks.csv', 'w', newline='') as csvfile:
    fieldnames = ['finger', 'part', 'x', 'y', 'z']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the BGR image to RGB before processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and draw the hand landmarks
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for finger in fingers:
                    parts = ['TIP', 'IP', 'MCP', 'CMC'] if finger == 'THUMB' else ['TIP', 'DIP', 'PIP', 'MCP']
                    for part in parts:
                        landmark = hand_landmarks.landmark[getattr(mp_hands.HandLandmark, f'{finger}_{part}')]
                        # Write the x, y, z coordinates to the CSV file
                        writer.writerow({'finger': finger, 'part': part, 'x': landmark.x, 'y': landmark.y, 'z': landmark.z})

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
