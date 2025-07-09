"""
Memory Tools - Agent-accessible tools for interacting with the memory system
"""

from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ..memory_manager import MemoryManager, MemoryType
import json

class MemorySearchInput(BaseModel):
    """Input for memory search operations"""
    query: str = Field(..., description="Search query for memory retrieval")
    memory_type: str = Field(default="all", description="Type of memory to search: crew_shared, agent_specific, external_consolidated, session_temporary, or all")
    tags: Optional[List[str]] = Field(default=None, description="Tags to filter by")
    limit: int = Field(default=10, description="Maximum number of results to return")

class MemoryStoreInput(BaseModel):
    """Input for memory storage operations"""
    content: str = Field(..., description="Content to store in memory")
    memory_type: str = Field(default="crew_shared", description="Type of memory to store in")
    tags: Optional[List[str]] = Field(default=None, description="Tags to associate with the memory")
    importance: int = Field(default=5, description="Importance level (1-10)")

class InteractionMemoryInput(BaseModel):
    """Input for storing interaction memories"""
    interaction_type: str = Field(..., description="Type of interaction: feedback, revision, collaboration, etc.")
    content: str = Field(..., description="Content of the interaction")
    importance: int = Field(default=5, description="Importance level (1-10)")

class FeedbackMemoryInput(BaseModel):
    """Input for storing feedback pattern memories"""
    feedback_content: str = Field(..., description="The feedback given")
    article_context: str = Field(..., description="Context of the article being reviewed")
    effectiveness: int = Field(..., description="How effective the feedback was (1-10)")

class BrandDecisionMemoryInput(BaseModel):
    """Input for storing brand decision memories"""
    decision_context: str = Field(..., description="Context where the brand decision was made")
    decision_made: str = Field(..., description="The decision that was made")
    rationale: str = Field(..., description="Reasoning behind the decision")

class MemorySearchTool(BaseTool):
    """Tool for searching memory across all accessible memory types"""
    name: str = "memory_search"
    description: str = "Search for relevant memories across all accessible memory types. Use this to find past interactions, feedback patterns, brand decisions, and other relevant context."
    args_schema: type[BaseModel] = MemorySearchInput
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self, query: str, memory_type: str = "all", tags: Optional[List[str]] = None, 
             limit: int = 10) -> str:
        """Search for memories"""
        try:
            if memory_type == "all":
                results = self.memory_manager.search_across_memories(
                    agent_role=self.agent_role,
                    query=query,
                    limit=limit
                )
                
                if not results:
                    return "No relevant memories found for your query."
                
                formatted_results = []
                for mem_type, memories in results.items():
                    formatted_results.append(f"\n=== {mem_type.value.upper()} MEMORIES ===")
                    for memory in memories:
                        formatted_results.append(f"- [{memory.timestamp.strftime('%Y-%m-%d %H:%M')}] {memory.content}")
                        if memory.tags:
                            formatted_results.append(f"  Tags: {', '.join(memory.tags)}")
                        formatted_results.append(f"  Importance: {memory.importance}/10")
                
                return "\n".join(formatted_results)
            else:
                # Search specific memory type
                try:
                    mem_type = MemoryType(memory_type)
                    memories = self.memory_manager.retrieve_memory(
                        agent_role=self.agent_role,
                        memory_type=mem_type,
                        query=query,
                        tags=tags,
                        limit=limit
                    )
                    
                    if not memories:
                        return f"No memories found in {memory_type} for your query."
                    
                    formatted_results = [f"=== {memory_type.upper()} MEMORIES ==="]
                    for memory in memories:
                        formatted_results.append(f"- [{memory.timestamp.strftime('%Y-%m-%d %H:%M')}] {memory.content}")
                        if memory.tags:
                            formatted_results.append(f"  Tags: {', '.join(memory.tags)}")
                        formatted_results.append(f"  Importance: {memory.importance}/10")
                    
                    return "\n".join(formatted_results)
                except ValueError:
                    return f"Invalid memory type: {memory_type}. Use: crew_shared, agent_specific, external_consolidated, session_temporary, or all"
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error searching memory: {e}"

class MemoryStoreTool(BaseTool):
    """Tool for storing information in memory"""
    name: str = "memory_store"
    description: str = "Store important information in memory for future reference. Use this to remember insights, decisions, patterns, or any other relevant information."
    args_schema: type[BaseModel] = MemoryStoreInput
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self, content: str, memory_type: str = "crew_shared", 
             tags: Optional[List[str]] = None, importance: int = 5) -> str:
        """Store content in memory"""
        try:
            # Parse content as JSON if possible, otherwise store as text
            try:
                content_dict = json.loads(content)
            except json.JSONDecodeError:
                content_dict = {"content": content}
            
            # Validate memory type
            try:
                mem_type = MemoryType(memory_type)
            except ValueError:
                return f"Invalid memory type: {memory_type}. Use: crew_shared, agent_specific, external_consolidated, session_temporary"
            
            # Store in memory
            memory_id = self.memory_manager.store_memory(
                agent_role=self.agent_role,
                memory_type=mem_type,
                content=content_dict,
                tags=tags or [],
                importance=importance
            )
            
            return f"Memory stored successfully with ID: {memory_id}"
        
        except PermissionError as e:
            return f"Access denied: {e}"
        except Exception as e:
            return f"Error storing memory: {e}"

