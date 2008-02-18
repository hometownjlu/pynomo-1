#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007-2008  Leif Roschier  <lefakkomies@users.sourceforge.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from nomo_axis import *
from nomo_axis_func import *
from numpy import *
from pyx import *
from copy import copy

class Nomo_Wrapper:
    """
    class for building nomographs consisting of many blocks (pieces connected by
    a line)
    """
    def __init__(self,params={},paper_width=10.0,paper_height=10.0,filename='dummy.pdf'):
                # default parameters
        self.params_default={
            'title_str':'',
            'title_x': paper_width/2.0,
            'title_y': paper_height,
            'title_box_width': paper_width/2.2}
        self.params=self.params_default
        self.params.update(params)
        self.block_stack=[]
        self.filename=filename
        self.paper_width=paper_width
        self.paper_height=paper_height
        #self._build_axes_wrapper_()

    def add_block(self,nomo_block):
        """
        adds nomograph (Nomo_Block) to the wrapper
        """
        self.block_stack.append(nomo_block)
        # TODO: calculate transformation according to tag

    def _calc_trafo_(self,x1,y1,x2,y2,x3,y3,x1d,y1d,x2d,y2d,x3d,y3d):
        """
        transforms three points to three points via rotation and scaling
        and transformation
        xd = alpha1*x+beta1*y+gamma1
        yd = alpha2*x+beta2*y+gamma2
        alpha3=0, beta3=0, gamma3=0
        """
        mat=array([[x1,y1,1.0,0.0,0.0,0.0],
                   [0,0,0,x1,y1,1],
                   [x2,y2,1,0,0,0],
                   [0,0,0,x2,y2,1],
                   [x3,y3,1,0,0,0],
                   [0,0,0,x3,y3,1]])
        #print rank(mat)
        inverse=linalg.inv(mat)
        vec=dot(inverse,[x1d,y1d,x2d,y2d,x3d,y3d])
        alpha1=vec[0]
        beta1=vec[1]
        gamma1=vec[2]
        alpha2=vec[3]
        beta2=vec[4]
        gamma2=vec[5]
        alpha3=0.0
        beta3=0.0
        gamma3=1.0
        return alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3

    def _update_trafo_(self):
        """
        updates transformation to self.alpha1,...
        updates blocks
        """
        #self.axes_wrapper.fit_to_paper()
        self.axes_wrapper._print_result_pdf_("dummy1.pdf")
        self.alpha1,self.beta1,self.gamma1,\
        self.alpha2,self.beta2,self.gamma2,\
        self.alpha3,self.beta3,self.gamma3 = self.axes_wrapper.give_trafo()
        # update last block trafos, note that trafo to align blocks should not be
        # changed
        for block in self.block_stack:
            block.change_last_transformation(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
                           alpha3=self.alpha3,beta3=self.beta3,gamma3=self.gamma3)

