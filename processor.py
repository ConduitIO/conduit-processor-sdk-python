# processor.py
import sdk
from proto.opencdc.v1 import opencdc_pb2
from proto.config.v1 import parameter_pb2

class SimpleProcessor(sdk.Processor):
    """
    A simple processor that adds a metadata field to each record,
    or filters it if another metadata field is present.
    """
    def specification(self) -> sdk.Specification:
        """Defines the processor's metadata and configuration parameters."""
        return sdk.Specification(
            name="py-processor-simple",
            version="v1.0.0",
            summary="A simple processor written in Python.",
            description="Adds a 'processed-by' metadata field to each record.",
            author="Meroxa, Inc.",
            params={}  # No parameters for this simple processor
        )

    def process(self, record: opencdc_pb2.Record) -> sdk.ProcessResult:
        """Processes a single OpenCDC record."""
        # Check for a specific metadata key to decide if we should filter the record.
        if record.metadata.get("over_threshold") == "true":
            # Use the SDK to signal that this record should be filtered.
            return sdk.ProcessResult.Filter()

        # Mutate the record by adding a new metadata field.
        record.metadata["processed-by"] = "py-processor-simple"

        # Use the SDK to signal that the record was processed successfully.
        return sdk.ProcessResult.Ack(record)

# The main entry point for the Wasm module.
# The `run` function registers the processor instance so the exported
# functions can use it. This is called by the Wasm runtime on startup.
sdk.run(SimpleProcessor())
