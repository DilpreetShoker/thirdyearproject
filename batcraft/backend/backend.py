import sys 
import math
import cv2
import mediapipe as mp
import numpy as np


# The following dictionaries show the results of averages for each metric
# These have been defined here to make running code easier.
# As the dataset expands in the future, these would extracted directly from the mongodb dataset.
viratKohli_data = {
    'Initial_foot_move_gradient': -4.5,
    'Leg_straight_gradient': 2.22,
    'Elbow_gradient_x':-22.98,
    'Elbow_gradient_y':-47.61,
    'Upper_body_gradient':2.3,
    'Upper_body_y_intercept':158.25,
    'Upper_body_end_angle':113.43
}

steveSmith_data = {
    'Initial_foot_move_gradient': -2.21,
    'Leg_straight_gradient': 2.67,
    'Elbow_gradient_x':-21.55,
    'Elbow_gradient_y':-62.99,
    'Upper_body_gradient':1.32,
    'Upper_body_y_intercept':170.73,
    'Upper_body_end_angle':135.35
}

babarAzam_data = {
    'Initial_foot_move_gradient': -3.23,
    'Leg_straight_gradient': 4.92,
    'Elbow_gradient_x': -44.54,
    'Elbow_gradient_y':-88.82,
    'Upper_body_gradient':1.33,
    'Upper_body_y_intercept':165.59,
    'Upper_body_end_angle':122.23
}

glennMaxwell_data = {
    'Initial_foot_move_gradient': -1.39,
    'Leg_straight_gradient': 3.22,
    'Elbow_gradient_x':-17.81,
    'Elbow_gradient_y':-55.66,
    'Upper_body_gradient':3.33,
    'Upper_body_y_intercept':155.23,
    'Upper_body_end_angle': 139.53
}

joeRoot_data = {
    'Initial_foot_move_gradient': -3.23,
    'Leg_straight_gradient': 4.92,
    'Elbow_gradient_x':-24.17,
    'Elbow_gradient_y':-82.15,
    'Upper_body_gradient':4.30,
    'Upper_body_y_intercept':175.39,
    'Upper_body_end_angle':129.23
}

rohitSharma_data = {
    'Initial_foot_move_gradient': -1.23,
    'Leg_straight_gradient': 2.39,
    'Elbow_gradient_x': -32.72,
    'Elbow_gradient_y':-53.71,
    'Upper_body_gradient':2.64,
    'Upper_body_y_intercept':154.78,
    'Upper_body_end_angle':126.83
}


#The data above is coverted to arrays
vk_array = list(viratKohli_data.values())
ss_array = list(steveSmith_data.values())
ba_array = list(babarAzam_data.values())
gm_array = list(glennMaxwell_data.values())
jr_array = list(joeRoot_data.values())
rs_array = list(rohitSharma_data.values())

#Each player is mapped to its respetive array
existing_data = {
    'Virat Kohli': vk_array,
    'Steve Smith': ss_array,
    'Babar Azam': ba_array,
    'Glenn Maxwell': gm_array,
    'Joe Root': jr_array,
    'Rohit Sharma': rs_array
}

##Feedback statements
feedback_sentences = {
    0: ['Move your front foot more towards the ball before you hit it',
        'You are moving you front foot across too much'],
    1: ['Straighten your front leg more as you are playing your shot',
        'Straighten your front leg less as you are playing your shot'],
    2: ['Move your elbows more towards the ball',
        'Keep your elbows closer to your body'],
    3: ['You need to keep your elbow higher',
        'You need to keep your elbow slightly lower'],
    4: ['You are leaning forward too much as you play the shot',
        'Lean more towards the ball as you play the shot'],
    5: ['Stand more upright at the start of your shot',
        'Lean more forward at the start of your shot'],
    6: ['Stand more upright at the end of your shot',
        'Lean more forward at the start of your shot'],
}


parts = [11,12,14,13,15,23,24,25,27,31]


#The function getPoseLandmarks takes as input:
#   frame: which is the image to apply pose estimation on
#   pose: MediaPipe built in Pose variable that defines the MediaPipe pose
#And it outputs:
#   landmarks: a dictionary which maps each landark  to its x and y coordinates
def getPoseLandmarks(frame, pose):
    #image is converted to RGB, which can be passed through Pose.process() function
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #built in mediapipe function that ouputs the results of pose estimatiom
    results = pose.process(imgRGB)
    landmarks = {}
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            if id in parts:
                landmarks[id] = [lm.x, lm.y]
    return landmarks

#The function normaliseDataPoints takes as input:
#   landmarks: a dictionary that maps each landmark to its y and x cordinates
#And outputs:
#   normalised_landmarks: A dictionary that maps each landmark to its normalised x and y cordinates
def normaliseDataPoints(landmarks):
    l_shoulder, r_shoulder ,l_hip,r_hip = np.array(landmarks[12]), np.array(landmarks[11]), np.array(landmarks[24]), np.array(landmarks[23])
    c = (1/4)*(l_shoulder+r_shoulder+l_hip+r_hip)

    normalised_landmarks = {}
    for each in landmarks:
        normalised_landmark = landmarks[each] - c
        normalised_landmarks[each] = normalised_landmark
        
    return normalised_landmarks

