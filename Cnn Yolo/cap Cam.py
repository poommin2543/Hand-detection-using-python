import cv2
import datetime

# Open the webcam (0 is the default webcam, change this if you have multiple webcams)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Initialize counter
image_counter = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Press "s" to save image', frame)

    # If 's' is pressed, save the frame
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Increment counter
        image_counter += 1
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        filename = f"{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
        print(f"{image_counter}")

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
