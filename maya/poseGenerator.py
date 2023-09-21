import numpy as np

from maya import cmds, OpenMaya

from fdda.core import api_utils
from fdda.core.context import KeepCurrentFrame, DisableRefresh
from fdda.core.skin import Skin


class PoseGenerator:

    def __init__(self, mesh: str):
        self._mesh = api_utils.get_node(mesh)
        self._skin = Skin.find(self._mesh)
    
    def __str__(self) -> str:
        return self.__repr__
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"
    
    @property
    def skin(self):
        return self._skin

    @DisableRefresh()
    @KeepCurrentFrame()
    def generate(self, samples_per_joint: int):
        """!@Brief Generate and apply on the source mesh a set of N random rotations per joint."""
        ranges = (np.array(self.skin.influences_ranges, dtype=np.float32) * 180.0) / np.pi
        random_rotation = np.random.uniform(low=ranges[:, :, 0],
                                            high=ranges[:, :, 1],
                                            size=(samples_per_joint, len(self.skin.influences_names), 3))

        frame = api_utils.start_frame()
        for rot in random_rotation:
            for i, joint_name in enumerate(self.skin.influences_names):
                cmds.currentTime(frame)
                cmds.rotate(rot[i][0], rot[i][1], rot[i][2], joint_name)
                cmds.setKeyframe(joint_name)
            frame += 1