#The function calculate sse takes as input:
#   x: x cordinates
#   y: y cordinates
#   slope: the gradient of the model used to fit the cordinates
#   intercept: the intercept of the model used to fit the cordinates
#And outputs:
#   the sum of squared errors between the preductions and the ground truth
def calculate_sse(x, y, slope, intercept):
    """Calculate the sum of squared errors for a linear fit."""
    x = np.array(x)  # Ensure x is a NumPy array
    y = np.array(y) 
    predictions = slope * x + intercept
    return np.sum((y - predictions) ** 2)

#Function find_best_breakpoint takes as input:
#   x: an array of x cordinates
#   y: an array of y cordinates
# And outputs:
#   best_breakpoint: the frame that is the best breakpoint
#   best_sse: the value of the sum of squared errors at the best breakpoint
def find_best_breakpoint(x, y):
    best_sse = np.inf
    best_breakpoint = None
    
    # Ensure at least two data points per segment by adjusting the range
    for breakpoint in range(2, len(x) - 2):  # Adjusted range
        # Split the data at the current breakpoint
        x1, y1 = x[:breakpoint],y[:breakpoint]
        x2, y2 = x[breakpoint:], y[breakpoint:]
        
        # Fit linear models to each segment
        slope1, intercept1 = np.polyfit(x1, y1, 1)
        slope2, intercept2 = np.polyfit(x2, y2, 1)
        
        # Calculate SSE for each segment
        sse1 = calculate_sse(x1, y1, slope1, intercept1)
        sse2 = calculate_sse(x2, y2, slope2, intercept2)
        
        # Calculate total SSE
        total_sse = sse1 + sse2
        
        # Update best breakpoint if this configuration has lower SSE
        if total_sse < best_sse:
            best_sse = total_sse
            best_breakpoint = breakpoint
            
    return best_breakpoint, best_sse

#The function find two slopes takes as input:
#   x: an array of x cordinates
#   y: an array of y cordinates
# And outputs:
#   slope1: the gradient of the first part of segmented regression
#   slope2: the gradient of the second part of semented regression
def find_two_slopes(x,y):
    b, e = find_best_breakpoint(x,y)
    # Fit linear models to the best segments
    x1, y1 = np.array(x[:b]), np.array(y[:b])
    x2, y2 = np.array(x[b:]), np.array(y[b:])
    slope1, intercept1 = np.polyfit(x1, y1, 1)
    slope2, intercept2 = np.polyfit(x2, y2, 1)
    # Generate line segments for plotting
    # line1 = slope1 * x1 + intercept1
    # line2 = slope2 * x2 + intercept2
    return slope1,slope2

#The function getFrontFootGradient takes as input:
#   landmarks: dictionary of key data points
# And ouputs:
#   the gradient of the initial front foot movement
def getFrontFootGradient(landmarks):
    x_values = [coordinate[0] for coordinate in landmarks[31]]
    frames = list(range(0,len(x_values)))
    slope, _ = find_two_slopes(x_values,frames)
    return slope
#The function getElbowGradients takes as input:
#   landmarks: dictionary of key data points
# And ouputs:
#   the gradient of the elbow novements on the y and x axis
def getElbowGradients(landmarks):
    elbow_x  = [coordinate[0] for coordinate in landmarks[13]]
    elbow_y  = [coordinate[1] for coordinate in landmarks[13]]
    frames = list(range(0,len(elbow_x)))
    slope_x, _ = np.polyfit(elbow_x, frames, 1)
    _, slope_y  = find_two_slopes(elbow_y,frames)
    return slope_x, slope_y

# function used get the vector between two points
def vector(a, b):
    return [b[0] - a[0], b[1] - a[1]]

# Function to calculate the dot product of two vectors
def dot_product(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]

# Function to calculate the magnitude of a vector
def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2)
#Function angle_between takes in as input:
#   v1: vector 1
#   v2L vector 2
#And outputs:
#   angle_deg: the angle in degrees between two vectors
def angle_between(v1, v2):
    cos_angle = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    return angle_deg
#Function angle_between takes in as input:
#   vertex1: array of cordinates for vertex 1
#   vertex2: array of cordinates for vertex 2
#   vertex3: array of cordinates for vertex 3
#And outputs:
#   angles: an array of angles at each frame
def getAnglesBetweenTwoVectors(vertex1,vertex2,vertex3):
    angles = []
    for i in range(len(vertex1)):
        vector1 = vector(vertex2[i], vertex1[i])  
        vector2 = vector(vertex2[i], vertex3[i])  
        angle = angle_between(vector1,vector2)
        angles.append(angle)
    return angles

