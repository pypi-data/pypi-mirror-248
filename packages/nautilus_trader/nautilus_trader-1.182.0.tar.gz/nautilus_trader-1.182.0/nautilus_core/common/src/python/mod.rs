// -------------------------------------------------------------------------------------------------
//  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
//  https://nautechsystems.io
//
//  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
//  You may not use this file except in compliance with the License.
//  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
// -------------------------------------------------------------------------------------------------

pub mod clock;
pub mod timer;

use pyo3::prelude::*;

use crate::{enums, logging};

/// Loaded as nautilus_pyo3.common
#[pymodule]
pub fn common(_: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<enums::ComponentState>()?;
    m.add_class::<enums::ComponentTrigger>()?;
    m.add_class::<enums::LogColor>()?;
    m.add_class::<enums::LogLevel>()?;
    m.add_class::<enums::LogFormat>()?;
    m.add_class::<logging::LogGuard>()?;
    m.add_function(wrap_pyfunction!(logging::set_global_log_collector, m)?)?;

    Ok(())
}
