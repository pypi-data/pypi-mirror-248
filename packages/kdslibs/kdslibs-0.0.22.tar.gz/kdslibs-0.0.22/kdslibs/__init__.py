
datadict={}
link = "data.py"


current_dir = os.path.dirname(os.path.abspath(__file__))
#current_dir = os.getcwd()




#General
import urllib.request
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas
import pandas as pd
import numpy as numpy
import seaborn as sns

# HOG
from skimage.feature import hog
from skimage import exposure

# Regular expression
import re
from bs4 import BeautifulSoup


# Stop Words, Stemmer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')

#count Vectorizer and Tf-Idf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

## Neural Networks
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

#Model
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

# Test-Train Split
from sklearn.model_selection import train_test_split

#Model Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report





def helpImport():
  """
#General
import urllib.request
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas
import pandas as pd
import numpy as numpy


# HOG
from skimage.feature import hog
from skimage import exposure

# Regular expression
import re
from bs4 import BeautifulSoup


# Stop Words, Stemmer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')

#count Vectorizer and Tf-Idf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


#Model
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

# Test-Train Split
from sklearn.model_selection import train_test_split

#Model Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
  """



# Construct the path to the resource file
resource_file_path = os.path.join(current_dir, link)


def setLink(linki):
  global  link
  link=linki


def printLink():
  global  link
  print(link)


def printall():
  print(readData(link))



def printhead(dataSearch):
  printchead(link,dataSearch)


def printchead(link,dataSearch):
  strs=readData(link).split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      if dataSearch in segmentData[0]:
        if len(segmentData)>1:
          #print(segmentData[0])
          #print("\n")
          print(segmentData[1])
        else:
          print(segmentData[0])
          print("No Data")

def readData(linki):
  #print(linki)
  with urllib.request.urlopen(linki) as url:
      s = url.read()
      # I'm guessing this would output the html source code ?
      return s.decode()

def printheader():
  print(printcheader(link))

def printcheader(link):
  strs=readData(link).split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      print(segmentData[0])

def convert_to_alphanumeric(input_string):
    alphanumeric_string = ''.join(char for char in input_string if char.isalnum())
    return alphanumeric_string

def getData():
  global datadict
  file_contents=""
  file_path = resource_file_path  # Replace with the actual file path
  #print(file_path)
  try:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        #print(file_contents)
  except FileNotFoundError:
    print(f"File '{file_path}' not found.")
  except IOError:
    print(f"Error reading file '{file_path}'.")

  strs=file_contents.split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      if len(segmentData)==2:
        datadict[convert_to_alphanumeric(segmentData[0])] = segmentData[1]

getData()

def getKeys():
  return datadict.keys()

def println(key):
  print(datadict[key])


def displayImagesFromPath(imagePath=[],gstr=[]):
  """
  finalImages=[]
  for eachPath in imagePath:
    images=[]
    original,grayImage=readImage(eachPath)
    images.append(original)
    images.append(grayImage)
    finalImages.append(images)
  displayImages(finalImages,gstr)

  """
  finalImages=[]
  for eachPath in imagePath:
    images=[]
    original,grayImage=readImage(eachPath)
    images.append(original)
    images.append(grayImage)
    finalImages.append(images)
  displayImages(finalImages,gstr)


#User Defined Function to Display Images
def displayImages(images=[],gstr=[], fsize=(16, 16)):
  """
    newStr=[]
  if len(gstr) ==0:
    for eachImageIndex in range(len(gstr),len(images)):
      print(newStr)
      newStr.append("Image_"+ str(eachImageIndex) )
  else:
    newStr=gstr
  if (len(images)==0) or len(images) !=len(newStr):
    print("No images passed or argument length does not match")
    return
  else:
    # Create a 4x4 subplot grid
    print(len(images[0]),len(images))
    noOfRows=len(images[0])
    #print(images[2].shape)
    noOfColumns =len(images)
    fig, axes = plt.subplots(noOfRows, noOfColumns, figsize=fsize)

    counter=0
    # Fill the subplots with content (sample data in this case)
    for i in range(noOfColumns):
      for j in range(noOfRows):
        ax = axes[j, i]
        img=images[i][j]
        if len(img.shape)==3:
          img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
          ax.imshow(img)
        else:
          ax.imshow(img,"gray")
        if j==0:
          ax.set_title(newStr[i])

    # Adjust spacing between subplots
    #plt.tight_layout()

    # Show the plot
    plt.show()
  """
  newStr=[]
  if len(gstr) ==0:
    for eachImageIndex in range(len(gstr),len(images)):
      print(newStr)
      newStr.append("Image_"+ str(eachImageIndex) )
  else:
    newStr=gstr
  if (len(images)==0) or len(images) !=len(newStr):
    print("No images passed or argument length does not match")
    return
  else:
    # Create a 4x4 subplot grid
    print(len(images[0]),len(images))
    noOfRows=len(images[0])
    #print(images[2].shape)
    noOfColumns =len(images)
    fig, axes = plt.subplots(noOfRows, noOfColumns, figsize=fsize)

    counter=0
    #Fill the subplots with content (sample data in this case)
    for i in range(noOfColumns):
      for j in range(noOfRows):
        ax = axes[j, i]
        img=images[i][j]
        if len(img.shape)==3:
          img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
          ax.imshow(img)
        else:
          ax.imshow(img,"gray")
        if j==0:
          ax.set_title(newStr[i])

    # Adjust spacing between subplots
    #plt.tight_layout()

    # Show the plot
    plt.show()

