#!/usr/bin/python
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This file is part of PyOpenNI.
#
# PyOpenNI is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyOpenNI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyOpenNI.  If not, see <http://www.gnu.org/licenses/>.
#
# PyOpenNI is Copyright (C) 2011, Xavier Mendez (jmendeth).
# OpenNI Python Wrapper (ONIPY) is Copyright (C) 2011, Gabriele Nataneli (gamix).
#
# ***** END GPL LICENSE BLOCK *****

"""
A nice and complete example of OpenNI:

it starts tracking some gestures and alerts you
when they're recognized.
"""

from openni import *
import redis
import json

try:
    red = redis.Redis(host='localhost', db=1)
    chan_name = "kinect"

    print "Initializing..."
    ctx = Context()
    ctx.init()
    gest = GestureGenerator()
    gest.create(ctx)

    # Add some gestures to look for
    print "Registering listeners..."
    gest.add_gesture("Wave")
    gest.add_gesture("Click")
    #gest.add_gesture("RaiseHand")
    #gest.add_gesture("MovingHand")

    # Register callbacks
    def gesture_detected(src, gesture, id, endPoint):
        """print "Detected gesture:", gesture
        print "    Id: %s" % id
        print "    Endpoint: %s" % endPoint
        print "    Src: %s" % src"""
        #data = json.dumps({"coord": id, "gesture": gesture})
        #print data
        red.publish(chan_name, gesture)

    def gesture_progress(src, gesture, point, progress): pass

    def get_interaction_phase(distance):
        if distance > 0 and distance < 70:
            red.publish(chan_name, "personal")
            print "personal"
        elif distance > 70 and distance < 1800:
            red.publish(chan_name, "subtle")
            print "subtle"
        elif distance > 1800 and distance < 3600:
            red.publish(chan_name, "implicit")
            print "implicit"
        elif distance > 3600 and distance < 8000:
            red.publish(chan_name, "ambient")
            print "ambient"
        else:
            red.publish(chan_name, "unknown phase")
            print "unknown"


    gest.register_gesture_cb(gesture_detected, gesture_progress)

    # Start generating
    print "Ready! Starting to detect gestures."

     # Create a depth generator
    depth = DepthGenerator()
    depth.create(ctx)

    # Set it to VGA maps at 30 FPS
    depth.set_resolution_preset(RES_VGA)
    depth.fps = 30

    ctx.start_generating_all()


    # Main loop:
    # process every frame until the user interrupts
    try:
        print "Press Control-C to quit.\n"
        while True: 
            ctx.wait_any_update_all()
            depthMap = depth.map

            # Get the coordinates of the middle pixel
            x = depthMap.width / 2
            y = depthMap.height / 2
            
            # Get the pixel at these coordinates
            distance = depthMap[x,y] 
            interaction_phase = get_interaction_phase(distance)

            data = json.dumps({"interaction_phase": interaction_phase})
            print data
            red.publish(chan_name, data)

    except KeyboardInterrupt: print

except OpenNIError, error:
    # When an error occurs:
    print "OpenNI raised an error:", error
