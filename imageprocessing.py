# TASK #
'''Problem: Image Processing and Analysis
You are given a folder containing a set of images in JPG format.
Your task is to write a Python script that performs the following operations:
Read all the images from the folder and create a list of image objects.
Implement a context manager that opens each image file and ensures it is closed properly after processing.
Use the concurrent.futures module to parallelize the image processing tasks across multiple CPU cores.
For each image, perform the following operations concurrently:
Convert the image to grayscale using image processing libraries like PIL or OpenCV.
Apply a noise reduction filter to the grayscale image.
Detect and extract faces from the processed image using a face detection algorithm or library.
Store the processed images and their corresponding face images in separate folders.
Use a database library (e.g., sqlite3 or an ORM like SQLAlchemy) to store metadata about the processed images,
 such as the image name, original size, processed size, and number of faces detected.
Generate a report summarizing the image processing results, including the total number of images processed,
 the average number of faces detected per image, and any other relevant statistics.'''
######################### Code BELOW ####################################################################
import time
import numpy as np
import imutils
import cv2
import multiprocessing
import os
import glob
import sqlite3
from runstats import RunStats


# easy way to load images using queue
def load_img(direct, q):
    try:
        img = cv2.imread(os.path.join("images/", direct), cv2.IMREAD_GRAYSCALE)
        q.put(img)
    except SystemError:
        print("Couldn't load images")


# let's apply noise reduction easily
def noise_reduction_filter(image):
    kernel = (3, 3)

    # makes dark images brighter
    #  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(image, 13, 100, 100)

    clahe = cv2.createCLAHE(2, kernel)
    edges = clahe.apply(blur)
    erode = cv2.erode(edges, kernel)
    dilate = cv2.dilate(erode, kernel)
    #    threshold = cv2.adaptiveThreshold(edges,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 4)
    # Removes white spaces and detach connected objects

    return dilate


if __name__ == '__main__':
    # helps count how many faces we have
    global i
    i = 0
    start = time.time()
    # Paths used:
    inputFiles = "images//"
    outputFaces = os.path.join("output", "facedata")
    outputImages = os.path.join("output", "noisereduced")

    # used for stats report
    totalFileSize = 0
    totalOutFile = 0
    facesdetected = []

    # initializes our databse
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("""CREATE TABLE imgdatas (
                        name text,
                        size integer,
                        procsize integer,
                        facedetections integer
                        )""")
    conn.commit()

    # function for average
    def average(total, items):
        mean = 0
        if items != 0:
            mean = total / items
        return mean


    def detect_faces(image):
        global i
        facesDetected = face_cascade.detectMultiScale(image, scaleFactor=1.03,
                                                      minNeighbors=5, minSize=(230, 230), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(facesDetected) > 0:

            for (x, y, w, h) in facesDetected:
                # cuts out faces from image
                face = loadedImage[y:y + h, x:x + w]

                # writes faces to disk
                cv2.imwrite(f'output//facedata//face{i}.jpg', face)
                i += 1
            facesdetected.append(facesDetected)
        return facesDetected

    # func for server stats
    def add_stats(stat):
        with conn:
            c.execute("INSERT INTO imgdatas VALUES (:name, :size, :procsize, :facedetections)",
                      {"name": stat.name, "size": stat.insize, "procsize": stat.outsize,
                       "facedetections": stat.numfaces})


    def run_image_proc(imagePath, q):
        try:
            # loads images using multiple processes/cpu cores
            proc = multiprocessing.Process(target=load_img, args=(imagePath, q))
            proc.start()
            processes.append(proc)

        except RuntimeError:
            print("Sorry, there seems to have been an error, please check for circular reasoning or looped process.")
        image = q.get()
        h, w = image.shape[:2]
        resized = imutils.resize(image, width=round(w * 3 / 4), height=round(h * 3 / 4), inter=cv2.INTER_AREA)
        return noise_reduction_filter(resized)


    queue = multiprocessing.Queue()

    # gets all the images in the folder
    path = os.listdir(inputFiles)
    imageFiles = []
    count = 0

    processes = []
    # Loads our face detection files
    face_cascade = cv2.CascadeClassifier(
        "haarcascade_frontalface_alt2.xml")  # cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # if the folder dont exist then it creates the output folders
    try:
        os.makedirs(outputFaces)
        os.makedirs(outputImages)

    except FileExistsError:
        pass

    # tries to clear the path
    for imgPath in path:
        files = glob.glob(outputImages + os.sep + "*")
        if count == 0:
            print(True)
            for f in files:
                os.remove(f)
            files = glob.glob(outputFaces + os.sep + "*")
            for f in files:
                os.remove(f)
        count += 1

        loadedImage = run_image_proc(imgPath, queue)

        imageFiles.append(loadedImage)

        # applies smoothing &  Applies noise reduction filters

        # writes the smoothened images to disk
        cv2.imwrite(f"output//noisereduced//{imgPath}{count}.jpg", loadedImage)

        ############################### FACE DETECTION ###############################################

        faces = detect_faces(loadedImage)

        # formats our run stats
        filestats = RunStats(name=imgPath, insize=os.path.getsize("images/" + imgPath) // 1000,
                             outsize=os.path.getsize(f"output//noisereduced//{imgPath}{count}.jpg") // 1000,
                             numfaces=len(faces))
        add_stats(filestats)

    # ends processes
    for p in processes:
        p.join()

    # Gets the filestats for console
    c.execute("""SELECT * from imgdatas""")

    # Gets metadata from sqlite3 server to use in stats and for user to see
    for imgstat in c.fetchall():
        print(
            f"Name: {imgstat[0]}, Input Size (in kb): {imgstat[1]}, Output Size (in kb): {imgstat[2]}, Faces Detected: {imgstat[3]} \n")
        totalFileSize += imgstat[1]
        totalOutFile += imgstat[2]
    end = time.time()

    # Writes a report
    print("<----------------- Report  ------------------>")
    print("Total faces detected: " + str(i))
    print("Number of images processed: " + str(len(imageFiles)))
    print("Average number of faces detected: " + str(average(i + 1, len(facesdetected))))
    print("Average input file size: " + str(average(totalFileSize, len(imageFiles))) + " KB")
    print("Average output file size: " + str(average(totalOutFile, len(imageFiles))) + " KB")
    print("Runtime: " + str(end - start) + " seconds")
    conn.close()
