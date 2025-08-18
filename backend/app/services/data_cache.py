"""
Simple Cache Service - In-Memory Caching
Provides basic caching functionality without external dependencies
"""
import json
import logging
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheService:
    """Simple in-memory cache service"""
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self.default_ttl = 300  # 5 minutes
    
    async def connect(self):
        """Initialize cache (no external connection needed)"""
        logger.info("Cache service ready (in-memory)")
    
    async def disconnect(self):
        """Clean up cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if key in self.cache:
                item = self.cache[key]
                # Check if expired
                if datetime.now() > item['expires']:
                    del self.cache[key]
                    return None
                return item['data']
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        try:
            expires = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
            self.cache[key] = {
                'data': value,
                'expires': expires
            }
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if key in self.cache:
                del self.cache[key]
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        active_keys = 0
        expired_keys = 0
        now = datetime.now()
        
        for key, item in self.cache.items():
            if now > item['expires']:
                expired_keys += 1
            else:
                active_keys += 1
        
        return {
            "total_keys": len(self.cache),
            "active_keys": active_keys,
            "expired_keys": expired_keys,
            "cache_type": "in-memory"
        }
