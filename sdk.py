# sdk.py
from typing import Dict, Optional, List

# No more sys.path manipulation here.
# Direct imports are used because the entry point script fixes the path.
from processor.v1 import processor_pb2
from opencdc.v1 import opencdc_pb2
from config.v1 import parameter_pb2

# Global instance of the user-defined processor
PROCESSOR: Optional['Processor'] = None

# --- Memory Management (Simulation for testing) ---
_WASM_MEMORY = bytearray(1024 * 128) # 128KB
_OFFSET = 0
def _malloc(size):
    global _OFFSET
    ptr = _OFFSET
    _OFFSET += size
    return ptr
def _get_memory_view():
    return _WASM_MEMORY

def write_to_memory(data: bytes) -> int:
    """Writes bytes to memory, returns a packed ptr-size uint64."""
    size = len(data)
    ptr = _malloc(size)
    _get_memory_view()[ptr:ptr+size] = data
    return (ptr << 32) | size

def read_from_memory(packed_ptr: int) -> bytes:
    """Reads bytes from a packed ptr-size uint64."""
    ptr = packed_ptr >> 32
    size = packed_ptr & 0xFFFFFFFF
    return _get_memory_view()[ptr:ptr+size]

# --- Processor Interface ---
class Processor:
    def specification(self) -> 'Specification':
        raise NotImplementedError
    def configure(self, config_map: Dict[str, str]):
        pass
    def open(self):
        pass
    def process(self, records: List[opencdc_pb2.Record]) -> List['ProcessedRecord']:
        raise NotImplementedError
    def teardown(self):
        pass

# --- SDK Data Structures ---
class Specification:
    def __init__(self, name: str, version: str, summary: str, description: str, author: str, params: Dict[str, parameter_pb2.Parameter]):
        self.name, self.version, self.summary, self.description, self.author, self.params = name, version, summary, description, author, params

class ProcessedRecord:
    @staticmethod
    def Ack(record: opencdc_pb2.Record) -> 'ProcessedRecord': return ProcessedRecord(record=record)
    @staticmethod
    def Filter() -> 'ProcessedRecord': return ProcessedRecord(filter=True)
    @staticmethod
    def Error(err: Exception) -> 'ProcessedRecord': return ProcessedRecord(error=err)

    def __init__(self, record=None, filter=False, error=None):
        self.record, self.filter, self.error = record, filter, error

# --- Wasm Exported Functions ---
def export(name):
    def decorator(func):
        setattr(func, '_export_name', name)
        return func
    return decorator

@export("conduit.processor.v1.specification")
def specification(packed_ptr: int) -> int:
    spec_model = PROCESSOR.specification()
    response = processor_pb2.Specify.Response(
        name=spec_model.name,
        version=spec_model.version,
        summary=spec_model.summary,
        description=spec_model.description,
        author=spec_model.author,
        parameters=spec_model.params
    )
    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.configure")
def configure(packed_ptr: int) -> int:
    req_bytes = read_from_memory(packed_ptr)
    request = processor_pb2.Configure.Request()
    request.ParseFromString(req_bytes)
    PROCESSOR.configure(request.parameters)
    response = processor_pb2.Configure.Response()
    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.open")
def open_processor(packed_ptr: int) -> int:
    PROCESSOR.open()
    response = processor_pb2.Open.Response()
    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.process")
def process(packed_ptr: int) -> int:
    req_bytes = read_from_memory(packed_ptr)
    request = processor_pb2.Process.Request()
    request.ParseFromString(req_bytes)
    
    results = PROCESSOR.process(request.records)

    response = processor_pb2.Process.Response()
    for res in results:
        processed_record_proto = processor_pb2.Process.ProcessedRecord()
        if res.error:
            processed_record_proto.error_record.error.message = str(res.error)
        elif res.filter:
            processed_record_proto.filter_record.SetInParent()
        else: # ACK
            processed_record_proto.single_record.CopyFrom(res.record)
        response.records.append(processed_record_proto)
        
    return write_to_memory(response.SerializeToString())

@export("conduit.processor.v1.teardown")
def teardown(packed_ptr: int) -> int:
    PROCESSOR.teardown()
    response = processor_pb2.Teardown.Response()
    return write_to_memory(response.SerializeToString())

# --- SDK Entrypoint ---
def run(processor: Processor):
    global PROCESSOR
    if not isinstance(processor, Processor):
        raise TypeError("argument must be an instance of sdk.Processor")
    PROCESSOR = processor
