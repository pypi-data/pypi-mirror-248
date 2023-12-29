from pyflare.sdk import pyflare_logger
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils.generic_utils import safe_assignment, append_properties, resolve_dataos_address, \
    enhance_connection_url
from pyflare.sdk.utils.pyflare_exceptions import InvalidInputException
from pyflare.sdk.writers.writer import Writer
from pyspark.sql import SparkSession


class DataOSOutput:
    def __init__(self, name, dataframe, parsed_outputs, spark, is_stream=None,
                 sink_format=None, mode=None, driver=None, options=None):
        self.output_name: str = name
        self.parsed_outputs: dict[str: Writer] = parsed_outputs
        self.spark: SparkSession = spark
        self.is_stream: bool = is_stream
        self.mode: str = mode
        self.driver = driver
        self.options: dict = options if options else {}
        self.sink_format: str = sink_format
        self.dataframe = dataframe
        self.process_outputs()

    def process_outputs(self):
        """

        Write the transformed dataset to sink, with the supplied parameters to dataos_sink decorator.
        """
        log = pyflare_logger.get_pyflare_logger(name=__name__)
        log.debug(f"dataos_write_output, output: {self.parsed_outputs}")
        resolved_address = resolve_dataos_address(self.output_name)
        if not self.parsed_outputs.get(resolved_address.get("depot", "")):
            raise InvalidInputException(f"Depot not loaded in current session: {self.output_name}")
        writer_instance: Writer = self.parsed_outputs.get(resolved_address.get("depot", "")).get('writer_instance')
        write_conf: WriteConfig = writer_instance.write_config
        write_conf.depot_details["collection"] = resolved_address.get("collection", "")
        write_conf.depot_details["dataset"] = resolved_address.get("dataset", "")
        write_conf.driver = self.driver
        writer_instance.spark = safe_assignment(writer_instance.spark, self.spark)
        write_conf.io_format = safe_assignment(write_conf.io_format, self.sink_format)
        write_conf.depot_details.get("connection", {})[f"{write_conf.depot_type()}Url"] = \
            enhance_connection_url(connection_url=write_conf.dataset_absolute_path(),
                                   collection=resolved_address.get("collection", ""),
                                   dataset=resolved_address.get("dataset", ""))
        write_conf.mode = safe_assignment(write_conf.mode, self.mode)
        write_conf.extra_options = append_properties(write_conf.extra_options,
                                                     self.options.pop( write_conf.io_format,{}))
        write_conf.spark_options = append_properties(write_conf.spark_options, self.options)
        writer_instance.write(self.dataframe)
