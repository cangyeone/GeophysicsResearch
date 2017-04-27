"""
Demo of a PathPatch object.
"""
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.xkcd()
fig, ax = plt.subplots()

Path = mpath.Path
path_data = [
    (Path.MOVETO, (1.58, -2.57)),
    (Path.CURVE4, (0.35, -1.1)),
    (Path.CURVE4, (-1.75, 2.0)),
    (Path.CURVE4, (0.375, 2.0)),
    (Path.LINETO, (0.85, 1.15)),
    (Path.CURVE4, (2.2, 3.2)),
    (Path.CURVE4, (3, 0.05)),
    (Path.CURVE4, (2.0, -0.5)),
    (Path.CLOSEPOLY, (1.58, -2.57)),
    ]




codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)


data=[(1.58, -2.57),(-1.5,2.3),(0.85, 1.15),
(1.58, -2.57),(-0,1),(0.85, 1.15),
(1.58, -2.57),(1,0),(0.85, 1.15),
(1.58, -2.57),(1.7,1),(0.85, 1.15),
(1.58, -2.57),(2,3),(0.85, 1.15)
]
code=[Path.MOVETO,Path.CURVE3,Path.CURVE3,
Path.MOVETO,Path.CURVE3,Path.CURVE3,
Path.MOVETO,Path.CURVE3,Path.CURVE3,
Path.MOVETO,Path.CURVE3,Path.CURVE3,
Path.MOVETO,Path.CURVE3,Path.CURVE3
]
pth=mpath.Path(data,code)
ppth=mpatches.PathPatch(pth, facecolor='none',
linestyle='dashed',
edgecolor='white', alpha=0.3)
#ax.add_patch(ppth)

# plot control points and connecting lines
x, y = zip(*path.vertices)
line, = ax.plot(x, y, 'go-')

ax.text(-2,-1.5,r"$\left[\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}\right]$!")
ax.text(-2,3,"Cangye@hotmail.com")
ax.text(1.58, -2.57,"1")
ax.text(0.35, -1.1,"2")
ax.text(-1.75, 2.0,"3")
ax.text(0.375, 2.0,"4")
ax.text(0.85, 1.15,"5")
ax.text(2.2, 3.2,"6")
ax.grid()
ax.axis('equal')
plt.show()
