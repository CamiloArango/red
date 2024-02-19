Eyes Taped Flask App
This Flask application allows users to upload photos and automatically cover the eyes with tape. It utilizes the MTCNN (Multi-Task Cascaded Convolutional Networks) model for face detection and image processing.

Installation and Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/eyes-taped.git
Navigate to the project directory:

bash
Copy code
cd eyes-taped
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Flask application:

bash
Copy code
python app.py
Access the application via your web browser at http://localhost:5000/red.

Usage
Upload photos where the eyes are clearly visible.
Choose a tape color from the dropdown menu.
Click or drag and drop the image to cover the eyes with tape.
Process the image to see the result.
Download the processed image if satisfied.
File Structure
app.py: Main Flask application file containing the backend logic.
index.html: HTML template for the user interface.
script.js: JavaScript file for client-side functionality.
style.css: CSS file for styling the interface.
static/: Directory containing static files such as images and CSS.
error.log: Log file for error logging.
Dependencies
Flask: Web framework for Python.
OpenCV: Library for computer vision and image processing.
MTCNN: Multi-Task Cascaded Convolutional Networks for face detection.
Bootstrap: Front-end CSS framework for responsive design.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Camilo Arango

Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

Support
If you find any issues or have any questions, please open an issue.
