# tb3_behaviors

Descargar todos los paquetes para que funcione flexbe:

```
$ cd
$ cd catkin_ws/src
$ git clone https://github.com/team-vigir/flexbe_behavior_engine.git
$ git clone https://github.com/FlexBE/flexbe_app.git
$ git clone https://github.com/FlexBE/generic_flexbe_states.git
$ cd ..
$ catkin_make
```

Crear un paquete inicial de estados y comportamientos:

```
$ cd catkin_ws/src
$ rosrun flexbe_widget create_repo tutorial
$ cd ..
$ catkin_make
```

Para ejecutar Flexbe:

```
$ roslaunch flexbe_app flexbe_full.launch
```

Simulación de robot en un mundo vacio:

```
$ roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
```