#User Defined Function to Read Images
def readImage(ipImagePath):
  """
  Input :
    ipImagePath : The path of an image to read
  return
     cv2.imread(ipImagePath),cv2.imread(ipImagePath,cv2.IMREAD_GRAYSCALE)
     The orginal Image and Grayscale Image
  """
  return cv2.imread(ipImagePath),cv2.imread(ipImagePath,cv2.IMREAD_GRAYSCALE)



#User Defined Function to Sobel Edge Detection
def edge_applySobel(ipImage):
  """
  def applySobel(ipImage):
  sobel_image_x = cv2.Sobel(ipImage, cv2.CV_64F, 1, 0, ksize=5)
  sobel_image_y = cv2.Sobel(ipImage, cv2.CV_64F, 0, 1, ksize=5)
  sobel_magnitude_image = cv2.magnitude(sobel_image_x, sobel_image_y)
  return sobel_magnitude_image
  """
  sobel_image_x = cv2.Sobel(ipImage, cv2.CV_64F, 1, 0, ksize=5)
  sobel_image_y = cv2.Sobel(ipImage, cv2.CV_64F, 0, 1, ksize=5)
  sobel_magnitude_image = cv2.magnitude(sobel_image_x, sobel_image_y)
  return sobel_magnitude_image


#User Defined Function to resize Images
def resizeImage(ipImage, height=224,width=224):
  """
  def resizeImage(ipImage, height=new_height,width=new_width):
  return cv2.resize(ipImage, (height, width))
  """
  return cv2.resize(ipImage, (height, width))

#User Defined Function to Canny Edge Detection
def edge_applyCanny(ipImage,th_lower=100, th_upper=200):
  """
  def applyCanny(ipImage,th_lower=100, th_upper=200):
  return cv2.Canny(ipImage, th_lower, th_upper)
  """
  return cv2.Canny(ipImage, th_lower, th_upper)





## WATERSHED SEGMENTATION
def seg_watershedSegmentation(ipImage,th_lower=100, th_upper=200):
  """
    image=ipImage.copy()
  # Convert the image to gray scale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply thresholding
  ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

  # Noise removal using morphological operations
  kernel = np.ones((3, 3), np.uint8)
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

  # Sure background area
  sure_bg = cv2.dilate(opening, kernel, iterations=3)

  # Finding sure foreground area
  dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
  ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

  # Finding unknown region
  sure_fg = np.uint8(sure_fg)
  unknown = cv2.subtract(sure_bg, sure_fg)

  # Marker labelling
  ret, markers = cv2.connectedComponents(sure_fg)
  markers = markers + 1
  markers[unknown == 255] = 0

  # Apply watershed algorithm
  #markers = cv2.watershed(image, markers)
  #image[markers == -1] = [255, 255, 255]  # Color the boundaries in red

  # Apply watershed algorithm
  markers = cv2.watershed(image, markers)

  # Get unique segment labels
  unique_labels = np.unique(markers)

  # Assign a random color to each segment
  colors = np.random.randint(0, 255, size=(len(unique_labels), 3))

  # Color each segment in the original image
  for label, color in zip(unique_labels, colors):
      image[markers == label] = color
  """
  image=ipImage.copy()
  # Convert the image to gray scale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply thresholding
  ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

  # Noise removal using morphological operations
  kernel = np.ones((3, 3), np.uint8)
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

  # Sure background area
  sure_bg = cv2.dilate(opening, kernel, iterations=3)

  # Finding sure foreground area
  dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
  ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

  # Finding unknown region
  sure_fg = np.uint8(sure_fg)
  unknown = cv2.subtract(sure_bg, sure_fg)

  # Marker labelling
  ret, markers = cv2.connectedComponents(sure_fg)
  markers = markers + 1
  markers[unknown == 255] = 0

  # Apply watershed algorithm
  #markers = cv2.watershed(image, markers)
  #image[markers == -1] = [255, 255, 255]  # Color the boundaries in red

  # Apply watershed algorithm
  markers = cv2.watershed(image, markers)

  # Get unique segment labels
  unique_labels = np.unique(markers)

  # Assign a random color to each segment
  colors = np.random.randint(0, 255, size=(len(unique_labels), 3))

  # Color each segment in the original image
  for label, color in zip(unique_labels, colors):
      image[markers == label] = color
  return image



