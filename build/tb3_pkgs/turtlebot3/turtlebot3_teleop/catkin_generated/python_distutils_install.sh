#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/root/ros1_ws/src/tb3_pkgs/turtlebot3/turtlebot3_teleop"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/root/ros1_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/root/ros1_ws/install/lib/python3/dist-packages:/root/ros1_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/root/ros1_ws/build" \
    "/usr/bin/python3" \
    "/root/ros1_ws/src/tb3_pkgs/turtlebot3/turtlebot3_teleop/setup.py" \
     \
    build --build-base "/root/ros1_ws/build/tb3_pkgs/turtlebot3/turtlebot3_teleop" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/root/ros1_ws/install" --install-scripts="/root/ros1_ws/install/bin"
