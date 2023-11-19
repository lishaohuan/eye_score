import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class Face_Landmark_Module():
    def __init__(self):
        self.results = None
        self.landmarker = None

    def draw_landmarks_on_image(self, rgb_image, detection_result):
      if detection_result is None:
        return rgb_image
      face_landmarks_list = detection_result.face_landmarks
      annotated_image = np.copy(rgb_image)

      # 结果中可能有多个脸，循环对每个脸处理
      for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]
        # 关键点坐标的预处理
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
        ])
        # 画关键点和网格
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
        # 画脸部轮廓
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
        # 画眼睛部分
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style())
        
      return annotated_image


    def print_result(self, result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result
        
    """
    mediapipe关于脸部关键点检测的阈值
    https://developers.google.com/mediapipe/solutions/vision/face_landmarker#configurations_options
	
    min_face_detection_confidence
        description: The minimum confidence score for the face detection to be considered successful.
        range:       0.0 - 1.0
        default: 	 0.5
    min_face_presence_confidence
        description: The minimum confidence score of face presence score in the face landmark detection.
        range:       0.0 - 1.0
        default:     0.5
    min_tracking_confidence	
        description: The minimum confidence score for the face tracking to be considered successful.
        range:       0.0 - 1.0
        default:     0.5
    """

    def load_model(self, model_path: str):
        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            min_face_detection_confidence=0.4,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            result_callback=self.print_result)
        self.landmarker = FaceLandmarker.create_from_options(options)