## REGION GROWNING
def seg_regionGrowing2(grayImage, threshold=50, seed_x_ratio=0.5, seed_y_ratio=0.5):
    """
    ## REGION GROWNING
def seg_regionGrowing2(grayImage, threshold=50, seed_x_ratio=0.5, seed_y_ratio=0.5):
    # Get the dimensions of the input grayscale image
    height, width = grayImage.shape

    # Calculate seed coordinates based on the ratios
    seed_x = int(height * seed_x_ratio)
    seed_y = int(width * seed_y_ratio)

    # Initialize a binary mask for the segmented region
    output_mask = np.zeros_like(grayImage, dtype=np.uint8)

    # Create a stack to keep track of pixels to be processed
    stack = [(seed_x, seed_y)]

    # Region growing process
    while stack:
        # Pop a pixel from the stack
        x, y = stack.pop()

        # Check if the pixel is within image bounds and has not been processed
        if 0 <= x < height and 0 <= y < width and output_mask[x, y] != 255:
            # Check intensity similarity with the seed pixel
            if abs(int(grayImage[x, y]) - int(grayImage[seed_x, seed_y])) <= threshold:
                # Add the pixel to the segmented region
                output_mask[x, y] = 255

                # Add neighboring pixels to the stack for further processing
                stack.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

    # Return the binary mask representing the segmented region
    return output_mask
    """
    # Get the dimensions of the input grayscale image
    height, width = grayImage.shape

    # Calculate seed coordinates based on the ratios
    seed_x = int(height * seed_x_ratio)
    seed_y = int(width * seed_y_ratio)

    # Initialize a binary mask for the segmented region
    output_mask = np.zeros_like(grayImage, dtype=np.uint8)

    # Create a stack to keep track of pixels to be processed
    stack = [(seed_x, seed_y)]

    # Region growing process
    while stack:
        # Pop a pixel from the stack
        x, y = stack.pop()

        # Check if the pixel is within image bounds and has not been processed
        if 0 <= x < height and 0 <= y < width and output_mask[x, y] != 255:
            # Check intensity similarity with the seed pixel
            if abs(int(grayImage[x, y]) - int(grayImage[seed_x, seed_y])) <= threshold:
                # Add the pixel to the segmented region
                output_mask[x, y] = 255

                # Add neighboring pixels to the stack for further processing
                stack.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

    # Return the binary mask representing the segmented region
    return output_mask


## K MEAN SEGMENTATION
def seg_kmeansSegment(grayImage,num_clusters=3):
  """
  ## K MEAN SEGMENTATION
def kmeansSegment(grayImage,num_clusters=3):
  # Reshape the image into a 2D array of pixels
  pixels = grayImage.reshape((-1, 1))  # Convert to 2D array of (B, G, R) values.
  print(pixels.shape)
  # Reshape the pixel array back to the original image shape
  reshaped_image = pixels.reshape(grayImage.shape)

  # Apply K-Means clustering
  kmeans = KMeans(n_clusters=num_clusters)
  kmeans.fit(pixels)
  labels = kmeans.labels_
  # Create an array of the same shape as the reshaped image to store the segmented result
  segmented_image = np.zeros_like(pixels)

  # Assign each pixel to its corresponding cluster center color
  for cluster_id in range(num_clusters):
    # Use boolean indexing to select pixels belonging to the current cluster
            segmented_image[labels == cluster_id] = kmeans.cluster_centers_[cluster_id]

  # Reshape the segmented image to match the original image shape
  segmented_image = segmented_image.reshape(grayImage.shape)

  # Assign a intensity color to each cluster
  cluster_colors = [0,127,255]

  # Convert the segmented image back to the original image data type
  segmented_image = segmented_image.astype(np.uint8)
  return segmented_image
  """
  # Reshape the image into a 2D array of pixels
  pixels = grayImage.reshape((-1, 1))  # Convert to 2D array of (B, G, R) values.
  print(pixels.shape)
  # Reshape the pixel array back to the original image shape
  reshaped_image = pixels.reshape(grayImage.shape)

  # Apply K-Means clustering
  kmeans = KMeans(n_clusters=num_clusters)
  kmeans.fit(pixels)
  labels = kmeans.labels_
  # Create an array of the same shape as the reshaped image to store the segmented result
  segmented_image = np.zeros_like(pixels)

  # Assign each pixel to its corresponding cluster center color
  for cluster_id in range(num_clusters):
    # Use boolean indexing to select pixels belonging to the current cluster
    segmented_image[labels == cluster_id] = kmeans.cluster_centers_[cluster_id]

  # Reshape the segmented image to match the original image shape
  segmented_image = segmented_image.reshape(grayImage.shape)

  # Assign a intensity color to each cluster
  cluster_colors = [0,127,255]

  # Convert the segmented image back to the original image data type
  segmented_image = segmented_image.astype(np.uint8)
  return segmented_image






