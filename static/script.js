document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const uploadArea = document.getElementById('upload-area');
    const imagePreview = document.getElementById('image-preview');
    const uploadText = document.getElementById('upload-text');
    const uploadIcon = document.getElementById('upload-icon');
    const fileInput = document.getElementById('upload-btn');
    const processButton = document.getElementById('process-btn');
    const downloadBtn = document.getElementById('download-btn');
    const processedImgPreview = document.getElementById('processed-image-preview');
    const tapeOptions = document.getElementById('tape-options');

    // Function to handle drag over event
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    // Function to handle drag leave event
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    // Function to handle drop event
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        const selectedTape = tapeOptions.value; // Get the selected tape option
        if (file) {
	    processImage(file, selectedTape)
            displayAndProcessImage(file, selectedTape); // Pass the selected tape option
        }
    });

    // Function to handle file input change event
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        const selectedTape = tapeOptions.value;
        if (file) {
            displayAndProcessImage(file, selectedTape);
        }
    });

    // Function to handle click event on the "Process Image" button
    processButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        const selectedTape = tapeOptions.value;
        if (file) {
            processImage(file, selectedTape);
        }
    });

    // Function to display image and process
    function displayAndProcessImage(file, selectedTape) {
        displayImage(file);
        processButton.style.display = 'block';
        // Set the selected tape option as a data attribute on the process button
        processButton.dataset.tape = selectedTape;
    }

    // Function to display image in the preview area
    function displayImage(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            uploadText.style.display = 'none';
            uploadIcon.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // Function to process the uploaded image
    function processImage(file, selectedTape) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('selected_tape', selectedTape); // Add selected tape option to the form data

        fetch('/red/process_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            
            // Function to handle download
            downloadBtn.onclick = function() {
                downloadImage(url);
            };
    
            downloadBtn.style.display = 'block';
            processButton.style.display = 'none'; // Hide the "Process Image" button 
            imagePreview.style.display = 'none'; // Hide the original image
            processedImgPreview.src = url;
            processedImgPreview.style.display = 'block'; // Show the processed image
        })
        .catch(error => console.error(error));
    }

    // Function to download the image
    function downloadImage(url) {
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = 'processed_image.jpg'; // Set the filename for download
        downloadLink.click();
        window.URL.revokeObjectURL(url);
    }
});
