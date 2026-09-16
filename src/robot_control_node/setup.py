from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robot_control_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manahmad',
    maintainer_email='manahmad@terpmail.umd.edu',
    description='Simple control node for a robot cube',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vehicle_controller = robot_control_node.control:main'
        ],
    },
)
