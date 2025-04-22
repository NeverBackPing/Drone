# Drone
Building a drone with two Raspberry Pico 2.
![pico2](https://github.com/user-attachments/assets/8d42a7fc-99b9-4547-b4c9-9317c40d22b8)

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
````


