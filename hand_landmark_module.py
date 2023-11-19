import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class Hand_Landmark_Module():
    def __init__(self):
        self.results = None

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        if detection_result is None:
            return rgb_image
        
        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

        # 结果中可能有多个手，循环对每个手处理
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]
            # 关键点坐标的预处理
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])
            # 画关键点和网格
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style())

        return annotated_image


    def print_result(self, result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result

    """
    mediapipe关于手部关键点检测的阈值
    https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#configurations_options
    min_hand_detection_confidence
        description: The minimum confidence score for the hand detection to be considered 
                     successful in palm detection model.
        range:       0.0 - 1.0
        default:     0.5
    min_hand_presence_confidence
        description: The minimum confidence score for the hand presence score in the hand 
                     landmark detection model. In Video mode and Live stream mode, if the 
                     hand presence confidence score from the hand landmark model is below 
                     this threshold, Hand Landmarker triggers the palm detection model. 
                     Otherwise, a lightweight hand tracking algorithm determines the 
                     location of the hand(s) for subsequent landmark detections.
        range:       0.0 - 1.0
        default:     0.5
    min_tracking_confidence
        description: The minimum confidence score for the hand tracking to be considered 
                     successful. This is the bounding box IoU threshold between hands in 
                     the current frame and the last frame. In Video mode and Stream mode 
                     of Hand Landmarker, if the tracking fails, Hand Landmarker triggers 
                     hand detection. Otherwise, it skips the hand detection.
        range:       0.0 - 1.0
        default:     0.5
    """
        
    def load_model(self, model_path: str):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            min_hand_detection_confidence=0.2,
            min_hand_presence_confidence=0.4,
            min_tracking_confidence=0.4,
            num_hands=2,
            result_callback=self.print_result)
        self.landmarker = HandLandmarker.create_from_options(options)
    
