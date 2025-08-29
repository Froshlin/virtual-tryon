# Froshlin/virtual-try-on

## Virtual Try-On System 👗

Welcome to the **Virtual Try-On System**, an AI-powered web application that allows users to virtually try on clothing using the FASHN AI API. This project features a Flask-based backend integrated with a client-side interface built with HTML, CSS, and JavaScript, providing a seamless experience for uploading images and selecting clothing for virtual try-on simulations.

### Table of Contents
- [Features](#features-🚀)
- [Prerequisites](#prerequisites-⚙️)
- [Installation](#installation-🔧)
- [Usage](#usage-💻)
- [Project Structure](#project-structure-📁)
- [Configuration](#configuration-⚙️)
- [API Integration](#api-integration-🔗)
- [Troubleshooting](#troubleshooting-🔧)
- [Contributing](#contributing-🤝)
- [License](#license-📜)

## Features 🚀
- 📷 Upload a customer image for virtual try-on.
- 👕 Select from a variety of preloaded clothing items to try on.
- 🕐 Real-time progress updates during the try-on process.
- :frame_photo: Preview of the final try-on result (once configured).
- 🎨 Responsive and modern dark-themed user interface.
- 🔒 Secure handling of API keys using environment variables.

## Prerequisites ⚙️
Before running the project, ensure you have the following installed:
- **Python 3.8+**: For the Flask backend.
- **pip**: Python package manager.
- **Git**: For cloning the repository.
- **Node.js and npm** (optional): For client-side development, though not required for this setup.
- **A FASHN AI API Key**: Sign up at [FASHN AI](https://fashn.ai) to obtain one.

## Installation 🔧
Follow these steps to set up the Virtual Try-On System locally:

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/Froshlin/virtual-try-on.git
cd virtual-try-on
```

### 2. Create a Virtual Environment
Set up a virtual environment to manage dependencies:
```bash
python -m venv venv
```
Activate it:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```
If `requirements.txt` is missing, create it by installing dependencies manually:
```bash
pip install flask opencv-python pillow requests python-dotenv numpy
pip freeze > requirements.txt
```

### 4. Configure the Environment
Create a `.env` file in the root directory with your FASHN API key:
```plaintext
FASHN_API_KEY=your_fashn_api_key_here
```
Add `.env` to `.gitignore` to keep it secure (already included by default).

### 5. Prepare Clothing Images
Place clothing images (e.g., `clothing_1.png`, `clothing_2.png`, `clothing_3.png`, `clothing_4.png`) in the `clothing_images` directory at the root level. Update the `get_clothing` endpoint in `server/app.py` with corresponding `id`, `name`, `imageUrl`, and `type` entries if adding new items.

## Usage 💻
### Steps
1. **Run the Application**
   Activate the virtual environment and start the server:
   ```bash
   python server/app.py
   ```
   The application will be available at `http://localhost:5000`.

2. **Interact with the Interface**
   - Upload a customer image via the "Customer Image" input.
   - Select a clothing item from the dropdown menu.
   - Click "Try On" to process the virtual try-on.
   - View the result image once processing is complete (ensure client-side handling is configured).

## Project Structure 📁
```
virtual-try-on/
│
├── data/
│   ├── uploads/         # Stores uploaded customer images and results (ignored by Git)
│   └── clothing_images/ # Stores clothing images (e.g., clothing_1.png)
├── client/              # Client-side files
│   ├── index.html       # Main HTML file
│   ├── scripts.js       # JavaScript for interactivity
│   └── styles.css       # CSS for styling
├── server/              # Server-side files
│   └── app.py           # Flask application
├── utils/               # Utility scripts
│   └── preprocess.py    # Image preprocessing logic
├── .env                 # Environment variables (not tracked)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Configuration ⚙️
- **API Key**: Stored in `.env` as `FASHN_API_KEY`.
- **FASHN API Base URL**: Set to `https://api.fashn.ai/v1` in `app.py`.
- **Image Paths**:
  - `UPLOAD_FOLDER`: Configured to `../data/uploads` from `server/app.py`, resolving to `/opt/render/project/src/data/uploads` on Render.
  - `CLOTHING_FOLDER`: Configured to `../clothing_images`, resolving to `/opt/render/project/src/clothing_images`.

## API Integration 🔗
This project uses the FASHN AI API (tryon-v1.6 model) for virtual try-on functionality:
- **Endpoint**: `/run` for processing, `/status/{task_id}` for polling.
- **Input**: Base64-encoded images for the model (customer) and garment (clothing).
- **Output**: A URL to the try-on result image, saved locally as `/uploads/result_*.png`.
- **Requirements**: A valid API key and internet connectivity.

## Troubleshooting 🔧
- **Try-On Fails**: Check the terminal or Render logs for errors (e.g., `PoseError` if the customer image lacks a detectable pose, or `Clothing image not found` if files are missing).
- **Result Preview Not Showing**: Ensure the client updates the image src with the `resultImage` URL from the `try_on` response. Verify logs show `Result saved to:` and `Serving file from:` with matching paths.
- **API Issues**: Confirm the FASHN API key is valid and the internet connection is active.
- **Deployment Errors**: If using Render, ensure `clothing_images` files are committed and `data/uploads` is dynamically created (ignored by `.gitignore`).

## Contributing 🤝
We welcome contributions to enhance this project! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit: `git commit -m "Description of changes"`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a pull request on GitHub.

Please ensure your code follows the existing style and includes appropriate documentation.

## License 📜
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.