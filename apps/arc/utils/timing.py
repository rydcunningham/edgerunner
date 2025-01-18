import time
import json
import os
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict
import atexit

class Timer:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.log_buffer: List[Dict] = []
        self.output_dir = None
        self.log_file = None
        
        # Register flush on exit
        atexit.register(self.flush_logs)
    
    def _ensure_log_file(self):
        """Ensure log file is initialized with current output directory."""
        if self.log_file is None:
            # Get output directory from environment or use default
            base_dir = os.environ.get('SIMULATION_OUTPUT_DIR', 'outputs')
            self.output_dir = os.path.join(base_dir, 'logs')
            
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Create timing log file
            self.log_file = os.path.join(self.output_dir, 'timing.jsonl')
    
    def flush_logs(self):
        """Write all remaining logs in buffer to file."""
        if self.log_buffer:
            self._ensure_log_file()
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