# Construct a 2-D grid and interpolate on it:

from scipy import interpolate
x = np.arange(-4.01, 4.01, 0.25)
y = np.arange(-5.01, 5.01, 0.05)
xx, yy = np.meshgrid(x, y)
z = np.sin(xx**2+yy**2)
f = interpolate.interp2d(x, y, z, kind='cubic')

# Now use the obtained interpolation function and plot the result:

import matplotlib.pyplot as plt
xnew = np.arange(-5.01, 5.01, 1e-2)
ynew = np.arange(-5.01, 5.01, 1e-2)
znew = f(xnew, ynew)
plt.plot(x, z[0, :], 'ro-', xnew, znew[0, :], 'b-')
plt.show()
