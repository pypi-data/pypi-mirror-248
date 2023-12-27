import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from _qwak_proto.qwak.feature_store.features.feature_set_types_pb2 import (
    KoalasTransformation as ProtoKoalasTransformation,
    SqlTransformation as ProtoSqlTransformation,
    TransformArguments as ProtoTransformArguments,
    Transformation as ProtoTransformation,
    UdfTransformation as ProtoUdfTransformation,
)
from qwak.exceptions import QwakException
from qwak.feature_store.feature_sets.transformations.aggregations.aggregations import (
    BaseAggregate,
    QwakAggregation,
)
from qwak.feature_store.feature_sets.transformations.aggregations.windows import Window
from qwak.tools.logger import logger as qwak_logger

logger = qwak_logger.get_qwak_logger(__name__)


class BaseTransformation(ABC):
    """
    Base class for Qwak transformations.

    Windows and aggregates are supported only for streaming aggregation featuresets.
    """

    windows: List[Window] = []
    aggregations: Tuple[BaseAggregate] = ()
    _artifact_path: Optional[str] = field(init=False, default=None)

    def aggregate(self, *aggregations: QwakAggregation):
        self.aggregations += aggregations
        return self

    def by_windows(self, *time_windows: str):
        self.windows += Window._from_string(*set(time_windows))
        return self

    def get_names(self) -> List[str]:
        return [a.get_name() for a in self.aggregations]

    def get_features_names(self) -> List[str]:
        if self.windows and self.aggregations:
            return [
                f"{name}_{tu.get_feature_suffix()}"
                for tu in self.windows
                for name in self.get_names()
            ]
        else:
            raise QwakException(
                "Feature names are retrieved for streaming aggregation featuresets only"
            )

    @classmethod
    def _from_proto(cls, proto: ProtoTransformation):
        function_mapping = {
            "sql_transformation": SparkSqlTransformation,
            "koalas_transformation": KoalasTransformation,
            "udf_transformation": UdfTransformation,
        }

        function_type: str = proto.WhichOneof("type")

        if function_type in function_mapping:
            function_class = function_mapping.get(function_type)
            return function_class._from_proto(proto)

        raise QwakException(f"Got unsupported transformation type: {function_type}")

    @abstractmethod
    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        pass

    def get_functions(self) -> Optional[List[Callable]]:
        return None

    def _validate_udfs(self):
        udfs: Optional[List[Callable]] = self.get_functions()

        if udfs and len(udfs) > 0:
            python_major = sys.version_info[0]
            python_minor = sys.version_info[1]
            if f"{python_major}.{python_minor}" != "3.8":
                raise QwakException(
                    f"Feature store UDFs are only supported for python 3.8, instead got: "
                    f"{python_major}.{python_minor}"
                )


class KoalasTransformation(BaseTransformation):
    """
    Koalas transformation, providing the user with the ability to define a Koalas based UDF for the transformation
    of the FeatureSet. This option will be deprecated in future versions.
    @param function: The Koalas function defined for the transformation
    @type: Callable
    @deprecated
    """

    def __init__(self, function: Callable, qwargs: Optional[Dict[str, str]] = None):
        logger.warning(
            "Koalas transformation is about to be deprecated. "
            "Please use SQL transformation or Pandas based UDFs instead"
        )

        qwargs = qwargs if qwargs else {}
        qwargs = {str(k): str(v) for k, v in qwargs.items()}
        self.qwargs = qwargs
        self.function = function
        self._artifact_path = None

    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        self._validate_udfs()

        if artifact_path:
            self._artifact_path = artifact_path

        return ProtoTransformation(
            koalas_transformation=ProtoKoalasTransformation(
                function_name=self.function.__name__,
                qwargs=ProtoTransformArguments(qwargs=self.qwargs),
            ),
            artifact_path=self._artifact_path,
        )

    @classmethod
    def _from_proto(cls, proto: "ProtoTransformation"):
        koalas_transformation = proto.koalas_transformation
        qwargs = {}
        if koalas_transformation.WhichOneof("args_option") == "qwargs":
            qwargs = koalas_transformation.qwargs.qwargs

        def f():
            print(
                f"Loading Koalas UDFs is not supported. Can not load {koalas_transformation.function_name}"
            )

        f.__name__ = koalas_transformation.function_name

        return cls(function=f, qwargs=qwargs)

    def get_functions(self) -> Optional[List[Callable]]:
        return [self.function]


@dataclass
class SparkSqlTransformation(BaseTransformation):
    """
    A Spark SQL transformation
    :param sql: A valid Spark SQL transformation
    Example transformation:
    ... code-block:: python
        SparkSqlTransformation("SELECT user_id, age FROM data_source")
    """

    sql: str = str()
    functions: Optional[List[Callable]] = None

    @classmethod
    def _from_proto(cls, proto: "ProtoSqlTransformation"):
        return cls(sql=proto.sql_transformation.sql)

    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        self._validate_udfs()

        return ProtoTransformation(
            sql_transformation=ProtoSqlTransformation(
                sql=self.sql,
                function_names=[function.__name__ for function in self.functions]
                if self.functions
                else None,
            ),
            artifact_path=artifact_path,
        )

    def get_functions(self) -> Optional[List[Callable]]:
        return self.functions


@dataclass
class UdfTransformation(BaseTransformation):
    """
    A UDF transformation
    :param function: A valid user defined function
    Example transformation:
    ... code-block:: python
        SparkSqlTransformation("SELECT user_id, age FROM data_source")
    """

    function: Callable = ()

    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        self._validate_udfs()

        if artifact_path:
            self._artifact_path = artifact_path

        return ProtoTransformation(
            artifact_path=artifact_path,
            udf_transformation=ProtoUdfTransformation(
                function_name=self.function.__name__
            ),
        )

    @classmethod
    def _from_proto(cls, proto: "ProtoTransformation"):
        return cls(
            function=lambda x: print("Loading UDFs is not yet supported"),
        )

    def get_functions(self) -> Optional[List[Callable]]:
        return [self.function]
