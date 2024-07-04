## OPEN SOURCE ROBOTICS FOR MYANMAR ( OSRFM )
### rom2109 Autonomous Mobile Robot simulation
<img src="/images/gazebo.png" width="519" height="300" align="center"/>

$ cd your_dir/catkin_ws/src

#### clone teleop package.
$ sudo apt-get install ros-noetic-teleop-twist-keyboard

#### install gazebo ros packages.
$ sudo apt-get install ros-noetic-ros-control \
$ sudo apt-get install ros-noetic-ros-controllers\
$ sudo apt-get install ros-noetic-gazebo-ros-pkgs

#### install joint state publisher gui.
$ sudo apt-get install ros-noetic-joint-state-publisher\
$ sudo apt-get install ros-noetic-joint-state-publisher-gui


#### clone ros navigation package.
$ sudo apt-get install ros-noetic-navigation\

$ cd catkin_ws\
$ catkin_make

Now, we can install ROM2109 robot's ROS Noetic packages for PC.

$ cd catkin_ws/src\
$ git clone -b noetic-devel git@github.com:ROM-robotics/rom2109_simulation.git

$ cd catkin_ws\
$ catkin_make\

Noetic မှာ roslaunch rom2109_gazebo gazebo_simulation_world.launch ကို run လို့ error ပေါ်ခဲ့ရင် \
gazebo.launch ကို run ပြီး simulation world ကို စိတ်ကြိုက်တည်ဆောက်ပြီး save world လုပ်ပါ။

```
rom2109_tall_gazebo.urdf ကို ပြင်ဆင်ပြီးဖြစ်သည်။ ကျန်တဲ့ urdf များကို သုံးမယ်ဆို ပြင်ဆင်ပါ။
```
