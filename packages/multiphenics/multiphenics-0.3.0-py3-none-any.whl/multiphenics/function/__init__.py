# Copyright (C) 2016-2022 by the multiphenics authors
#
# This file is part of multiphenics.
#
# multiphenics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# multiphenics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with multiphenics. If not, see <http://www.gnu.org/licenses/>.
#

from multiphenics.function.assign import assign
from multiphenics.function.block_assign import block_assign
from multiphenics.function.block_element import BlockElement
from multiphenics.function.block_function import BlockFunction
from multiphenics.function.block_function_space import BlockFunctionSpace
from multiphenics.function.block_split import block_split
from multiphenics.function.block_test_function import BlockTestFunction
from multiphenics.function.block_trial_function import BlockTrialFunction
from multiphenics.function.split import split
from multiphenics.function.test_function import TestFunction
from multiphenics.function.trial_function import TrialFunction

__all__ = [
    'assign',
    'block_assign',
    'BlockElement',
    'BlockFunction',
    'BlockFunctionSpace',
    'block_split',
    'BlockTestFunction',
    'BlockTrialFunction',
    'split',
    'TestFunction',
    'TrialFunction'
]