class InteractionMemoryTool(BaseTool):
    """Tool for storing interaction-specific memories"""
    name: str = "interaction_memory"
    description: str = "Store interaction-specific memories like feedback, revisions, or collaboration events. Use this to remember important interactions for learning and improvement."
    args_schema: type[BaseModel] = InteractionMemoryInput
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self, interaction_type: str, content: str, importance: int = 5) -> str:
        """Store interaction memory"""
        try:
            # Parse content as JSON if possible
            try:
                content_dict = json.loads(content)
            except json.JSONDecodeError:
                content_dict = {"content": content}
            
            self.memory_manager.store_interaction(
                agent_role=self.agent_role,
                interaction_type=interaction_type,
                content=content_dict,
                importance=importance
            )
            
            return f"Interaction memory stored: {interaction_type}"
        
        except Exception as e:
            return f"Error storing interaction memory: {e}"

class FeedbackMemoryTool(BaseTool):
    """Tool for storing feedback pattern memories"""
    name: str = "feedback_memory"
    description: str = "Store feedback patterns and their effectiveness for learning. Use this to remember what types of feedback work well and what doesn't."
    args_schema: type[BaseModel] = FeedbackMemoryInput
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self, feedback_content: str, article_context: str, effectiveness: int) -> str:
        """Store feedback pattern memory"""
        try:
            self.memory_manager.store_feedback_pattern(
                agent_role=self.agent_role,
                feedback_content=feedback_content,
                article_context=article_context,
                effectiveness=effectiveness
            )
            
            return f"Feedback pattern stored (effectiveness: {effectiveness}/10)"
        
        except Exception as e:
            return f"Error storing feedback memory: {e}"

class BrandDecisionMemoryTool(BaseTool):
    """Tool for storing brand decision memories"""
    name: str = "brand_decision_memory"
    description: str = "Store important brand interpretation decisions and their rationale. Use this to remember how brand guidelines were applied in specific contexts."
    args_schema: type[BaseModel] = BrandDecisionMemoryInput
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self, decision_context: str, decision_made: str, rationale: str) -> str:
        """Store brand decision memory"""
        try:
            self.memory_manager.store_brand_decision(
                agent_role=self.agent_role,
                decision_context=decision_context,
                decision_made=decision_made,
                rationale=rationale
            )
            
            return f"Brand decision stored: {decision_made}"
        
        except Exception as e:
            return f"Error storing brand decision memory: {e}"

class MemoryStatsTool(BaseTool):
    """Tool for getting memory statistics"""
    name: str = "memory_stats"
    description: str = "Get statistics about memory usage and storage. Use this to understand memory state and identify consolidation opportunities."
    args_schema: type[BaseModel] = BaseModel
    
    def __init__(self, memory_manager: MemoryManager, agent_role: str):
        super().__init__()
        self.memory_manager = memory_manager
        self.agent_role = agent_role
    
    def _run(self) -> str:
        """Get memory statistics"""
        try:
            stats = self.memory_manager.get_memory_stats(self.agent_role)
            
            formatted_stats = ["=== MEMORY STATISTICS ==="]
            for memory_type, type_stats in stats.items():
                formatted_stats.append(f"\n{memory_type.upper()}:")
                formatted_stats.append(f"  Total entries: {type_stats['total_entries']}")
                formatted_stats.append(f"  Consolidation candidates: {type_stats['consolidation_candidates']}")
                formatted_stats.append(f"  Average importance: {type_stats['average_importance']:.1f}/10")
                if type_stats['oldest_entry']:
                    formatted_stats.append(f"  Oldest entry: {type_stats['oldest_entry']}")
                if type_stats['newest_entry']:
                    formatted_stats.append(f"  Newest entry: {type_stats['newest_entry']}")
            
            return "\n".join(formatted_stats)
        
        except Exception as e:
            return f"Error getting memory stats: {e}"

def create_memory_tools(memory_manager: MemoryManager, agent_role: str) -> List[BaseTool]:
    """Create memory tools for an agent"""
    return [
        MemorySearchTool(memory_manager, agent_role),
        MemoryStoreTool(memory_manager, agent_role),
        InteractionMemoryTool(memory_manager, agent_role),
        FeedbackMemoryTool(memory_manager, agent_role),
        BrandDecisionMemoryTool(memory_manager, agent_role),
        MemoryStatsTool(memory_manager, agent_role)
    ]