#    def _update_block_trafos_(self):
#        """
#        updates (adds) transformation to blocks
#        """
#        for block in self.block_stack:
#            block.add_transformation(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
#                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
#                           alpha3=self.alpha3,beta3=self.beta3,gamma3=self.gamma3)

    def build_axes_wrapper(self):
        """
        builds full instance of class Axes_Wrapper to find
        transformation
        """
        self.axes_wrapper=Axes_Wrapper(paper_width=self.paper_width,
                                       paper_height=self.paper_height)
        for block in self.block_stack:
            for atom in block.atom_stack:
                self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x,atom.give_y,
                                                        atom.params['u_min'],
                                                        atom.params['u_max']))

    def do_transformation(self,method='scale paper',params=None):
        """
        main function to find and update transformation up to atoms
        """
        try:
            {'scale paper': self._do_scale_to_canvas_trafo_,
             'optimize':self._do_optimize_trafo_,
             'polygon':self._do_polygon_trafo_,
             'rotate': self._do_rotate_trafo_}[method](params)
        except KeyError:
            print "Wrong transformation identifier"

        #self.alpha1,self.beta1,self.gamma1,\
        #self.alpha2,self.beta2,self.gamma2,\
        #self.alpha3,self.beta3,self.gamma3 = self.axes_wrapper.give_trafo()
        self._update_trafo_()

    def _do_scale_to_canvas_trafo_(self,params):
        """
        Finds transformation to scale to canvas
        """
        self.axes_wrapper.fit_to_paper()
        self.axes_wrapper._print_result_pdf_("dummy1_paper.pdf")

    def _do_optimize_trafo_(self,params):
        """
        Finds "optimal" transformation
        """
        self.axes_wrapper.optimize_transformation()
        self.axes_wrapper._print_result_pdf_("dummy1_optimize.pdf")

    def _do_polygon_trafo_(self,params):
        """
        Finds "polygon" transformation
        """
        self.axes_wrapper.make_polygon_trafo()
        self.axes_wrapper._print_result_pdf_("dummy1_polygon.pdf")

    def _do_rotate_trafo_(self,params):
        """
        Finds transformation to scale to canvas
        """
        self.axes_wrapper.rotate_canvas(params)
        self.axes_wrapper._print_result_pdf_("dummy1_rotate.pdf")

    def draw_nomogram(self,canvas):
        """
        draws the nomogram = draws blocks, titles, etc.
        """
        for block in self.block_stack:
            block.draw(canvas)
        c.writePDFfile(self.filename)

    def align_blocks(self):
        """
        aligns blocks w.r.t. each other according to 'tag' fields
        in Atom params dictionary
        """
        for idx1,block1 in enumerate(self.block_stack):
            for idx2,block2 in enumerate(self.block_stack):
                if idx2>idx1:
                    for atom1 in block1.atom_stack:
                        for atom2 in block2.atom_stack:
                            if atom1.params['tag']==atom2.params['tag']\
                            and not atom1.params['tag']=='none':
                                print atom1.params['tag']
                                alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
                                self._find_trafo_2_atoms_(atom1,atom2)
                                block2.add_transformation(alpha1,beta1,gamma1,
                                                           alpha2,beta2,gamma2,
                                                           alpha3,beta3,gamma3)
        # let's make identity matrix that will be changed when optimized
        for block in self.block_stack:
            block.add_transformation()


    def _find_trafo_2_atoms_(self,atom1,atom2):
        """
        finds transformation that aligns atom2 to atom1
        In practice takes endpoints and a third point in 90 degree
        to form a triangle for both atoms to be aligned
        """
        # taking points from atom1
        u_start=atom1.params['u_min']
        u_stop=atom1.params['u_max']
        x1_atom_1=atom1.give_x(u_start)
        y1_atom_1=atom1.give_y(u_start)
        x2_atom_1=atom1.give_x(u_stop)
        y2_atom_1=atom1.give_y(u_stop)
        x3_atom_1=x1_atom_1+(y2_atom_1-y1_atom_1)*0.01
        y3_atom_1=y1_atom_1-(x2_atom_1-x1_atom_1)*0.01

        x1_atom_2=atom2.give_x(u_start)
        y1_atom_2=atom2.give_y(u_start)
        x2_atom_2=atom2.give_x(u_stop)
        y2_atom_2=atom2.give_y(u_stop)
        x3_atom_2=x1_atom_2+(y2_atom_2-y1_atom_2)*0.01
        y3_atom_2=y1_atom_2-(x2_atom_2-x1_atom_2)*0.01
        alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
        self._calc_trafo_(x1_atom_2,y1_atom_2,x2_atom_2,y2_atom_2,x3_atom_2,y3_atom_2,
                     x1_atom_1,y1_atom_1,x2_atom_1,y2_atom_1,x3_atom_1,y3_atom_1)
        return alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3

