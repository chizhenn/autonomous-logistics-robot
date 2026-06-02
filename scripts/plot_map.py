#!/usr/bin/env python
import yaml, matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import rospkg, os

pkg = rospkg.RosPack().get_path('slam_navigation')

# load map
m  = yaml.safe_load(open(os.path.join(pkg, 'maps', 'my_map.yaml')))
img_path = m['image']
if not os.path.isabs(img_path):
    img_path = os.path.join(pkg, 'maps', img_path)
img = np.array(Image.open(img_path))
res, ox, oy = m['resolution'], m['origin'][0], m['origin'][1]

# load waypoints
wp = yaml.safe_load(open(os.path.join(pkg, 'maps', 'waypoints.yaml')))

plt.imshow(img, cmap='gray', origin='upper')
for name, p in wp.items():
    px = (p['x'] - ox) / res            
    py = img.shape[0] - (p['y'] - oy) / res
    plt.plot(px, py, 'ro')
    plt.text(px+5, py, name, color='red')

out = os.path.join(pkg, 'maps', 'waypoints_map.png')  
plt.savefig(out, dpi=110, bbox_inches='tight')
print("Saved:", out)
plt.show()