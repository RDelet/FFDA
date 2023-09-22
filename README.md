# FFDA
[Fast and Deep Deformation Approximations](http://graphics.berkeley.edu/papers/Bailey-FDD-2018-08/index.html)

# Authors
- [Rémi Deletrain](https://fr.linkedin.com/in/r%C3%A9mi-deletrain-3b296028)
- [Thomas Léglantier](https://www.linkedin.com/in/thomas-l%C3%A9glantier-ab318b157)

# Launch
```python
import sys

sys.path.insert(0, r"PATH/OF/YOUR/CODE")

from maya import cmds, OpenMaya

from fdda.maya import bind, train, generate_pose
from fdda.training.PyTorch.settings import Settings


selected = cmds.ls(selection=True, long=True)
if len(selected) != 2:
    raise RuntimeError("Selected Source and Destination !")
source, destination = selected

settings = Settings.default()
settings.split = 0.1
settings.units = 256
settings.device = Settings.kGpu

output_path = train(source, destination, settings, build_pose=True, num_pose=40)
bind(destination, output_path)
```
# Results
https://github.com/RDelet/FFDA/assets/7300189/eb5d7f20-a253-43f3-b71c-3908d721ff0e