def test_train_split(X,y,  test_size = 0.20):
  """
  def test_train_split(X,y,  test_size = 0.20):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
  return X_train, X_test, y_train, y_test
  """
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
  return X_train, X_test, y_train, y_test








## FEATURE EXTRACTION

def extract_contourbased(origImage,grayimage):
  """
  def contourbased(origImage,grayimage):
  # Apply a threshold to create a binary image
  _, binary_image = cv2.threshold(grayimage, 200, 255, cv2.THRESH_BINARY)
  # Find contours in the binary image
  contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # Iterate through the contours
  for contour in contours:
      # Calculate contour-based features
      area = cv2.contourArea(contour)
      perimeter = cv2.arcLength(contour, True)
  # Check if area is zero to avoid division by zero
  if area == 0:
          compactness = 0
  else:
          compactness = (perimeter ** 2) / (4 * np.pi * area)
  # Draw the contours on the original image (optional)
  contour_image = cv2.drawContours(origImage.copy(), contours, -1, (0, 255, 0), 2)
  contour_image2 = cv2.drawContours(np.zeros_like(origImage), contours, -1, (255, 255, 255), 3)
  return contour_image,contour_image2

  """
  # Apply a threshold to create a binary image
  _, binary_image = cv2.threshold(grayimage, 200, 255, cv2.THRESH_BINARY)
  # Find contours in the binary image
  contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # Iterate through the contours
  for contour in contours:
      # Calculate contour-based features
      area = cv2.contourArea(contour)
      perimeter = cv2.arcLength(contour, True)
  # Check if area is zero to avoid division by zero
  if area == 0:
          compactness = 0
  else:
          compactness = (perimeter ** 2) / (4 * np.pi * area)
  # Draw the contours on the original image (optional)
  contour_image = cv2.drawContours(origImage.copy(), contours, -1, (0, 255, 0), 2)
  contour_image2 = cv2.drawContours(np.zeros_like(origImage), contours, -1, (255, 255, 255), 3)
  return contour_image,contour_image2



#rom skimage import data, color
def extract_HOG(grayimage):
  """
  def HOG(grayimage):
      # Calculate HOG features
      fd, hog_image = hog(grayimage, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True)
      # HOG rescaled images
      hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
      return hog_image_rescaled
  """
  # Calculate HOG features
  fd, hog_image = hog(grayimage, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True)
  # HOG rescaled images
  hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
  return hog_image_rescaled



# IMAGE ENHANCEMENT

# User Defined Function for Contract Stretching
def enhance_contrast_stretching(ipImage):
    """
    def contrast_stretching(ipImage):

    r_min_intensity=0
    r_max_intensity=255
    g_min_intensity=0
    g_max_intensity=255
    b_min_intensity=0
    b_max_intensity=255

    b, g, r = cv2.split(ipImage)

    #b-channel
    b_stretched_image = ((b - np.max(b)) / (np.max(b) - np.min(b))) * (b_max_intensity - b_min_intensity) + b_min_intensity

    #g-channel
    g_stretched_image = ((g - np.max(g)) / (np.max(g) - np.min(g))) * (g_max_intensity - g_min_intensity) + g_min_intensity

    #r-channel
    r_stretched_image = ((r - np.max(r)) / (np.max(r) - np.min(r))) * (r_max_intensity - r_min_intensity) + r_min_intensity

    stretched_image = cv2.merge((b_stretched_image, g_stretched_image, r_stretched_image))
    stretched_image = np.uint8(stretched_image)
    return stretched_image
    """

    r_min_intensity=0
    r_max_intensity=255
    g_min_intensity=0
    g_max_intensity=255
    b_min_intensity=0
    b_max_intensity=255

    b, g, r = cv2.split(ipImage)

    #b-channel
    b_stretched_image = ((b - np.max(b)) / (np.max(b) - np.min(b))) * (b_max_intensity - b_min_intensity) + b_min_intensity

    #g-channel
    g_stretched_image = ((g - np.max(g)) / (np.max(g) - np.min(g))) * (g_max_intensity - g_min_intensity) + g_min_intensity

    #r-channel
    r_stretched_image = ((r - np.max(r)) / (np.max(r) - np.min(r))) * (r_max_intensity - r_min_intensity) + r_min_intensity

    stretched_image = cv2.merge((b_stretched_image, g_stretched_image, r_stretched_image))
    stretched_image = np.uint8(stretched_image)
    return stretched_image


