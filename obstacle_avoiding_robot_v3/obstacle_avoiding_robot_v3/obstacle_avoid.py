import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')

        self.scan_subscriber = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.cmd_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Obstacle avoider started.')

    def scan_callback(self, msg):

        # Find the minimum distance in the FRONT sector.
        # LiDAR angles go from -180° to +180°,
        # so 0° (straight ahead) is in the middle.
        front_distances = []

        for i, r in enumerate(msg.ranges):

            if not math.isfinite(r):
                continue

            angle = msg.angle_min + i * msg.angle_increment

            # Front = -30° to +30°
            if -math.radians(30) <= angle <= math.radians(30):
                if msg.range_min < r < msg.range_max:
                    front_distances.append(r)

        if not front_distances:
            self.get_logger().warn(
                'No valid forward LiDAR readings. Stopping robot.'
            )
            self.cmd_publisher.publish(Twist())
            return

        front_distance = min(front_distances)

        cmd = Twist()

        if front_distance < 0.9:

            # Obstacle ahead -> stop forward motion and turn
            cmd.linear.x = 0.0
            cmd.angular.z = 0.35

            self.get_logger().info(
                f'Obstacle ahead: {front_distance:.2f} m -> turning'
            )

        else:

            # Path clear -> move forward
            cmd.linear.x = 0.30
            cmd.angular.z = 0.0

        self.cmd_publisher.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    node = ObstacleAvoider()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        # Stop robot safely before shutting down ROS
        if rclpy.ok():
            stop = Twist()
            node.cmd_publisher.publish(stop)

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
