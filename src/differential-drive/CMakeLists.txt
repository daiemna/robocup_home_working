cmake_minimum_required(VERSION 2.8.3)
project(differential_drive)

find_package(catkin REQUIRED)

catkin_package()

catkin_install_python(PROGRAMS
   scripts/pid_velocity.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)