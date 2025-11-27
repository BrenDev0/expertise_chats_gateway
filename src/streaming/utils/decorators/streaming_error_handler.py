from functools import wraps
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def streaming_error_hanlder(module: str) -> Callable:
    def decorator(func: Callable):
        @wraps
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                connection_id = kwargs.get("chat_id", "MISSING CONNECTION ID") 
                return await func(*args, **kwargs)
                
            except Exception as e:
                if "closed" in str(e).lower() or "disconnect" in str(e).lower():
                    logger.info(f"Connection {connection_id} disconnected")
                    return
                
                logger.error(f"Error in {module} :::: Connection id: {connection_id} ::::, Error sending data :::: {e}")
                raise e
        
        return async_wrapper
    
    return decorator