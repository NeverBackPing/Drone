#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/device.h>
#include <zephyr/sys/printk.h>

int main(void)
{
    const struct device *mpu6050 = DEVICE_DT_GET_ANY(invensense_mpu6050);

    if (!device_is_ready(mpu6050)) {
        printk("MPU6050 not ready!\n");
        return -1;
    }

    printk("MPU6050 ready\n");

    struct sensor_value accel_x, accel_y, accel_z;
    struct sensor_value gyro_x, gyro_y, gyro_z;

    while (1) {
        int ret = sensor_sample_fetch(mpu6050);
        if (ret < 0) {
            printk("Failed to fetch sensor data (%d)\n", ret);
            continue;
        }

        sensor_channel_get(mpu6050, SENSOR_CHAN_ACCEL_X, &accel_x);
        sensor_channel_get(mpu6050, SENSOR_CHAN_ACCEL_Y, &accel_y);
        sensor_channel_get(mpu6050, SENSOR_CHAN_ACCEL_Z, &accel_z);

        sensor_channel_get(mpu6050, SENSOR_CHAN_GYRO_X, &gyro_x);
        sensor_channel_get(mpu6050, SENSOR_CHAN_GYRO_Y, &gyro_y);
        sensor_channel_get(mpu6050, SENSOR_CHAN_GYRO_Z, &gyro_z);

        printf("Accel: X=%.2f Y=%.2f Z=%.2f | Gyro: X=%.2f Y=%.2f Z=%.2f\n",
               sensor_value_to_double(&accel_x),
               sensor_value_to_double(&accel_y),
               sensor_value_to_double(&accel_z),
               sensor_value_to_double(&gyro_x),
               sensor_value_to_double(&gyro_y),
               sensor_value_to_double(&gyro_z));

        k_sleep(K_MSEC(500));
    }
	return 0;
}
