import cv2
import os
import sqlite3
from multiprocessing import Pool


def process_image(img_path):
    # Open image
    image = cv2.imread(img_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply noise reduction filter
    smooth_img = cv2.bilateralFilter(gray, 11, 21, 69)

    # Detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(smooth_img, scaleFactor=1.03, minNeighbors=5, minSize=(230, 230))

    # Store processed image and faces
    img_name = os.path.basename(img_path)
    img_name_no_ext = os.path.splitext(img_name)[0]

    processed_img_dir = 'output/processed_images'
    face_dir = 'output/faces'

    os.makedirs(processed_img_dir, exist_ok=True)
    os.makedirs(face_dir, exist_ok=True)

    processed_img_path = os.path.join(processed_img_dir, img_name)
    face_paths = []

    # Save processed image and faces
    cv2.imwrite(processed_img_path, smooth_img)

    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        face_path = os.path.join(face_dir, f'{img_name_no_ext}_face{i}.jpg')
        cv2.imwrite(face_path, face)
        face_paths.append(face_path)

    return img_name, os.path.getsize(img_path), os.path.getsize(processed_img_path), len(faces), face_paths


def process_images(image_folder):
    # Create a pool of worker processes
    pool = Pool()

    # Get the list of image files
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

    # Process images in parallel
    results = pool.map(process_image, image_files)

    # Save results to the in-memory database
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    c.execute('''CREATE TABLE image_data (
                    name TEXT PRIMARY KEY,
                    size INTEGER,
                    processed_size INTEGER,
                    num_faces INTEGER,
                    face_paths TEXT
                  )''')

    for img_name, size, processed_size, num_faces, face_paths in results:
        c.execute("INSERT INTO image_data VALUES (?, ?, ?, ?, ?)",
                  (img_name, size, processed_size, num_faces, ','.join(face_paths)))

    conn.commit()

    return conn


def generate_report(conn):
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM image_data")
    total_images = c.fetchone()[0]

    c.execute("SELECT AVG(num_faces) FROM image_data")
    avg_faces = c.fetchone()[0]

    c.execute("SELECT AVG(size), AVG(processed_size) FROM image_data")
    avg_size, avg_processed_size = c.fetchone()

    print("<----------------- Report  ------------------>")
    print(f"Total images processed: {total_images}")
    print(f"Average number of faces detected per image: {avg_faces:.2f}")
    print(f"Average input file size: {avg_size:.2f} bytes")
    print(f"Average processed file size: {avg_processed_size:.2f} bytes")


if __name__ == '__main__':
    image_folder = 'images'

    conn = process_images(image_folder)
    generate_report(conn)

    conn.close()
