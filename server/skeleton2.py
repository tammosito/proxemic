#!/usr/bin/python

from openni import *
import redis
import json
from datetime import datetime

red = redis.Redis(host='localhost', db=1)
chan_name = "kinect"


user_is_tracked = False
phases = {
    'personal' : 0,
    'subtle' : 0,
    'implicit' : 0,
    'ambient' : 0,
}
update_time = datetime.now()

ctx = Context()
ctx.init()

gest = GestureGenerator()
gest.create(ctx)

depth = DepthGenerator()
depth.create(ctx)

# Create the user generator
user = UserGenerator()
user.create(ctx)

# Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap


# Declare the callbacks
def new_user(src, id):
    global user_is_tracked
    user_is_tracked = True
    
    print "1/4 User {} detected." .format(id)
    red.publish(chan_name, 'user_detected')
   

def lost_user(src, id):
    user_is_tracked = False
    print "--- User {} lost." .format(id)
    red.publish(chan_name, 'user_lost')

def set_interaction_phase(distance):
    global phases

    if distance > 0 and distance < 60:
        phases['personal'] = phases['personal'] + 1

    elif distance > 60 and distance < 1500:
        phases['subtle'] = phases['subtle'] + 1

    elif distance > 1500 and distance < 4000:
        phases['implicit'] = phases['implicit'] + 1

    elif distance > 4000 and distance < 8000:
        phases['ambient'] = phases['ambient'] + 1

    else:
        phases['ambient'] = phases['ambient'] + 1


def get_smooth_phase(interval):
    global phases
    global update_time
    # if phases[time] 2 sektunden her:
    
    #alle phases auf 0 setzt, time auf now setzten
    now = datetime.now()
    then = update_time
    tdelta = now - then
    delta = tdelta.total_seconds()

    if delta >= interval:
        active_phase = max(phases, key=phases.get)

        phases['personal'] = 0
        phases['subtle'] = 0
        phases['implicit'] = 0
        phases['ambient'] = 0

        update_time = datetime.now()

        print active_phase
        red.publish(chan_name, active_phase)

# Register callbacks
def gesture_detected(src, gesture, id, endPoint):
        if user_is_tracked:
            print gesture
            red.publish(chan_name, gesture)

def gesture_progress(src, gesture, point, progress): pass


# Register them
user.register_user_cb(new_user, lost_user)

# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

#set depth settings
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

#register gestures
gest.add_gesture("Click")

gest.register_gesture_cb(gesture_detected, gesture_progress)

# Start generating
ctx.start_generating_all()
print "0/4 Starting to detect users. Press Ctrl-C to exit."


while True:
    # Update to next frame
    ctx.wait_and_update_all()

    if user_is_tracked:
        depthMap = depth.map

        # Get the coordinates of the middle pixel
        x = depthMap.width / 2
        y = depthMap.height / 2
            
        # Get the pixel at these coordinates
        distance = depthMap[x,y]
        set_interaction_phase(distance)

        get_smooth_phase(1.5)
