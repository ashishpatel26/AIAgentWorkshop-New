"""
Rate limiting and retry utilities for API calls.
Implements exponential backoff and intelligent rate limit handling.
"""

import time
import random
from typing import Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Intelligent rate limiter with exponential backoff and jitter."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.last_request_time = 0
        self.request_count = 0

    def _calculate_delay(self, attempt: int, error_message: str = "") -> float:
        """Calculate delay with exponential backoff and jitter."""
        # Extract retry-after from error message if available
        retry_after = self._extract_retry_after(error_message)

        if retry_after:
            delay = retry_after
        else:
            # Exponential backoff: base_delay * (2 ^ attempt)
            delay = self.base_delay * (2 ** attempt)

        # Add jitter (±25%) to prevent thundering herd
        jitter = delay * 0.25 * (random.random() * 2 - 1)
        delay += jitter

        # Cap at max_delay
        delay = min(delay, self.max_delay)

        return max(delay, 0.1)  # Minimum 100ms delay

    def _extract_retry_after(self, error_message: str) -> Optional[float]:
        """Extract retry-after time from error message."""
        import re

        # Look for X-RateLimit-Reset header pattern
        reset_match = re.search(r'X-RateLimit-Reset["\']:\s*["\']([^"\']+)["\']', error_message)
        if reset_match:
            try:
                reset_timestamp = int(reset_match.group(1))
                current_time = int(time.time() * 1000)
                if reset_timestamp > current_time:
                    return (reset_timestamp - current_time) / 1000.0
            except (ValueError, IndexError):
                pass

        return None

    def _is_rate_limit_error(self, error: Exception) -> bool:
        """Check if error is a rate limit error."""
        error_str = str(error).lower()
        return any(keyword in error_str for keyword in [
            'rate limit', '429', 'too many requests', 'quota exceeded'
        ])

    def call_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function with intelligent retry logic.

        Args:
            func: Function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result of successful function call

        Raises:
            Last exception encountered after all retries exhausted
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                # Rate limiting: ensure minimum time between requests
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                min_interval = 0.2  # 200ms minimum between requests

                if time_since_last < min_interval:
                    time.sleep(min_interval - time_since_last)

                self.last_request_time = time.time()
                self.request_count += 1

                # Make the API call
                result = func(*args, **kwargs)

                # Success! Reset rate limiting state
                if attempt > 0:
                    logger.info(f"Request succeeded after {attempt} retries")

                return result

            except Exception as e:
                last_exception = e

                if not self._is_rate_limit_error(e):
                    # Not a rate limit error, don't retry
                    logger.error(f"Non-rate-limit error: {e}")
                    raise e

                if attempt == self.max_retries:
                    # All retries exhausted
                    logger.error(f"All {self.max_retries} retries exhausted. Last error: {e}")
                    raise e

                # Calculate delay and wait
                delay = self._calculate_delay(attempt, str(e))
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{self.max_retries + 1}), "
                             f"retrying in {delay:.2f} seconds: {e}")

                time.sleep(delay)

        # This should never be reached, but just in case
        raise last_exception

def create_rate_limited_llm(config: dict) -> Any:
    """
    Create a rate-limited LLM instance.

    This is a factory function that wraps LLM creation with rate limiting.
    """
    from langchain_openai import ChatOpenAI

    rate_limiter = RateLimiter(
        max_retries=config.get('max_retries', 3),
        base_delay=config.get('retry_delay', 1.0)
    )

    def create_llm():
        return ChatOpenAI(
            temperature=config['temperature'],
            model=config['model'],
            api_key=config['api_key'],
            base_url=config['api_base']
        )

    # For now, return the LLM directly. In production, you'd wrap the call method
    # with rate_limiter.call_with_retry
    return create_llm()

# Global rate limiter instance
_default_rate_limiter = RateLimiter()

def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _default_rate_limiter

def set_global_rate_limits(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    """Configure global rate limiting parameters."""
    global _default_rate_limiter
    _default_rate_limiter = RateLimiter(max_retries, base_delay, max_delay)