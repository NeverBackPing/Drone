/* ************************************************************************** */
/*                                                                            */
/*                              NEVERBACKPING                                 */
/*                          Embedded RTOS Drone Project                       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/mpu6050.h"

K_THREAD_DEFINE(mpu6050_id, STACK_SIZE, gyroscope, NULL, NULL, NULL, MPU6050_PRIORITY, 0, 0);

void	gyroscope(void)
{
	const struct device *const mpu6050 = DEVICE_DT_GET_ONE(invensense_mpu6050);
	struct	sensor_value accel[3] = {0};
	struct	sensor_value gyro[3] = {0};

	if (!device_is_ready(mpu6050))
	{
		while (1)
		{
			printf("ERROR: MPU6050 not ready\n");
			k_msleep(5);
		}
	}

	printf("START: While for read MPU6050\n");
	while (1)
	{
		sensor_sample_fetch(mpu6050);

		sensor_channel_get(mpu6050, SENSOR_CHAN_ACCEL_XYZ, accel);
		sensor_channel_get(mpu6050, SENSOR_CHAN_GYRO_XYZ, gyro);

		printf("Accel X: %f, Y: %f, Z: %f\n",
				sensor_value_to_double(&accel[0]),
				sensor_value_to_double(&accel[1]),
				sensor_value_to_double(&accel[2]));

		printf("Gyro X: %f, Y: %f, Z: %f\n",
				sensor_value_to_double(&gyro[0]),
				sensor_value_to_double(&gyro[1]),
				sensor_value_to_double(&gyro[2]));
		k_msleep(5);
	}
	while (1)
	{
		printf("Error: FATAL can't read again\n");
		k_msleep(5);
	}
}
