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
    # fieldnames = ['THUMB_TIP_X', 'THUMB_TIP_Y', 'THUMB_TIP_Z','THUMB_DIP_X', 'THUMB_DIP_Y', 'THUMB_DIP_Z','THUMB_PIP_X', 'THUMB_PIP_Y', 'THUMB_PIP_Z','THUMB_MCP_X', 'THUMB_MCP_Y', 'THUMB_MCP_Z'
    #               ,'INDEX_TIP_X', 'INDEX_TIP_Y', 'INDEX_TIP_Z','INDEX_DIP_X', 'INDEX_DIP_Y', 'INDEX_DIP_Z','INDEX_PIP_X', 'INDEX_PIP_Y', 'INDEX_PIP_Z','INDEX_MCP_X', 'INDEX_MCP_Y', 'INDEX_MCP_Z'
    #               ,'MIDDLE_TIP_X', 'MIDDLE_TIP_Y', 'MIDDLE_TIP_Z','MIDDLE_DIP_X', 'MIDDLE_DIP_Y', 'MIDDLE_DIP_Z','MIDDLE_PIP_X', 'MIDDLE_PIP_Y', 'MIDDLE_PIP_Z','MIDDLE_MCP_X', 'MIDDLE_MCP_Y', 'MIDDLE_MCP_Z'
    #               ,'RING_TIP_X', 'RING_TIP_Y', 'RING_TIP_Z','RING_DIP_X', 'RING_DIP_Y', 'RING_DIP_Z','RING_PIP_X', 'RING_PIP_Y', 'RING_PIP_Z','RING_MCP_X', 'RING_MCP_Y', 'RING_MCP_Z'
    #               ,'PINKY_TIP_X', 'PINKY_TIP_Y', 'PINKY_TIP_Z','PINKY_DIP_X', 'PINKY_DIP_Y', 'PINKY_DIP_Z','PINKY_PIP_X', 'PINKY_PIP_Y', 'PINKY_PIP_Z','PINKY_MCP_X', 'PINKY_MCP_Y', 'PINKY_MCP_Z'
    #               ]
    fieldnames = [f'{finger}_{part}_{coordinate}' for finger in fingers for part in ['TIP', 'DIP', 'PIP', 'MCP'] for coordinate in ['X', 'Y', 'Z']]

    # fieldnames = ['finger', 'part', 'x','y','z']
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
                row = {}
                for finger in fingers:
                    # Corrected parts of the fingers
                    parts = ['TIP', 'IP', 'MCP', 'CMC'] if finger == 'THUMB' else ['TIP', 'DIP', 'PIP', 'MCP']
                    for part in parts:
                        landmark = hand_landmarks.landmark[getattr(mp_hands.HandLandmark, f'{finger}_{part}')]
                        print(f"{finger} {part}: x={landmark.x}, y={landmark.y}, z={landmark.z}")
                         # Write the x, y, z coordinates to the CSV file
                        # writer.writerow({'finger': finger, 'part': part, 'x': landmark.x, 'y': landmark.y, 'z': landmark.z})
                        for coordinate in ['X', 'Y', 'Z']:
                            row[f'{finger}_{part}_{coordinate}'] = getattr(landmark, coordinate.lower())
                writer.writerow(row)
                        
                        # Print or store the landmark data as required
                        # print(landmark)

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
