#include <stdint.h>

#define	SRAM_START	0x20000000U
#define	SRAM_SIZE	(20U * 1024U)
#define	SRAM_END	((SRAM_START) + (SRAM_SIZE))

#define	STACK_START SRAM_END

