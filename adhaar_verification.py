import cv2
import numpy as np

Aadhar_regions={
    "face": (10, 150, 220, 250),          # (x, y, w, h)
    "aadhaar_no": (240, 400, 350, 50),    # Aadhaar number at bottom-center
    "goi_logo": (70, 10, 100, 120),         # GOI logo at top-left
    "goi_text": (180, 10, 500, 90),       # "Government of India" text
    "qr_code": (650, 290, 190, 160),      # QR Code at right-center
    "name_dob": (240, 160, 420, 200),     # Name, DOB section
    "bottom_line": (100, 470, 700, 60),    # Bottom line across card
    }

def is_content_present(region,image, threshold=50):
    x, y, w, h = region
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    roi = gray[y:y+h, x:x+w]  # Extract region of interest
    _, binary = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY)  # Binary threshold
    content = cv2.countNonZero(binary)  # Count non-zero pixels
    return content > threshold  # Check if content exceeds threshold

def visual_verification(image_path):
  regions=Aadhar_regions
  image = cv2.imread(image_path) #Scaling image to standard dimensions
  height, width = 540, 860
  image = cv2.resize(image, (width, height))
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  results = {}
  for key, box in regions.items():
      content_present = is_content_present(box,image)
      results[key] = content_present

      # Draw bounding box for visualization
      color = (0, 255, 0) if content_present else (0, 0, 255)  # Green if valid, Red if missing
      x, y, w, h = box
      cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
      cv2.putText(image, key, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
  is_valid = all(results.values())
  if is_valid:
    return(True)
  else:
    return(False)

def Validate_aadhaar_num(aadhaarNum):

    if (len(aadhaarNum) == 12 and aadhaarNum.isdigit()):


      #takes in Aadhaar number as a string
      mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
      perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]
      try:
          i = len(aadhaarNum)
          j = 0
          x = 0

          while i > 0:
              i -= 1
              x = mult[x][perm[(j % 8)][int(aadhaarNum[i])]]
              j += 1
          if x == 0:
              return True
          else:
              return False

      except ValueError:
          return 'Invalid Aadhar Number'
      except IndexError:
          return 'Invalid Aadhar Number'

    else :
      return False
