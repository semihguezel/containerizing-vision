#! /usr/bin/env python3

# Import built-in libraries
import os
import time
import threading

# Import third-party packages
import cv2
from ultralytics import YOLO

# Import custom modules
from helpers.frame_queue_handler import FrameQueueHandler
from helpers.utilities import generate_random_rgb_color_list, read_yaml_file


class YoloDetector:
    def __init__(self):
        """
        Initialize the YoloDetector class.

        This class is designed for object detection using YOLO (You Only Look Once) model.

        Attributes:
        - video_path (str): The path to the input video file.
        - frame_rate (int): The frame rate at which frames are processed.
        - model (YOLO): The YOLO model for object detection.
        - confidence (float): Confidence threshold for object detection.
        - iou (float): Intersection over Union (IOU) threshold for object detection.
        - font (int): OpenCV font for displaying class names.
        - font_scale (float): Font scale for displaying class names.
        - line_thickness (int): Thickness of lines in bounding boxes.
        - num_classes (int): Number of classes in the YOLO model.
        - color_list (list): List of random RGB colors for different classes.
        - queue_handler (FrameQueueHandler): Queue handler for managing frames in a thread-safe manner.
        """
        current_path = os.getcwd()
        self.parsed_data = read_yaml_file(current_path + "/config/configuration.yaml")

        self.video_path = self.parsed_data['video_path']
        self.frame_rate = self.parsed_data['frame_rate']

        # Load a model
        self.model = YOLO(current_path + self.parsed_data['model_parameters']['path'])
        self.confidence = self.parsed_data['model_parameters']['conf']
        self.iou = self.parsed_data['model_parameters']['iou']

        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.font_scale = 1
        self.line_thickness = 2
        self.num_classes = len(self.model.names)
        self.color_list = generate_random_rgb_color_list(self.num_classes)

        self.queue_handler = FrameQueueHandler(max_size=5)

    def read_frames(self):
        """
        Read frames from the input video and put them in the queue.

        This method reads frames from the input video and puts them into the frame queue for further processing.
        """

        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            # # Adjust the playback rate by changing the delay
            # cv2.waitKey(self.frame_rate) & 0xFF

            self.queue_handler.put(frame)
            time.sleep(1 / self.frame_rate)

        cap.release()

        cv2.destroyAllWindows()

    def inference(self):
        """
        Perform object detection inference on a frame.

        This method retrieves a frame from the queue and performs YOLO object detection inference.

        Returns:
        - frame (numpy.ndarray): The frame with bounding boxes drawn around detected objects.
        """

        frame = self.queue_handler.get()

        results = self.model.predict(source=frame, conf=self.confidence, iou=self.iou, stream=True)

        for result in results:
            for detection in result:
                x1 = int(detection.boxes.xyxy[0][0])
                y1 = int(detection.boxes.xyxy[0][1])
                x2 = int(detection.boxes.xyxy[0][2])
                y2 = int(detection.boxes.xyxy[0][3])

                class_id = int(detection.boxes.cls)
                class_name = self.model.names[class_id]
                confidence_score = round(float(detection.boxes.conf) * 100, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), self.color_list[class_id], self.line_thickness)

                cv2.putText(frame, '{} [{}]'.format(class_name, confidence_score),
                            (x1, y1), self.font, self.font_scale,
                            self.color_list[class_id],
                            self.line_thickness,
                            cv2.LINE_AA)
        return frame

    def process_and_display_frames(self):
        """
        Continuously process frames and display the result.

        This method continuously processes frames using the inference method and displays the resulting frames.
        """
        while True:
            processed_frame = self.inference()

            if processed_frame is not None:
                cv2.imshow('Frame', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Instantiate YoloDetector
    yolo_detector = YoloDetector()

    # Create a thread to read frames from the video
    read_thread = threading.Thread(target=yolo_detector.read_frames)
    read_thread.start()

    # Process and display frames in the main thread
    yolo_detector.process_and_display_frames()
