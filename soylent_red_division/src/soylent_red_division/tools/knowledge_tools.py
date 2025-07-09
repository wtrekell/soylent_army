"""
Knowledge Tools - Agent-accessible tools for interacting with the knowledge system
"""

from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ..knowledge_manager import KnowledgeManager, KnowledgeType, KnowledgeStatus
import json

class KnowledgeSearchInput(BaseModel):
    """Input for knowledge search operations"""
    query: str = Field(..., description="Search query for knowledge retrieval")
    knowledge_types: Optional[List[str]] = Field(default=None, description="Knowledge types to search: brand_foundation, personas, writing_examples, templates, user_preferences, contextual")
    tags: Optional[List[str]] = Field(default=None, description="Tags to filter by")
    limit: int = Field(default=10, description="Maximum number of results to return")

class KnowledgeGetInput(BaseModel):
    """Input for getting specific knowledge items"""
    item_id: str = Field(..., description="ID of the knowledge item to retrieve")

class KnowledgeByTypeInput(BaseModel):
    """Input for getting knowledge by type"""
    knowledge_type: str = Field(..., description="Type of knowledge: brand_foundation, personas, writing_examples, templates, user_preferences, contextual")

class BrandContextInput(BaseModel):
    """Input for getting brand context"""
    context_type: str = Field(default="full", description="Type of context: minimal, full")

class KnowledgeUpdateInput(BaseModel):
    """Input for updating knowledge items"""
    item_id: str = Field(..., description="ID of the knowledge item to update")
    new_content: str = Field(..., description="New content for the knowledge item")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata to update")

class KnowledgeSearchTool(BaseTool):
    """Tool for searching knowledge across all accessible knowledge types"""
    name: str = "knowledge_search"
    description: str = "Search for relevant knowledge across all accessible knowledge types. Use this to find brand information, writing examples, templates, and other knowledge resources."
    args_schema: type[BaseModel] = KnowledgeSearchInput
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self, query: str, knowledge_types: Optional[List[str]] = None, 
             tags: Optional[List[str]] = None, limit: int = 10) -> str:
        """Search for knowledge items"""
        try:
            # Convert string knowledge types to enum
            kt_enums = None
            if knowledge_types:
                kt_enums = []
                for kt_str in knowledge_types:
                    try:
                        kt_enums.append(KnowledgeType(kt_str))
                    except ValueError:
                        return f"Invalid knowledge type: {kt_str}. Valid types: brand_foundation, personas, writing_examples, templates, user_preferences, contextual"
            
            results = self.knowledge_manager.search_knowledge(
                agent_role=self.agent_role,
                query=query,
                knowledge_types=kt_enums,
                tags=tags,
                limit=limit
            )
            
            if not results:
                return "No knowledge items found matching your query."
            
            formatted_results = [f"=== KNOWLEDGE SEARCH RESULTS FOR: '{query}' ==="]
            for item in results:
                formatted_results.append(f"\n**{item.title}** ({item.knowledge_type.value})")
                formatted_results.append(f"Version: {item.version} | Updated: {item.last_modified.strftime('%Y-%m-%d')}")
                if item.tags:
                    formatted_results.append(f"Tags: {', '.join(item.tags)}")
                
                # Show content preview (first 200 chars)
                content_preview = item.content[:200]
                if len(item.content) > 200:
                    content_preview += "..."
                formatted_results.append(f"Content: {content_preview}")
                formatted_results.append(f"ID: {item.id}")
                formatted_results.append("---")
            
            return "\n".join(formatted_results)
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error searching knowledge: {e}"

class KnowledgeGetTool(BaseTool):
    """Tool for getting specific knowledge items by ID"""
    name: str = "knowledge_get"
    description: str = "Get a specific knowledge item by its ID. Use this when you have the exact ID of a knowledge item you want to retrieve."
    args_schema: type[BaseModel] = KnowledgeGetInput
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self, item_id: str) -> str:
        """Get specific knowledge item"""
        try:
            item = self.knowledge_manager.get_knowledge_item(self.agent_role, item_id)
            
            if not item:
                return f"Knowledge item '{item_id}' not found."
            
            formatted_result = [f"=== KNOWLEDGE ITEM: {item.title} ==="]
            formatted_result.append(f"Type: {item.knowledge_type.value}")
            formatted_result.append(f"Version: {item.version}")
            formatted_result.append(f"Status: {item.status.value}")
            formatted_result.append(f"Last Modified: {item.last_modified.strftime('%Y-%m-%d %H:%M')}")
            if item.tags:
                formatted_result.append(f"Tags: {', '.join(item.tags)}")
            if item.dependencies:
                formatted_result.append(f"Dependencies: {', '.join(item.dependencies)}")
            formatted_result.append(f"\n**Content:**\n{item.content}")
            
            return "\n".join(formatted_result)
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error getting knowledge item: {e}"

