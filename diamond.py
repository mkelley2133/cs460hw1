# File: diamond.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class DiamondNode(Node):
    def __init__(self):
        super().__init__('diamond_drawer')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_in_diamond)
        
        # State machine for drawing the diamond
        self.states = ['initial_turn', 'side_1', 'turn_1', 'side_2', 'turn_2', 'side_3', 'turn_3', 'side_4', 'stop']
        self.current_state_index = 0
        self.counter = 0

        # Parameters for the diamond
        self.linear_speed = 2.0
        self.angular_speed = math.pi / 2  # 90 degrees/sec
        
        # Durations are based on 0.1s timer period
        self.initial_turn_duration = 5 # 0.5s for a 45-degree turn
        self.side_duration = 20        # 2 seconds per side
        self.turn_duration = 10        # 1 second per 90-degree turn

        self.get_logger().info('Drawing a diamond...')

    def move_in_diamond(self):
        msg = Twist()
        state = self.states[self.current_state_index]

        if state == 'initial_turn':
            msg.angular.z = self.angular_speed
            if self.counter >= self.initial_turn_duration:
                self.counter = 0
                self.current_state_index += 1
        elif 'side' in state:
            msg.linear.x = self.linear_speed
            if self.counter >= self.side_duration:
                self.counter = 0
                self.current_state_index += 1
        elif 'turn' in state:
            msg.angular.z = self.angular_speed
            if self.counter >= self.turn_duration:
                self.counter = 0
                self.current_state_index += 1
        else: # 'stop' state
            self.get_logger().info('Finished drawing diamond.')
            self.timer.cancel()

        self.publisher_.publish(msg)
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    diamond_node = DiamondNode()
    rclpy.spin(diamond_node)
    
    diamond_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()