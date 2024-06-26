# Pacman time counter

Pacman time counter is an application designed for windows to help keep track of time.

It is essenstially an alarm clock, that takes the time duration as an input. Close to the set time, it puts an animation of a pacman on the upper side of the screen that depicts a pacman eating dots. Dots represent minutes, and when the last dot is eaten (time's up!) the pacman becomes huge and engulfs the whole screen. 

![pacman eating points](https://github.com/SakuOrdrTab/pacman_proto/assets/113209622/098ab787-672a-4249-9a7a-5ae698833d3e)

The app was designed to prevent representations to use more time than allowed and was inspired by Spine Congresses: If representer has been allowed 10 minutes and he intends on speaking for 15 minutes this will not happen; put the pacman running for 11 minutes, and his/hers show will be over then!

![pacman eats the screen](https://github.com/SakuOrdrTab/pacman_proto/assets/113209622/fdfd810c-d879-46b4-bbd1-c9255c6405d7)

The GUI is done with PySide6. The app window should remain on top of all applications, otherwise this would not be much of use, wouldn't it?

Helps keep track of time in coding, too ;)

## Installing

For those users, that are more familiar with lecturer's overusing their time, I have included a Windows executable, to be found in the dist folder:

https://github.com/SakuOrdrTab/pacman_proto/blob/main/dist/pacman.exe

Of course, executables are very system-dependant, and I have no idea, how well this adapts to other windows configurations than mine..
It was built using Windows 11 and a normal dekstop computer.

More robust way is of course is to run it as a python script:

After cloning, create a venv:<br>
```python -m venv .venv```

Activate venv:<br>
```.venv/Scripts/activate```

run the script:<br>
```python pacman.py <optional argument: minutes to go>```


