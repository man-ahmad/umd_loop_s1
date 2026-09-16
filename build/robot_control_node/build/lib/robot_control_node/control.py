import rclpy
import math
import random
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose 
from sensor_msgs.msg import LaserScan

# This isn't minimal publisher anymore but i stole the name from the tutorial and now am too lazy to change it
class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')

        # So we need to share (x, y) between the pub/sub, I dunno if this is the best way but...
        self.x = None
        self.y = None

        self.bot_ranges = None # jerry rigged but i legit have 10 mins forgive me

        self.waypoints = [] 
        for _ in range(5):
            self.waypoints.append((random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)))

        self.current_waypoint = 0

        self.velocity_pub = self.create_publisher(Twist, '/model/vehicle/cmd_vel', 10)
        self.pos_sub = self.create_subscription(Pose, '/model/vehicle/pose', self.pos_callback, 10)
        self.sensor_sub = self.create_subscription(LaserScan, '/model/vehicle/lidar_sensor', self.sensor_callback, 10)
        timer_period = 0.1 # Assuming this is how many times the msg gets published?
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def sensor_callback(self, msg):
        self.bot_ranges = msg.ranges
        # so we can use it in timer callback

    def pos_callback(self, msg):
        self.get_logger().info(f'{msg.position.x}')
        self.x = msg.position.x
        self.y = msg.position.y

    def timer_callback(self):
        target_x, target_y = self.waypoints[self.current_waypoint]
        allMore = True

        msg = Twist()

        if self.x is None or self.y is None:
            return
        else:
            if not self.bot_ranges is None:
                for i in range(len(self.bot_ranges)):
                    if self.bot_ranges[i] < 1.0:
                        allMore = False
                        break

            if allMore:
                dx = target_x - self.x
                dy = target_y - self.y

                dist = math.sqrt(dx**2 + dy**2) # pythagorean thrm go brrrrrrr
                if dist < 0.1: # arbitrary btw
                    if self.current_waypoint >= len(self.waypoints) - 1:
                        msg.linear.x = 0
                        msg.linear.y = 0
                    else:
                        self.current_waypoint = self.current_waypoint + 1
                else:
                    msg.linear.x = 1.0 * dx / dist
                    msg.linear.y = 1.0 * dy / dist # normalize, then in that direction go at 1.0
            else:
                msg.linear.x = 0
                msg.angular.z = 0.5

        self.velocity_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher) # these are terrible names

    minimal_publisher.destroy_node() # guess you need to 'free' the node
    rclpy.shutdown()

if __name__ == '__main__':
    main()