# User Defined Function for Histogram Equalization
def enhance_histogram_equalization(ipImage):
    """
    def histogram_equalization(ipImage):
    b, g, r = cv2.split(ipImage)
    b_equalized = cv2.equalizeHist(b)
    g_equalized = cv2.equalizeHist(g)
    r_equalized = cv2.equalizeHist(r)
    enhanced_image = cv2.merge((b_equalized, g_equalized, r_equalized))
    return enhanced_image
    """
    b, g, r = cv2.split(ipImage)
    b_equalized = cv2.equalizeHist(b)
    g_equalized = cv2.equalizeHist(g)
    r_equalized = cv2.equalizeHist(r)
    enhanced_image = cv2.merge((b_equalized, g_equalized, r_equalized))
    return enhanced_image

# User Defined Function for Intensity Level Slicing
def enhance_intensityLevelSlicing(ipImage):
  """
    lower_bound = 180
  upper_bound = 255
  grayImage=cv2.cvtColor(ipImage, cv2.COLOR_BGR2GRAY)
  mask = np.zeros_like(ipImage)
  mask[(grayImage >= lower_bound) & (grayImage <= upper_bound)] = 255

  sliced_image = cv2.bitwise_and(ipImage, mask)
  return sliced_image
  """
  lower_bound = 180
  upper_bound = 255
  grayImage=cv2.cvtColor(ipImage, cv2.COLOR_BGR2GRAY)
  mask = np.zeros_like(ipImage)
  mask[(grayImage >= lower_bound) & (grayImage <= upper_bound)] = 255

  sliced_image = cv2.bitwise_and(ipImage, mask)
  return sliced_image

# User Defined Function for Gamma Correcton
def enhance_gamma_correction(image, gamma=1.5):
    """
    def gamma_correction(image, gamma=1.5):
    look_up_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype('uint8')
    return cv2.LUT(image, look_up_table)
    """
    look_up_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype('uint8')
    return cv2.LUT(image, look_up_table)




def nlp_clean_text(input_string):
    """
    def clean_text(input_string):
      # Step 1: Remove HTML tags using BeautifulSoup
      soup = BeautifulSoup(input_string, "html.parser")
      cleaned_text = soup.get_text()

      # Step 2: Remove special characters using regex
      cleaned_text = re.sub(r"[^a-zA-Z\s]", "", cleaned_text)

      # Optionally, remove extra whitespaces
      cleaned_text = " ".join(cleaned_text.split())
      #cleaned_text = cleaned_text.replace(" .","")

      cleaned_text=cleaned_text.lower()


      return cleaned_text
    """
    # Step 1: Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(input_string, "html.parser")
    cleaned_text = soup.get_text()

    # Step 2: Remove special characters using regex
    cleaned_text = re.sub(r"[^a-zA-Z\s]", "", cleaned_text)

    # Optionally, remove extra whitespaces
    cleaned_text = " ".join(cleaned_text.split())
    #cleaned_text = cleaned_text.replace(" .","")

    cleaned_text=cleaned_text.lower()


    return cleaned_text

def nlp_remove_stopwords(input_text):
    """
    def nlp_remove_stopwords(input_text):
    # Tokenize the input text into words
    words = nltk.word_tokenize(input_text)

    # Get the list of English stop words
    stop_words = set(stopwords.words("english"))

    # Remove stop words from the list of words
    filtered_words = [word for word in words if word not in stop_words]

    # Join the filtered words back into a string
    cleaned_text = " ".join(filtered_words)

    return cleaned_text
    """
    # Tokenize the input text into words
    words = nltk.word_tokenize(input_text)

    # Get the list of English stop words
    stop_words = set(stopwords.words("english"))

    # Remove stop words from the list of words
    filtered_words = [word for word in words if word not in stop_words]

    # Join the filtered words back into a string
    cleaned_text = " ".join(filtered_words)

    return cleaned_text

def nlp_apply_stemming(input_text):
    """
    def nlp_apply_stemming(input_text):
    # Initialize the Porter stemmer
    stemmer = PorterStemmer()

    # Tokenize the input text into words
    words = nltk.word_tokenize(input_text)

    # Apply stemming to each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Join the stemmed words back into a string
    stemmed_text = " ".join(stemmed_words)

    return stemmed_text
    """
    # Initialize the Porter stemmer
    stemmer = PorterStemmer()

    # Tokenize the input text into words
    words = nltk.word_tokenize(input_text)

    # Apply stemming to each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Join the stemmed words back into a string
    stemmed_text = " ".join(stemmed_words)

    return stemmed_text

def visualize_wordcloud(df, textCol, classCol):
  """
  def visualize_wordcloud(df, textCol, classCol):
  from collections import Counter
  from wordcloud import WordCloud, ImageColorGenerator
  pos_data = df.loc[df[classCol] == 1]
  pos_head_lines = pos_data[textCol]
  words = [eachword for eachheadline in pos_head_lines for eachword in eachheadline.split()]
  word_could_dict=Counter(words)

  wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)
  plt.figure(figsize=(15,8))
  plt.imshow(wordcloud)
  plt.axis("off")
  """
  from collections import Counter
  from wordcloud import WordCloud, ImageColorGenerator
  pos_data = df.loc[df[classCol] == 1]
  pos_head_lines = pos_data[textCol]
  words = [eachword for eachheadline in pos_head_lines for eachword in eachheadline.split()]
  word_could_dict=Counter(words)

  wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)
  plt.figure(figsize=(15,8))
  plt.imshow(wordcloud)
  plt.axis("off")


