#--------------------------------------
# Importing all the necessary libraries 
#--------------------------------------
import numpy as np
import cv2
import imutils
import os
import math

#defining global variables
#initialising background as None
bg = None

#---------------------------------------------------------------------------
# To find the running average over the background for Background subtraction 
#---------------------------------------------------------------------------
def run_avg(current_image, alpha):
  global bg
  #initialising background
  if bg is None:
    # modify the data type of image, setting to 32-bit floating point
    bg = current_image.copy().astype("float32")
    return
  # using the cv2.accumulateWeighted() function to compute the weighted average 
  # that updates the running average 
  cv2.accumulateWeighted(current_image, bg, alpha) 

#-----------------------------------------------------
# To segment the handfrom rest of the background image
#-----------------------------------------------------
def segment(current_image, threshold = 25):
  global bg
  # find the absolute difference between background and current frame after converting the background back to 8 bit image
  diff = cv2.absdiff(bg.astype('uint8'), current_image) 

  # threshold the difference image so that we get the foreground
  thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

  # get the contours in the thresholded image
  cnts, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  # return None, if no contours detected
  if len(cnts) == 0:
    return
  else:
    # based on contour area, get the maximum contour area which is the hand
    segmented = max(cnts, key=cv2.contourArea)
    return (thresholded, segmented)

#-----------------------------------------------------------------------------------------
# To count the number of fingers for defining the gesture for controlling the media player
#-----------------------------------------------------------------------------------------
def count_fingers(maxcontour, frame, top, right):
  # To cover the max contour
  hull = cv2.convexHull(maxcontour)
  cv2.drawContours(frame, [hull + (right, top)], -1, (0, 255, 0), 2)

  hull = cv2.convexHull(maxcontour, returnPoints=False)
  # we find convexity defects, which is the deepest point of deviation on the contour
  defects = cv2.convexityDefects(maxcontour,hull)
  count_defects = 0
  # finding the start, end and farthest point in the cavity
  for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(maxcontour[s][0])
    end = tuple(maxcontour[e][0])
    far = tuple(maxcontour[f][0])
    # finding the distances of the lines forming triangle in the cavity
    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    # Using cosine formula to find the angle
    angle = (math.acos((b**2 + c**2 - a**2)/(2*b*c))*180)/3.14

    # Ignore the defects which are small and wide
    # Probably not fingers
    if angle <= 90:
      count_defects += 1
      cv2.circle(clone,far,5,[255,0,0],-1)

    cv2.line(frame,start,end,[0,255,0],2)

  return count_defects

#----------------------------
# To control VLC media player
#----------------------------
def media_control(cd):
# To play the media player with a fist
  if cd== 0:
    cv2.putText(frame,"Video play", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)
    os.system("vlc-ctrl play")
# To pause te media player with a V symbol
  elif cd == 1:
    cv2.putText(frame,"Video pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)
    os.system("vlc-ctrl pause")
# To mute the media player with three fingers
  elif cd == 2:
    cv2.putText(frame,"Mute", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)
    os.system("vlc-ctrl volume 0")
# To volume up the media player by 10%
  elif cd == 3:
    cv2.putText(frame,"Volume up", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)
    os.system("vlc-ctrl volume +10%")
# To volume down the media player with a palm
  elif cd == 4:
    cv2.putText(frame,"Volume down", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)
    os.system("vlc-ctrl volume -10%")
# No action otherwise
  else:
    pass
  return

#-----------------
# MAIN FUNCTION
#-----------------
if __name__ == "__main__":

  # initialize weight for running average
  alpha = 0.5
  
  #access the webcam
  camera = cv2.VideoCapture(0)
 
  # region of interest (ROI) coordinates
  top, right, bottom, left = 10, 350, 225, 590
 
  # initialize counter for num of frames
  num_frames = 0

  #infinite loop untill interrupted
  while(True):

    # read the current frame from the camera 
    _, frame = camera.read()
  
    # resize the frame
    frame = imutils.resize(frame, width=700)
    # flip the frame so that it is not the mirror view

    frame = cv2.flip(frame, 1)
 
    # clone the frame
    clone = frame.copy()

    # define the ROI over the frame
    roi = frame[top:bottom, right:left]

    # convert the roi to grayscale and blur it
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # to get the background, keep looking till a threshold of 30 frames is reached
    # so that our running average model gets calibrated
   
    cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

    if num_frames < 30:
      run_avg(gray, alpha)
    else:
      # segment the hand region
      hand = segment(gray)
  
      # check whether hand region is segmented
      if hand is not None:
        # if yes, unpack the thresholded image and
        # segmented region
        (thresholded, segmented) = hand
        # Convexity defects
        points = count_fingers(segmented, clone, top, right)
        # draw the segmented hand region with contours and display the frame
        cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255),2)
        
        cv2.imshow("Thesholded", thresholded)
        # control media player
        media_control(points)
    
       
    # increment the number of frames
    num_frames += 1

    # display the frame with segmented hand
    cv2.imshow("Video Feed", clone)

    # Wait for Esc key to stop the program  
    k = cv2.waitKey(30) & 0xff
    if k == 27:
      break

# free up memory
camera.release()
cv2.destroyAllWindows()




