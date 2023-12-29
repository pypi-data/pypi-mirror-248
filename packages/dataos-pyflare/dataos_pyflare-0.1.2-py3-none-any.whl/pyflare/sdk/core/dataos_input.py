# from __future__ import annotations
from typing import Tuple, Any, Union

from pyflare.sdk import pyflare_logger
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils.generic_utils import safe_assignment, append_properties, resolve_dataos_address, \
    enhance_connection_url
from pyspark.sql import SparkSession, DataFrame

from pyflare.sdk.utils.pyflare_exceptions import InvalidInputException


class DataOSInput:
    def __init__(self, name, parsed_inputs, spark, is_stream=None,
                 source_format=None, driver=None, query=None, options=None):
        self.input_name: str = name
        self.parsed_inputs: dict[str: Reader] = parsed_inputs
        self.spark: SparkSession = spark
        self.is_stream: bool = is_stream
        self.source_format: str = source_format
        self.driver = driver
        self.query = query
        self.options: dict = options if options else {}

    def process_inputs(self) -> Tuple[Any, Any]:
        """
        
        Read dataset from a source with the supplied parameters and
        create a temp view with the name passed in the dataos_source decorator.
        """
        log = pyflare_logger.get_pyflare_logger(name=__name__)
        log.debug(f"dataos_read_input, input: {self.parsed_inputs}")
        resolved_address = resolve_dataos_address(self.input_name)

        if not self.parsed_inputs.get(resolved_address.get("depot", "")):
            raise InvalidInputException(f"Depot not loaded in current session: {self.input_name}")
        reader_instance: Reader = self.parsed_inputs.get(resolved_address.get("depot", "")).get('reader_instance')
        read_conf: ReadConfig = reader_instance.read_config
        read_conf.io_format = safe_assignment(read_conf.io_format, self.source_format)
        read_conf.depot_details["collection"] = resolved_address.get("collection", "")
        read_conf.depot_details["dataset"] = resolved_address.get("dataset", "")
        read_conf.depot_details.get("connection", {})[f"{read_conf.depot_type()}Url"] = \
            enhance_connection_url(connection_url=read_conf.dataset_absolute_path(),
                                   collection=resolved_address.get("collection", ""),
                                   dataset=resolved_address.get("dataset", ""))
        read_conf.driver = self.driver
        read_conf.query = self.query
        reader_instance.spark = safe_assignment(reader_instance.spark, self.spark)
        read_conf.extra_options = append_properties(read_conf.extra_options, self.options.pop(read_conf.io_format, {}))
        read_conf.spark_options = append_properties(read_conf.spark_options, self.options)
        df = reader_instance.read()
        # df.createOrReplaceTempView(self.input_name)
        return df, resolved_address.get("depot", "")
