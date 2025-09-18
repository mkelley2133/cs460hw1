# File: rectangle.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class RectangleNode(Node):
    def __init__(self):
        super().__init__('rectangle_drawer')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_in_rectangle)
        
        # State machine variables
        self.states = ['forward_1', 'turn_1', 'forward_2', 'turn_2', 'forward_3', 'turn_3', 'forward_4', 'stop']
        self.current_state = 0
        self.counter = 0

        # Parameters for the rectangle
        self.linear_speed = 2.0
        self.angular_speed = math.pi / 2  # 90 degrees per second
        self.side_long_duration = 30  # 3 seconds (30 * 0.1s)
        self.side_short_duration = 15 # 1.5 seconds (15 * 0.1s)
        self.turn_duration = 10       # 1 second (10 * 0.1s)

        self.get_logger().info('Drawing a rectangle...')

    def move_in_rectangle(self):
        msg = Twist()
        state = self.states[self.current_state]

        if state in ['forward_1', 'forward_3']: # Long sides
            msg.linear.x = self.linear_speed
            if self.counter >= self.side_long_duration:
                self.counter = 0
                self.current_state += 1
        elif state in ['forward_2', 'forward_4']: # Short sides
            msg.linear.x = self.linear_speed
            if self.counter >= self.side_short_duration:
                self.counter = 0
                self.current_state += 1
        elif state in ['turn_1', 'turn_2', 'turn_3']: # Turns
            msg.angular.z = self.angular_speed
            if self.counter >= self.turn_duration:
                self.counter = 0
                self.current_state += 1
        else: # Stop state
            self.get_logger().info('Finished drawing rectangle.')
            self.timer.cancel() # Stop the timer

        self.publisher_.publish(msg)
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    rectangle_node = RectangleNode()
    rclpy.spin(rectangle_node)
    
    rectangle_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()