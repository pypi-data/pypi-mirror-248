# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from nautilus_trader.indicators.base.indicator cimport Indicator


cdef class Stochastics(Indicator):
    cdef object _highs
    cdef object _lows
    cdef object _c_sub_l
    cdef object _h_sub_l

    cdef readonly int period_k
    """The K window period.\n\n:returns: `int`"""
    cdef readonly int period_d
    """The D window period.\n\n:returns: `int`"""
    cdef readonly double value_k
    """The current K line value..\n\n:returns: `double`"""
    cdef readonly double value_d
    """The current D line value.\n\n:returns: `double`"""

    cpdef void update_raw(self, double high, double low, double close)
