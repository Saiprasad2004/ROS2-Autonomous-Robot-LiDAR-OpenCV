import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge

import cv2


class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        # Convert ROS image messages into OpenCV images
        self.bridge = CvBridge()

        # Store the latest LiDAR scan
        self.latest_scan = None

        # Subscribe to the LiDAR topic
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Subscribe to the robot's camera topic
        self.subscription = self.create_subscription(
            Image,
            '/camera',
            self.image_callback,
            10
        )

        self.get_logger().info('Camera subscriber started!')

    def scan_callback(self, msg):
        self.latest_scan = msg

    def get_obstacle_distances(self):
        if self.latest_scan is None:
            return None

        scan = self.latest_scan

        sectors = {
            'LEFT': (-60, -15),
            'FRONT': (-15, 15),
            'RIGHT': (15, 60)
        }

        distances = {}

        for direction, (start_deg, end_deg) in sectors.items():
            valid_ranges = []

            for i, distance in enumerate(scan.ranges):
                angle = scan.angle_min + i * scan.angle_increment
                angle_deg = angle * 180.0 / 3.141592653589793

                if start_deg <= angle_deg <= end_deg:
                    if (
                        scan.range_min <= distance <= scan.range_max
                    ):
                        valid_ranges.append(distance)

            distances[direction] = (
                min(valid_ranges) if valid_ranges else None
            )

        return distances
    def image_callback(self, msg):
        # 1. Convert the ROS image message into an OpenCV image
        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        # 2. Convert the color image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect edges in the grayscale image
        edges = cv2.Canny(gray, 100, 200)
        contours, hierarchy = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Convert the color image from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for dark pixels
        black_mask = cv2.inRange(
            hsv,
            (0, 0, 0),
            (180, 255, 60)
        )
        
        # Find contours of dark objects using the mask
        black_contours, hierarchy = cv2.findContours(
            black_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Draw bounding boxes around detected dark regions
        mask_annotated = frame.copy()

        # Draw bounding boxes only when an obstacle is close
        distance_threshold = 1.8  # metres

        distances = self.get_obstacle_distances()
        front_distance = distances['FRONT'] if distances else None

        show_box = (
            front_distance is not None
            and front_distance <= distance_threshold
        )

        # Get the latest LiDAR distances
        distances = self.get_obstacle_distances()

        if distances is not None:
            y_text = 30

            for direction, distance in distances.items():
                if distance is not None:
                    text = f'{direction}: {distance:.2f} m'
                else:
                    text = f'{direction}: No reading'

                cv2.putText(
                    mask_annotated,
                    text,
                    (10, y_text),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2
                )

                y_text += 30

        for contour in black_contours:
            area = cv2.contourArea(contour)

            if area > 500 and show_box :
                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(
                    mask_annotated,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )
        annotated = frame.copy()

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(
                    annotated,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        # 3. Display the original color image
        cv2.imshow('Robot Camera - Color', frame)

        # 4. Display the grayscale image
        cv2.imshow('Robot Camera - Grayscale', gray)

        # Display the detected edges
        cv2.imshow('Robot Camera - Edges', edges)

        cv2.imshow('Black Object Mask', black_mask)

        cv2.imshow('Mask-Based Bounding Boxes', mask_annotated)

        cv2.imshow('Robot Camera - Contours', annotated)

        # 5. Allow both windows to refresh
        cv2.waitKey(1)

        # 6. Print the image dimensions
        height, width, channels = frame.shape
        self.get_logger().info(
            f'Image received: width={width}, height={height}, '
            f'channels={channels}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = CameraSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
