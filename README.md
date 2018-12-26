# RPy-Frame
RPy-Frame is a python software made for Raspberry PI that enables you to make your own awesome-looking budget digital photo frame.

### Screens
![](screen1.png)
![](screen2.png)
![](screen3.png)

### Highlights & features
- Makes a slideshow of your photos, where each image is displayed for a configured amount of time
- Photos are played in random order, however, once a photo is played a few images that were taken at about the same time will be played after it. The aim was to see a part of the event.
- Photos are either scaled down so that they fit the screen or enlarged and scrolled during the playback. Since I find this behaviour tricky to get right, there are quite a few configuration rules available to tweak it.
- When photo does not take the full screen, a background will be generated with a pattern that will use the dominant colors of the current photo.
- There's also support for a phisical button, that can do the following at the moment:
	- short press: toggle date display
	- long press: advance to next photo
- Almost everything is configurable - have a look at src/settings.py

### Running the slideshow

You can run the presentation by executing the following:
```bash
python3.6 main.py /path/to/your/images/dir
```
You can always press Q or Esc during the presentation to stop it (to quit the app). If you don't specify the path to the images, then samples dir will be used.

If you want to explore configuration options of the app, then edit settings.py file. Currently there's no other documentation of all the settings but the settings.py, which is heavily commented.

You can run the program on your PC/Mac as well. Then you can use Q key to exit presentation or space to simulate the phisical button. On PC it's suggested to run it in dev/demo mode:
```bash
python3.6 main.py dev
```

# Installation
### Python 3.6
rpy-frame needs Python 3.6 to run. If you are using Raspberry PI, chances are you don’t have it yet and it might not be available through the apt package. Follow this guide to install it:
https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f

### Clone the repository

Clone rpy-frame repository:
```bash
git clone https://github.com/peterdolenc/rpy-frame.git
```

Try running it
```bash
cd rpy-frame/src
python3.6 main.py
```

### Install python packages
Probably you will need to install all the missing python packages first. For me the recipe was the following:

```bash
sudo apt-get update
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-setuptools python3-dev python3 libportmidi-dev
sudo apt-get install python3-numpy libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libavformat-dev libswscale-dev libjpeg-dev
sudo pip3.6 install --upgrade pip
sudo pip3.6 install pygame
sudo pip3.6 install pillow
```

# Optional setup
There are two extra optional setup steps that you might want to configure.

### Auto start presentation on boot
Comming soon.

### Turn off the display during the night to save energy
Comming soon.

### Setting up the phisical button
Comming soon.

# Credits:

Code for the patterns taken and adapted from:
https://github.com/eleanorlutz/AnimatedPythonPatterns/blob/master/PatternMaker.ipynb

Original idea and some base concepts for pygame photo frame:
https://github.com/gitajt/PGslideshow

