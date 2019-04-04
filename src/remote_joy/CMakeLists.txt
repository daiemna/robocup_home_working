cmake_minimum_required(VERSION 2.8.3)
project(remote_joy)

find_package(catkin REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES remote_joy
#  CATKIN_DEPENDS joy rospy
#  DEPENDS system_lib
)

catkin_install_python(PROGRAMS
   scripts/vr_remote.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)