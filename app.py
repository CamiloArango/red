import logging
from flask import Flask, request, send_file, render_template, Response, jsonify
import cv2
from mtcnn import MTCNN
import numpy as np
import io
import os
import traceback

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Load the MTCNN model
detector = MTCNN()

class ImageCounter:
    def __init__(self):
        self.count = 0
        self.filename = 'image_count.txt'

        # Load count from file if the file exists
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.count = int(f.read())

    def increment(self):
        self.count += 1
        self.save_count()

    def get_count(self):
        return self.count

    def save_count(self):
        with open(self.filename, 'w') as f:
            f.write(str(self.count))

image_counter = ImageCounter()

@app.route('/red')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        image_counter.increment()
        # Load the uploaded image
        file = request.files['image']
        filename = file.filename  # Get the original filename

        # Convert the image stream to OpenCV format
        image_stream = io.BytesIO()
        file.save(image_stream)
        image_stream.seek(0)
        image = np.frombuffer(image_stream.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Convert image to RGB (MTCNN works with RGB images)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces in the image
        faces = detector.detect_faces(image_rgb)

        # Get the selected tape image option from the request
        selected_tape = request.form['selected_tape']  # Assuming it's sent as a form field

        # Load the selected tape image
        tape_image_path = f'static/images/tapes/{selected_tape}.png'
        tape_image = cv2.imread(tape_image_path, cv2.IMREAD_UNCHANGED)

        # Iterate through each face and cover the eyes with tape
        for face in faces:
            keypoints = face['keypoints']
            
            # Get the coordinates of the eyes
            left_eye_x, left_eye_y = keypoints['left_eye']
            right_eye_x, right_eye_y = keypoints['right_eye']
            
            # Calculate the dimensions and position to place the tape over each eye
            tape_width = int(np.abs(right_eye_x - left_eye_x) * 3.25)
            tape_height = int(tape_width * tape_image.shape[0] / tape_image.shape[1])
            tape_x = int((left_eye_x + right_eye_x) / 2 - tape_width / 2)
            tape_y = int((left_eye_y + right_eye_y) / 2 - tape_height / 2)
            
            # Resize the tape image to fit the dimensions
            resized_tape = cv2.resize(tape_image, (tape_width, tape_height))
            
            # Extract the alpha channel of the tape image
            tape_alpha = resized_tape[:, :, 3] / 255.0
            
            # Overlay the tape image onto the original image
            for c in range(3):  # Loop over RGB channels
                image[tape_y:tape_y+tape_height, tape_x:tape_x+tape_width, c] = \
                    (1 - tape_alpha) * image[tape_y:tape_y+tape_height, tape_x:tape_x+tape_width, c] + \
                    tape_alpha * resized_tape[:, :, c]  # No need to multiply by 255

        # Encode the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', image)

        # Convert to bytes
        img_bytes = img_encoded.tobytes()

        # Manually set the Content-Disposition header
        headers = {
            "Content-Disposition": f"attachment; filename={filename}"
        }

        return Response(img_bytes, mimetype='image/jpeg', headers=headers)

    except Exception as e:
        # Log the error with traceback
        logging.error(f"An error occurred: {traceback.format_exc()}")
        # Return a response indicating failure
        return Response("An error occurred while processing the image.", status=500)

@app.route('/image_count')
def get_image_count():
    return jsonify({'count': image_counter.get_count()})

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=False)