#The function getUpperBodyGradients takes as input:
#   landmarks: dictionary of key data points
# And ouputs:
#   slope: the gradient of the upper body movement
#   intercept: the starting angle
#   final_angle: the end angle
def getUpperBodyGradients(landmarks):
    l_hip = [coordinate for coordinate in landmarks[23]]
    l_knee = [coordinate for coordinate in landmarks[25]]
    l_shoulder = [coordinate for coordinate in landmarks[11]]
    angles = getAnglesBetweenTwoVectors(l_shoulder,l_hip,l_knee)
    frames = list(range(0,len(angles)))
    slope, intercept = np.polyfit(frames, angles, 1)
    final_angle = slope * frames[len(frames)-1] + intercept
    return slope, intercept, final_angle

#The function getUpperBodyGradients takes as input:
#   landmarks: dictionary of key data points
# And ouputs:
#   slope: the gradient of leg straightening movement
def getLegAngles(landmarks):
    knee  = [coordinate for coordinate in landmarks[23]]
    ankle = [coordinate for coordinate in landmarks[25]]
    hip = [coordinate for coordinate in landmarks[27]]
    angles = getAnglesBetweenTwoVectors(hip,knee,ankle)
    frames = list(range(0,len(angles)))
    slope, _ = np.polyfit(frames, angles, 1)
    return slope 

#Function used to calculate the euclidean distance between two vectors
def euclidean_distance(vector1, vector2):
    return np.sqrt(np.sum((np.array(vector1) - np.array(vector2)) ** 2))

#Function getPlayerMatchings takes as input:
#   user_data: data obtained from user input
#And ouptuts:
#   player_matched: the name of the player that is the most similar
#   player_diff: the difference between the player matched and user data
#   percentage_score: the percentage that the player is matched to the user with
#   player_score: the score of similarity between player_mathced and user
def getPlayersMatching(user_data):
    player_matched = ''
    max_score = 0
    total_score= 0
    player_diff = []
    player_score = 0
    for each in existing_data:
        diff = np.array(existing_data[each]) - np.array(user_data)
        diss = euclidean_distance(np.array(existing_data[each]),np.array(user_data))
        score = 1/diss
        total_score+=score
        if score>max_score:
            player_score = diss
            max_score = score
            player_matched = each
            player_diff = diff
        final_score = (max_score/total_score)*100
        percentage_Score = final_score.round(0)
    return player_matched,player_diff, percentage_Score, player_score

#Function used to work out the top 3 elements to give feedback upon
def find_top_three_indexes(arr):
    # Enumerate the array to pair each element with its index
    indexed_array = list(enumerate(arr))
    
    # Sort the array based on values in descending order, keeping the indexes
    indexed_array.sort(key=lambda x: x[1], reverse=True)
    
    # Extract the indexes of the top 3 values
    top_three_indexes = [index for index, value in indexed_array[:3]]
    
    return top_three_indexes

#Function getFeedback takes as input:
#   diff: the differences between the data
#And outputs:
#   feedback: the feedback given
def getFeedback(diff):
    feedback = []
    feedback_points = find_top_three_indexes(diff)
    for each in feedback_points:
        if diff[each]>0:
            feedback.append(feedback_sentences[each][0])
        else:
            feedback.append(feedback_sentences[each][1])
    return feedback

#The function getAnalysisFrom Video takes as input:
#   pathname: path to the video
#And outputs/prints:
#   the analysis needed to pass on to the API
def getAnalysisFromVideo(pathname):
    frame_landmarks = {i: [] for i in range(33)}
    mpPose = mp.solutions.pose.Pose()
    #Open video for video capture
    cap = cv2.VideoCapture(pathname)
    if (cap.isOpened()==False):
        print("Error opening video stream")
        return 0
    count = 0
    while (cap.isOpened()):
        #Get the image at the current frame
        ret,frame = cap.read()
        if ret == True:
            landmarks = getPoseLandmarks(frame, mpPose)
            if len(landmarks)>0:
                normalised_landmarks = normaliseDataPoints(landmarks)
                for id, landmark in normalised_landmarks.items():
                    frame_landmarks[id].append(landmark)
        else:
            break
    if len(frame_landmarks)==0:
        print('unkown')
        return 
    
    #The following code uses the functions above to get the analysis on the video
    ff_gradient = getFrontFootGradient(frame_landmarks)
    egx,egy = getElbowGradients(frame_landmarks)
    ubg,ub_intercept, ub_final = getUpperBodyGradients(frame_landmarks)
    lsg = getLegAngles(frame_landmarks)
    player_data = [ff_gradient,lsg,egx,egy,ubg,ub_intercept,ub_final]
    player_matched, diff,score, player_score= getPlayersMatching(player_data)
    feedback_given = getFeedback(diff)
    if abs(player_score)<5:
        classification = 'excellent'
    elif abs(player_score)<11:
        classification = 'good'
    elif abs(player_score)<20:
        classification = 'average'
    else:
        classification = 'needs improvement'
    print(player_matched, ',',score,',',feedback_given[0],',',feedback_given[1],',',feedback_given[2], ',', classification )

getAnalysisFromVideo(sys.argv[1])
sys.stdout.flush()
sys.stderr.flush()