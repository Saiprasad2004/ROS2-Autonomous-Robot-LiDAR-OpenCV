from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'obstacle_avoiding_robot_v3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')
        ),
        (
            os.path.join('share', package_name, 'worlds'),
            glob('worlds/*')
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='prasad',
    maintainer_email='pasupulaprasad22@gmail.com',
    description='Obstacle avoiding robot',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'obstacle_avoid = obstacle_avoiding_robot_v3.obstacle_avoid:main',
            'odom_tf_publisher = obstacle_avoiding_robot_v3.odom_tf_publisher:main',
        ],
    },
)
