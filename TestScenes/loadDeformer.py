import json 

from MLDeform import deformer
deformer.load_plugin()

from maya import cmds
deformer1 = cmds.deformer(mesh, type='mldeformer')
cmds.select(deformer1)

data_file = '..\\output_data.json'
cmds.setAttr(deformer1[0] + '.trainingData', data_file, type='string')

with open(data_file, 'r') as f:
    data = json.load(f)
    
joint_names = data.get('joint_names')
for i, joint in enumerate(joint_names):
    cmds.connectAttr('%s.worldMatrix' % joint, '%s.matrix[%s]' % (deformer1[0], i))    