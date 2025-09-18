# File: random.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import random
import math

class RandomWalkNode(Node):
    def __init__(self):
        super().__init__('random_walk')
        
        # Publisher for velocity commands
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        
        # Subscriber for turtle's current position
        self.subscriber = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10)
            
        # Timer to control the movement logic
        self.timer = self.create_timer(0.1, self.move_callback)
        
        self.current_pose = None
        self.is_turning = False
        self.turn_start_time = 0
        self.turn_duration = 0
        
        self.get_logger().info('Random walk node started. Turtle will wander and avoid walls.')

    def pose_callback(self, msg):
        """Callback function to receive the turtle's pose."""
        self.current_pose = msg

    def move_callback(self):
        """Main logic for moving the turtle."""
        if self.current_pose is None:
            return  # Wait until we have pose data

        msg = Twist()
        
        # Wall avoidance logic
        wall_threshold = 1.0
        is_near_wall = (self.current_pose.x < wall_threshold or 
                        self.current_pose.x > 11.0 - wall_threshold or 
                        self.current_pose.y < wall_threshold or 
                        self.current_pose.y > 11.0 - wall_threshold)

        if self.is_turning:
            # Continue turning for the set duration
            current_time = self.get_clock().now().nanoseconds / 1e9
            if current_time - self.turn_start_time < self.turn_duration:
                msg.angular.z = 3.0  # Constant turning speed
            else:
                self.is_turning = False # Stop turning
        elif is_near_wall:
            # If near a wall, start a turn
            self.is_turning = True
            self.turn_start_time = self.get_clock().now().nanoseconds / 1e9
            self.turn_duration = random.uniform(0.5, 1.5) # Turn for a random duration
            msg.linear.x = 0.0
            msg.angular.z = 3.0 # Start turning
        else:
            # Move forward with slight random adjustments
            msg.linear.x = 2.0
            msg.angular.z = random.uniform(-0.5, 0.5)

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    random_walk_node = RandomWalkNode()
    rclpy.spin(random_walk_node)

    random_walk_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()