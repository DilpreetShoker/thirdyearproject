import json
import numpy as np
import cv2
import mediapipe as mp
import numpy as np
import os


parts = [11,13,15,23,25,27,31]
##Function copied from backend
def getPoseLandmarks(frame, pose):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    landmarks = {}
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            if id in parts:
                landmarks[id] = [lm.x, lm.y]
    return landmarks

def calculate_euclidean_accuracy(predictions, ground_truths):
    total_error = 0
    valid_points = 0
    for pid, coords in predictions.items():
        if pid in ground_truths:
            gt_coords = ground_truths[pid]
            error = np.sqrt((gt_coords[0] - coords[0]) ** 2 + (gt_coords[1] - coords[1]) ** 2)
            total_error += error
            valid_points += 1
    return total_error / valid_points if valid_points > 0 else None

def calculate_threshold_accuracy(predictions, ground_truths, threshold=0.15):
    correct = 0
    total = 0
    for pid, coords in predictions.items():
        if pid in ground_truths:
            gt_coords = ground_truths[pid]
            if np.sqrt((gt_coords[0] - coords[0]) ** 2 + (gt_coords[1] - coords[1]) ** 2) < threshold:
                correct += 1
            total += 1
    return correct / total if total > 0 else None

# Assuming pose and other initialization has been done previously
errors_euclidean = {}
errors_threshold = {}

# Load the annotations file
with open('backend/_annotations.coco.json', 'r') as file:
    data = json.load(file)
# Create a dictionary to map image IDs to their file names
image_id_to_file_name = {img['id']: img['file_name'] for img in data['images']}

# Prepare a dictionary to store image dimensions for normalization
image_dimensions = {img['id']: (img['width'], img['height']) for img in data['images']}

# Mapping landmark IDs to their positions in the keypoints array
keypoints_order = {
    "13": 0,  # First item in the keypoints array
    "11": 1,
    "23": 2,
    "25": 3,
    "27": 4,
    "31": 5,
    "15": 6
}

# Dictionary to hold the normalized keypoints
normalized_keypoints = {}

# Process each annotation to extract and normalise keypoints
for annotation in data['annotations']:
    image_id = annotation['image_id']
    keypoints = np.array(annotation['keypoints']).reshape(-1, 3)  # Convert flat list to array (x, y, visibility)
    image_width, image_height = image_dimensions[image_id]

    # Normalize keypoints using the defined order
    keypoints_dict = {}
    for label, idx in keypoints_order.items():
        # Normalize each coordinate (x by width, y by height)
        normalized_x = keypoints[idx, 0] / image_width
        normalized_y = keypoints[idx, 1] / image_height
        keypoints_dict[int(label)] = [normalized_x, normalized_y]

    normalized_keypoints[image_id] = keypoints_dict

# Print normalized keypoints for an example image to verify
example_image_id = 0  # Change as needed

image_directory = "backend/test_images"
pose = mp.solutions.pose.Pose()
for image_id, file_name in image_id_to_file_name.items():
    image_path = os.path.join(image_directory, file_name)
    frame = cv2.imread(image_path)
    if frame is None:
        continue
    
    predicted_landmarks = getPoseLandmarks(frame, pose)

    # Get ground truth keypoints for the current image
    gt_keypoints = normalized_keypoints.get(image_id, {})

    # Calculate accuracy using both methods
    euclidean_accuracy = calculate_euclidean_accuracy(predicted_landmarks, gt_keypoints)
    threshold_accuracy = calculate_threshold_accuracy(predicted_landmarks, gt_keypoints,0.3)

    if euclidean_accuracy is not None:
        errors_euclidean[image_id] = euclidean_accuracy
    if threshold_accuracy is not None:
        errors_threshold[image_id] = threshold_accuracy

pose.close()

# Calculate and print average accuracies
average_euclidean = sum(errors_euclidean.values()) / len(errors_euclidean) 
average_threshold = sum(errors_threshold.values()) / len(errors_threshold) 

print(f"Average Euclidean Error: {average_euclidean}")
print(f"Average Threshold Accuracy: {average_threshold}")
