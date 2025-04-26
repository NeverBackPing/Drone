# Drone
Building a drone with two Raspberry Pico 2 Zephyr RTOS.

## Work environment
We need to install and create a Python environment 
so as not to "pollute" our Linux environment.
```
$ sudo  apt install  -y  python3-venv
```
```
$ python3 -m venv  .venv
```
```
$ source .venv/bin/activate
```
```
(.venv)$ // you are in the python environment now
```
## Build tool
West is the meta tool used by Zephyr to group together a multitude of commands and tools
```
(.venv)$ pip  install  west
```
```
west init
```
```
west update
```


