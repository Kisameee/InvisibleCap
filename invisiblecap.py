import time

import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera stream")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'result.avi' file.
output = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (frame_width, frame_height))

time.sleep(2)
background = 0

for i in range(10):
    ret, background = cap.read()
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_val = np.array([10, 120, 70])
    upper_val = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_val, upper_val)

    lower_val = np.array([0, 150, 70])
    upper_val = np.array([10, 255, 255])
    mask2 = cv2.inRange(hsv, lower_val, upper_val)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)

    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    final_output = cv2.flip(final_output, 2)
    # Display the resulting frame
    record = cv2.imshow('result', final_output)
    # Write the frame into the file 'result.avi'
    output.write(record)

    # Close the input stream and release camera
    keyboard = cv2.waitKey(1) & 0xFF == ord('q')
    if keyboard:
        break
    else:
        break

# When everything done, release the video capture and video write objects
cap.release()
# output.release()

# Closes all the frames
cv2.destroyAllWindows()
