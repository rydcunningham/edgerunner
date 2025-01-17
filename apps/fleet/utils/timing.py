import time
import json
import os
from datetime import datetime
from contextlib import contextmanager

class Timer:
    def __init__(self):
        self.output_dir = "outputs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Create timing log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"{self.output_dir}/timing_logs_{timestamp}.jsonl"
    
    @contextmanager
    def timer(self, operation: str):
        """Context manager for timing operations and logging to JSONL file."""
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            # Log timing information
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "duration_seconds": duration
            }
            
            with open(self.log_file, 'a') as f:
                json.dump(log_entry, f)
                f.write('\n')

# Global timer instance
timer = Timer() 