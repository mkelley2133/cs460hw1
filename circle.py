# File: circle.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class CircleNode(Node):
    def __init__(self):
        super().__init__('circle_drawer')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.move_in_circle)
        self.get_logger().info('Drawing a circle...')

    def move_in_circle(self):
        msg = Twist()
        # Set constant linear velocity for forward motion
        msg.linear.x = 2.0
        # Set constant angular velocity for turning
        msg.angular.z = 1.0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    circle_node = CircleNode()
    rclpy.spin(circle_node)
    
    # Cleanup
    circle_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()