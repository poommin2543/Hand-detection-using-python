import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Initialize the hand detection model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while(True):
    ret, frame = cap.read()
     # Convert the BGR image to RGB before processing
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and draw the hand landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        # for hand_landmarks in results.multi_hand_landmarks:
        #     mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        for hand_number, hand_landmarks in enumerate(results.multi_hand_landmarks):
            print(f'Hand {hand_number}:')
        # for landmark in hand_landmarks.landmark:
        #     # landmark.x, landmark.y, and landmark.z are the normalized [0, 1] coordinates in the image
        #     print(f'  x: {landmark.x}, y: {landmark.y}, z: {landmark.z}')
        thumb_tip = hand_landmarks.landmark[4]
        print(f'Thumb tip: x={thumb_tip.x}, y={thumb_tip.y}, z={thumb_tip.z}')
        mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        # Tip of thumb
    cv2.imshow('frame', frame)
	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# Destroy all the windows
cv2.destroyAllWindows()