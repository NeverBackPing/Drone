#MCU
MCU=cortex-m3

# Compiler and Compiler flags
CPP=arm-none-eabi-g++
CFLAGS= -mcpu=$(MCU) -mthumb -std=c++20 -O0 -Wno-register
#LDFLAGS=

# Clear
RM = rm -rf

#PROGRAM NAME
NAME = drone.elf

# SOURCES FILE

SRCS = $(shell ls srcs/*.cpp)

# OBJECT
OBJS = $(SRCS:.cpp=.o)

# ASSEMBLY
ASM = $(SRCS:.cpp=.s)

# FILE OBJECT
%.o: %.cpp
	$(CPP) $(CFLAGS) -c $< -o $@
	@echo "Generated obj file: $@ ✅"

%.s: %.cpp
	$(CPP) $(CFLAGS) -S $< -o $@
	@echo "Generated assembly file: $@ ✅"

# COMPILATION
all: $(ASM) $(NAME)

$(NAME): $(OBJS)
	@$(CPP) $(OBJS) -o $(NAME)
	@echo "Compiled ✅"
	@echo "The program $(NAME) is created ✅"

clean:
	@$(RM) $(OBJS) $(ASM)
	@echo ".o files are destroyed ✅"

fclean: clean
	@$(RM) $(NAME)
	@echo "Everything is clean ✅"

re: fclean all

.PHONY: all clean fclean re