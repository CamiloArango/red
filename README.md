# Eyes Taped

This is a Flask web application that allows users to upload photos and apply virtual tape over the eyes in the uploaded images. The application uses the MTCNN (Multi-Task Cascaded Convolutional Neural Network) model for face detection.

## Features

- Upload photos where eyes are clearly visible.
- Select from different tape options to cover the eyes.
- Process uploaded images to apply tape over the eyes.
- Download the processed images.

## How to Use

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/eyes-taped.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python app.py
    ```

4. Open your web browser and go to [http://localhost:5000/red](http://localhost:5000/red).

5. Drag and drop your photo into the designated area or click to select a file.
6. Choose the tape color from the dropdown menu.
7. Click on the "Process Image" button.
8. Once processed, you can download the image with the tape applied.

## Dependencies

- Flask
- OpenCV
- MTCNN
- NumPy

## File Structure

- `app.py`: Flask application file containing server-side logic.
- `index.html`: HTML template for the front-end interface.
- `script.js`: JavaScript file handling client-side functionality.
- `style.css`: CSS file for styling the web interface.

## Credits

- This project utilizes the MTCNN model for face detection.

## License

[MIT License](LICENSE)
