#    PyNomo - nomographs with Python
#    Copyright (C) 2007-2008  Leif Roschier
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
from nomo_wrapper import *


class Nomographer:
    """
    Top-level class to build nomographs
    """
    def __init__(self,params):
        """
        params hold all information to build the nomograph
        """
        self._check_params_(params) # sets default values for missing keys
        wrapper=Nomo_Wrapper(paper_width=params['paper_width'],
                             paper_height=params['paper_height'],
                             filename=params['filename'])
        blocks=[]
        for block_para in params['block_params']:
            # TYPE 1
            if block_para['block_type']=='type_1':
                self._check_block_type_1_params_(block_para)
                blocks.append(Nomo_Block_Type_1(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     proportion=block_para['proportion'])
                wrapper.add_block(blocks[-1])
            # TYPE 2
            if block_para['block_type']=='type_2':
                self._check_block_type_2_params_(block_para)
                blocks.append(Nomo_Block_Type_2(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
            # TYPE 3
            if block_para['block_type']=='type_3':
                self._check_block_type_3_params_(block_para)
                blocks.append(Nomo_Block_Type_3(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                for axis_params in block_para['f_params']:
                    self._check_axis_params_(axis_params)
                    blocks[-1].add_F(axis_params)
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
            # TYPE 4
            if block_para['block_type']=='type_4':
                self._check_block_type_4_params_(block_para)
                blocks.append(Nomo_Block_Type_4(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                self._check_axis_params_(block_para['f4_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].define_F4(block_para['f4_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     float_axis=block_para['float_axis'],
                                     padding=block_para['padding'])
                wrapper.add_block(blocks[-1])
            # TYPE 5
            if block_para['block_type']=='type_5':
                self._check_block_type_5_params_(block_para)
                blocks.append(Nomo_Block_Type_5(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                blocks[-1].define_block(block_para)
                blocks[-1].set_block()
                wrapper.add_block(blocks[-1])
            # TYPE 6
            if block_para['block_type']=='type_6':
                self._check_block_type_6_params_(block_para)
                blocks.append(Nomo_Block_Type_6(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                blocks[-1].define(params1=block_para['f1_params'],
                                  params2=block_para['f2_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     type=block_para['type'],
                                     x_empty=block_para['x_empty'],
                                     y_empty=block_para['y_empty'])
                wrapper.add_block(blocks[-1])
            # TYPE 7
            if block_para['block_type']=='type_7':
                self._check_block_type_7_params_(block_para)
                blocks.append(Nomo_Block_Type_7(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width_1=block_para['width_1'],
                                     angle_u=block_para['angle_u'],
                                     angle_v=block_para['angle_v'])
                wrapper.add_block(blocks[-1])
            # TYPE 8
            if block_para['block_type']=='type_8':
                self._check_block_type_8_params_(block_para)
                blocks.append(Nomo_Block_Type_8(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f_params'])
                blocks[-1].define_F(block_para['f_params'])
                blocks[-1].set_block(length=block_para['length'])
                wrapper.add_block(blocks[-1])
            # TYPE 9
            if block_para['block_type']=='type_9':
                self._check_block_type_9_params_(block_para)
                blocks.append(Nomo_Block_Type_9(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_determinant(block_para['f1_params'],
                                              block_para['f2_params'],
                                              block_para['f3_params'],
                                              transform_ini=block_para['transform_ini'])

                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
        wrapper.align_blocks()
        wrapper.build_axes_wrapper() # build structure for transformations
        for trafo in params['transformations']:
            if len(trafo)>1:
                wrapper.do_transformation(method=trafo[0],params=trafo[1])
            else:
                wrapper.do_transformation(method=trafo[0])
        c=canvas.canvas()
        wrapper.draw_nomogram(c)

    def _check_params_(self,params):
        """
        checks if main params ok and adds default values
        """
        params_default={
                      'filename':'pynomo_default.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      #'block_params':[test1_block1_params,test1_block2_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_1_params_(self,params):
        """
        checks if block type 1 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0,
                         'proportion':1.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_2_params_(self,params):
        """
        checks if block type 2 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_3_params_(self,params):
        """
        checks if block type 3 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_4_params_(self,params):
        """
        checks if block type 4 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0,
                         'float_axis':'F1 or F2',
                         'padding':0.9}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_5_params_(self,params):
        """
        checks if block type 5 params ok and adds default values
        """
        params_default={
             'mirror_x':False,
             'mirror_y':False,
           'width':10.0,
           'height':10.0,
           #'u_func':lambda u:u,
           #'v_func':lambda x,v:x+v,
           #'u_values':[10.0,15.0,20.0,25.0,30.0,40.0,50.0,60.0],
           #'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
           'v_tick_side':'left',
           'u_title':'',
           'v_title':'',
           'u_reference':False, # manual labels
           'v_reference':False,
           'w_reference':False,
           'wd_reference':False,
           'wd_tick_levels':0,
           'wd_tick_text_levels':0,
           'wd_tag':'none',
           'w_tick_levels':0,
           'w_tick_text_levels':0,
           'horizontal_guides':False,
           }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_6_params_(self,params):
        """
        checks if block type 6 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0,
                         'type':'parallel',
                         'x_empty':0.2,
                         'y_empty':0.2
                         }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_7_params_(self,params):
        """
        checks if block type 7 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width_1':10.0,
                         'angle_u':45.0,
                         'angle_v':45.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_8_params_(self,params):
        """
        checks if block type 8 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'length':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_9_params_(self,params):
        """
        checks if block type 9 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0,
                         'transform_ini':False
                         }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_axis_params_(self,params):
        """
        checks (TODO: if axis params ok) and adds default values
        """
        params_default={
            'ID':'none', # to identify the axis
            'tag':'none', # for aligning block wrt others
            #'u_min':0.1,
            #'u_max':1.0,
            #'F':lambda u:u, # x-coordinate
            #'G':lambda u:u, # y-coordinate
            'title':'',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear', #'linear' 'log' 'manual point' 'manual line'
            'tick_levels':4,
            'tick_text_levels':3,
            'tick_side':'right',
            'reference':False,
            'reference padding': 0.20, # fraction of reference line over other lines
            'manual_axis_data':{},
            'title_distance_center':0.5,
            'title_opposite_tick':True,
            'title_draw_center':False
            }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

if __name__=='__main__':
    """
    tests
    """
    test1=False
    if test1:
        test1_f1_para={
                'u_min':1.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F1',
                'tick_levels':3,
                'tick_text_levels':2,
                }
        test1_f2_para={
                'u_min':0.1,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F2',
                'tick_levels':3,
                'tick_text_levels':2,
                'scale_type':'log',
                        }
        test1_f3_para={
                'u_min':1.0,
                'u_max':10.0,
                #'function':lambda u:u*12.0,
                'function':lambda u:u,
                'title':'F3',
                'tag':'A',
                'tick_side':'right'
                        }
        test1_f4_para={
                'u_min':-10.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F2',
                'tick_levels':3,
                'tick_text_levels':2,
                        }
        test1_block1_params={
                             'block_type':'type_1',
                             'width':10.0,
                             'height':10.0,
                             'proportion':0.5,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_block7_params={
                             'block_type':'type_7',
                             'width_1':10.0,
                             'angle_u':60.0,
                             'angle_v':60.0,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_params={
                      'filename':'test1.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test1_block1_params,test1_block7_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test1_params)

        test2_block2_params={
                             'block_type':'type_2',
                             'width':10.0,
                             'height':10.0,
                             'proportion':0.5,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test2_params={
                      'filename':'test2.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test2_block2_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test2_params)

        test3_block3_params={
                             'block_type':'type_3',
                             'width':10.0,
                             'height':10.0,
                             'f_params':[test1_f1_para,test1_f1_para,
                                         test1_f1_para,test1_f1_para,test1_f4_para]
                             }

        test3_params={
                      'filename':'test3.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test3_block3_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test3_params)

        test4_block4_params={
                             'block_type':'type_4',
                                'f1_params':test1_f1_para,
                                'f2_params':test1_f2_para,
                                'f3_params':test1_f3_para,
                                'f4_params':test1_f1_para,
                             }

        test4_params={
                      'filename':'test4.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test4_block4_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }

        Nomographer(test4_params)


        def f1(x,u):
            #return log(log(x/(x-u/100.0))/log(1+u/100.0))
            return log(log(x/(x-u/(100.0*12.0)))/log(1+u/(100.0*12.0)))

        test5_block5_params={
                           'block_type':'type_5',
                           'u_func':lambda u:log(u*12.0),
                           'v_func':f1,
                           'u_values':[10.0,15.0,20.0,25.0,30.0,40.0,50.0,60.0],
                           'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
                             }


        test5_params={
                      'filename':'test5.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test5_block5_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }

        Nomographer(test5_params)


        test6_block6_params={
                             'block_type':'type_6',
                                'f1_params':test1_f1_para,
                                'f2_params':test1_f2_para,
                             }
        test6_params={
                      'filename':'test6.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test6_block6_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test6_params)

    F_start=-40.0
    F_stop=90.0
    C_start=-40.0
    C_stop=30.0

    def celcius(fahrenheit):
        return (fahrenheit-32.0)/1.8

    test8_f1_para={
            'tag':'A',
            'u_min':F_start,
            'u_max':F_stop,
            'function':lambda u:celcius(u),
            'title':r'$^\circ$ F',
            'tick_levels':4,
            'tick_text_levels':3,
            'align_func':celcius,
            'title_x_shift':0.5
            }
    test8_f1c_para={
            'tag':'A',
            'u_min':F_start,
            'u_max':F_stop,
            'function':lambda u:celcius(u),
            'title':r'$^\circ$ F',
            'tick_levels':4,
            'tick_text_levels':3,
            'align_func':celcius,
            'title_x_shift':0.5,
            'align_x_offset':7.0
            }
    test8_f2_para={
            'tag':'A',
            'u_min':C_start,
            'u_max':C_stop,
            'function':lambda u:u,
            'title':r'$^\circ$ C',
            'tick_levels':5,
            'tick_text_levels':3,
            'scale_type':'linear',
            'tick_side':'left',
            'title_x_shift':-0.5
    }

    test8_block8a_params={
                         'block_type':'type_8',
                            'f_params':test8_f1_para
                         }
    test8_block8c_params={
                         'block_type':'type_8',
                            'f_params':test8_f1c_para
                            }
    test8_block8b_params={
                         'block_type':'type_8',
                         'length':5.0,
                            'f_params':test8_f2_para
                         }
    test8_params={
                  'filename':'test8.pdf',
                  'paper_height':20.0,
                  'paper_width':2.0,
                  'block_params':[test8_block8b_params,test8_block8a_params,
                                  test8_block8c_params],
                  'transformations':[('scale paper',)]
                  }
    Nomographer(test8_params)


    test9_f1_para={
            'u_min':0.5,
            'u_max':1.0,
            'f':lambda u:2*(u*u-1.0),
            'g':lambda u:3*u*(u+1.0),
            'h':lambda u:(-u*(u-1.0)),
            'title':'p',
            'tick_side':'left',
            'tick_levels':4,
            'tick_text_levels':2
            }
    test9_f2_para={
            'u_min':1.0,
            'u_max':0.75,
            'f':lambda v:v,
            'g':lambda v:1.0,
            'h':lambda v:(-v*v),
            'title':'h',
            'tick_side':'right',
            'tick_levels':3,
            'tick_text_levels':2
            }
    test9_f3_para={
            'u_min':1.0,
            'u_max':0.5,
            'f':lambda w:2.0*(2.0*w+1.0),
            'g':lambda w:3.0*(w+1.0),
            'h':lambda w:(-(w+1.0)*(2.0*w+1.0)),
            'title':'L',
            'tick_side':'left',
            'tick_levels':4,
            'tick_text_levels':2
            }
    test9_block_params={
                         'block_type':'type_9',
                         'f1_params':test9_f1_para,
                         'f2_params':test9_f2_para,
                         'f3_params':test9_f3_para,
                         'transform_ini':True,
                         }

    test9_params={
                  'filename':'test9.pdf',
                  'paper_height':10.0,
                  'paper_width':10.0,
                  'block_params':[test9_block_params],
                  'transformations':[('scale paper',)]
                  }
    Nomographer(test9_params)