def visualize_history(history):
  """
  def visualize_history(history):
  # Plot results
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']
  loss = history.history['loss']
  val_loss = history.history['val_loss']

  epochs = range(1, len(acc)+1)

  plt.plot(epochs, acc, 'g', label='Training accuracy')
  plt.plot(epochs, val_acc, 'r', label='Validation accuracy')
  plt.title('Training and validation accuracy')
  plt.legend()

  plt.figure()

  plt.plot(epochs, loss, 'g', label='Training loss')
  plt.plot(epochs, val_loss, 'r', label='Validation loss')
  plt.title('Training and validation loss')
  plt.legend()
  plt.show()
  """
  # Plot results
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']
  loss = history.history['loss']
  val_loss = history.history['val_loss']

  epochs = range(1, len(acc)+1)

  plt.plot(epochs, acc, 'g', label='Training accuracy')
  plt.plot(epochs, val_acc, 'r', label='Validation accuracy')
  plt.title('Training and validation accuracy')
  plt.legend()

  plt.figure()

  plt.plot(epochs, loss, 'g', label='Training loss')
  plt.plot(epochs, val_loss, 'r', label='Validation loss')
  plt.title('Training and validation loss')
  plt.legend()
  plt.show()

def visualize_classificationEvaluation(y_test,y_pred,target_names = ['No', 'Yes']):
  """
  def model_classificationEvaluation(y_test,y_pred):
  confusion_m=confusion_matrix(y_test,y_pred)
  accuracy=accuracy_score(y_test,y_pred)
  print(classification_report(y_test,y_pred))
  return confusion_m,accuracy
  """
  confusion_m=confusion_matrix(y_test,y_pred)
  accuracy=accuracy_score(y_test,y_pred)
  # Plot Confusion Matrix
  sns.heatmap(confusion_m, annot=True, cbar=False, fmt='d', cmap='Blues')
  plt.ylabel('True Label')
  plt.xlabel('Predicted Label')
  plt.title('Confusion Matrix')
  plt.show()
  print(classification_report(y_test,y_pred), target_names=target_names)
  return confusion_m,accuracy

def vector_BOW(X_text,y,max_features=5000):
  """
  def vector_BOW(X_text,y)
  cv = CountVectorizer(max_features=max_features)
  #  X = cv.fit_transform(df["Review"].values).toarray()
  X = cv.fit_transform(X_text).toarray()
  #  y=df["col"].values
  bow = cv.get_feature_names_out()
  return X,y,bow
  """
  cv = CountVectorizer(max_features=max_features)
  #  X = cv.fit_transform(df["Review"].values).toarray()
  X = cv.fit_transform(X_text).toarray()
  #  y=df["col"].values
  bow = cv.get_feature_names_out()
  return cv,X,y,bow

def vector_Tokenize_textToSequence(X,max_words = 1000):
  """
  def vector_Token_padToSequence(X,max_words = 1000):
  # Tokenization
  tokenizer = Tokenizer(num_words=max_words)
  tokenizer.fit_on_texts(X)
  X_sequences = tokenizer.texts_to_sequences(X)
  return tokenizer,X_sequences
  """
  # Tokenization
  tokenizer = Tokenizer(num_words=max_words)
  tokenizer.fit_on_texts(X)
  X_sequences = tokenizer.texts_to_sequences(X)
  return tokenizer,X_sequences

def vector_tfidf(X_text,y,max_features=5000):
  """
  def vector_tfidf(X_text,y,max_features=5000):
  tv = TfidfVectorizer(max_features=5000)
  #X = tv.fit_transform(df_sentiment["Review_processed"].values).toarray()
  #y=df_sentiment["Sentiment"].values
  
  X = tv.fit_transform(X_text).toarray()
  tfidf = tv.get_feature_names_out()
  return X,y,tfidf
  """
  tv = TfidfVectorizer(max_features=5000)
  #X = tv.fit_transform(df_sentiment["Review_processed"].values).toarray()
  #y=df_sentiment["Sentiment"].values
  
  X = tv.fit_transform(X_text).toarray()
  tfidf = tv.get_feature_names_out()
  return tv,X,y,tfidf


def model_MultinomialNB(X_train, y_train,X_test):
  """
  def model_MultinomialNB(X_train, y_train,X_test):
  model = MultinomialNB().fit(X_train, y_train)
  y_pred=model.predict(X_test)
  return model, y_pred
  """
  model = MultinomialNB().fit(X_train, y_train)
  y_pred=model.predict(X_test)
  return model, y_pred




