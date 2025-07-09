"""
LLM Manager - Central LLM Configuration and Failover System
Handles role-based LLM assignment, task-level overrides, and automatic failover
"""

import yaml
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from crewai import LLM

class LLMManager:
    """
    Manages LLM configuration, assignment, and failover for the crew.
    
    Features:
    - Role-based LLM assignment
    - Task-level LLM overrides
    - Automatic failover on API failures
    - Environment-agnostic configuration
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize LLM Manager with configuration file."""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "llm_config.yaml"
        
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self._llm_cache = {}  # Cache for created LLM instances
        
    def _load_config(self) -> Dict[str, Any]:
        """Load LLM configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            raise Exception(f"Failed to load LLM configuration from {self.config_path}: {e}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for LLM operations."""
        logger = logging.getLogger("LLMManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def get_llm_for_role(self, role: str, task_llm_config: Optional[Dict[str, Any]] = None) -> LLM:
        """
        Get LLM instance for a specific role with optional task-level override.
        
        Priority:
        1. Task-level LLM configuration (highest)
        2. Role-based LLM configuration
        3. Default LLM configuration (lowest)
        
        Args:
            role: Agent role (e.g., 'writer', 'editor', 'researcher')
            task_llm_config: Optional task-specific LLM configuration
        
        Returns:
            LLM instance with failover capability
        """
        # Priority 1: Task-level override
        if task_llm_config:
            self.logger.info(f"Using task-level LLM override for role '{role}'")
            return self._create_llm_with_failover(task_llm_config, role)
        
        # Priority 2: Role-based configuration
        role_config = self.config.get('role_llm_mapping', {}).get(role)
        if role_config:
            self.logger.info(f"Using role-based LLM configuration for role '{role}'")
            return self._create_llm_with_failover(role_config['primary'], role, role_config.get('backup'))
        
        # Priority 3: Default configuration
        default_config = self.config.get('default_llm', {})
        self.logger.warning(f"No specific LLM config found for role '{role}', using default")
        return self._create_llm_with_failover(default_config, role)
    
    def _create_llm_with_failover(self, primary_config: Dict[str, Any], role: str, backup_config: Optional[Dict[str, Any]] = None) -> LLM:
        """
        Create LLM instance with automatic failover capability.
        
        Args:
            primary_config: Primary LLM configuration
            role: Agent role for cache key
            backup_config: Optional backup LLM configuration
        
        Returns:
            LLM instance with failover
        """
        cache_key = f"{role}_{primary_config.get('model', 'unknown')}"
        
        # Return cached instance if available
        if cache_key in self._llm_cache:
            return self._llm_cache[cache_key]
        
        try:
            # Create primary LLM
            llm = self._create_single_llm(primary_config)
            
            # Test the LLM with a simple call
            if self._test_llm(llm, primary_config):
                self.logger.info(f"Primary LLM '{primary_config.get('model')}' is operational for role '{role}'")
                self._llm_cache[cache_key] = llm
                return llm
            else:
                raise Exception("Primary LLM failed health check")
                
        except Exception as e:
            self.logger.warning(f"Primary LLM failed for role '{role}': {e}")
            
            # Try backup if available
            if backup_config:
                return self._try_backup_llm(backup_config, role, primary_config)
            else:
                # Try to get backup from role config
                role_config = self.config.get('role_llm_mapping', {}).get(role, {})
                backup_config = role_config.get('backup')
                if backup_config:
                    return self._try_backup_llm(backup_config, role, primary_config)
                else:
                    # Final fallback to default
                    return self._create_single_llm(self.config.get('default_llm', {}))
    
    def _try_backup_llm(self, backup_config: Dict[str, Any], role: str, primary_config: Dict[str, Any]) -> LLM:
        """Try backup LLM configuration."""
        try:
            backup_llm = self._create_single_llm(backup_config)
            if self._test_llm(backup_llm, backup_config):
                self.logger.info(f"Backup LLM '{backup_config.get('model')}' is operational for role '{role}'")
                return backup_llm
            else:
                raise Exception("Backup LLM failed health check")
        except Exception as e:
            self.logger.error(f"Backup LLM also failed for role '{role}': {e}")
            
            # Try tertiary if available
            role_config = self.config.get('role_llm_mapping', {}).get(role, {})
            tertiary_config = role_config.get('tertiary')
            if tertiary_config:
                try:
                    tertiary_llm = self._create_single_llm(tertiary_config)
                    self.logger.info(f"Using tertiary LLM '{tertiary_config.get('model')}' for role '{role}'")
                    return tertiary_llm
                except Exception as tertiary_e:
                    self.logger.error(f"Tertiary LLM also failed: {tertiary_e}")
            
            # Final fallback
            self.logger.error(f"All LLM options failed for role '{role}', using default")
            return self._create_single_llm(self.config.get('default_llm', {}))
    
    def _create_single_llm(self, llm_config: Dict[str, Any]) -> LLM:
        """Create a single LLM instance from configuration."""
        if not llm_config:
            raise Exception("Empty LLM configuration provided")
        
        # Extract configuration parameters
        model = llm_config.get('model')
        if not model:
            raise Exception("No model specified in LLM configuration")
        
        # Create LLM with configuration
        llm_params = {
            'model': model,
            'temperature': llm_config.get('temperature', 0.1),
        }
        
        # Add optional parameters if present
        if 'max_tokens' in llm_config:
            llm_params['max_tokens'] = llm_config['max_tokens']
        
        return LLM(**llm_params)
    
    def _test_llm(self, llm: LLM, config: Dict[str, Any]) -> bool:
        """
        Test LLM with a simple call to verify it's working.
        
        Args:
            llm: LLM instance to test
            config: LLM configuration for timeout
        
        Returns:
            True if LLM is operational, False otherwise
        """
        try:
            # Simple test call with timeout
            timeout = config.get('timeout', 30)
            
            # This is a minimal test - in production you might want a more robust health check
            response = llm.call("Test", timeout=timeout)
            return response is not None
            
        except Exception as e:
            self.logger.warning(f"LLM health check failed: {e}")
            return False
    
    def get_failover_settings(self) -> Dict[str, Any]:
        """Get failover configuration settings."""
        return self.config.get('failover_settings', {})
    
    def list_available_roles(self) -> List[str]:
        """Get list of roles with LLM configuration."""
        return list(self.config.get('role_llm_mapping', {}).keys())
    
    def get_role_config(self, role: str) -> Optional[Dict[str, Any]]:
        """Get complete configuration for a specific role."""
        return self.config.get('role_llm_mapping', {}).get(role)
    
    def reload_config(self) -> None:
        """Reload configuration from file and clear cache."""
        self.config = self._load_config()
        self._llm_cache.clear()
        self.logger.info("LLM configuration reloaded")