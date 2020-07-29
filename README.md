# Hand Gesture Controlled VLC Player #
Recognizes hand gestures using OpenCV and Python and controls VLC player depending on the gesture using the vlc python bindings.
## Libraries Needed ##
- numpy
- cv2
- math
- imutils
- os
## How it works ##
- Capture real time video sequence from camera
- Captured video is converted into grayscale and further blurred to remove strong pixels
- To reduce the region to be processed a ROI defined at the top right corner of the frame where the hand is placed for recognition.
- Running average method over 30 frames is used for background subtraction and giving the hand region as foreground. 
- Convex Hull and convexity defects are further used to find the number for fingers raised which is equal to one more than total number of defects.
- Based on the number of defects VLC player is controlled. Available Commands are
  - Play 
  - Pause 
  - Mute 
  - Volumpe up by 10%
  - Volume down by 10%
