"""PCOS Configuration Loader

Loads the 4 YAML config files at startup and makes them available as singletons.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from functools import lru_cache


# Base directory for PCOS configs
PCOS_DIR = Path(__file__).parent.parent / "pcos"


@lru_cache()
def load_yaml(filename: str) -> Dict[str, Any]:
    """Load a YAML file from the pcos directory."""
    filepath = PCOS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache()
def get_identity_config() -> Dict[str, Any]:
    """Load identity data (user profile)."""
    # Try to load data file first, fall back to schema
    try:
        return load_yaml("identity_data.yaml")
    except FileNotFoundError:
        return load_yaml("identity.yaml")


@lru_cache()
def get_world_model_config() -> Dict[str, Any]:
    """Load world model data (actual beliefs)."""
    # Try to load data file first, fall back to schema
    try:
        return load_yaml("world_model_data.yaml")
    except FileNotFoundError:
        return load_yaml("world_model.yaml")


@lru_cache()
def get_strategy_engine_config() -> Dict[str, Any]:
    """Load strategy_engine.yaml configuration."""
    return load_yaml("strategy_engine.yaml")


@lru_cache()
def get_decision_engine_config() -> Dict[str, Any]:
    """Load decision_engine.yaml configuration."""
    return load_yaml("decision_engine.yaml")


@lru_cache()
def get_benchmark_scenarios() -> Dict[str, Any]:
    """Load decision_benchmark.yaml scenarios."""
    return load_yaml("decision_benchmark.yaml")


class PCOSConfig:
    """PCOS Configuration singleton."""

    def __init__(self):
        self.identity = get_identity_config()
        self.world_model = get_world_model_config()
        self.strategy_engine = get_strategy_engine_config()
        self.decision_engine = get_decision_engine_config()
        self.benchmark = get_benchmark_scenarios()

    def get_identity_values(self) -> list[str]:
        """Get list of core values."""
        return [v["name"] for v in self.identity.get("core_values", [])]

    def get_identity_preferences(self) -> Dict[str, Any]:
        """Get known preferences."""
        return self.identity.get("known_preferences", {})

    def get_identity_focus(self) -> Dict[str, Any]:
        """Get current focus."""
        return self.identity.get("current_focus", {})

    def get_world_model_beliefs(self) -> list[Dict[str, Any]]:
        """Get all beliefs from world model."""
        return self.world_model.get("beliefs", [])

    def get_confidence_config(self) -> Dict[str, Any]:
        """Get confidence system configuration."""
        return self.world_model.get("confidence", {})

    def get_decision_engine_rules(self) -> Dict[str, Any]:
        """Get decision engine rules."""
        return self.decision_engine


# Global config instance
_config: PCOSConfig = None


def get_config() -> PCOSConfig:
    """Get or create the global PCOS config."""
    global _config
    if _config is None:
        _config = PCOSConfig()
    return _config
