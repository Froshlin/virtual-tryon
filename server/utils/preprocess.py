import cv2
import numpy as np

def preprocess_image(image_path, is_clothing=False):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Resize to 1024x1024 to align with FASHN quality expectations, no other modifications
    img = cv2.resize(img, (1024, 1024), interpolation=cv2.INTER_AREA)
    
    if is_clothing:
        # Ensure transparency for clothing images
        if img.shape[2] == 3:
            alpha = np.ones((1024, 1024, 1), dtype=np.uint8) * 255
            img = np.concatenate((img, alpha), axis=2)
    else:
        # No background removal or edge detection for model image to preserve pose
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            alpha = np.ones((1024, 1024, 1), dtype=np.uint8) * 255
            img = np.concatenate((img[:, :, :3], alpha), axis=2)
        print("Model image preserved with original pose data, shape:", img.shape)
    
    return img