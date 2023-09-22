import json
import numpy as np
import os

from maya import cmds

from fdda import kBipedLimitsPath
from fdda.maya.core import api_utils
from fdda.maya.core.context import KeepCurrentFrame, DisableRefresh
from fdda.maya.core.skin import Skin


class PoseGenerator:

    def __init__(self, mesh: str):
        self._mesh = api_utils.get_node(mesh)
        self._skin = Skin.find(self._mesh)
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"
    
    @property
    def skin(self) -> Skin:
        return self._skin

    def _get_pose_data(self, data_path: str = None) -> np.array:
        data = {}
        if data_path and os.path.exists(data_path):
            with open(data_path, "r") as stream:
                data = json.load(stream)
        
        ranges = []
        for inf in self._skin.influences_names:
            short_name = inf.split("|")[-1].split(":")[-1]
            ranges.append(data.get(short_name, api_utils.get_rotation_limits(inf)))
        
        return np.array(ranges, dtype=np.float32)
    
    def _get_random_rotation(self, samples: int, data_path: str = None):
        ranges = self._get_pose_data(data_path)
        return np.random.uniform(low=ranges[:, :, 0],
                                 high=ranges[:, :, 1],
                                 size=(samples, self.skin.influences_count(), 3))

    @DisableRefresh()
    @KeepCurrentFrame()
    def generate(self, samples: int, data_path: str = kBipedLimitsPath):
        """!@Brief Generate and apply on the source mesh a set of N random rotations per joint."""
        random_rotation = self._get_random_rotation(samples, data_path)
        api_utils.set_time_line(0, samples)
        frame = api_utils.start_frame()
        for rot in random_rotation:
            for i, joint_name in enumerate(self.skin.influences_names):
                cmds.currentTime(frame)
                cmds.rotate(rot[i][0], rot[i][1], rot[i][2], joint_name)
                cmds.setKeyframe(joint_name)
            frame += 1