def example_seg():
  """
# Read Images, Convert to grayscale,  Resize Image, Sobel and Canny Edge detection.
origImages=[]
watershedSegments=[]
kmeansSegments=[]
regionGrowings=[]

for eachPath in range(len(imagePath)):
  #Read Images
  origImage,grayImage=readImage(imagePath[eachPath])

  #Apply watershedSegment
  watershedSegment=seg_watershedSegmentation(origImage)

  #Apply watershedSegment
  kmeansSeg=seg_kmeansSegment(grayImage)

  #Apply   regionGrowing
  regionGrowing=seg_regionGrowing2(grayImage)


  origImages.append(origImage)
  watershedSegments.append(watershedSegment)
  kmeansSegments.append(kmeansSeg)
  regionGrowings.append(regionGrowing)

displayImages([origImages,watershedSegments,regionGrowings,kmeansSegments],["Original","watershed","RegionGrow","kmeans(3)"])
"""


def exmaple_extract():
  """
  # Read Images, Convert to grayscale,  Resize Image, Sobel and Canny Edge detection.
origImages=[]
countourBaseds=[]
countourBasedscts=[]
hogImages=[]
for eachPath in range(len(imagePath)):
  #Read Images
  origImage,grayImage=imutil.readImage(imagePath[eachPath])

  #Apply countourBased
  countourBased,countourBasedsct=imutil.extract_contourbased(origImage,grayImage)

  #Apply HOG
  hogImage=imutil.extract_HOG(grayImage)

  origImages.append(origImage)
  countourBaseds.append(countourBased)
  countourBasedscts.append(countourBasedsct)
  hogImages.append(hogImage)

imutil.displayImages([origImages,countourBaseds,countourBasedscts,hogImages],["Original","countour","counter_features","hogImages"],fsize=(16,5))
  """

def example_edge():
  """
  # Read Images, Convert to grayscale,  Resize Image, Sobel and Canny Edge detection.
origImages=[]
grayImages=[]
resizedImages=[]
cannyImages=[]
sobelImages=[]
for eachPath in range(len(imagePath)):
  #Read Images
  origImage,grayImage=readImage(imagePath[eachPath])

  #Resize Image to 400 x 400
  resizedImage=resizeImage(grayImage,600,400)

  #Apply Canny
  cannyImage=applyCanny(resizedImage)

  #Apply Sobel
  sobelImage=applySobel(resizedImage)

  origImages.append(origImage)
  grayImages.append(grayImage)
  resizedImages.append(resizedImage)
  cannyImages.append(cannyImage)
  sobelImages.append(sobelImage)

displayImages([origImages,grayImages,resizedImages],["Original","Gray","Resized"])
  """


def example_enhance():
  """
  # Read Images, Convert to grayscale,  Resize Image, Contrast Stretching, Histogram Equilization adn Intensity Level Slicing
origImages=[]
grayImages=[]
resizedImages=[]
histImages=[]
gammaImages=[]
contrastStretchImages=[]
intensityImages=[]

for eachPath in range(len(imagePath)):
  #Read Images
  origImage,grayImage=readImage(imagePath[eachPath])

  #Resize Image to 400 x 400
  resizedImage=resizeImage(origImage,600,400)

  #Apply Historgram Equilization
  histImage=histogram_equalization(resizedImage)

  #Apply  Contract Stretching
  contrastStretchImage=contrast_stretching(resizedImage)

  # Apply Intensity Level Correction
  intensityImage=intensityLevelSlicing(resizedImage)

  origImages.append(origImage)
  grayImages.append(grayImage)
  resizedImages.append(resizedImage)
  contrastStretchImages.append(contrastStretchImage)
  histImages.append(histImage)
  intensityImages.append(intensityImage)

displayImages([origImages,resizedImages,histImages,intensityImages,contrastStretchImages],["Original","Resized","Histogram Equilization","Intensity Sliced","Contract Stretched"])


  """