class Nomo_Block:
    """
    class to hold separate nomograph blocks connected by a single line in
    order to build the whole nomograph consisting of multiple blocks
    """
    def __init__(self,mirror=False):
        """
        if mirror=True the transformation wrt to other blocks is mirrored
        """

        """
        Idea is that block has one own tranformation that aligns it with respect to other
        blocks and one overall transformation that optimizes axes w.r.t. paper size.
        Overall transformation is calculated using class Axis_Wrapper in nomo_axis_func.py
        in wrapper class Nomo_Wrapper.
        """
        # initial transformation
        self.atom_stack=[] # atoms
        self.trafo_stack=[] # stack for transformation matrices for block
        self.add_transformation() # adds initial unit transformation


    def add_atom(self,atom):
        """
        adds atom to the block
        """
        self.atom_stack.append(atom)

    def add_transformation(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                             alpha2=0.0,beta2=1.0,gamma2=0.0,
                             alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        adds transformation to be applied as a basis.
        all transformation matrices are multiplied together
        """
        trafo_mat = array([[alpha1,beta1,gamma1],
                          [alpha2,beta2,gamma2],
                          [alpha3,beta3,gamma3]])
        self.trafo_stack.append(trafo_mat)
        self._calculate_total_trafo_mat_() # update coeffs (also in atoms)

    def change_last_transformation(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                                   alpha2=0.0,beta2=1.0,gamma2=0.0,
                                   alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        adds transformation to be applied as a basis.
        all transformation matrices are multiplied together
        """
        trafo_mat = array([[alpha1,beta1,gamma1],
                          [alpha2,beta2,gamma2],
                          [alpha3,beta3,gamma3]])
        self.trafo_stack.pop() # last away
        self.trafo_stack.append(trafo_mat)
        self._calculate_total_trafo_mat_() # update coeffs (also in atoms)

    def _calculate_total_trafo_mat_(self):
        """
        calculates total transformation matrix and
        master coeffs self.alpha1,self.beta1,...
        """
        stack_copy=copy(self.trafo_stack)
        stack_copy.reverse()
        trafo_mat=stack_copy.pop()
        for matrix in stack_copy:
            trafo_mat=dot(trafo_mat,matrix) # matrix multiplication
        self.alpha1=trafo_mat[0][0]
        self.beta1=trafo_mat[0][1]
        self.gamma1=trafo_mat[0][2]
        self.alpha2=trafo_mat[1][0]
        self.beta2=trafo_mat[1][1]
        self.gamma2=trafo_mat[1][2]
        self.alpha3=trafo_mat[2][0]
        self.beta3=trafo_mat[2][1]
        self.gamma3=trafo_mat[2][2]
        self._set_trafo_to_atoms()

    def _set_trafo_to_atoms(self):
        """
        sets overall transformation to all atoms
        """
        for atom in self.atom_stack:
            atom.set_trafo(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
                           alpha3=self.alpha3,beta3=self.beta3,gamma3=self.gamma3)

#    Maybe not needed
#
#    def give_trafo_x(self,x,y):
#        """
#        transformed x-coordinate
#        """
#        return ((self.alpha1*x+self.beta1*y+self.gamma1)\
#        /(self.alpha3*x+self.beta3*y+self.gamma3))
#
#    def give_trafo_y(self,x,y):
#        """
#        transformed y-coordinate
#        """
#        return ((self.alpha2*x+self.beta2*y+self.gamma2)\
#        /(self.alpha3*x+self.beta3*y+self.gamma3))


    def draw(self,canvas):
        """
        draws the Atoms of block
        """
        for atom in self.atom_stack:
            atom.draw(canvas)

class Nomo_Block_Type_1(Nomo_Block):
    """
    type F1+F2=F3
    """
    def __init__(self):
        super(Nomo_Block_Type_1,self).__init__()

    def define_F1(self,params):
        """
        defines function F1
        """
        params['F']=lambda u:-1
        params['G']=lambda u:params['function'](u)
        self.atom_F1=Nomo_Atom(params)
        self.add_atom(self.atom_F1)
        # for axis calculations
        self.F1_axis=Axis_Wrapper(f=params['F'],g=params['G'],
                             start=params['u_min'],stop=params['u_max'])

    def define_F2(self,params):
        """
        defines function F2
        """
        params['F']=lambda u:0
        params['G']=lambda u:-0.5*params['function'](u)
        self.atom_F2=Nomo_Atom(params)
        self.add_atom(self.atom_F2)
        # for axis calculations
        self.F2_axis=Axis_Wrapper(f=params['F'],g=params['G'],
                             start=params['u_min'],stop=params['u_max'])

    def define_F3(self,params):
        """
        defines function F3
        """
        params['F']=lambda u:1.0
        params['G']=lambda u:-1.0*params['function'](u)
        self.atom_F3=Nomo_Atom(params)
        self.add_atom(self.atom_F3)
        # for axis calculations original parameters
        self.F3_axis=Axis_Wrapper(f=params['F'],g=params['G'],
                             start=params['u_min'],stop=params['u_max'])


    def set_width_height_propotion_original(self,width=10.0,height=10.0,proportion=1.0):
        """
        sets original width, height and x-distance proportion for the nomogram before
        transformations
        """
        p=proportion
        delta_1=proportion*width/(1+proportion)
        delta_3=width/(proportion+1)
        f1_max=self.F1_axis.calc_highest_point()
        f1_min=self.F1_axis.calc_lowest_point()
        f2_max=self.F2_axis.calc_highest_point()
        f2_min=self.F2_axis.calc_lowest_point()
        f3_max=self.F3_axis.calc_highest_point()
        f3_min=self.F3_axis.calc_lowest_point()
        # assume mu_3=1, mu_1 = proportion for a moment
        max_y=max(p*f1_max,p/(1+p)*f2_max,f3_max)
        min_y=min(p*f1_max,p/(1+p)*f2_max,f3_max)
        y_distance=max_y-min_y
        multiplier=height/y_distance
        mu_1=p*multiplier
        mu_3=multiplier
        # redefine scaled functions
        self.atom_F1.f=self.F1_axis.f*delta_1
        self.atom_F1.g=self.F1_axis.g*mu_1
        self.atom_F2.f=self.F2_axis.f
        self.atom_F2.g=self.F2_axis.g*(mu_1*mu_3)/(mu_1+mu_3)
        self.atom_F3.f=self.F1_axis.f*delta_3
        self.atom_F3.g=self.F1_axis.g*mu_3


class Nomo_Atom:
    """
    class for single axis or equivalent.
    """
    def __init__(self,params):
        # default parameters
        self.params_default={
            'u_min':0.1,
            'u_max':1.0,
            'F':lambda u:u, # x-coordinate
            'G':lambda u:u, # y-coordinate
            'title':'f1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear', #'linear' 'log' 'manual point' 'manual line'
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'} # for aligning block wrt others
        self.params=self.params_default
        self.params.update(params)
        self.set_trafo() # initialize
        self.f = self.params['F'] # x-coord func
        self.g = self.params['G'] # y-coord func

    def set_trafo(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                           alpha2=0.0,beta2=1.0,gamma2=0.0,
                           alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        """
        self.alpha1=alpha1
        self.beta1=beta1
        self.gamma1=gamma1
        self.alpha2=alpha2
        self.beta2=beta2
        self.gamma2=gamma2
        self.alpha3=alpha3
        self.beta3=beta3
        self.gamma3=gamma3

    def give_x(self,u):
        """
        x-function
        """
        value=(self.alpha1*self.f(u)+self.beta1*self.g(u)+self.gamma1)/\
        (self.alpha3*self.f(u)+self.beta3*self.g(u)+self.gamma3)
        return value

    def give_y(self,u):
        """
        y-function
        """
        value=(self.alpha2*self.f(u)+self.beta2*self.g(u)+self.gamma2)/\
        (self.alpha3*self.f(u)+self.beta3*self.g(u)+self.gamma3)
        return value

    def draw(self,canvas):
        """
        draws the axis
        """
        p=self.params
        Nomo_Axis(func_f=self.give_x,func_g=self.give_y,
                  start=p['u_min'],stop=p['u_max'],
                  turn=-1,title=p['title'],canvas=canvas,type=p['scale_type'],
                  tick_levels=p['tick_levels'],tick_text_levels=p['tick_text_levels'],
                  side=p['tick_side'])


if __name__=='__main__':
    """
    testing
    """
    test=Nomo_Wrapper()
    #print test._calc_trafo_(1,0,1,1,2,0,1,0,1,1,2,0)
    #print test._calc_trafo_(1,0,1,1,2,0,4,1,4,2,5,1)
    """
    0. build definitions of atoms
    1. build block1
    2. build block2
    3. build nomowrapper
    4. add block1 and block2
    5. optimize transformation
    6. draw nomogram in nomowrapper
    """

    # build atoms
    block1_atom1_para={
            'u_min':3.0,
            'u_max':10.0,
            'F':lambda u:0,
            'G':lambda u:u,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'}
    b1_atom1=Nomo_Atom(params=block1_atom1_para)

    block1_atom2_para={
            'u_min':3.0,
            'u_max':10.0,
            'F':lambda u:1.0,
            'G':lambda u:u,
            'title':'b1 a2',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'}
    b1_atom2=Nomo_Atom(params=block1_atom2_para)

    block1_atom3_para={
            'u_min':0.0,
            'u_max':10.0,
            'F':lambda u:2.0,
            'G':lambda u:u,
            'title':'b1 a3',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}

    b1_atom3=Nomo_Atom(params=block1_atom3_para)

    # block 2
    block2_atom1_para={
            'u_min':0.0,
            'u_max':10.0,
            'F':lambda u:u,
            'G':lambda u:0.0+0.1*u,
            'title':'b2 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'B'}
    b2_atom1=Nomo_Atom(params=block2_atom1_para)

    block2_atom2_para={
            'u_min':0.0,
            'u_max':10.0,
            'F':lambda u:u,
            'G':lambda u:1.0+0.1*u,
            'title':'b2 a2',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'}
    b2_atom2=Nomo_Atom(params=block2_atom2_para)

    block2_atom3_para={
            'u_min':1.0,
            'u_max':10.0,
            'F':lambda u:u,
            'G':lambda u:2.0+0.1*u,
            'title':'b2 a3',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'left',
            'tag':'A'}

    b2_atom3=Nomo_Atom(params=block2_atom3_para)

    # block 3
    block3_atom1_para={
            'u_min':0.0,
            'u_max':10.0,
            'F':lambda u:u,
            'G':lambda u:0.0+0.5*u,
            'title':'b3 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'}
    b3_atom1=Nomo_Atom(params=block3_atom1_para)

    block3_atom2_para={
            'u_min':0.0,
            'u_max':10.0,
            'F':lambda u:0.1*u**2,
            'G':lambda u:1.0+0.5*u,
            'title':'b3 a2',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'none'}
    b3_atom2=Nomo_Atom(params=block3_atom2_para)

    block3_atom3_para={
            'u_min':1.0,
            'u_max':10.0,
            'F':lambda u:u,
            'G':lambda u:2.0+0.5*u,
            'title':'b3 a3',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'left',
            'tag':'B'}

    b3_atom3=Nomo_Atom(params=block3_atom3_para)


    block1=Nomo_Block()
    block1.add_atom(b1_atom1)
    block1.add_atom(b1_atom2)
    block1.add_atom(b1_atom3)

    block2=Nomo_Block()
    block2.add_atom(b2_atom1)
    block2.add_atom(b2_atom2)
    block2.add_atom(b2_atom3)

    block3=Nomo_Block()
    block3.add_atom(b3_atom1)
    block3.add_atom(b3_atom2)
    block3.add_atom(b3_atom3)

    wrapper=Nomo_Wrapper(paper_width=40.0,paper_height=20.0)
    wrapper.add_block(block1)
    wrapper.add_block(block2)
    wrapper.add_block(block3)
    wrapper.align_blocks()
    wrapper.build_axes_wrapper() # build structure for optimization
    #wrapper.do_transformation(method='scale paper')
    wrapper.do_transformation(method='rotate',params=30.0)
    wrapper.do_transformation(method='rotate',params=30.0)
    #wrapper.do_transformation(method='rotate',params=20.0)
    #wrapper.do_transformation(method='rotate',params=90.0)
    #wrapper.do_transformation(method='polygon')
    #wrapper.do_transformation(method='optimize')
    wrapper.do_transformation(method='scale paper')
    c=canvas.canvas()
    wrapper.draw_nomogram(c)