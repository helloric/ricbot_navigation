import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mapdesc_ros'


setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    requires=['mapdesc'],
    zip_safe=True,
    maintainer='abresser',
    maintainer_email='Andreas.Bresser@dfki.de',
    description='ROS 2 wrapper for the map description',
    license='BSD-3',
    tests_require=['pytest', 'pytest-cov'],
    entry_points={
        'console_scripts': [
            'mapdesc_service = mapdesc_ros.node:main',
        ],
    }
)
