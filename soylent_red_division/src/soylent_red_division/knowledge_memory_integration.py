"""
Knowledge-Memory Integration - Bridge between knowledge and memory systems for enhanced learning
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging
from .knowledge_manager import KnowledgeManager, KnowledgeType, KnowledgeItem
from .memory_manager import MemoryManager, MemoryType
from pathlib import Path

class KnowledgeMemoryIntegration:
    """
    Integrates knowledge and memory systems for enhanced learning and adaptation
    """
    
    def __init__(self, knowledge_manager: KnowledgeManager, memory_manager: MemoryManager):
        self.knowledge_manager = knowledge_manager
        self.memory_manager = memory_manager
        self.logger = logging.getLogger("KnowledgeMemoryIntegration")
    
    def store_knowledge_usage(self, agent_role: str, knowledge_item_id: str, 
                             usage_context: str, effectiveness: int):
        """Store how knowledge was used and its effectiveness"""
        try:
            knowledge_item = self.knowledge_manager.get_knowledge_item(agent_role, knowledge_item_id)
            if not knowledge_item:
                return False
            
            usage_memory = {
                'knowledge_item_id': knowledge_item_id,
                'knowledge_type': knowledge_item.knowledge_type.value,
                'knowledge_title': knowledge_item.title,
                'usage_context': usage_context,
                'effectiveness': effectiveness,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in appropriate memory based on effectiveness
            if effectiveness >= 8:
                memory_type = MemoryType.EXTERNAL_CONSOLIDATED
            elif effectiveness >= 6:
                memory_type = MemoryType.CREW_SHARED
            else:
                memory_type = MemoryType.AGENT_SPECIFIC
            
            self.memory_manager.store_memory(
                agent_role=agent_role,
                memory_type=memory_type,
                content=usage_memory,
                tags=['knowledge_usage', knowledge_item.knowledge_type.value],
                importance=effectiveness
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error storing knowledge usage: {e}")
            return False
    
    def get_knowledge_usage_patterns(self, agent_role: str, 
                                   knowledge_type: KnowledgeType = None) -> List[Dict[str, Any]]:
        """Get patterns of knowledge usage from memory"""
        try:
            tags = ['knowledge_usage']
            if knowledge_type:
                tags.append(knowledge_type.value)
            
            # Search across all accessible memory types
            usage_memories = []
            for memory_type in [MemoryType.CREW_SHARED, MemoryType.AGENT_SPECIFIC, MemoryType.EXTERNAL_CONSOLIDATED]:
                try:
                    memories = self.memory_manager.retrieve_memory(
                        agent_role=agent_role,
                        memory_type=memory_type,
                        tags=tags,
                        limit=50
                    )
                    usage_memories.extend(memories)
                except PermissionError:
                    continue
            
            # Convert to usage patterns
            patterns = []
            for memory in usage_memories:
                if isinstance(memory.content, dict) and 'knowledge_item_id' in memory.content:
                    patterns.append(memory.content)
            
            return patterns
        except Exception as e:
            self.logger.error(f"Error getting knowledge usage patterns: {e}")
            return []
    
    def recommend_knowledge(self, agent_role: str, current_context: str, 
                          limit: int = 5) -> List[KnowledgeItem]:
        """Recommend knowledge items based on past usage patterns and current context"""
        try:
            # Get usage patterns
            usage_patterns = self.get_knowledge_usage_patterns(agent_role)
            
            # Score knowledge items based on past effectiveness and context relevance
            knowledge_scores = {}
            
            # Score based on usage patterns
            for pattern in usage_patterns:
                item_id = pattern.get('knowledge_item_id')
                if item_id:
                    effectiveness = pattern.get('effectiveness', 5)
                    context_similarity = self._calculate_context_similarity(
                        current_context, 
                        pattern.get('usage_context', '')
                    )
                    
                    score = effectiveness * (1 + context_similarity)
                    knowledge_scores[item_id] = knowledge_scores.get(item_id, 0) + score
            
            # Get top-scored knowledge items
            sorted_items = sorted(knowledge_scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for item_id, score in sorted_items[:limit]:
                try:
                    item = self.knowledge_manager.get_knowledge_item(agent_role, item_id)
                    if item:
                        recommendations.append(item)
                except PermissionError:
                    continue
            
            # If we don't have enough recommendations, add some based on context search
            if len(recommendations) < limit:
                search_results = self.knowledge_manager.search_knowledge(
                    agent_role=agent_role,
                    query=current_context,
                    limit=limit - len(recommendations)
                )
                
                # Add items not already in recommendations
                existing_ids = {item.id for item in recommendations}
                for item in search_results:
                    if item.id not in existing_ids:
                        recommendations.append(item)
            
            return recommendations[:limit]
        except Exception as e:
            self.logger.error(f"Error recommending knowledge: {e}")
            return []
    
    def _calculate_context_similarity(self, context1: str, context2: str) -> float:
        """Simple context similarity calculation"""
        if not context1 or not context2:
            return 0.0
        
        words1 = set(context1.lower().split())
        words2 = set(context2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def update_knowledge_from_memory(self, agent_role: str) -> Dict[str, int]:
        """Update knowledge based on memory insights"""
        try:
            # Only allow updates for authorized roles
            if agent_role not in ['brand_author']:
                raise PermissionError("Knowledge updates require admin permissions")
            
            updates_made = {
                'brand_improvements': 0,
                'template_updates': 0,
                'example_additions': 0
            }
            
            # Get feedback patterns from memory
            feedback_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['feedback', 'pattern'],
                limit=100
            )
            
            # Analyze feedback for knowledge improvements
            brand_feedback = []
            template_feedback = []
            
            for memory in feedback_memories:
                content = memory.content
                if isinstance(content, dict):
                    feedback_content = content.get('feedback_content', '')
                    effectiveness = content.get('effectiveness', 5)
                    
                    if effectiveness >= 7:  # High-effectiveness feedback
                        if any(keyword in feedback_content.lower() for keyword in ['brand', 'voice', 'tone', 'style']):
                            brand_feedback.append(content)
                        elif any(keyword in feedback_content.lower() for keyword in ['template', 'structure', 'format']):
                            template_feedback.append(content)
            
            # Generate improvement suggestions (this could be enhanced with LLM processing)
            if brand_feedback:
                # Could trigger brand guideline updates based on consistent feedback
                self.logger.info(f"Found {len(brand_feedback)} high-value brand feedback items")
                updates_made['brand_improvements'] = len(brand_feedback)
            
            if template_feedback:
                # Could trigger template improvements
                self.logger.info(f"Found {len(template_feedback)} high-value template feedback items")
                updates_made['template_updates'] = len(template_feedback)
            
            return updates_made
        except Exception as e:
            self.logger.error(f"Error updating knowledge from memory: {e}")
            return {}
    
    def create_knowledge_from_interaction(self, agent_role: str, interaction_context: str,
                                        key_insights: List[str], importance: int = 7) -> Optional[str]:
        """Create new contextual knowledge from successful interactions"""
        try:
            if importance < 7:  # Only create knowledge from high-value interactions
                return None
            
            # Create new contextual knowledge item
            knowledge_content = {
                'source': 'interaction_learning',
                'context': interaction_context,
                'insights': key_insights,
                'created_from_memory': True,
                'importance': importance,
                'created_at': datetime.now().isoformat()
            }
            
            # Store as contextual knowledge and in memory
            memory_id = self.memory_manager.store_memory(
                agent_role=agent_role,
                memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
                content=knowledge_content,
                tags=['contextual_knowledge', 'interaction_learning'],
                importance=importance
            )
            
            self.logger.info(f"Created contextual knowledge from interaction: {memory_id}")
            return memory_id
        except Exception as e:
            self.logger.error(f"Error creating knowledge from interaction: {e}")
            return None
    
    def get_integration_stats(self, agent_role: str) -> Dict[str, Any]:
        """Get statistics about knowledge-memory integration"""
        try:
            stats = {
                'knowledge_usage_entries': 0,
                'feedback_patterns': 0,
                'contextual_knowledge_created': 0,
                'top_used_knowledge_types': {},
                'average_effectiveness': 0.0
            }
            
            # Get usage patterns
            usage_patterns = self.get_knowledge_usage_patterns(agent_role)
            stats['knowledge_usage_entries'] = len(usage_patterns)
            
            if usage_patterns:
                # Calculate type usage
                type_counts = {}
                effectiveness_scores = []
                
                for pattern in usage_patterns:
                    kt = pattern.get('knowledge_type', 'unknown')
                    type_counts[kt] = type_counts.get(kt, 0) + 1
                    
                    effectiveness = pattern.get('effectiveness', 5)
                    effectiveness_scores.append(effectiveness)
                
                stats['top_used_knowledge_types'] = dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True))
                stats['average_effectiveness'] = sum(effectiveness_scores) / len(effectiveness_scores)
            
            # Get feedback patterns
            feedback_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['feedback', 'pattern'],
                limit=1000
            )
            stats['feedback_patterns'] = len(feedback_memories)
            
            # Get contextual knowledge created
            contextual_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
                tags=['contextual_knowledge'],
                limit=1000
            )
            stats['contextual_knowledge_created'] = len(contextual_memories)
            
            return stats
        except Exception as e:
            self.logger.error(f"Error getting integration stats: {e}")
            return {}
    
    def optimize_knowledge_access(self, agent_role: str) -> Dict[str, Any]:
        """Optimize knowledge access patterns based on usage data"""
        try:
            usage_patterns = self.get_knowledge_usage_patterns(agent_role)
            
            optimization_results = {
                'frequently_used_items': [],
                'underused_items': [],
                'suggested_cache_items': [],
                'access_patterns': {}
            }
            
            if not usage_patterns:
                return optimization_results
            
            # Analyze usage frequency
            item_usage = {}
            for pattern in usage_patterns:
                item_id = pattern.get('knowledge_item_id')
                if item_id:
                    item_usage[item_id] = item_usage.get(item_id, 0) + 1
            
            # Sort by usage frequency
            sorted_usage = sorted(item_usage.items(), key=lambda x: x[1], reverse=True)
            
            # Get frequently used items (top 20%)
            top_count = max(1, len(sorted_usage) // 5)
            optimization_results['frequently_used_items'] = [
                item_id for item_id, count in sorted_usage[:top_count]
            ]
            
            # Get underused items (items used only once)
            optimization_results['underused_items'] = [
                item_id for item_id, count in sorted_usage if count == 1
            ]
            
            # Suggest cache items (frequently used + high effectiveness)
            effectiveness_by_item = {}
            for pattern in usage_patterns:
                item_id = pattern.get('knowledge_item_id')
                effectiveness = pattern.get('effectiveness', 5)
                if item_id:
                    if item_id not in effectiveness_by_item:
                        effectiveness_by_item[item_id] = []
                    effectiveness_by_item[item_id].append(effectiveness)
            
            # Calculate average effectiveness per item
            avg_effectiveness = {}
            for item_id, scores in effectiveness_by_item.items():
                avg_effectiveness[item_id] = sum(scores) / len(scores)
            
            # Suggest items with high usage and high effectiveness for caching
            cache_candidates = []
            for item_id, usage_count in sorted_usage[:10]:  # Top 10 most used
                if avg_effectiveness.get(item_id, 0) >= 7:  # High effectiveness
                    cache_candidates.append(item_id)
            
            optimization_results['suggested_cache_items'] = cache_candidates
            
            return optimization_results
        except Exception as e:
            self.logger.error(f"Error optimizing knowledge access: {e}")
            return {}