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
## Screenshots ##
Recognizing fist used for playing video with zero counting defects or cavity
![Screenshot (104)](https://user-images.githubusercontent.com/51263342/88828475-eb636900-d1e8-11ea-8aa7-52a13efe5e77.png)
Recognizing palm used for volume down by 10%  with 4 counting defects or cavity represented by blue dots
![Screenshot (103)](https://user-images.githubusercontent.com/51263342/88828440-df77a700-d1e8-11ea-9c27-c5367958e36f.png)
Recognizing a V symbol or two fingers used for pausing the video with one counting defects or cavity shown by blue dot
![Screenshot (102)](https://user-images.githubusercontent.com/51263342/88828413-d71f6c00-d1e8-11ea-8639-f3bd158854df.png)
## Requirements ##
- python 3
- VLC python binding
 - Run pip install vlc-ctrl
- Works on Linux currently as a dependency of the VLC binding 'dbus' works efficiently on linux but a port to Windows is still in progress 