def example_myReview(myreview, cv,model,label_mapping = {0: 'negative', 1: 'positive'}):
  """
  def example_myReview(myreview, cv,model,label_mapping = {0: 'negative', 1: 'positive'}):
  print("Input : ",myreview)

  myreview_preprocess=nlp_clean_text(myreview)
  print("cleaning : ",myreview_preprocess)

  myreview_preprocess=nlp_remove_stopwords(myreview_preprocess)
  print("Remove StopWords : ",myreview_preprocess)

  myreview_preprocess=nlp_apply_stemming(myreview_preprocess)
  print("Apply Stemming : ",myreview_preprocess)

  myX=cv.transform([myreview_preprocess]).toarray()
  print("Model Features : ",myX)

  mypredict=model.predict(myX)
  

  # Create a function to convert label-encoded list to normal form
  def decode_labels(encoded_list, label_mapping):
      decoded_list = [label_mapping[label] for label in encoded_list]
      return decoded_list

  # Call the function to decode the list
  decoded_mypredict = decode_labels(mypredict, label_mapping)
  print("Prediction:  : ",decoded_mypredict)
  """


  print("Input : ",myreview)

  myreview_preprocess=nlp_clean_text(myreview)
  print("cleaning : ",myreview_preprocess)

  myreview_preprocess=nlp_remove_stopwords(myreview_preprocess)
  print("Remove StopWords : ",myreview_preprocess)

  myreview_preprocess=nlp_apply_stemming(myreview_preprocess)
  print("Apply Stemming : ",myreview_preprocess)

  myX=cv.transform([myreview_preprocess]).toarray()
  print("Model Features : ",myX)

  mypredict=model.predict(myX)
  

  # Create a function to convert label-encoded list to normal form
  def decode_labels(encoded_list, label_mapping):
      decoded_list = [label_mapping[label] for label in encoded_list]
      return decoded_list

  # Call the function to decode the list
  decoded_mypredict = decode_labels(mypredict, label_mapping)
  print("Prediction:  : ",decoded_mypredict)









def example_predict(myreview, tokenizer, model,max_words=50):
  """
  def example_predict(myreview, tokenizer, model,max_words=50):
  print("Input : ",myreview)

  myreview_preprocess=nlp_clean_text(myreview)
  print("cleaning : ",myreview_preprocess)


  myX=tokenizer.texts_to_sequences([myreview_preprocess])
  myX_padded = pad_sequences(myX, maxlen=max_words)

  mypredict=model.predict(myX_padded)
  label_mapping = {0: 'Not a Sarcasm', 1: 'Sarcasm'}
  print(mypredict)

  threshold = 0.5  # Change this to your desired threshold
  mypredict = [1 if x > threshold else 0 for x in mypredict]

  # Create a function to convert label-encoded list to normal form
  def decode_labels(encoded_list, label_mapping):
      decoded_list = [label_mapping[label] for label in encoded_list]
      return decoded_list

  # Call the function to decode the list
  decoded_mypredict = decode_labels(mypredict, label_mapping)
  print("Prediction:  : ",decoded_mypredict)
  """
  print("Input : ",myreview)

  myreview_preprocess=nlp_clean_text(myreview)
  print("cleaning : ",myreview_preprocess)


  myX=tokenizer.texts_to_sequences([myreview_preprocess])
  myX_padded = pad_sequences(myX, maxlen=max_words)

  mypredict=model.predict(myX_padded)
  label_mapping = {0: 'No', 1: 'Yes'}
  print(mypredict)

  threshold = 0.5  # Change this to your desired threshold
  mypredict = [1 if x > threshold else 0 for x in mypredict]

  # Create a function to convert label-encoded list to normal form
  def decode_labels(encoded_list, label_mapping):
      decoded_list = [label_mapping[label] for label in encoded_list]
      return decoded_list

  # Call the function to decode the list
  decoded_mypredict = decode_labels(mypredict, label_mapping)
  print("Prediction:  : ",decoded_mypredict)



def example_model_lstm(X_train, X_test,y_train,y_test,inputLen=50,max_words=1000):
  """
  def example_model_lstm(X_train, X_test,y_train,y_test,inputLen=50,max_words=1000)
  # Build LSTM Model
  embedding_dim = 50
  lstm_units = 100
  X_train_padded = pad_sequences(X_train, maxlen=inputLen)
  X_test_padded = pad_sequences(X_test, maxlen=inputLen)

  model = Sequential()
  model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=inputLen))
  model.add(LSTM(units=lstm_units, dropout=0.2, recurrent_dropout=0.25)))
  model.add(Dense(1, activation='sigmoid'))

  # Compile the model
  model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  # Train the model
  history= model.fit(X_train_padded, y_train, epochs=10, batch_size=32, validation_split=0.1)

  # Evaluate the model
  loss, accuracy = model.evaluate(X_test_padded, y_test)
  return model, history, loss, accuracy
  """
  # Build LSTM Model
  embedding_dim = 50
  lstm_units = 100
  X_train_padded = pad_sequences(X_train, maxlen=inputLen)
  X_test_padded = pad_sequences(X_test, maxlen=inputLen)

  model = Sequential()
  model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=inputLen))
  model.add(LSTM(units=lstm_units, dropout=0.2, recurrent_dropout=0.25))
  model.add(Dense(1, activation='sigmoid'))

  # Compile the model
  model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  # Train the model
  history= model.fit(X_train_padded, y_train, epochs=10, batch_size=32, validation_split=0.1)

  # Evaluate the model
  loss, accuracy = model.evaluate(X_test_padded, y_test)
  return model, history, loss, accuracy







def downloadFromKaggle(apiurl):
  """
  def downloadFromKaggle(apiurl):
  import opendatasets as od
  od.download("apiurl")
  """
  import opendatasets as od
  od.download("apiurl")




