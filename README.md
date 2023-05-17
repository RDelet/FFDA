# MLDeform

A library for machine learning of skeletal deformations on a skinned mesh.

This will try and make the logic as DCC agnostic as possible but the main target implementation will be
Autodesk Maya 2018 and above.

I encourage others to help improve this repo or to add implementations for other applications.

## Overview

This is a quick ELI5 overview of the system and the methodology used.

Let's say you have a production rig that has lots of complex pose driven deformations. These can be things like complex skinning where each vertice has multiple joints influencing it, or things like pose driven blendshapes, deltamushes and other deformers of that nature.

The cost to process all of these adds up and your character rig can get very slow.

Instead what if the computer could guess where the vertices should be based on the position of the joints?
This is where machine learning can be useful.

The first step is to reduce our complexity down. We do this by making sure that each vertex is influenced by only one joint and has no other deformers. This already speeds up our deformation speeds of the rig but leaves us with some very ugly deformations. The joints however help give stable deformations and allow us to have direct control over the rig itself.

Next, we make a record for each vertex on how far it is from where it's meant to be. We repeat this for each frame of our sample animation, and also record the rotation and translation values of our joints.

Now we have all the data needed for training our machine learning model.
For each joint, it is given the rotation and translation values of the joints as an input, and it's given the vertex offsets as the output. Based on that, it figures out the best way to go from the input to the output to guess the vertex offset values.

Finally we save the trained model out and can load it back in to our scene. If everything worked correctly it will be able to move the vertices to their correct positions based on the joint positions.

This can be incredibly quick, giving us a very good approximation of our initial complex rig, while being much quicker.

In fact, with some extra work, you can take this trained model and put it on a mobile device like an iPad and have it running faster than the initial rig could have on a super powered desktop, all while giving reasonably close approximations of the deformations we wanted.

As animators animate more scenes, we can feed more data into the machine learning model and it will get better over time too.
    
## Usage

### Installation

If you have the dependencies above installed, you can install this package by placing the MLDeform directory anywhere
on your `PYTHONPATH`.

If you're using Maya you can place the MLDeform directory in your scripts directory.

You need to install `Maya 2022`

Once installed run the following in command line:

```
mayapy.exe -m pip install numpy
mayapy.exe -m pip install tensorflow==1.15
mayapy.exe -m pip install matplotlib
```

### Train

```python
import os

import fdda
from fdda.logger import log
from fdda.architecture import Settings


# Activate pycharm debug (only for pycharm pro)
debug_with_pycharm = True
if debug_with_pycharm:
    from fdda import pycharm_debug
    pycharm_debug.connect(port=50016)

# Get output directory
scene_name = cmds.file(query=True, sceneName=True)
if not scene_name:
    raise RuntimeError("Scene must be save before train !")

directory_path, file_name = os.path.split(scene_name)
output_path = os.path.normpath(os.path.join(directory_path, file_name.split(".")[0]))
if not os.path.exists(output_path):
    os.mkdir(output_path)
    log.info(f"Create directory: {output_path}")

# Train
settings = Settings.default()
settings.rate = 1e-4
settings.layers = 5
settings.epochs = 300
fdda.build_models("Tube", "Tube1", output_path, settings=settings, bind=True)
```

## Notes

This repo is not very mature.
Known issues:

* Normalization causes deformation issues. Still need to fix it.
* No C++ deformer for Maya yet
* Data structure may change to be lighter.

## Reference Reading

Here are projects used as references for this


* [Fast and Deep Deformation Approximations](http://graphics.berkeley.edu/papers/Bailey-FDD-2018-08/index.html)
 ( Stephen W. Bailey, Dave Otte, Paul Dilorenzo, and James F. O'Brien. )
 
* ['Fast and Deep Deformation Approximations’ Implementation](http://3deeplearner.com/fdda-implementation/)
 ( [3DeepLearner](http://3deeplearner.com/) )

* (https://github.com/syedharoonalam/MLDeform)
 
 
## Dependencies
 
 There are a few Python depencies you will need.
 
### Required
 
* **six**
   
 Needed for supporting Python3

* **tensorflow**
 
  Required for the actual training and deformers.
    
  **NOTE:** Some platforms have issues importing Tensorflow into Maya.
    
  To workaround this, you need to add a file called `__init__.py` to the `google` package so that it can be imported properly.
    
  Find the google package by running `from google import protobuf;print(protobuf.__file__)`.
  This gives you the location of the protobuf folder.
  The parent directory will be the google package.
 
 * **pandas**

    Necessary for efficient processing of data objects  
  
* **matplotlib**

  If you intend to display training plots, this is an optional requirement.
