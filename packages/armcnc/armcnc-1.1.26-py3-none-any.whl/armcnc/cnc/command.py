"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class Command:

    def __init__(self, father):
        self.father = father
        self.linuxcnc = linuxcnc
        self.api = self.linuxcnc.command()

    def check_mdi(self):
        self.father.status.api.poll()
        return not self.father.status.api.estop and self.father.status.api.enabled and self.father.status.api.homed.count(1) == len(self.father.framework.machine.axes) and self.father.status.api.interp_state == linuxcnc.INTERP_IDLE

    def set_mdi(self, command):
        self.father.status.api.poll()
        if self.check_mdi():
            self.set_mode(linuxcnc.MODE_MDI, 0.5)
            self.api.mdi(command)

    def get_mode(self):
        self.father.status.api.poll()
        return self.father.status.api.task_mode

    def set_mode(self, m, t, *p):
        self.father.status.api.poll()
        if self.father.status.api.task_mode == m or self.father.status.api.task_mode in p:
            return True
        self.api.mode(m)
        if t == 0:
            self.api.wait_complete()
        else:
            self.api.wait_complete(t)
        self.father.status.api.poll()
        return True

    def set_teleop_enable(self, value):
        # 1:teleop, 0: joint
        self.father.status.api.poll()
        self.api.teleop_enable(value)
        self.api.wait_complete()

    def set_motion_teleop(self, value):
        self.api.teleop_enable(value)
        self.api.wait_complete(0.1)
        self.father.status.api.poll()

    def set_teleop_enable_mode(self, value):
        self.father.status.api.poll()
        if self.father.status.api.task_mode != linuxcnc.MODE_MANUAL:
            self.set_mode(linuxcnc.MODE_MANUAL, 1)
        if self.get_jog_mode():
            return
        self.set_motion_teleop(value)
        return True

    def get_jog_mode(self):
        self.father.status.api.poll()
        if self.father.status.api.kinematics_type == linuxcnc.KINEMATICS_IDENTITY and self.is_homed():
            teleop_mode = 1
            mode = False
        elif self.father.status.api.motion_mode == linuxcnc.TRAJ_MODE_FREE:
            teleop_mode = 0
            mode = True
        else:
            teleop_mode = 1
            mode = False
        if mode and self.father.status.api.motion_mode != linuxcnc.TRAJ_MODE_FREE or not mode and self.father.status.api.motion_mode != linuxcnc.TRAJ_MODE_TELEOP:
            self.set_teleop_enable(teleop_mode)
        return mode

    def on_start(self, line):
        self.father.status.api.poll()
        if self.father.status.api.paused:
            self.on_restart()
            return False
        # 后续需要增加持久化存储
        self.set_mode(linuxcnc.MODE_AUTO, 0)
        if self.father.status.api.interp_state != linuxcnc.INTERP_IDLE:
            return False
        self.api.auto(linuxcnc.AUTO_RUN, int(line))

    def on_restart(self):
        self.father.status.api.poll()
        if not self.father.status.api.paused:
            return False
        if self.father.status.api.task_mode not in (linuxcnc.MODE_AUTO, linuxcnc.MODE_MDI):
            return False
        self.set_mode(linuxcnc.MODE_AUTO, 0.5, linuxcnc.MODE_MDI)
        self.api.auto(linuxcnc.AUTO_RESUME)

    def on_pause(self):
        self.father.status.api.poll()
        if self.father.status.api.task_mode != linuxcnc.MODE_AUTO or self.father.status.api.interp_state not in (linuxcnc.INTERP_READING, linuxcnc.INTERP_WAITING):
            return False
        self.api.auto(linuxcnc.AUTO_PAUSE)

    def on_stop(self):
        self.set_mode(linuxcnc.MODE_AUTO, 0.5)
        self.api.abort()
        self.api.wait_complete()
        # 后续需要增加换刀信号的触发

    def jog_continuous(self, axis, speed, mode):
        if self.father.framework.machine.task_state:
            if mode == "":
                mode = self.get_jog_mode()
            self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
            self.api.jog(linuxcnc.JOG_CONTINUOUS, mode, int(axis), speed)

    def jog_increment(self, axis, speed, increment, mode):
        if self.father.framework.machine.task_state:
            if mode == "":
                mode = self.get_jog_mode()
            increment = float(increment)
            self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
            self.api.jog(linuxcnc.JOG_INCREMENT, mode, int(axis), speed, increment)

    def jog_stop(self, axis, mode):
        if mode == "":
            mode = self.get_jog_mode()
        self.api.jog(linuxcnc.JOG_STOP, mode, int(axis))

    def set_spindle_on(self, speed):
        self.set_spindle_speed(speed)

    def set_spindle_forward(self, speed):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.spindle(linuxcnc.SPINDLE_FORWARD, speed)

    def set_spindle_reverse(self, speed):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.spindle(linuxcnc.SPINDLE_REVERSE, speed)

    def set_spindle_faster(self):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.spindle(0, linuxcnc.SPINDLE_INCREASE)

    def set_spindle_slower(self):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.spindle(0, linuxcnc.SPINDLE_DECREASE)

    def set_spindle_off(self):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.spindle(linuxcnc.SPINDLE_OFF)

    def set_spindle_speed(self, speed):
        self.father.status.api.poll()
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        if self.father.status.api.spindle[0]["direction"] == 1 or self.father.status.api.spindle[0]["direction"] == 0:
            self.api.spindle(linuxcnc.SPINDLE_FORWARD, speed)
        if self.father.status.api.spindle[0]["direction"] == -1:
            self.api.spindle(linuxcnc.SPINDLE_REVERSE, speed)

    def is_spindle_running(self):
        self.father.status.api.poll()
        if self.father.status.api.spindle[0]["enabled"]:
            return self.father.status.api.spindle[0]["speed"]
        else:
            return 0

    def set_spindle_override(self, value):
        value = int(value) / 100.0
        self.api.spindleoverride(value)

    def set_max_velocity(self, value):
        value = float(value) / 60
        self.api.maxvel(value)

    def set_feed_rate(self, value):
        value = value / 100.0
        self.api.feedrate(value)

    def set_offset(self, data):
        command = data["name"]
        self.set_mdi(command)
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)

    def set_axis_offset(self, data):
        command = "G10 L20 " + data["name"] + " X" + data["x"] + " Y" + data["y"] + " Z" + data["z"]
        self.set_mdi(command)
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)

    def home_all(self):
        self.set_teleop_enable(0)
        self.api.home(-1)
        self.api.wait_complete()

    def home_axis(self, axis):
        self.set_teleop_enable(0)
        self.api.home(axis)
        self.api.wait_complete()

    def un_home_all(self):
        for x in range(len(self.father.framework.machine.axes) - 1, -1, -1):
            self.un_home_axis(x)

    def un_home_axis(self, axis):
        self.father.status.api.poll()
        if self.father.status.api.task_mode != linuxcnc.MODE_MANUAL:
            self.set_mode(linuxcnc.MODE_MANUAL, 1)
        self.set_motion_teleop(0)
        self.api.unhome(axis)

    def is_homed(self):
        axes = len(self.father.framework.machine.axes)
        for i in range(0, axes):
            if self.father.framework.machine.info["homed"][i] != 1:
                return False
        return True

    def is_manual(self):
        self.father.status.api.poll()
        if self.father.status.api.task_state != linuxcnc.STATE_ON:
            return False
        return self.father.status.api.interp_state == linuxcnc.INTERP_IDLE or self.father.status.api.task_mode == linuxcnc.MODE_MDI

    def override_limits(self):
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.override_limits()
        self.api.wait_complete(0.5)

    def program_open(self, file):
        try:
            self.api.program_open(self.father.framework.machine.workspace + "/programs/" + file)
        except linuxcnc.error as e:
            self.father.framework.utils.service.service_write({"command": "launch:program:open", "message": "", "data": {"status": False, "file": file}})
            self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
            return False
        self.father.framework.utils.service.service_write({"command": "launch:program:open", "message": "", "data": {"status": True, "file": file}})
