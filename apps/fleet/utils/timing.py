import time
import json
import os
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict
import atexit

class Timer:
    def __init__(self, batch_size: int = 100):
        self.output_dir = "outputs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Create timing log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"{self.output_dir}/timing_logs_{timestamp}.jsonl"
        
        # Buffer for batching log entries
        self.log_buffer: List[Dict] = []
        self.batch_size = batch_size
        
        # Register flush on exit
        atexit.register(self.flush_logs)
    
    def flush_logs(self):
        """Write all remaining logs in buffer to file."""
        if self.log_buffer:
            with open(self.log_file, 'a') as f:
                for entry in self.log_buffer:
                    json.dump(entry, f)
                    f.write('\n')
            self.log_buffer.clear()
    
    @contextmanager
    def timer(self, operation: str):
        """Context manager for timing operations and buffering logs."""
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "duration_seconds": duration
            }
            
            # Add to buffer
            self.log_buffer.append(log_entry)
            
            # If buffer reaches batch size, write to file
            if len(self.log_buffer) >= self.batch_size:
                self.flush_logs()

# Global timer instance
timer = Timer() 