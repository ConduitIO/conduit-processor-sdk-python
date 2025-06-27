# processor.py
import sdk
from typing import List
from opencdc.v1 import opencdc_pb2
from config.v1 import parameter_pb2

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
            params={}
        )

    def process(self, records: List[opencdc_pb2.Record]) -> List[sdk.ProcessedRecord]:
        """Processes a list of OpenCDC records."""
        # ********* BUG FIX IS HERE *********
        # This now iterates through the list of records.
        processed_records = []
        for record in records:
            # Check for a specific metadata key to decide if we should filter the record.
            if record.metadata.get("over_threshold") == "true":
                # Use the SDK to signal that this record should be filtered.
                processed_records.append(sdk.ProcessedRecord.Filter())
            else:
                # Mutate the record by adding a new metadata field.
                record.metadata["processed-by"] = "py-processor-simple"
                # Use the SDK to signal that the record was processed successfully.
                processed_records.append(sdk.ProcessedRecord.Ack(record))
        return processed_records
