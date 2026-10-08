nano run_6axis.py

import mujoco
import mujoco.viewer
import time

model = mujoco.MjModel.from_xml_path("robot_6axis.xml")
data = mujoco.MjData(model)

active_joint = 0  # Default selected joint (Joint 1)
step_size = 0.05  # Step rotation per key press (in radians)

def key_callback(key):
    global active_joint
    # Press number keys 1 through 6 to select a joint
    if ord('1') <= key <= ord('6'):
        active_joint = key - ord('1')
        print(f"Selected Joint {active_joint + 1}")
    
    # Up Arrow: Rotate joint forward
    elif key == 265:  
        data.ctrl[active_joint] += step_size
        print(f"Joint {active_joint + 1} Target: {data.ctrl[active_joint]:.2f} rad")
    
    # Down Arrow: Rotate joint backward
    elif key == 264:  
        data.ctrl[active_joint] -= step_size
        print(f"Joint {active_joint + 1} Target: {data.ctrl[active_joint]:.2f} rad")

print("\n================ CONTROLS ================")
print("1. KEYBOARD: Press 1-6 to select a joint, UP/DOWN arrows to rotate.")
print("2. GUI SLIDERS: Press Tab to view left panel -> Control tab -> drag sliders.")
print("3. PAUSE: Press Spacebar to pause physics execution.")
print("==========================================\n")

with mujoco.viewer.launch_passive(model, data, key_callback=key_callback) as viewer:
    while viewer.is_running():
        step_start = time.time()

        # Step physics sub-loops for stable rendering
        for _ in range(5):
            mujoco.mj_step(model, data)

        viewer.sync()

        # Frame rate sync
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
