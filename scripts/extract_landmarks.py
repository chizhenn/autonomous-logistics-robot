#!/usr/bin/env python
import os, yaml, rospkg
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')           
import matplotlib.pyplot as plt
 
# load map from package
pkg = rospkg.RosPack().get_path('slam_navigation')
map_yaml = os.path.join(pkg, 'maps', 'my_map.yaml')
with open(map_yaml) as f:
    m = yaml.safe_load(f)
 
img_path = m['image']
if not os.path.isabs(img_path):
    img_path = os.path.join(pkg, 'maps', img_path)
img = np.array(Image.open(img_path).convert('L'))
 
# wall pixels are dark; collect their (x,y) coordinates
walls = np.argwhere(img < 50)           
coords = np.column_stack([walls[:,1], walls[:,0]]).astype(float)  # (x,y)
 
# RANSAC line extraction
def ransac_lines(points, n_lines=12, iters=300, thresh=2.0, min_inliers=40):
    pts = points.copy()
    lines = []
    for _ in range(n_lines):
        if len(pts) < min_inliers:
            break
        best_in, best = None, None
        for _ in range(iters):
            i, j = np.random.choice(len(pts), 2, replace=False)
            p1, p2 = pts[i], pts[j]
            d = p2 - p1
            norm = np.hypot(*d)
            if norm == 0:
                continue
            nx, ny = -d[1]/norm, d[0]/norm
            dist = np.abs((pts - p1) @ np.array([nx, ny]))
            inl = dist < thresh
            if best_in is None or inl.sum() > best_in.sum():
                best_in, best = inl, (p1, p2)
        if best_in is None or best_in.sum() < min_inliers:
            break
        inpts = pts[best_in]
        mean = inpts.mean(0)
        _, _, vt = np.linalg.svd(inpts - mean)
        dirv = vt[0]
        t = (inpts - mean) @ dirv
        e1 = mean + dirv*t.min()
        e2 = mean + dirv*t.max()
        lines.append((e1, e2))
        pts = pts[~best_in]
    return lines
 
lines = ransac_lines(coords)
print("Landmarks (walls) extracted:", len(lines))
 
# plot result
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(img, cmap='gray'); ax[0].set_title('Original Map'); ax[0].axis('off')
ax[1].imshow(img, cmap='gray', alpha=0.3)
for e1, e2 in lines:
    ax[1].plot([e1[0], e2[0]], [e1[1], e2[1]], 'r-', lw=2)
    ax[1].plot([e1[0], e2[0]], [e1[1], e2[1]], 'bo', ms=4)
ax[1].set_title('Landmark Extraction (RANSAC)\nred=walls, blue=corners/endpoints')
ax[1].axis('off')
plt.tight_layout()
 
out = os.path.join(pkg, 'maps', 'landmarks.png')
plt.savefig(out, dpi=110, bbox_inches='tight')
print("Saved:", out)