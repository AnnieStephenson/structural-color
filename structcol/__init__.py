# Copyright 2016, Vinothan N. Manoharan, Sofia Makgiriadou
#
# This file is part of the structural-color python package.
#
# This package is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This package is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this package. If not, see <http://www.gnu.org/licenses/>.

"""
The structural-color (structcol) python package includes theoretical models for
predicting the structural color from disordered colloidal samples (also known
as "photonic glasses").


Notes
-----
Based on work by Sofia Magkiriadou in the Manoharan Lab at Harvard University
[1]_

Requires pint:
PyPI: https://pypi.python.org/pypi/Pint/
Github: https://github.com/hgrecco/pint
Docs: https://pint.readthedocs.io/en/latest/

References
----------
[1] Magkiriadou, S., Park, J.-G., Kim, Y.-S., and Manoharan, V. N. “Absence of
Red Structural Color in Photonic Glasses, Bird Feathers, and Certain Beetles”
Physical Review E 90, no. 6 (2014): 62302. doi:10.1103/PhysRevE.90.062302

.. moduleauthor :: Vinothan N. Manoharan <vnm@seas.harvard.edu>
.. moduleauthor :: Sofia Magkiriadou <sofia@physics.harvard.edu>.
"""

# Load the default unit registry from pint and use it everywhere.
# Using the unit registry (and wrapping all functions) ensures that we don't
# make unit mistakes.
# Also load commonly used functions from pymie package
from pymie import Quantity, ureg, q, index_ratio, size_parameter, np, mie

def refraction(angles, n_before, n_after):
    '''
    Returns angles after refracting through an interface
    
    Parameters
    ----------
    angles: float or array of floats
        angles relative to normal before the interface
    n_before: float
        Refractive index of the medium light is coming from
    n_after: float
        Refractive index of the medium light is going to
    
    '''
    snell = n_before / n_after * np.sin(angles)
    snell[abs(snell) > 1] = np.nan # this avoids a warning
    return np.arcsin(snell)

def normalize(x,y,z):
    '''
    normalize a vector
    
    Parameters
    ----------
    x: float or array
        1st component of vector
    y: float or array
        2nd component of vector
    z: float or array
        3rd component of vector
    
    Returns
    -------
    array of normalized vector(s) components
    '''
    magnitude = np.sqrt(np.abs(x)**2 + np.abs(y)**2 + np.abs(z)**2)

    # we ignore divide by zero error here because we do not want an error
    # in the case where we try to normalize a null vector <0,0,0>
    with np.errstate(divide='ignore',invalid='ignore'):
        return np.array([x/magnitude, y/magnitude, z/magnitude])