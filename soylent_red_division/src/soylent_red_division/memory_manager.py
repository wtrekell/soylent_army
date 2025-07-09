"""
Memory Manager - Comprehensive Memory System with Fine-Grained Access Controls
Handles crew-level, agent-level, external, and session-specific memory with consolidation
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

class MemoryType(Enum):
    """Types of memory available in the system"""
    CREW_SHARED = "crew_shared"
    AGENT_SPECIFIC = "agent_specific"
    EXTERNAL_CONSOLIDATED = "external_consolidated"
    SESSION_TEMPORARY = "session_temporary"

class MemoryAccessLevel(Enum):
    """Access levels for memory"""
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"
    ADMIN = "admin"

@dataclass
class MemoryEntry:
    """Structure for memory entries"""
    id: str
    timestamp: datetime
    memory_type: MemoryType
    agent_id: str
    content: Dict[str, Any]
    tags: List[str]
    importance: int  # 1-10 scale
    access_level: MemoryAccessLevel
    consolidation_candidate: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'memory_type': self.memory_type.value,
            'agent_id': self.agent_id,
            'content': self.content,
            'tags': self.tags,
            'importance': self.importance,
            'access_level': self.access_level.value,
            'consolidation_candidate': self.consolidation_candidate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            memory_type=MemoryType(data['memory_type']),
            agent_id=data['agent_id'],
            content=data['content'],
            tags=data['tags'],
            importance=data['importance'],
            access_level=MemoryAccessLevel(data['access_level']),
            consolidation_candidate=data.get('consolidation_candidate', False)
        )

class MemoryAccessControl:
    """Manages access controls for different agent roles"""
    
    def __init__(self):
        self.access_matrix = {
            'brand_author': {
                MemoryType.CREW_SHARED: MemoryAccessLevel.ADMIN,
                MemoryType.AGENT_SPECIFIC: MemoryAccessLevel.ADMIN,
                MemoryType.EXTERNAL_CONSOLIDATED: MemoryAccessLevel.ADMIN,
                MemoryType.SESSION_TEMPORARY: MemoryAccessLevel.ADMIN
            },
            'writer': {
                MemoryType.CREW_SHARED: MemoryAccessLevel.READ_WRITE,
                MemoryType.AGENT_SPECIFIC: MemoryAccessLevel.READ_WRITE,
                MemoryType.EXTERNAL_CONSOLIDATED: MemoryAccessLevel.READ_ONLY,
                MemoryType.SESSION_TEMPORARY: MemoryAccessLevel.READ_WRITE
            },
            'editor': {
                MemoryType.CREW_SHARED: MemoryAccessLevel.READ_WRITE,
                MemoryType.AGENT_SPECIFIC: MemoryAccessLevel.READ_WRITE,
                MemoryType.EXTERNAL_CONSOLIDATED: MemoryAccessLevel.READ_ONLY,
                MemoryType.SESSION_TEMPORARY: MemoryAccessLevel.READ_ONLY
            },
            'researcher': {
                MemoryType.CREW_SHARED: MemoryAccessLevel.READ_ONLY,
                MemoryType.AGENT_SPECIFIC: MemoryAccessLevel.READ_WRITE,
                MemoryType.EXTERNAL_CONSOLIDATED: MemoryAccessLevel.READ_ONLY,
                MemoryType.SESSION_TEMPORARY: MemoryAccessLevel.READ_ONLY
            }
        }
    
    def can_access(self, agent_role: str, memory_type: MemoryType, operation: str) -> bool:
        """Check if agent can perform operation on memory type"""
        if agent_role not in self.access_matrix:
            return False
        
        access_level = self.access_matrix[agent_role].get(memory_type, MemoryAccessLevel.READ_ONLY)
        
        if operation == 'read':
            return access_level in [MemoryAccessLevel.READ_ONLY, MemoryAccessLevel.READ_WRITE, MemoryAccessLevel.ADMIN]
        elif operation == 'write':
            return access_level in [MemoryAccessLevel.READ_WRITE, MemoryAccessLevel.ADMIN]
        elif operation == 'admin':
            return access_level == MemoryAccessLevel.ADMIN
        
        return False
    
    def get_accessible_memory_types(self, agent_role: str) -> List[MemoryType]:
        """Get all memory types accessible to an agent"""
        if agent_role not in self.access_matrix:
            return []
        
        return list(self.access_matrix[agent_role].keys())

class MemoryManager:
    """
    Comprehensive memory management system with fine-grained access controls
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_dir = project_root / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Memory storage files
        self.crew_memory_file = self.memory_dir / "crew_shared.json"
        self.agent_memory_file = self.memory_dir / "agent_specific.json"
        self.external_memory_file = self.memory_dir / "external_consolidated.json"
        self.session_memory_file = self.memory_dir / "session_temporary.json"
        self.consolidation_log_file = self.memory_dir / "consolidation_log.json"
        
        # Initialize access control
        self.access_control = MemoryAccessControl()
        
        # Initialize memory storage
        self.memories = {
            MemoryType.CREW_SHARED: self._load_memory(self.crew_memory_file),
            MemoryType.AGENT_SPECIFIC: self._load_memory(self.agent_memory_file),
            MemoryType.EXTERNAL_CONSOLIDATED: self._load_memory(self.external_memory_file),
            MemoryType.SESSION_TEMPORARY: self._load_memory(self.session_memory_file)
        }
        
        # Session tracking
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now()
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Consolidation settings
        self.consolidation_settings = {
            'auto_consolidate_threshold': 100,  # entries
            'consolidation_interval_days': 7,
            'importance_threshold': 5,
            'similarity_threshold': 0.8
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for memory operations"""
        logger = logging.getLogger("MemoryManager")
        if not logger.handlers:
            handler = logging.FileHandler(self.memory_dir / "memory_operations.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_memory(self, file_path: Path) -> List[MemoryEntry]:
        """Load memory from file"""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [MemoryEntry.from_dict(entry) for entry in data]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Error loading memory from {file_path}: {e}")
            return []
    
    def _save_memory(self, memory_type: MemoryType):
        """Save memory to file"""
        file_map = {
            MemoryType.CREW_SHARED: self.crew_memory_file,
            MemoryType.AGENT_SPECIFIC: self.agent_memory_file,
            MemoryType.EXTERNAL_CONSOLIDATED: self.external_memory_file,
            MemoryType.SESSION_TEMPORARY: self.session_memory_file
        }
        
        file_path = file_map[memory_type]
        memories = self.memories[memory_type]
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([memory.to_dict() for memory in memories], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving memory to {file_path}: {e}")
    
    def store_memory(self, agent_role: str, memory_type: MemoryType, content: Dict[str, Any], 
                    tags: List[str] = None, importance: int = 5) -> str:
        """Store a memory entry"""
        # Check access permissions
        if not self.access_control.can_access(agent_role, memory_type, 'write'):
            raise PermissionError(f"Agent {agent_role} cannot write to {memory_type}")
        
        # Create memory entry
        memory_id = str(uuid.uuid4())
        memory_entry = MemoryEntry(
            id=memory_id,
            timestamp=datetime.now(),
            memory_type=memory_type,
            agent_id=agent_role,
            content=content,
            tags=tags or [],
            importance=importance,
            access_level=MemoryAccessLevel.READ_WRITE
        )
        
        # Store in appropriate memory type
        self.memories[memory_type].append(memory_entry)
        self._save_memory(memory_type)
        
        # Log the operation
        self.logger.info(f"Memory stored: {memory_id} by {agent_role} in {memory_type}")
        
        # Check for auto-consolidation
        if len(self.memories[memory_type]) > self.consolidation_settings['auto_consolidate_threshold']:
            self._auto_consolidate(memory_type)
        
        return memory_id
    
    def retrieve_memory(self, agent_role: str, memory_type: MemoryType, 
                       query: str = None, tags: List[str] = None, 
                       limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memory entries"""
        # Check access permissions
        if not self.access_control.can_access(agent_role, memory_type, 'read'):
            raise PermissionError(f"Agent {agent_role} cannot read from {memory_type}")
        
        memories = self.memories[memory_type]
        
        # Filter by tags if provided
        if tags:
            memories = [m for m in memories if any(tag in m.tags for tag in tags)]
        
        # Simple query matching (could be enhanced with embedding similarity)
        if query:
            query_lower = query.lower()
            memories = [m for m in memories if self._matches_query(m.content, query_lower)]
        
        # Sort by importance and recency
        memories.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        
        return memories[:limit]
    
    def _matches_query(self, content: Dict[str, Any], query: str) -> bool:
        """Simple query matching against content"""
        content_str = json.dumps(content).lower()
        return query in content_str
    
    def search_across_memories(self, agent_role: str, query: str, 
                              limit: int = 20) -> Dict[MemoryType, List[MemoryEntry]]:
        """Search across all accessible memory types"""
        results = {}
        accessible_types = self.access_control.get_accessible_memory_types(agent_role)
        
        for memory_type in accessible_types:
            try:
                memories = self.retrieve_memory(agent_role, memory_type, query, limit=limit)
                if memories:
                    results[memory_type] = memories
            except PermissionError:
                continue
        
        return results
    
    def store_interaction(self, agent_role: str, interaction_type: str, 
                         content: Dict[str, Any], importance: int = 5):
        """Store interaction-specific memory"""
        interaction_content = {
            'interaction_type': interaction_type,
            'session_id': self.session_id,
            'agent_role': agent_role,
            'content': content,
            'context': {
                'session_start': self.session_start.isoformat(),
                'interaction_time': datetime.now().isoformat()
            }
        }
        
        # Store in appropriate memory based on importance and type
        if importance >= 7:  # High importance goes to crew shared
            memory_type = MemoryType.CREW_SHARED
        elif interaction_type in ['feedback', 'revision', 'collaboration']:
            memory_type = MemoryType.AGENT_SPECIFIC
        else:
            memory_type = MemoryType.SESSION_TEMPORARY
        
        self.store_memory(
            agent_role=agent_role,
            memory_type=memory_type,
            content=interaction_content,
            tags=[interaction_type, 'interaction'],
            importance=importance
        )
    
    def store_feedback_pattern(self, agent_role: str, feedback_content: str, 
                              article_context: str, effectiveness: int):
        """Store feedback patterns for learning"""
        feedback_memory = {
            'feedback_content': feedback_content,
            'article_context': article_context,
            'effectiveness': effectiveness,
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id
        }
        
        self.store_memory(
            agent_role=agent_role,
            memory_type=MemoryType.CREW_SHARED,
            content=feedback_memory,
            tags=['feedback', 'pattern', 'learning'],
            importance=effectiveness
        )
    
    def store_brand_decision(self, agent_role: str, decision_context: str, 
                           decision_made: str, rationale: str):
        """Store brand interpretation decisions"""
        brand_memory = {
            'decision_context': decision_context,
            'decision_made': decision_made,
            'rationale': rationale,
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id
        }
        
        self.store_memory(
            agent_role=agent_role,
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            content=brand_memory,
            tags=['brand', 'decision', 'interpretation'],
            importance=8
        )
    
    def _auto_consolidate(self, memory_type: MemoryType):
        """Automatically consolidate memories when threshold is reached"""
        self.logger.info(f"Auto-consolidation triggered for {memory_type}")
        
        # Mark candidates for consolidation
        memories = self.memories[memory_type]
        old_threshold = datetime.now() - timedelta(days=self.consolidation_settings['consolidation_interval_days'])
        
        for memory in memories:
            if (memory.timestamp < old_threshold and 
                memory.importance < self.consolidation_settings['importance_threshold']):
                memory.consolidation_candidate = True
        
        # Log consolidation opportunity
        candidates = [m for m in memories if m.consolidation_candidate]
        self.logger.info(f"Marked {len(candidates)} memories for consolidation in {memory_type}")
    
    def manual_consolidation(self, agent_role: str, memory_type: MemoryType = None) -> Dict[str, Any]:
        """Manually trigger memory consolidation"""
        if not self.access_control.can_access(agent_role, memory_type or MemoryType.CREW_SHARED, 'admin'):
            raise PermissionError(f"Agent {agent_role} cannot perform consolidation")
        
        consolidation_results = {}
        
        # Consolidate specific type or all types
        types_to_consolidate = [memory_type] if memory_type else list(MemoryType)
        
        for mem_type in types_to_consolidate:
            if mem_type == MemoryType.SESSION_TEMPORARY:
                continue  # Skip session memory
            
            memories = self.memories[mem_type]
            candidates = [m for m in memories if m.consolidation_candidate]
            
            if candidates:
                # Group similar memories
                consolidated = self._consolidate_similar_memories(candidates)
                
                # Remove old memories and add consolidated ones
                self.memories[mem_type] = [m for m in memories if not m.consolidation_candidate]
                self.memories[mem_type].extend(consolidated)
                
                # Save updated memory
                self._save_memory(mem_type)
                
                consolidation_results[mem_type.value] = {
                    'original_count': len(candidates),
                    'consolidated_count': len(consolidated),
                    'space_saved': len(candidates) - len(consolidated)
                }
        
        # Log consolidation results
        self._log_consolidation(consolidation_results)
        
        return consolidation_results
    
    def _consolidate_similar_memories(self, memories: List[MemoryEntry]) -> List[MemoryEntry]:
        """Consolidate similar memories into summary entries"""
        # Group by tags and content similarity
        groups = {}
        
        for memory in memories:
            # Create grouping key based on tags and content type
            key = tuple(sorted(memory.tags))
            if key not in groups:
                groups[key] = []
            groups[key].append(memory)
        
        consolidated = []
        
        for tag_group, group_memories in groups.items():
            if len(group_memories) > 1:
                # Create consolidated memory
                consolidated_content = {
                    'consolidation_type': 'similar_memories',
                    'original_count': len(group_memories),
                    'consolidated_summary': self._create_summary(group_memories),
                    'common_patterns': self._extract_patterns(group_memories),
                    'consolidation_timestamp': datetime.now().isoformat()
                }
                
                consolidated_memory = MemoryEntry(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    memory_type=group_memories[0].memory_type,
                    agent_id='system_consolidation',
                    content=consolidated_content,
                    tags=list(tag_group) + ['consolidated'],
                    importance=max(m.importance for m in group_memories),
                    access_level=MemoryAccessLevel.READ_ONLY
                )
                
                consolidated.append(consolidated_memory)
            else:
                # Single memory, keep as is
                consolidated.extend(group_memories)
        
        return consolidated
    
    def _create_summary(self, memories: List[MemoryEntry]) -> str:
        """Create a summary of multiple memories"""
        # Simple summarization - could be enhanced with LLM
        contents = [str(m.content) for m in memories]
        return f"Consolidated {len(memories)} memories with common patterns"
    
    def _extract_patterns(self, memories: List[MemoryEntry]) -> List[str]:
        """Extract common patterns from memory group"""
        # Simple pattern extraction - could be enhanced
        all_tags = [tag for memory in memories for tag in memory.tags]
        common_tags = [tag for tag in set(all_tags) if all_tags.count(tag) > 1]
        return common_tags
    
    def _log_consolidation(self, results: Dict[str, Any]):
        """Log consolidation results"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'consolidation_results': results,
            'session_id': self.session_id
        }
        
        try:
            # Load existing log
            consolidation_log = []
            if self.consolidation_log_file.exists():
                with open(self.consolidation_log_file, 'r', encoding='utf-8') as f:
                    consolidation_log = json.load(f)
            
            # Add new entry
            consolidation_log.append(log_entry)
            
            # Save updated log
            with open(self.consolidation_log_file, 'w', encoding='utf-8') as f:
                json.dump(consolidation_log, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error logging consolidation: {e}")
    
    def get_memory_stats(self, agent_role: str) -> Dict[str, Any]:
        """Get memory statistics for accessible memory types"""
        stats = {}
        accessible_types = self.access_control.get_accessible_memory_types(agent_role)
        
        for memory_type in accessible_types:
            memories = self.memories[memory_type]
            stats[memory_type.value] = {
                'total_entries': len(memories),
                'consolidation_candidates': len([m for m in memories if m.consolidation_candidate]),
                'average_importance': sum(m.importance for m in memories) / len(memories) if memories else 0,
                'oldest_entry': min(m.timestamp for m in memories).isoformat() if memories else None,
                'newest_entry': max(m.timestamp for m in memories).isoformat() if memories else None
            }
        
        return stats
    
    def clear_session_memory(self):
        """Clear temporary session memory"""
        self.memories[MemoryType.SESSION_TEMPORARY].clear()
        self._save_memory(MemoryType.SESSION_TEMPORARY)
        self.logger.info("Session memory cleared")
    
    def export_memory(self, agent_role: str, memory_type: MemoryType, 
                     output_path: Path) -> bool:
        """Export memory to file"""
        if not self.access_control.can_access(agent_role, memory_type, 'read'):
            raise PermissionError(f"Agent {agent_role} cannot export {memory_type}")
        
        try:
            memories = self.memories[memory_type]
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'memory_type': memory_type.value,
                'exported_by': agent_role,
                'entries': [memory.to_dict() for memory in memories]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Memory exported to {output_path} by {agent_role}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting memory: {e}")
            return False