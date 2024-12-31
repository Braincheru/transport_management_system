# app/services/logger.py
from functools import wraps
import logging
from datetime import datetime
import os

class LoggerService:
    def __init__(self):
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'transport_system_{datetime.now().strftime("%Y%m")}.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('transport_system')

    def log_action(self, action_type):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                try:
                    result = f(*args, **kwargs)
                    self.logger.info(f'{action_type}: Success - {f.__name__}')
                    return result
                except Exception as e:
                    self.logger.error(f'{action_type}: Error in {f.__name__} - {str(e)}')
                    raise
            return wrapped
        return decorator

logger_service = LoggerService()