cmake_minimum_required(VERSION 3.20.0)

add_library(drone_headers INTERFACE)

target_include_directories(drone_headers INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
