"""
Reasoning Integration - Bridge between reasoning engine and memory/knowledge systems
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging
from .reasoning_engine import ReasoningEngine, ReasoningContext, ExecutionPlan, PlanStep, DecisionType
from .memory_manager import MemoryManager, MemoryType
from .knowledge_manager import KnowledgeManager, KnowledgeType
from pathlib import Path

class ReasoningIntegration:
    """
    Integrates reasoning engine with memory and knowledge systems for enhanced planning
    """
    
    def __init__(self, reasoning_engine: ReasoningEngine, memory_manager: MemoryManager, 
                 knowledge_manager: KnowledgeManager):
        self.reasoning_engine = reasoning_engine
        self.memory_manager = memory_manager
        self.knowledge_manager = knowledge_manager
        self.logger = logging.getLogger("ReasoningIntegration")
    
    def create_context_aware_plan(self, agent_role: str, plan_type: str, 
                                 base_requirements: Dict[str, Any]) -> ExecutionPlan:
        """Create a plan enhanced with memory and knowledge context"""
        try:
            # Get relevant knowledge for context
            knowledge_context = self._get_knowledge_context(agent_role, base_requirements)
            
            # Get memory insights for planning
            memory_insights = self._get_memory_insights(agent_role, base_requirements)
            
            # Enhance requirements with context
            enhanced_requirements = {
                **base_requirements,
                'knowledge_context': knowledge_context,
                'memory_insights': memory_insights,
                'past_successes': memory_insights.get('successful_patterns', []),
                'common_pitfalls': memory_insights.get('failure_patterns', [])
            }
            
            # Create reasoning context
            context = ReasoningContext(
                task_type=base_requirements.get('task_type', 'content_creation'),
                content_requirements=enhanced_requirements,
                brand_constraints=knowledge_context.get('brand_constraints', {}),
                target_personas=base_requirements.get('target_personas', []),
                available_resources=self._get_available_resources(agent_role),
                success_criteria=base_requirements.get('success_criteria', {}),
                time_constraints=base_requirements.get('time_constraints'),
                quality_thresholds=base_requirements.get('quality_thresholds')
            )
            
            # Create plan with enhanced context
            plan = self.reasoning_engine.create_plan(plan_type, context, agent_role)
            
            # Store plan creation in memory
            self._store_plan_creation_memory(agent_role, plan, enhanced_requirements)
            
            return plan
            
        except Exception as e:
            self.logger.error(f"Error creating context-aware plan: {e}")
            raise
    
    def make_knowledge_informed_decision(self, agent_role: str, decision_type: DecisionType,
                                       base_context: Dict[str, Any]) -> Dict[str, Any]:
        """Make a decision informed by knowledge and memory"""
        try:
            # Get relevant knowledge
            knowledge_items = self.knowledge_manager.search_knowledge(
                agent_role=agent_role,
                query=base_context.get('query', ''),
                knowledge_types=[KnowledgeType.BRAND_FOUNDATION, KnowledgeType.WRITING_EXAMPLES],
                limit=10
            )
            
            # Get decision patterns from memory
            decision_patterns = self._get_decision_patterns(agent_role, decision_type)
            
            # Enhance context with knowledge and memory
            enhanced_context = ReasoningContext(
                task_type=base_context.get('task_type', 'decision_making'),
                content_requirements={
                    **base_context,
                    'knowledge_references': [item.id for item in knowledge_items],
                    'decision_patterns': decision_patterns
                },
                brand_constraints=self._extract_brand_constraints(knowledge_items),
                target_personas=base_context.get('target_personas', []),
                available_resources={},
                success_criteria=base_context.get('success_criteria', {})
            )
            
            # Make decision
            decision = self.reasoning_engine.make_decision(decision_type, enhanced_context)
            
            # Store decision in memory
            self._store_decision_memory(agent_role, decision_type, decision, enhanced_context)
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Error making knowledge-informed decision: {e}")
            raise
    
    def adapt_plan_from_feedback(self, agent_role: str, plan_id: str, 
                               feedback: Dict[str, Any]) -> bool:
        """Adapt plan based on feedback and past experience"""
        try:
            plan = self.reasoning_engine.get_plan(plan_id)
            if not plan:
                return False
            
            # Analyze feedback patterns
            feedback_analysis = self._analyze_feedback_patterns(agent_role, feedback)
            
            # Get similar past adaptations
            similar_adaptations = self._get_similar_adaptations(agent_role, feedback)
            
            # Store feedback in memory
            self._store_feedback_memory(agent_role, plan_id, feedback, feedback_analysis)
            
            # Update plan based on insights
            adaptation_success = self._apply_plan_adaptations(plan, feedback_analysis, similar_adaptations)
            
            return adaptation_success
            
        except Exception as e:
            self.logger.error(f"Error adapting plan from feedback: {e}")
            return False
    
    def _get_knowledge_context(self, agent_role: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Get relevant knowledge context for planning"""
        context = {
            'brand_constraints': {},
            'templates': [],
            'examples': [],
            'personas': []
        }
        
        try:
            # Get brand foundation
            brand_items = self.knowledge_manager.get_knowledge_by_type(agent_role, KnowledgeType.BRAND_FOUNDATION)
            if brand_items:
                context['brand_constraints'] = {
                    'voice_characteristics': brand_items[0].metadata.get('voice_characteristics', []),
                    'values': brand_items[0].metadata.get('values', []),
                    'enforcement_rules': brand_items[0].metadata.get('enforcement_rules', [])
                }
            
            # Get relevant templates
            task_type = requirements.get('task_type', '')
            if task_type:
                templates = self.knowledge_manager.search_knowledge(
                    agent_role=agent_role,
                    query=task_type,
                    knowledge_types=[KnowledgeType.TEMPLATES],
                    limit=5
                )
                context['templates'] = [{'id': t.id, 'title': t.title} for t in templates]
            
            # Get writing examples
            examples = self.knowledge_manager.get_knowledge_by_type(agent_role, KnowledgeType.WRITING_EXAMPLES)
            context['examples'] = [{'id': e.id, 'title': e.title} for e in examples[:3]]
            
            # Get personas
            personas = self.knowledge_manager.get_knowledge_by_type(agent_role, KnowledgeType.PERSONAS)
            context['personas'] = [{'id': p.id, 'title': p.title} for p in personas]
            
        except Exception as e:
            self.logger.error(f"Error getting knowledge context: {e}")
        
        return context
    
    def _get_memory_insights(self, agent_role: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Get memory insights for planning"""
        insights = {
            'successful_patterns': [],
            'failure_patterns': [],
            'optimization_suggestions': [],
            'past_decisions': []
        }
        
        try:
            # Get successful interaction patterns
            successful_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['interaction', 'success'],
                limit=10
            )
            
            for memory in successful_memories:
                if memory.importance >= 7:
                    insights['successful_patterns'].append({
                        'pattern': memory.content.get('interaction_type', ''),
                        'effectiveness': memory.importance,
                        'context': memory.content.get('context', {})
                    })
            
            # Get failure patterns
            failure_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.AGENT_SPECIFIC,
                tags=['failure', 'error'],
                limit=5
            )
            
            for memory in failure_memories:
                insights['failure_patterns'].append({
                    'pattern': memory.content.get('error_type', ''),
                    'context': memory.content.get('context', {}),
                    'lesson': memory.content.get('lesson_learned', '')
                })
            
            # Get past decisions
            task_type = requirements.get('task_type', '')
            if task_type:
                decision_memories = self.memory_manager.retrieve_memory(
                    agent_role=agent_role,
                    memory_type=MemoryType.CREW_SHARED,
                    query=task_type,
                    tags=['decision'],
                    limit=5
                )
                
                for memory in decision_memories:
                    insights['past_decisions'].append({
                        'decision_type': memory.content.get('decision_type', ''),
                        'outcome': memory.content.get('outcome', ''),
                        'effectiveness': memory.importance
                    })
            
        except Exception as e:
            self.logger.error(f"Error getting memory insights: {e}")
        
        return insights
    
    def _get_available_resources(self, agent_role: str) -> Dict[str, Any]:
        """Get available resources for planning"""
        resources = {
            'knowledge_items': 0,
            'memory_entries': 0,
            'templates': 0,
            'examples': 0
        }
        
        try:
            # Get knowledge stats
            knowledge_stats = self.knowledge_manager.get_knowledge_stats(agent_role)
            resources['knowledge_items'] = knowledge_stats.get('accessible_items', 0)
            resources['templates'] = knowledge_stats.get('by_type', {}).get('templates', 0)
            resources['examples'] = knowledge_stats.get('by_type', {}).get('writing_examples', 0)
            
            # Get memory stats
            memory_stats = self.memory_manager.get_memory_stats(agent_role)
            total_memory = sum(stats.get('total_entries', 0) for stats in memory_stats.values())
            resources['memory_entries'] = total_memory
            
        except Exception as e:
            self.logger.error(f"Error getting available resources: {e}")
        
        return resources
    
    def _get_decision_patterns(self, agent_role: str, decision_type: DecisionType) -> List[Dict[str, Any]]:
        """Get decision patterns from memory"""
        patterns = []
        
        try:
            decision_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                query=decision_type.value,
                tags=['decision'],
                limit=10
            )
            
            for memory in decision_memories:
                patterns.append({
                    'decision_type': memory.content.get('decision_type', ''),
                    'context': memory.content.get('context', {}),
                    'outcome': memory.content.get('outcome', ''),
                    'effectiveness': memory.importance,
                    'timestamp': memory.timestamp.isoformat()
                })
        
        except Exception as e:
            self.logger.error(f"Error getting decision patterns: {e}")
        
        return patterns
    
    def _extract_brand_constraints(self, knowledge_items: List) -> Dict[str, Any]:
        """Extract brand constraints from knowledge items"""
        constraints = {}
        
        for item in knowledge_items:
            if item.knowledge_type == KnowledgeType.BRAND_FOUNDATION:
                constraints.update({
                    'voice_mandatory': True,
                    'persona_targeting_required': True,
                    'authenticity_protection': True,
                    'ethical_integration': True
                })
            elif item.knowledge_type == KnowledgeType.WRITING_EXAMPLES:
                constraints.update({
                    'style_consistency_required': True,
                    'tone_matching_required': True
                })
        
        return constraints
    
    def _analyze_feedback_patterns(self, agent_role: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback patterns"""
        analysis = {
            'feedback_type': 'general',
            'urgency': 'medium',
            'scope': 'content',
            'similar_past_feedback': []
        }
        
        try:
            # Analyze feedback content
            feedback_content = feedback.get('content', '')
            
            # Determine feedback type
            if any(word in feedback_content.lower() for word in ['structure', 'organization', 'flow']):
                analysis['feedback_type'] = 'structural'
            elif any(word in feedback_content.lower() for word in ['voice', 'tone', 'brand']):
                analysis['feedback_type'] = 'voice'
            elif any(word in feedback_content.lower() for word in ['technical', 'accuracy', 'detail']):
                analysis['feedback_type'] = 'technical'
            
            # Determine urgency
            if any(word in feedback_content.lower() for word in ['urgent', 'critical', 'must']):
                analysis['urgency'] = 'high'
            elif any(word in feedback_content.lower() for word in ['minor', 'suggestion', 'consider']):
                analysis['urgency'] = 'low'
            
            # Find similar past feedback
            similar_feedback = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                query=feedback_content[:50],
                tags=['feedback'],
                limit=5
            )
            
            analysis['similar_past_feedback'] = [
                {
                    'content': mem.content.get('feedback_content', ''),
                    'effectiveness': mem.importance,
                    'resolution': mem.content.get('resolution', '')
                }
                for mem in similar_feedback
            ]
        
        except Exception as e:
            self.logger.error(f"Error analyzing feedback patterns: {e}")
        
        return analysis
    
    def _get_similar_adaptations(self, agent_role: str, feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get similar past adaptations"""
        adaptations = []
        
        try:
            # Search for similar adaptation memories
            adaptation_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['adaptation', 'plan_change'],
                limit=5
            )
            
            for memory in adaptation_memories:
                adaptations.append({
                    'adaptation_type': memory.content.get('adaptation_type', ''),
                    'original_issue': memory.content.get('original_issue', ''),
                    'solution': memory.content.get('solution', ''),
                    'effectiveness': memory.importance
                })
        
        except Exception as e:
            self.logger.error(f"Error getting similar adaptations: {e}")
        
        return adaptations
    
    def _store_plan_creation_memory(self, agent_role: str, plan: ExecutionPlan, 
                                  requirements: Dict[str, Any]):
        """Store plan creation in memory"""
        try:
            plan_memory = {
                'plan_id': plan.id,
                'plan_type': plan.plan_type,
                'requirements': requirements,
                'steps_count': len(plan.steps),
                'estimated_duration': plan.estimated_duration,
                'created_at': plan.created_at.isoformat()
            }
            
            self.memory_manager.store_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                content=plan_memory,
                tags=['plan_creation', plan.plan_type],
                importance=6
            )
        
        except Exception as e:
            self.logger.error(f"Error storing plan creation memory: {e}")
    
    def _store_decision_memory(self, agent_role: str, decision_type: DecisionType,
                             decision: Dict[str, Any], context: ReasoningContext):
        """Store decision in memory"""
        try:
            decision_memory = {
                'decision_type': decision_type.value,
                'decision': decision,
                'context': context.to_dict(),
                'confidence': decision.get('confidence', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            self.memory_manager.store_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                content=decision_memory,
                tags=['decision', decision_type.value],
                importance=int(decision.get('confidence', 0) * 10)
            )
        
        except Exception as e:
            self.logger.error(f"Error storing decision memory: {e}")
    
    def _store_feedback_memory(self, agent_role: str, plan_id: str, feedback: Dict[str, Any],
                             analysis: Dict[str, Any]):
        """Store feedback in memory"""
        try:
            feedback_memory = {
                'plan_id': plan_id,
                'feedback': feedback,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            self.memory_manager.store_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                content=feedback_memory,
                tags=['feedback', analysis.get('feedback_type', 'general')],
                importance=7 if analysis.get('urgency') == 'high' else 5
            )
        
        except Exception as e:
            self.logger.error(f"Error storing feedback memory: {e}")
    
    def _apply_plan_adaptations(self, plan: ExecutionPlan, feedback_analysis: Dict[str, Any],
                              similar_adaptations: List[Dict[str, Any]]) -> bool:
        """Apply adaptations to plan based on feedback"""
        try:
            # This is a simplified implementation
            # In a real system, this would involve more sophisticated plan modification
            
            feedback_type = feedback_analysis.get('feedback_type', 'general')
            urgency = feedback_analysis.get('urgency', 'medium')
            
            # Adjust plan based on feedback type
            if feedback_type == 'structural':
                # Add structural review step
                for step in plan.steps:
                    if step.step_type == 'content_creation':
                        step.estimated_duration += 10
                        step.metadata['structural_review_added'] = True
            
            elif feedback_type == 'voice':
                # Add voice validation step
                for step in plan.steps:
                    if step.step_type == 'brand_validation':
                        step.estimated_duration += 5
                        step.metadata['enhanced_voice_validation'] = True
            
            # Update plan metadata
            plan.metadata['feedback_adaptations'] = {
                'feedback_type': feedback_type,
                'urgency': urgency,
                'adapted_at': datetime.now().isoformat()
            }
            
            plan.updated_at = datetime.now()
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error applying plan adaptations: {e}")
            return False
    
    def get_integration_stats(self, agent_role: str) -> Dict[str, Any]:
        """Get integration statistics"""
        stats = {
            'plans_created': 0,
            'decisions_made': 0,
            'feedback_processed': 0,
            'adaptations_applied': 0,
            'knowledge_utilization': 0,
            'memory_utilization': 0
        }
        
        try:
            # Get plan creation stats
            plan_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['plan_creation'],
                limit=1000
            )
            stats['plans_created'] = len(plan_memories)
            
            # Get decision stats
            decision_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['decision'],
                limit=1000
            )
            stats['decisions_made'] = len(decision_memories)
            
            # Get feedback stats
            feedback_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['feedback'],
                limit=1000
            )
            stats['feedback_processed'] = len(feedback_memories)
            
            # Get adaptation stats
            adaptation_memories = self.memory_manager.retrieve_memory(
                agent_role=agent_role,
                memory_type=MemoryType.CREW_SHARED,
                tags=['adaptation'],
                limit=1000
            )
            stats['adaptations_applied'] = len(adaptation_memories)
            
            # Calculate utilization rates
            total_actions = sum([stats['plans_created'], stats['decisions_made'], 
                               stats['feedback_processed'], stats['adaptations_applied']])
            
            if total_actions > 0:
                stats['knowledge_utilization'] = (stats['decisions_made'] / total_actions) * 100
                stats['memory_utilization'] = (stats['feedback_processed'] / total_actions) * 100
        
        except Exception as e:
            self.logger.error(f"Error getting integration stats: {e}")
        
        return stats