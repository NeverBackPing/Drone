#include "../includes/drone.h"

int	main(void)
{
	const struct device *const mpu6050 = DEVICE_DT_GET_ONE(invensense_mpu6050);
	struct	sensor_value accel[3] = {0};
	struct	sensor_value gyro[3] = {0};

	if (!device_is_ready(mpu6050))
	{
		while (1)
		{
			printf("ERROR: MPU6050 not ready\n");
		}
		return (1);
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

		k_sleep(K_MSEC(500));
	}
	while (1)
	{
		printf("Error: exit loop\n");
	}
	return (0);
}
