#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import math

class ReceptionBotNavigator(Node):
    def __init__(self):
        super().__init__('reception_navigator')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Define named waypoints (x, y, yaw_degrees)
        self.waypoints = {
            'reception_desk': (0.0, 6.0, 180.0),
            'waiting_area':   (-6.0, 6.0, 0.0),
            'meeting_room':   (7.0, -5.0, 90.0),
            'home':           (0.0, 0.0, 0.0),
        }

    def send_goal(self, location_name):
        if location_name not in self.waypoints:
            self.get_logger().error(f'Unknown location: {location_name}')
            return

        x, y, yaw_deg = self.waypoints[location_name]
        yaw = math.radians(yaw_deg)

        goal_msg = NavigateToPose.Goal()
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        # Convert yaw to quaternion
        pose.pose.orientation.z = math.sin(yaw / 2)
        pose.pose.orientation.w = math.cos(yaw / 2)
        goal_msg.pose = pose

        self.get_logger().info(f'Navigating to {location_name} ({x}, {y})')
        self._client.wait_for_server()
        future = self._client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)

def main():
    rclpy.init()
    nav = ReceptionBotNavigator()
    # Example: go to reception desk, then waiting area, then home
    for location in ['reception_desk', 'waiting_area', 'home']:
        nav.send_goal(location)
    rclpy.shutdown()

if __name__ == '__main__':
    main()