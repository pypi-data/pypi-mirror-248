# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Show Functions Node

This is a SQL Query Execution Plan Node.
"""
from typing import Iterable

import pyarrow

from opteryx import functions
from opteryx import operators
from opteryx.models import QueryProperties
from opteryx.operators import BasePlanNode


class ShowFunctionsNode(BasePlanNode):
    def __init__(self, properties: QueryProperties, **config):
        super().__init__(properties=properties)

    @property
    def name(self):  # pragma: no cover
        return "Show Functions"

    @property
    def config(self):  # pragma: no cover
        return ""

    def execute(self) -> Iterable:
        buffer = []

        for function in functions.functions():
            buffer.append({"name": function, "type": "function"})
        for aggregate in operators.aggregators():
            buffer.append({"name": aggregate, "type": "aggregator"})

        table = pyarrow.Table.from_pylist(buffer)
        table = Columns.create_table_metadata(
            table=table,
            expected_rows=len(buffer),
            name="show_functions",
            table_aliases=[],
            disposition="calculated",
            path="show_functions",
        )

        yield table
        return
