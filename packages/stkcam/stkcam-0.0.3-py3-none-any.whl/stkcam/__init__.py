from enum import Enum
import threading
import re

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject
Gst.init(None)


class CamType(Enum):
    OV5647 = 1
    IMX219 = 2

BOOT_CONFIG_PATH = '/boot/config.txt'

BOOT_OVERLAY_SETTINGS = {
    CamType.OV5647: 'camera-ov5647-overlay',
    CamType.IMX219: ''
}

def check_config(value: str) -> bool:
    with open(BOOT_CONFIG_PATH, 'r') as file:
        match = False
        for line in file:
            match = re.search(r'^overlay=(.*)', line)
            if match:
                match_value = match.group(1)
                return True if match_value == value else False
    return False

def check_cam_seeting(type: CamType):
    if type == CamType.OV5647 and check_config(BOOT_OVERLAY_SETTINGS[type]):
        pass
    elif type == CamType.IMX219 and not check_config(BOOT_OVERLAY_SETTINGS[CamType.OV5647]):
        pass
    else:
        raise Exception(
            'Should set camera configuration by command, sudo tinker-config, and reboot device'
        )

class TKCam:
    def __init__(self, cam_type: CamType):
        check_cam_seeting(cam_type)
        self.cam = None
        self._idle = True

    def _on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.cam.set_state(Gst.State.NULL)
            self._idle = True
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            self._idle = True
            print('error: {}, {}'.format(err, debug))
        return True

    @property
    def idle(self):
        return self._idle

    def preview(self):
        if self._idle:
            pipe_string = 'v4l2src ! video/x-raw,format=NV12,width=640,height=480 ! videoconvert ! autovideosink'   # fix 640:480 now
            self.cam = Gst.parse_launch(pipe_string)
            bus = self.cam.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)
            g_loop = threading.Thread(target=GObject.MainLoop().run)
            g_loop.daemon = True
            g_loop.start()
            self.cam.set_state(Gst.State.PLAYING)
            self._idle = False
        else:
            print('camera is busy now')

    def take_image(self, file_path: str):
        if self._idle:
            pipe_string = 'v4l2src num-buffers=1 ! video/x-raw,format=NV12,width=640,height=480 ! jpegenc ! multifilesink location={}'.format(file_path) # fix 640:480 now
            self.cam = Gst.parse_launch(pipe_string)
            bus = self.cam.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)
            g_loop = threading.Thread(target=GObject.MainLoop().run)
            g_loop.daemon = True
            g_loop.start()
            self.cam.set_state(Gst.State.PLAYING)
            self._idle = False
        else:
            print('camera is busy now')