cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

project(drone)

add_subdirectory(includes)

target_sources(app PRIVATE src/main.c src/mpu6050/mpu6050.c)

target_link_libraries(app PRIVATE drone_headers)
