#  Copyright 2022 The FeatHub Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import timedelta
from typing import Any, Tuple, Optional

from pyflink.table.types import DataType, DataTypes

from feathub.common.exceptions import FeathubException
from feathub.feature_views.feature import Feature
from feathub.feature_views.transforms.agg_func import AggFunc
from feathub.feature_views.transforms.over_window_transform import OverWindowTransform
from feathub.feature_views.transforms.sliding_window_transform import (
    SlidingWindowTransform,
)
from feathub.processors.flink.flink_types_utils import to_flink_type
from feathub.processors.flink.table_builder.flink_sql_expr_utils import (
    to_flink_sql_expr,
)


class AggregationFieldDescriptor:
    """
    Descriptor of a field computed by aggregation.
    """

    def __init__(
        self,
        field_name: str,
        field_data_type: DataType,
        expr: str,
        agg_func: AggFunc,
        window_size: timedelta,
        limit: Optional[int],
        filter_expr: Optional[str],
    ) -> None:
        self.field_name = field_name
        self.field_data_type = field_data_type
        self.expr = expr
        self.agg_func = agg_func
        self.window_size = window_size
        self.limit = limit
        self.filter_expr = filter_expr

    @staticmethod
    def from_feature(feature: Feature) -> "AggregationFieldDescriptor":
        transform = feature.transform
        if not (
            isinstance(transform, SlidingWindowTransform)
            or isinstance(transform, OverWindowTransform)
        ):
            raise FeathubException(
                f"Cannot convert {feature} to AggregationFieldDescriptor."
            )
        filter_expr = (
            to_flink_sql_expr(transform.filter_expr)
            if transform.filter_expr is not None
            else None
        )
        return AggregationFieldDescriptor(
            feature.name,
            to_flink_type(feature.dtype),
            to_flink_sql_expr(transform.expr),
            transform.agg_func,
            transform.window_size,
            transform.limit,
            filter_expr,
        )


INTEGER_TYPES = {
    type(DataTypes.TINYINT()),
    type(DataTypes.SMALLINT()),
    type(DataTypes.INT()),
    type(DataTypes.BIGINT()),
}

FLOAT_TYPES = {type(DataTypes.FLOAT()), type(DataTypes.DOUBLE())}


# TODO: remove this method as it's function can be supported by
#  Java's AggFunc.getResult(AggFunc.createAccumulator()).
def get_default_value_and_type(
    agg_descriptor: AggregationFieldDescriptor,
) -> Tuple[Any, DataType]:
    default_type = agg_descriptor.field_data_type
    if (
        agg_descriptor.agg_func == AggFunc.COUNT
        or agg_descriptor.agg_func == AggFunc.SUM
    ):
        if type(agg_descriptor.field_data_type) in INTEGER_TYPES:
            default_value: Any = 0
        elif type(agg_descriptor.field_data_type) in FLOAT_TYPES:
            default_value = 0.0
        else:
            raise FeathubException(
                f"Unsupported DataType of AggFunc COUNT or SUM: "
                f"{type(agg_descriptor.field_data_type)}"
            )
    else:
        # TODO: Change the default value of collection-typed agg functions
        #  (COLLECT_LIST, VALUE_COUNTS, etc) to empty collection after
        #  FLINK-32494 is resolved
        default_value = None
    return (
        default_value,
        default_type,
    )
