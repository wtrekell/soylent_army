"""
Knowledge Manager - Comprehensive Knowledge Integration System
Handles brand knowledge, templates, examples, and dynamic knowledge loading with versioning and validation
"""

import json
import os
import yaml
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import glob
import re
from collections import defaultdict

class KnowledgeType(Enum):
    """Types of knowledge in the system"""
    BRAND_FOUNDATION = "brand_foundation"
    PERSONAS = "personas"
    WRITING_EXAMPLES = "writing_examples"
    TEMPLATES = "templates"
    USER_PREFERENCES = "user_preferences"
    CONTEXTUAL = "contextual"

class KnowledgeStatus(Enum):
    """Status of knowledge items"""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DRAFT = "draft"
    ARCHIVED = "archived"

@dataclass
class KnowledgeItem:
    """Structure for knowledge items"""
    id: str
    knowledge_type: KnowledgeType
    title: str
    content: str
    file_path: str
    last_modified: datetime
    version: str
    tags: List[str]
    status: KnowledgeStatus
    dependencies: List[str]
    metadata: Dict[str, Any]
    content_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'knowledge_type': self.knowledge_type.value,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'last_modified': self.last_modified.isoformat(),
            'version': self.version,
            'tags': self.tags,
            'status': self.status.value,
            'dependencies': self.dependencies,
            'metadata': self.metadata,
            'content_hash': self.content_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeItem':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            knowledge_type=KnowledgeType(data['knowledge_type']),
            title=data['title'],
            content=data['content'],
            file_path=data['file_path'],
            last_modified=datetime.fromisoformat(data['last_modified']),
            version=data['version'],
            tags=data['tags'],
            status=KnowledgeStatus(data['status']),
            dependencies=data['dependencies'],
            metadata=data['metadata'],
            content_hash=data['content_hash']
        )

class KnowledgeAccessControl:
    """Manages access controls for different knowledge types"""
    
    def __init__(self):
        self.access_matrix = {
            'brand_author': {
                KnowledgeType.BRAND_FOUNDATION: ['read', 'write', 'version'],
                KnowledgeType.PERSONAS: ['read', 'write', 'version'],
                KnowledgeType.WRITING_EXAMPLES: ['read', 'write', 'version'],
                KnowledgeType.TEMPLATES: ['read', 'write', 'version'],
                KnowledgeType.USER_PREFERENCES: ['read', 'write'],
                KnowledgeType.CONTEXTUAL: ['read', 'write']
            },
            'writer': {
                KnowledgeType.BRAND_FOUNDATION: ['read'],
                KnowledgeType.PERSONAS: ['read'],
                KnowledgeType.WRITING_EXAMPLES: ['read'],
                KnowledgeType.TEMPLATES: ['read'],
                KnowledgeType.USER_PREFERENCES: ['read'],
                KnowledgeType.CONTEXTUAL: ['read', 'write']
            },
            'editor': {
                KnowledgeType.BRAND_FOUNDATION: ['read'],
                KnowledgeType.PERSONAS: ['read'],
                KnowledgeType.WRITING_EXAMPLES: ['read'],
                KnowledgeType.TEMPLATES: ['read'],
                KnowledgeType.USER_PREFERENCES: ['read'],
                KnowledgeType.CONTEXTUAL: ['read']
            },
            'researcher': {
                KnowledgeType.BRAND_FOUNDATION: ['read'],
                KnowledgeType.PERSONAS: ['read'],
                KnowledgeType.WRITING_EXAMPLES: ['read'],
                KnowledgeType.TEMPLATES: ['read'],
                KnowledgeType.USER_PREFERENCES: [],
                KnowledgeType.CONTEXTUAL: ['read']
            }
        }
    
    def can_access(self, agent_role: str, knowledge_type: KnowledgeType, operation: str) -> bool:
        """Check if agent can perform operation on knowledge type"""
        if agent_role not in self.access_matrix:
            return False
        
        permissions = self.access_matrix[agent_role].get(knowledge_type, [])
        return operation in permissions
    
    def get_accessible_types(self, agent_role: str) -> List[KnowledgeType]:
        """Get all knowledge types accessible to an agent"""
        if agent_role not in self.access_matrix:
            return []
        
        return [kt for kt, perms in self.access_matrix[agent_role].items() if perms]

