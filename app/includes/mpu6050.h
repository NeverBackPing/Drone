/* ************************************************************************** */
/*                                                                            */
/*                              NEVERBACKPING                                 */
/*                          Embedded RTOS Drone Project                       */
/*                                                                            */
/* ************************************************************************** */

#ifndef	MPU6050_H
# define MPU6050_H

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/logging/log.h>
#include <zephyr/drivers/rtc.h>
#include <zephyr/sys/util.h>

#define STACK_SIZE 2048
#define MPU6050_PRIORITY 1

void	gyroscope(void);

#endif
