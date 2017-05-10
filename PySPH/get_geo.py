import numpy as np
from scipy import interpolate
import numpy
from numpy import concatenate, where, array
try:
    from pysph.base.utils import get_particle_array_wcsph, get_particle_array_iisph
except:
    print("Need PySPH,try to download....")
    import os
    os.system("pip install pysph")


class GetGeo():
    def __init__(self,fileName='srtm_57_06.asc'):
        try:
            self.file=open(fileName,'r')
        except:
            print("Try to download SRTM data..")
    def get_data(self,xrange=[101.90,101.96],yrange=[30.82,30.88],xn=100,yn=100):
        adata=self.file.readlines()
        self.file.close()
        ncols=int(self.get_head_num(adata[0])[1])
        nrows=int(self.get_head_num(adata[1])[1])
        xmin =float(self.get_head_num(adata[2])[1])
        ymin =float(self.get_head_num(adata[3])[1])
        cell =float(self.get_head_num(adata[4])[1])
        
        xl =int((xrange[0]-xmin)/cell)
        xr =int((xrange[1]-xmin)/cell)
        
        yl =int((yrange[0]-ymin)/cell)
        yr =int((yrange[1]-ymin)/cell)
        
        xrg=np.linspace(0,xrange[1]-xrange[0]-cell,xr-xl)
        yrg=np.linspace(0,yrange[1]-yrange[0]-cell,yr-yl)
        
        
        Z=self.get_body_num(adata,xl,xr,yl,yr)
        func= interpolate.interp2d(xrg,yrg,Z,kind='cubic')
        
        NX=np.linspace(0,xrange[1]-xrange[0]-cell,xn)
        NY=np.linspace(0,xrange[1]-xrange[0]-cell,yn)
        NZ=func(NX,NY)

        import matplotlib.pyplot as plt

        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt 

        fig = plt.figure()
        ax = Axes3D(fig)

        NNX,NNY=np.meshgrid(NX,NY)
        ax.plot_wireframe(NNX,NNY,NZ)
        plt.show()
        return NZ
    def get_head_num(self,st):
        return [aa for aa in st.split(' ') if len(aa)>0]
    def get_body_num(self,adata,xl,xr,yl,yr):
        re=[]
        for itr in adata[6+yl:6+yr]:
            re.append([float(aa) for aa in itr.strip().split(' ') 
            if(len(aa))>0][xl:xr])
        return np.array(re)

    
    