class KnowledgeManager:
    """
    Comprehensive knowledge management system with dynamic loading, versioning, and validation
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.knowledge_root = project_root / "knowledge"
        self.knowledge_cache_dir = project_root / "knowledge_cache"
        self.knowledge_cache_dir.mkdir(exist_ok=True)
        
        # Knowledge storage files
        self.knowledge_index_file = self.knowledge_cache_dir / "knowledge_index.json"
        self.knowledge_versions_file = self.knowledge_cache_dir / "versions.json"
        self.knowledge_dependencies_file = self.knowledge_cache_dir / "dependencies.json"
        
        # Initialize access control
        self.access_control = KnowledgeAccessControl()
        
        # Initialize knowledge storage
        self.knowledge_items: Dict[str, KnowledgeItem] = {}
        self.knowledge_graph: Dict[str, List[str]] = defaultdict(list)
        self.version_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Load existing knowledge
        self._load_knowledge_index()
        self._scan_and_update_knowledge()
        
        # Knowledge validation settings
        self.validation_settings = {
            'check_dependencies': True,
            'validate_content_format': True,
            'check_for_conflicts': True,
            'auto_resolve_minor_conflicts': False
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for knowledge operations"""
        logger = logging.getLogger("KnowledgeManager")
        if not logger.handlers:
            handler = logging.FileHandler(self.knowledge_cache_dir / "knowledge_operations.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_knowledge_index(self):
        """Load knowledge index from cache"""
        if not self.knowledge_index_file.exists():
            return
        
        try:
            with open(self.knowledge_index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item_data in data:
                    item = KnowledgeItem.from_dict(item_data)
                    self.knowledge_items[item.id] = item
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Error loading knowledge index: {e}")
    
    def _save_knowledge_index(self):
        """Save knowledge index to cache"""
        try:
            with open(self.knowledge_index_file, 'w', encoding='utf-8') as f:
                json.dump([item.to_dict() for item in self.knowledge_items.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving knowledge index: {e}")
    
    def _compute_content_hash(self, content: str) -> str:
        """Compute hash for content change detection"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def _extract_metadata_from_content(self, content: str, file_path: str) -> Tuple[Dict[str, Any], str]:
        """Extract metadata from markdown frontmatter or YAML files"""
        metadata = {}
        clean_content = content
        
        if file_path.endswith('.md'):
            # Extract YAML frontmatter
            if content.startswith('---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    try:
                        metadata = yaml.safe_load(parts[1])
                        clean_content = parts[2].strip()
                    except yaml.YAMLError:
                        pass
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            try:
                metadata = yaml.safe_load(content)
                clean_content = yaml.dump(metadata, default_flow_style=False)
            except yaml.YAMLError:
                pass
        
        return metadata or {}, clean_content
    
    def _determine_knowledge_type(self, file_path: str) -> KnowledgeType:
        """Determine knowledge type based on file path"""
        path_parts = Path(file_path).parts
        
        if 'brand' in path_parts:
            if 'brand-foundation' in file_path:
                return KnowledgeType.BRAND_FOUNDATION
            else:
                return KnowledgeType.PERSONAS
        elif 'examples' in path_parts:
            return KnowledgeType.WRITING_EXAMPLES
        elif 'templates' in path_parts:
            return KnowledgeType.TEMPLATES
        elif 'user_preference' in file_path:
            return KnowledgeType.USER_PREFERENCES
        else:
            return KnowledgeType.CONTEXTUAL
    
    def _scan_and_update_knowledge(self):
        """Scan knowledge directory and update index"""
        knowledge_files = []
        
        # Scan for all knowledge files
        for ext in ['*.md', '*.yaml', '*.yml', '*.txt']:
            knowledge_files.extend(glob.glob(str(self.knowledge_root / "**" / ext), recursive=True))
        
        for file_path in knowledge_files:
            try:
                # Skip hidden files and cache
                if any(part.startswith('.') for part in Path(file_path).parts):
                    continue
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Generate item ID based on relative path
                rel_path = Path(file_path).relative_to(self.knowledge_root)
                item_id = str(rel_path).replace('/', '_').replace('\\', '_')
                
                # Compute content hash
                content_hash = self._compute_content_hash(content)
                
                # Check if item exists and has changed
                existing_item = self.knowledge_items.get(item_id)
                if existing_item and existing_item.content_hash == content_hash:
                    continue  # No changes
                
                # Extract metadata and clean content
                metadata, clean_content = self._extract_metadata_from_content(content, file_path)
                
                # Get file stats
                file_stat = os.stat(file_path)
                last_modified = datetime.fromtimestamp(file_stat.st_mtime)
                
                # Determine knowledge type
                knowledge_type = self._determine_knowledge_type(file_path)
                
                # Create or update knowledge item
                knowledge_item = KnowledgeItem(
                    id=item_id,
                    knowledge_type=knowledge_type,
                    title=metadata.get('title', Path(file_path).stem.replace('_', ' ').replace('-', ' ').title()),
                    content=clean_content,
                    file_path=str(rel_path),
                    last_modified=last_modified,
                    version=metadata.get('version', self._generate_version(existing_item)),
                    tags=metadata.get('tags', []),
                    status=KnowledgeStatus(metadata.get('status', 'active')),
                    dependencies=metadata.get('dependencies', []),
                    metadata=metadata,
                    content_hash=content_hash
                )
                
                # Store the item
                self.knowledge_items[item_id] = knowledge_item
                
                # Log update
                action = "updated" if existing_item else "added"
                self.logger.info(f"Knowledge item {action}: {item_id}")
                
            except Exception as e:
                self.logger.error(f"Error processing knowledge file {file_path}: {e}")
        
        # Save updated index
        self._save_knowledge_index()
    
    def _generate_version(self, existing_item: Optional[KnowledgeItem] = None) -> str:
        """Generate version number for knowledge item"""
        if not existing_item:
            return "1.0.0"
        
        # Parse existing version and increment
        try:
            parts = existing_item.version.split('.')
            if len(parts) == 3:
                major, minor, patch = map(int, parts)
                return f"{major}.{minor}.{patch + 1}"
        except ValueError:
            pass
        
        return "1.0.0"
    
    def get_knowledge_item(self, agent_role: str, item_id: str) -> Optional[KnowledgeItem]:
        """Get specific knowledge item with access control"""
        item = self.knowledge_items.get(item_id)
        if not item:
            return None
        
        if not self.access_control.can_access(agent_role, item.knowledge_type, 'read'):
            raise PermissionError(f"Agent {agent_role} cannot read {item.knowledge_type}")
        
        return item
    
    def search_knowledge(self, agent_role: str, query: str, 
                        knowledge_types: List[KnowledgeType] = None,
                        tags: List[str] = None, limit: int = 20) -> List[KnowledgeItem]:
        """Search knowledge items"""
        results = []
        accessible_types = self.access_control.get_accessible_types(agent_role)
        
        # Filter by knowledge types if specified
        if knowledge_types:
            accessible_types = [kt for kt in accessible_types if kt in knowledge_types]
        
        for item in self.knowledge_items.values():
            # Check access permissions
            if item.knowledge_type not in accessible_types:
                continue
            
            # Check status
            if item.status == KnowledgeStatus.ARCHIVED:
                continue
            
            # Check tags filter
            if tags and not any(tag in item.tags for tag in tags):
                continue
            
            # Simple text matching
            if query.lower() in item.title.lower() or query.lower() in item.content.lower():
                results.append(item)
        
        # Sort by relevance (simple scoring)
        def relevance_score(item):
            score = 0
            query_lower = query.lower()
            if query_lower in item.title.lower():
                score += 3
            if query_lower in item.content.lower():
                score += 1
            if any(tag.lower() == query_lower for tag in item.tags):
                score += 2
            return score
        
        results.sort(key=relevance_score, reverse=True)
        return results[:limit]
    
    def get_knowledge_by_type(self, agent_role: str, knowledge_type: KnowledgeType) -> List[KnowledgeItem]:
        """Get all knowledge items of a specific type"""
        if not self.access_control.can_access(agent_role, knowledge_type, 'read'):
            raise PermissionError(f"Agent {agent_role} cannot read {knowledge_type}")
        
        return [item for item in self.knowledge_items.values() 
                if item.knowledge_type == knowledge_type and item.status != KnowledgeStatus.ARCHIVED]
    
    def get_brand_context(self, agent_role: str, context_type: str = "full") -> str:
        """Get brand context for agent injection"""
        try:
            brand_items = self.get_knowledge_by_type(agent_role, KnowledgeType.BRAND_FOUNDATION)
            persona_items = self.get_knowledge_by_type(agent_role, KnowledgeType.PERSONAS)
            example_items = self.get_knowledge_by_type(agent_role, KnowledgeType.WRITING_EXAMPLES)
            template_items = self.get_knowledge_by_type(agent_role, KnowledgeType.TEMPLATES)
            
            if context_type == "minimal":
                # Just brand foundation
                brand_context = "\n\n=== BRAND FOUNDATION (MANDATORY) ===\n\n"
                for item in brand_items:
                    brand_context += f"{item.content}\n\n"
                return brand_context
            
            elif context_type == "full":
                # Complete brand context
                brand_context = "\n\n=== MANDATORY BRAND KNOWLEDGE - THIS IS LAW ===\n\n"
                
                # Brand foundation
                for item in brand_items:
                    brand_context += f"## BRAND FOUNDATION (MANDATORY)\n{item.content}\n\n"
                
                # Personas
                if persona_items:
                    brand_context += "## TARGET PERSONAS (MANDATORY)\n"
                    for item in persona_items:
                        brand_context += f"### {item.title}\n{item.content}\n\n"
                
                # Writing examples
                if example_items:
                    brand_context += "## WRITING STYLE EXAMPLES (MANDATORY REFERENCE)\n"
                    for item in example_items:
                        brand_context += f"### Example: {item.title}\n{item.content}\n\n"
                
                # Templates
                if template_items:
                    brand_context += "## ARTICLE TEMPLATE (MANDATORY STRUCTURE)\n"
                    for item in template_items:
                        brand_context += f"{item.content}\n\n"
                
                # Enforcement rules
                brand_context += """
=== BRAND ENFORCEMENT RULES ===

1. ALL content must align with the brand foundation - no exceptions
2. ALL writing must match the voice characteristics in the brand foundation
3. ALL content must serve the target personas identified in the brand materials
4. ALL output must be validated against the writing examples for style consistency
5. ALL articles must follow the template structure when applicable
6. The brand voice uses first person because it represents authentic expertise - DO NOT fabricate personal experiences
7. Use supplied materials only - never invent examples or personal anecdotes
8. When personal experience would strengthen content, use annotations like [AUTHOR: add personal example]
9. Brand compliance is NOT optional - it is LAW

VIOLATION OF BRAND STANDARDS IS UNACCEPTABLE AND MUST BE CORRECTED IMMEDIATELY.
"""
                return brand_context
            
            else:
                raise ValueError(f"Unknown context_type: {context_type}")
                
        except PermissionError as e:
            self.logger.error(f"Permission error getting brand context: {e}")
            return "BRAND ACCESS DENIED - INSUFFICIENT PERMISSIONS"
        except Exception as e:
            self.logger.error(f"Error getting brand context: {e}")
            return "BRAND CONTEXT UNAVAILABLE - SYSTEM ERROR"
    
    def validate_knowledge_consistency(self) -> Dict[str, List[str]]:
        """Validate knowledge consistency across all items"""
        issues = {
            'missing_dependencies': [],
            'circular_dependencies': [],
            'conflicting_content': [],
            'outdated_references': [],
            'format_violations': []
        }
        
        # Check dependencies
        for item in self.knowledge_items.values():
            for dep_id in item.dependencies:
                if dep_id not in self.knowledge_items:
                    issues['missing_dependencies'].append(f"{item.id} depends on missing {dep_id}")
        
        # Check for circular dependencies (simplified)
        def has_circular_dep(item_id: str, visited: set, path: list) -> bool:
            if item_id in path:
                return True
            if item_id in visited:
                return False
            
            visited.add(item_id)
            path.append(item_id)
            
            item = self.knowledge_items.get(item_id)
            if item:
                for dep in item.dependencies:
                    if has_circular_dep(dep, visited, path.copy()):
                        return True
            
            return False
        
        for item_id in self.knowledge_items:
            if has_circular_dep(item_id, set(), []):
                issues['circular_dependencies'].append(f"Circular dependency detected involving {item_id}")
        
        return issues
    
    def update_knowledge_item(self, agent_role: str, item_id: str, 
                             new_content: str, metadata: Dict[str, Any] = None) -> bool:
        """Update knowledge item with access control"""
        item = self.knowledge_items.get(item_id)
        if not item:
            raise ValueError(f"Knowledge item {item_id} not found")
        
        if not self.access_control.can_access(agent_role, item.knowledge_type, 'write'):
            raise PermissionError(f"Agent {agent_role} cannot write to {item.knowledge_type}")
        
        try:
            # Create new version
            new_version = self._generate_version(item)
            new_hash = self._compute_content_hash(new_content)
            
            # Update item
            item.content = new_content
            item.last_modified = datetime.now()
            item.version = new_version
            item.content_hash = new_hash
            
            if metadata:
                item.metadata.update(metadata)
                item.tags = metadata.get('tags', item.tags)
                item.status = KnowledgeStatus(metadata.get('status', item.status.value))
            
            # Save to file
            file_path = self.knowledge_root / item.file_path
            with open(file_path, 'w', encoding='utf-8') as f:
                if item.metadata:
                    f.write("---\n")
                    yaml.dump(item.metadata, f, default_flow_style=False)
                    f.write("---\n\n")
                f.write(new_content)
            
            # Save index
            self._save_knowledge_index()
            
            self.logger.info(f"Updated knowledge item {item_id} to version {new_version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating knowledge item {item_id}: {e}")
            return False
    
    def get_knowledge_stats(self, agent_role: str) -> Dict[str, Any]:
        """Get knowledge statistics"""
        accessible_types = self.access_control.get_accessible_types(agent_role)
        stats = {
            'total_items': len(self.knowledge_items),
            'accessible_items': 0,
            'by_type': {},
            'by_status': defaultdict(int),
            'last_updated': None
        }
        
        latest_update = None
        for item in self.knowledge_items.values():
            if item.knowledge_type in accessible_types:
                stats['accessible_items'] += 1
                
                # Count by type
                type_name = item.knowledge_type.value
                if type_name not in stats['by_type']:
                    stats['by_type'][type_name] = 0
                stats['by_type'][type_name] += 1
                
                # Count by status
                stats['by_status'][item.status.value] += 1
                
                # Track latest update
                if not latest_update or item.last_modified > latest_update:
                    latest_update = item.last_modified
        
        if latest_update:
            stats['last_updated'] = latest_update.isoformat()
        
        return stats
    
    def refresh_knowledge(self) -> Dict[str, int]:
        """Refresh knowledge from filesystem"""
        before_count = len(self.knowledge_items)
        self._scan_and_update_knowledge()
        after_count = len(self.knowledge_items)
        
        return {
            'items_before': before_count,
            'items_after': after_count,
            'items_added': after_count - before_count,
            'timestamp': datetime.now().isoformat()
        }