class KnowledgeByTypeTool(BaseTool):
    """Tool for getting all knowledge items of a specific type"""
    name: str = "knowledge_by_type"
    description: str = "Get all knowledge items of a specific type. Use this to retrieve all brand foundation items, personas, writing examples, templates, etc."
    args_schema: type[BaseModel] = KnowledgeByTypeInput
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self, knowledge_type: str) -> str:
        """Get knowledge items by type"""
        try:
            # Convert string to enum
            try:
                kt_enum = KnowledgeType(knowledge_type)
            except ValueError:
                return f"Invalid knowledge type: {knowledge_type}. Valid types: brand_foundation, personas, writing_examples, templates, user_preferences, contextual"
            
            items = self.knowledge_manager.get_knowledge_by_type(self.agent_role, kt_enum)
            
            if not items:
                return f"No {knowledge_type} items found."
            
            formatted_results = [f"=== {knowledge_type.upper().replace('_', ' ')} ITEMS ==="]
            for item in items:
                formatted_results.append(f"\n**{item.title}**")
                formatted_results.append(f"ID: {item.id} | Version: {item.version}")
                if item.tags:
                    formatted_results.append(f"Tags: {', '.join(item.tags)}")
                
                # Show content preview for lists
                content_preview = item.content[:150]
                if len(item.content) > 150:
                    content_preview += "..."
                formatted_results.append(f"Preview: {content_preview}")
                formatted_results.append("---")
            
            return "\n".join(formatted_results)
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error getting knowledge by type: {e}"

class BrandContextTool(BaseTool):
    """Tool for getting brand context for content creation"""
    name: str = "brand_context"
    description: str = "Get comprehensive brand context for content creation. Use this before writing to ensure brand compliance."
    args_schema: type[BaseModel] = BrandContextInput
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self, context_type: str = "full") -> str:
        """Get brand context"""
        try:
            if context_type not in ["minimal", "full"]:
                return "Invalid context_type. Use 'minimal' or 'full'."
            
            brand_context = self.knowledge_manager.get_brand_context(self.agent_role, context_type)
            return brand_context
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error getting brand context: {e}"

class KnowledgeUpdateTool(BaseTool):
    """Tool for updating knowledge items (requires write permissions)"""
    name: str = "knowledge_update"
    description: str = "Update a knowledge item with new content. Use this to modify existing knowledge items when you have write permissions."
    args_schema: type[BaseModel] = KnowledgeUpdateInput
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self, item_id: str, new_content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Update knowledge item"""
        try:
            success = self.knowledge_manager.update_knowledge_item(
                agent_role=self.agent_role,
                item_id=item_id,
                new_content=new_content,
                metadata=metadata or {}
            )
            
            if success:
                return f"Successfully updated knowledge item: {item_id}"
            else:
                return f"Failed to update knowledge item: {item_id}"
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except ValueError as e:
            return f"Invalid request: {e}"
        except Exception as e:
            return f"Error updating knowledge item: {e}"

class KnowledgeStatsTool(BaseTool):
    """Tool for getting knowledge statistics"""
    name: str = "knowledge_stats"
    description: str = "Get statistics about the knowledge base. Use this to understand what knowledge is available and when it was last updated."
    args_schema: type[BaseModel] = BaseModel
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self) -> str:
        """Get knowledge statistics"""
        try:
            stats = self.knowledge_manager.get_knowledge_stats(self.agent_role)
            
            formatted_stats = ["=== KNOWLEDGE STATISTICS ==="]
            formatted_stats.append(f"Total items in system: {stats['total_items']}")
            formatted_stats.append(f"Accessible to you: {stats['accessible_items']}")
            
            if stats['last_updated']:
                formatted_stats.append(f"Last updated: {stats['last_updated']}")
            
            formatted_stats.append("\n**By Knowledge Type:**")
            for kt, count in stats['by_type'].items():
                formatted_stats.append(f"  {kt.replace('_', ' ').title()}: {count}")
            
            formatted_stats.append("\n**By Status:**")
            for status, count in stats['by_status'].items():
                formatted_stats.append(f"  {status.title()}: {count}")
            
            return "\n".join(formatted_stats)
        
        except Exception as e:
            return f"Error getting knowledge stats: {e}"

class KnowledgeValidationTool(BaseTool):
    """Tool for validating knowledge consistency"""
    name: str = "knowledge_validate"
    description: str = "Validate knowledge consistency and identify potential issues. Use this to check for missing dependencies, conflicts, or format violations."
    args_schema: type[BaseModel] = BaseModel
    
    def __init__(self, knowledge_manager: KnowledgeManager, agent_role: str):
        super().__init__()
        self.knowledge_manager = knowledge_manager
        self.agent_role = agent_role
    
    def _run(self) -> str:
        """Validate knowledge consistency"""
        try:
            # Only allow validation for users with admin-like permissions
            if self.agent_role not in ['brand_author']:
                return "Knowledge validation requires admin permissions."
            
            issues = self.knowledge_manager.validate_knowledge_consistency()
            
            if not any(issues.values()):
                return "✅ Knowledge validation passed - no issues found."
            
            formatted_issues = ["⚠️ KNOWLEDGE VALIDATION ISSUES FOUND:"]
            
            for issue_type, issue_list in issues.items():
                if issue_list:
                    formatted_issues.append(f"\n**{issue_type.replace('_', ' ').title()}:**")
                    for issue in issue_list:
                        formatted_issues.append(f"  - {issue}")
            
            return "\n".join(formatted_issues)
        
        except Exception as e:
            return f"Error validating knowledge: {e}"

def create_knowledge_tools(knowledge_manager: KnowledgeManager, agent_role: str) -> List[BaseTool]:
    """Create knowledge tools for an agent"""
    tools = [
        KnowledgeSearchTool(knowledge_manager, agent_role),
        KnowledgeGetTool(knowledge_manager, agent_role),
        KnowledgeByTypeTool(knowledge_manager, agent_role),
        BrandContextTool(knowledge_manager, agent_role),
        KnowledgeStatsTool(knowledge_manager, agent_role)
    ]
    
    # Add update tool for agents with write permissions
    if agent_role in ['brand_author']:
        tools.append(KnowledgeUpdateTool(knowledge_manager, agent_role))
        tools.append(KnowledgeValidationTool(knowledge_manager, agent_role))
    
    return tools