from pyzoltan.core.carray import LongArray
class DamBreak3DGeometry(object):
    def __init__(
        self, container_height=2.0, container_width=2.0, container_length=2.0,
        fluid_column_height=0.55, fluid_column_width=1.0, fluid_column_length=1.228,
        obstacle_center_x=2.5, obstacle_center_y=0,
        obstacle_length=0.16, obstacle_height=0.161, obstacle_width=0.4,
        nboundary_layers=5, with_obstacle=True, dx=0.02, hdx=1.2, rho0=1000.0):

        # save the geometry details
        self.container_width = container_width
        self.container_length = container_length
        self.container_height = container_height

        self.fluid_column_length=fluid_column_length
        self.fluid_column_width=fluid_column_width
        self.fluid_column_height=fluid_column_height

        self.obstacle_center_x = obstacle_center_x
        self.obstacle_center_y = obstacle_center_y

        self.obstacle_width=obstacle_width
        self.obstacle_length=obstacle_length
        self.obstacle_height=obstacle_height

        self.nboundary_layers=nboundary_layers
        self.dx=dx

        self.hdx = hdx
        self.rho0 = rho0
        self.with_obstacle = with_obstacle

    def get_max_speed(self, g=9.81):
        return numpy.sqrt( 2 * g * self.fluid_column_height )

    def create_particles(self, **kwargs):
        fluid_column_height=self.fluid_column_height
        fluid_column_width=self.fluid_column_width
        fluid_column_length=self.fluid_column_length

        container_height = self.container_height
        container_length = self.container_length
        container_width = self.container_width

        obstacle_height = self.obstacle_height
        obstacle_length = self.obstacle_length
        obstacle_width = self.obstacle_width

        obstacle_center_x = self.obstacle_center_x
        obstacle_center_y = self.obstacle_center_y

        nboundary_layers = self.nboundary_layers
        dx = self.dx

        # get the domain limits
        ghostlims = nboundary_layers * dx

        xmin, xmax = 0.0 -ghostlims, container_length + ghostlims
        ymin, ymax = 0.0 - ghostlims, container_width + ghostlims
        zmin, zmax = 0.0 - ghostlims, container_height + ghostlims
        
        cw2 = 0.5 * container_width
        #ymin, ymax = -cw2 - ghostlims, cw2 + ghostlims

        # create all particles
        #import matplotlib.pyplot as plt

        #from mpl_toolkits.mplot3d import Axes3D
        #import matplotlib.pyplot as plt 

        #ig = plt.figure()
        #ax = Axes3D(fig)
        eps = 0.1 * dx
        xx, yy, zz = numpy.mgrid[xmin:xmax+eps:dx,
                                 ymin:ymax+eps:dx,
                                 zmin:zmax+eps:dx]

        x = xx.ravel(); y = yy.ravel(); z = zz.ravel()

        
        geom=GetGeo()
        gem=geom.get_data(xn=len(xx),yn=len(xx[0]))
        gem=np.transpose(gem)
        ges=np.ones_like(xx)
        
        for itr in range(len(xx[0,0])):
            ges[:,:,itr]=ges[:,:,itr]*gem
        ge=ges.ravel()
        
        ge=ge-np.min(ge)-0.1
        ge=ge/np.max(ge)*0.8
        #import matplotlib.pyplot as plt

        #from mpl_toolkits.mplot3d import Axes3D
        #import matplotlib.pyplot as plt 

        #ig = plt.figure()
        #ax = Axes3D(fig)

        # create a dummy particle array from which we'll sort
        pa = get_particle_array_wcsph(name='block', x=x, y=y, z=z)
        #pa.
        # get the individual arrays
        indices = []
        findices = []
        oindices = []

        obw2 = 0.5 * obstacle_width
        obl2 = 0.5 * obstacle_length
        obh = obstacle_height
        ocx = obstacle_center_x
        ocy = obstacle_center_y

        print(obw2,obl2,obh)
        #ax.scatter3D(x,y,z,alpha=0.05)
        gggx=xmax-xmin
        gggy=ymax-ymin
        for i in range(x.size):
            xi = x[i]; yi = y[i]; zi = ge[i]-z[i]

            # fluid
            if ( (xmin+gggx*0.4< xi <= xmin+gggx*0.6) and \
                     (ymin+gggy*0.4< yi < ymin+gggy*0.6) and \
                     (0 < -zi <= 0.3) ):
                #ax.scatter3D(xi,yi,zi,alpha=0.5)
                findices.append(i)

            # obstacle
            if ( (ocx-obl2 <= xi <= ocx+obl2) and \
                     (ocy-obw2 <= yi <= ocy+obw2) and \
                     (0 < -zi <= obh) ):
                #ax.scatter3D(xi,yi,zi,alpha=0.5)
                findices.append(i)
                oindices.append(i)
        #plt.show()
        # extract the individual arrays
        fa = LongArray(len(findices)); fa.set_data(numpy.array(findices))
        fluid = pa.extract_particles(fa)
        fluid.set_name('fluid')

        if self.with_obstacle:
            oa = LongArray(len(oindices)); oa.set_data(numpy.array(oindices))
            obstacle = pa.extract_particles(oa)
            obstacle.set_name('obstacle')
        """
        indices = concatenate( (where( y <= -cw2 )[0],
                                where( y >= cw2 )[0],
                                where( x >= container_length )[0],
                                where( x <= 0 )[0],
                                where( z <= 0 )[0]) )
        """
        # remove duplicates
        #        indices = array(list(set(indices)))
        indices=np.where(ge>z)[0]
        #print(np.where(ge>z))
        wa = LongArray(indices.size); wa.set_data(indices)
        boundary = pa.extract_particles(wa)
        boundary.set_name('boundary')

        # create the particles
        if self.with_obstacle:
            particles = [fluid, boundary, obstacle]
        else:
            particles = [fluid, boundary]

        # set up particle properties
        h0 = self.hdx * dx

        volume = dx**3
        m0 = self.rho0 * volume

        for pa in particles:
            pa.m[:] = m0
            pa.h[:] = h0

            pa.rho[:] = self.rho0

        nf = fluid.num_real_particles
        nb = boundary.num_real_particles

        if self.with_obstacle:
            no = obstacle.num_real_particles
            print("3D dam break with %d fluid, %d boundary, %d obstacle particles"%(nf, nb, no))
        else:
            print("3D dam break with %d fluid, %d boundary particles"%(nf, nb))


        # load balancing props for the arrays
        #fluid.set_lb_props(['x', 'y', 'z', 'u', 'v', 'w', 'rho', 'h', 'm', 'gid',
        #                    'x0', 'y0', 'z0', 'u0', 'v0', 'w0', 'rho0'])
        fluid.set_lb_props( list(fluid.properties.keys()) )

        #boundary.set_lb_props(['x', 'y', 'z', 'rho', 'h', 'm', 'gid', 'rho0'])
        #obstacle.set_lb_props(['x', 'y', 'z', 'rho', 'h', 'm', 'gid', 'rho0'])
        boundary.set_lb_props( list(boundary.properties.keys()) )

        # boundary and obstacle particles can do with a reduced list of properties
        # to be saved to disk since they are fixed
        boundary.set_output_arrays( ['x', 'y', 'z', 'rho', 'm', 'h', 'p', 'tag', 'pid', 'gid'] )

        if self.with_obstacle:
            obstacle.set_lb_props( list(obstacle.properties.keys()) )
            obstacle.set_output_arrays( ['x', 'y', 'z', 'rho', 'm', 'h', 'p', 'tag', 'pid', 'gid'] )

        return particles
import numpy as np
import os 

if __name__=="__main__":
    #print(os.getcwd())
    aa=GetGeo()
    aa.get_data()
    dx = 0.1
    nboundary_layers=3
    hdx = 1.2
    rho0 = 1000.0
    
    geom=DamBreak3DGeometry(
            dx=dx, nboundary_layers=nboundary_layers, hdx=hdx, rho0=rho0,
            with_obstacle=False)
    fluid, boundary = geom.create_particles()
    print(type(fluid))