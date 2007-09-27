#    PyNomo - nomographs with Python
#    Copyright (C) 2007  Leif Roschier
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
""" PyNomo - nomographs or nomograms with Python

Pynomo is a program to create (pdf) nomographs (nomograms)
using Python interpreter. A nomograph (nomogram) is a graphical
solution to an equation.
"""
from distutils.core import setup
setup(name='PyNomo',
      version='0.1.0a1',
      description='PyNomo - Python Nomograms',
      author='Leif Roschier',
      author_email='lefakkomies@sourceforge.net',
      url='http://pynomo.org/',
      download_url='http://sourceforge.net/project/showfiles.php?group_id=201522',
      packages=['pynomo'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: by Industry or Sector :: Science/Research',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI-Approved Open Source :: GNU General Public License (GPL)',
          'Operating System :: Grouping and Descriptive Categories :: OS Independent (Written in an interpreted language)',
          'Programming Language :: Python',
          ],
      )