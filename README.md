Virtual Try-On System :dress:





Welcome to the Virtual Try-On System, an AI-powered web application that allows users to virtually try on clothing using the FASHN AI API. This project integrates a Flask backend with a client-side interface built with HTML, CSS, and JavaScript, enabling seamless image uploads and clothing selection for virtual try-on experiences.



Table of Contents





Features



Prerequisites



Installation



Usage



Project Structure



Configuration



API Integration



Contributing



License



Features :rocket:





:camera: Upload a customer image for virtual try-on.



:shirt: Select from a variety of clothing items to try on.



:clock1: Real-time progress updates during the try-on process.



:frame_photo: Display of the final try-on result.



:art: Responsive and modern dark-themed user interface.



:lock: Secure handling of API keys using environment variables.



Prerequisites :gear:

Before running the project, ensure you have the following installed:





Python 3.8+



pip (Python package manager)



Git (for cloning the repository)



Node.js and npm (optional, for client-side development, though not required for this setup)



A FASHN AI API key (sign up at FASHN AI to obtain one)



Installation :wrench:

1. Clone the Repository

Clone this repository to your local machine using:

git clone https://github.com/yourusername/virtual-try-on-system.git
cd virtual-try-on-system

2. Create a Virtual Environment

Set up a virtual environment to manage dependencies:

python -m venv venv

Activate it:





On Windows:

venv\Scripts\activate



On macOS/Linux:

source venv/bin/activate

3. Install Dependencies

Install the required Python packages:

pip install -r requirements.txt

(Note: If requirements.txt is not present, create it by running pip freeze > requirements.txt after installing dependencies manually below.)

Manually install key dependencies if needed:

pip install flask opencv-python pillow requests python-dotenv numpy

4. Configure the Environment





Create a .env file in the root directory with your FASHN API key:

FASHN_API_KEY=your_fashn_api_key_here



Ensure .env is added to .gitignore to keep it secure.

5. Prepare Clothing Images





Place clothing images (e.g., clothing_1.png, clothing_2.png) in the data/clothing_images directory.



Update the get_clothing endpoint in server/app.py with corresponding id, name, imageUrl, and type entries if adding new items.



Usage :computer:







Step



Description





1. Run the Application



Activate the virtual environment and start the server:
python server/app.py
The application will be available at http://localhost:5000.





2. Interact with the Interface



- Upload a customer image via the "Customer Image" input.
- Select a clothing item from the dropdown menu.
- Click "Try On" to process the virtual try-on.
- View the result image once processing is complete.





3. Troubleshooting



- If the try-on fails, check the terminal for error messages (e.g., PoseError) and ensure the customer image contains a detectable human pose.
- Verify the FASHN API key and internet connection.



Project Structure :file_folder:

virtual-try-on-system/
│
├── data/
│   ├── uploads/          # Stores uploaded customer images and results
│   └── clothing_images/  # Stores clothing images
│
├── client/               # Client-side files
│   ├── index.html        # Main HTML file
│   ├── scripts.js        # JavaScript for interactivity
│   └── styles.css        # CSS for styling
│
├── server/               # Server-side files
│   └── app.py            # Flask application
│
├── utils/                # Utility scripts
│   └── preprocess.py     # Image preprocessing logic
│
├── .env                  # Environment variables (not tracked)
├── .gitignore            # Git ignore file
├── README.md             # This file
└── requirements.txt      # Python dependencies (optional)



Configuration :gear:





API Key: Stored in .env as FASHN_API_KEY.



FASHN API Base URL: Set to https://api.fashn.ai/v1 in app.py.



Image Paths: Configured in app.config for uploads and clothing images.



API Integration :link:

This project uses the FASHN AI API (tryon-v1.6 model) for virtual try-on functionality:





Endpoint: /run for processing, /status/{task_id} for polling.



Input: Base64-encoded images for the model and garment.



Output: A URL to the try-on result image.



Requirements: A valid API key and internet connectivity.



Contributing :handshake:

We welcome contributions to enhance this project! To contribute:





Fork the repository.



Create a new branch: git checkout -b feature-branch.



Make your changes and commit: git commit -m "Description of changes".



Push to the branch: git push origin feature-branch.



Open a pull request on GitHub.

Please ensure your code follows the existing style and includes appropriate documentation.



License :scroll:

This project is licensed under the MIT License. See the LICENSE file for details.

(Note: Create a LICENSE file with MIT License text if not already present. You can generate one on GitHub when creating the repository.)