/* ************************************************************************** */
/*                                                                            */
/*                              NEVERBACKPING                                 */
/*                          Embedded RTOS Drone Project                       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/drone.h"
#include "../includes/mpu6050.h"
#include "zephyr/kernel.h"

int	main(void)
{
	while (1)
	{
		k_sleep(K_MSEC(1000));
	}
	return (0);
}
