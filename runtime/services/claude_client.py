"""LLM Client

Unified client for multiple LLM providers.
Supports: DeepSeek, Kimi (Moonshot), Qwen (DashScope), MIMO

All providers use OpenAI-compatible API format.
"""

import os
import json
import time
from typing import Optional, Dict, Any
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

load_dotenv()


# Provider configurations
PROVIDERS = {
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url_env": "DEEPSEEK_BASE_URL",
        "model_env": "DEEPSEEK_MODEL",
        "default_base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "temperature": 0.3,
    },
    "kimi": {
        "api_key_env": "KIMI_API_KEY",
        "base_url_env": "KIMI_BASE_URL",
        "model_env": "KIMI_MODEL",
        "default_base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
        "temperature": 1.0,  # kimi-k2.6 only accepts 1.0
    },
    "qwen": {
        "api_key_env": "QWEN_API_KEY",
        "base_url_env": "QWEN_BASE_URL",
        "model_env": "QWEN_MODEL",
        "default_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "temperature": 0.3,
    },
    "mimo": {
        "api_key_env": "MIMO_API_KEY",
        "base_url_env": "MIMO_BASE_URL",
        "model_env": "MIMO_MODEL",
        "default_base_url": "https://api.mimo.ai/v1",
        "default_model": "mimo-chat",
        "temperature": 0.3,
    },
}


class LLMClient:
    """Unified LLM client for multiple providers."""

    def __init__(self, provider: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "deepseek")

        if self.provider not in PROVIDERS:
            raise ValueError(f"Unknown provider: {self.provider}. Must be one of: {list(PROVIDERS.keys())}")

        config = PROVIDERS[self.provider]

        # Get API key
        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise ValueError(f"API key not found. Set {config['api_key_env']} in .env")

        # Get base URL
        base_url = os.getenv(config["base_url_env"], config["default_base_url"])

        # Get model
        self.model = os.getenv(config["model_env"], config["default_model"])

        # Get default temperature for this provider
        self.default_temperature = config.get("temperature", 0.3)

        # Create OpenAI client
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        print(f"LLM Client initialized: {self.provider} ({self.model})")

    def reason(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = None,
        max_retries: int = 3,
    ) -> str:
        """Send a reasoning request to the LLM with retry logic."""
        # Use provider's default temperature if not specified
        if temperature is None:
            temperature = self.default_temperature

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                return response.choices[0].message.content
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                    print(f"[Retry] Rate limited, waiting {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"LLM API error ({self.provider}): Rate limited after {max_retries} retries")
            except APIError as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"[Retry] API error, waiting {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"LLM API error ({self.provider}): {e}")
            except Exception as e:
                raise RuntimeError(f"LLM API error ({self.provider}): {e}")

    def reason_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        """Send a reasoning request and parse JSON response."""
        response_text = self.reason(system_prompt, user_prompt, max_tokens, temperature)

        # Try to parse JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON block in markdown
        import re
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Try to find any JSON-like object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON from response: {response_text[:500]}")


# Global client instance
_client: Optional[LLMClient] = None


def get_llm_client(provider: str = None) -> LLMClient:
    """Get or create the global LLM client."""
    global _client
    if _client is None or (provider and _client.provider != provider):
        _client = LLMClient(provider)
    return _client


# Backward compatibility alias
def get_claude_client():
    """Alias for get_llm_client for backward compatibility."""
    return get_llm_client()
