"""
Validation Tools - Agent-accessible tools for content validation and guardrails
"""

from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ..validation_engine import ValidationEngine, ValidationType, ValidationSeverity, ValidationStatus
import json

class ValidateContentInput(BaseModel):
    """Input for content validation"""
    content: str = Field(..., description="Content to validate")
    target_personas: List[str] = Field(default=[], description="Target personas for the content")
    source_materials: str = Field(default="", description="Source materials used for content creation")
    validation_types: List[str] = Field(default=[], description="Specific validation types to run (optional)")

class ValidateRealTimeInput(BaseModel):
    """Input for real-time validation"""
    partial_content: str = Field(..., description="Partial content being written")
    context: Dict[str, Any] = Field(default={}, description="Context for validation")

class GetValidationResultInput(BaseModel):
    """Input for getting validation results"""
    result_id: str = Field(..., description="ID of the validation result to retrieve")

class GetValidationHistoryInput(BaseModel):
    """Input for getting validation history"""
    content_id: str = Field(..., description="ID of the content to get validation history for")

class ValidateContentTool(BaseTool):
    """Tool for comprehensive content validation"""
    name: str = "validate_content"
    description: str = "Perform comprehensive brand compliance and quality validation on content. Use this to ensure content meets all brand standards before publication."
    args_schema: type[BaseModel] = ValidateContentInput
    
    def __init__(self, validation_engine: ValidationEngine, agent_role: str):
        super().__init__()
        self.validation_engine = validation_engine
        self.agent_role = agent_role
    
    def _run(self, content: str, target_personas: List[str] = None, 
             source_materials: str = "", validation_types: List[str] = None) -> str:
        """Run comprehensive content validation"""
        try:
            # Convert string validation types to enums
            validation_type_enums = None
            if validation_types:
                validation_type_enums = []
                for vt in validation_types:
                    try:
                        validation_type_enums.append(ValidationType(vt))
                    except ValueError:
                        pass  # Skip invalid types
            
            # Run validation
            result = self.validation_engine.validate_content(
                content=content,
                target_personas=target_personas or [],
                source_materials=source_materials,
                validation_types=validation_type_enums
            )
            
            # Format response
            response = [f"=== CONTENT VALIDATION RESULT ==="]
            response.append(f"Validation ID: {result.id}")
            response.append(f"Overall Status: {result.overall_status.value.upper()}")
            response.append(f"Overall Score: {result.overall_score:.1f}/100")
            response.append(f"Issues Found: {len(result.issues)}")
            
            if result.overall_status == ValidationStatus.PASSED:
                response.append("\\n✅ CONTENT PASSED ALL VALIDATIONS")
                response.append("Content meets all brand compliance and quality standards.")
            else:
                response.append(f"\\n⚠️ VALIDATION {result.overall_status.value.upper()}")
                
                # Group issues by severity
                critical_issues = [i for i in result.issues if i.severity == ValidationSeverity.CRITICAL]
                high_issues = [i for i in result.issues if i.severity == ValidationSeverity.HIGH]
                medium_issues = [i for i in result.issues if i.severity == ValidationSeverity.MEDIUM]
                low_issues = [i for i in result.issues if i.severity == ValidationSeverity.LOW]
                
                if critical_issues:
                    response.append(f"\\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
                    for issue in critical_issues[:3]:  # Show top 3
                        response.append(f"  • {issue.message}")
                        response.append(f"    {issue.description}")
                        if issue.suggestions:
                            response.append(f"    Suggestion: {issue.suggestions[0]}")
                
                if high_issues:
                    response.append(f"\\n⚠️ HIGH PRIORITY ISSUES ({len(high_issues)}):")
                    for issue in high_issues[:3]:  # Show top 3
                        response.append(f"  • {issue.message}")
                        if issue.suggestions:
                            response.append(f"    Suggestion: {issue.suggestions[0]}")
                
                if medium_issues:
                    response.append(f"\\n📋 MEDIUM PRIORITY ISSUES ({len(medium_issues)}):")
                    for issue in medium_issues[:2]:  # Show top 2
                        response.append(f"  • {issue.message}")
                
                if low_issues:
                    response.append(f"\\n💡 LOW PRIORITY ISSUES ({len(low_issues)}):")
                    response.append(f"  {len(low_issues)} minor issues found")
            
            # Overall suggestions
            if result.suggestions:
                response.append(f"\\n**Overall Recommendations:**")
                for suggestion in result.suggestions:
                    response.append(f"  • {suggestion}")
            
            response.append(f"\\n**Validation Details:**")
            response.append(f"  Types checked: {', '.join(vt.value for vt in result.validation_types)}")
            response.append(f"  Target personas: {', '.join(target_personas) if target_personas else 'None specified'}")
            response.append(f"  Source materials: {'Provided' if source_materials else 'Not provided'}")
            response.append(f"  Validation ID: {result.id}")
            
            return "\\n".join(response)
        
        except Exception as e:
            return f"Error during validation: {e}"

class ValidateRealTimeTool(BaseTool):
    """Tool for real-time content validation"""
    name: str = "validate_realtime"
    description: str = "Perform real-time validation on content being written. Use this to catch critical issues early in the writing process."
    args_schema: type[BaseModel] = ValidateRealTimeInput
    
    def __init__(self, validation_engine: ValidationEngine, agent_role: str):
        super().__init__()
        self.validation_engine = validation_engine
        self.agent_role = agent_role
    
    def _run(self, partial_content: str, context: Dict[str, Any] = None) -> str:
        """Run real-time validation on partial content"""
        try:
            issues = self.validation_engine.validate_real_time(
                partial_content=partial_content,
                context=context or {}
            )
            
            if not issues:
                return "✅ No critical issues detected in current content"
            
            response = [f"⚠️ REAL-TIME VALIDATION ALERTS ({len(issues)})"]
            
            for issue in issues:
                response.append(f"\\n• {issue.severity.value.upper()}: {issue.message}")
                response.append(f"  {issue.description}")
                if issue.suggestions:
                    response.append(f"  💡 {issue.suggestions[0]}")
            
            return "\\n".join(response)
        
        except Exception as e:
            return f"Error during real-time validation: {e}"

class GetValidationResultTool(BaseTool):
    """Tool for retrieving validation results"""
    name: str = "get_validation_result"
    description: str = "Retrieve detailed validation results by ID. Use this to get full details about a previous validation."
    args_schema: type[BaseModel] = GetValidationResultInput
    
    def __init__(self, validation_engine: ValidationEngine, agent_role: str):
        super().__init__()
        self.validation_engine = validation_engine
        self.agent_role = agent_role
    
    def _run(self, result_id: str) -> str:
        """Get detailed validation result"""
        try:
            result = self.validation_engine.get_validation_result(result_id)
            
            if not result:
                return f"Validation result '{result_id}' not found."
            
            response = [f"=== VALIDATION RESULT DETAILS ==="]
            response.append(f"ID: {result.id}")
            response.append(f"Content ID: {result.content_id}")
            response.append(f"Status: {result.overall_status.value}")
            response.append(f"Score: {result.overall_score:.1f}/100")
            response.append(f"Validated: {result.validated_at.strftime('%Y-%m-%d %H:%M')}")
            response.append(f"Validator Version: {result.validator_version}")
            
            if result.issues:
                response.append(f"\\n**Issues ({len(result.issues)}):**")
                
                # Group by validation type
                issues_by_type = {}
                for issue in result.issues:
                    vt = issue.validation_type.value
                    if vt not in issues_by_type:
                        issues_by_type[vt] = []
                    issues_by_type[vt].append(issue)
                
                for validation_type, issues in issues_by_type.items():
                    response.append(f"\\n**{validation_type.replace('_', ' ').title()}:**")
                    for issue in issues:
                        response.append(f"  • {issue.severity.value.upper()}: {issue.message}")
                        response.append(f"    {issue.description}")
                        if issue.suggestions:
                            response.append(f"    Suggestions: {', '.join(issue.suggestions[:2])}")
            
            if result.suggestions:
                response.append(f"\\n**Overall Recommendations:**")
                for suggestion in result.suggestions:
                    response.append(f"  • {suggestion}")
            
            return "\\n".join(response)
        
        except Exception as e:
            return f"Error retrieving validation result: {e}"

class GetValidationHistoryTool(BaseTool):
    """Tool for getting validation history"""
    name: str = "get_validation_history"
    description: str = "Get validation history for specific content. Use this to track validation improvements over time."
    args_schema: type[BaseModel] = GetValidationHistoryInput
    
    def __init__(self, validation_engine: ValidationEngine, agent_role: str):
        super().__init__()
        self.validation_engine = validation_engine
        self.agent_role = agent_role
    
    def _run(self, content_id: str) -> str:
        """Get validation history for content"""
        try:
            history = self.validation_engine.get_content_validation_history(content_id)
            
            if not history:
                return f"No validation history found for content '{content_id}'"
            
            # Sort by date
            history.sort(key=lambda x: x.validated_at, reverse=True)
            
            response = [f"=== VALIDATION HISTORY FOR {content_id} ==="]
            response.append(f"Total validations: {len(history)}")
            
            for i, result in enumerate(history, 1):
                response.append(f"\\n**Validation {i}:**")
                response.append(f"  ID: {result.id}")
                response.append(f"  Date: {result.validated_at.strftime('%Y-%m-%d %H:%M')}")
                response.append(f"  Status: {result.overall_status.value}")
                response.append(f"  Score: {result.overall_score:.1f}/100")
                response.append(f"  Issues: {len(result.issues)}")
                
                if result.issues:
                    critical = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.CRITICAL)
                    high = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.HIGH)
                    medium = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.MEDIUM)
                    low = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.LOW)
                    
                    issue_summary = []
                    if critical: issue_summary.append(f"{critical} critical")
                    if high: issue_summary.append(f"{high} high")
                    if medium: issue_summary.append(f"{medium} medium")
                    if low: issue_summary.append(f"{low} low")
                    
                    response.append(f"    ({', '.join(issue_summary)})")
            
            # Show improvement trend
            if len(history) > 1:
                recent_score = history[0].overall_score
                oldest_score = history[-1].overall_score
                trend = recent_score - oldest_score
                
                response.append(f"\\n**Improvement Trend:**")
                if trend > 0:
                    response.append(f"  📈 Improved by {trend:.1f} points")
                elif trend < 0:
                    response.append(f"  📉 Decreased by {abs(trend):.1f} points")
                else:
                    response.append(f"  📊 No change in score")
            
            return "\\n".join(response)
        
        except Exception as e:
            return f"Error retrieving validation history: {e}"

class ValidationStatsTool(BaseTool):
    """Tool for getting validation statistics"""
    name: str = "validation_stats"
    description: str = "Get validation system statistics and insights. Use this to understand validation patterns and system health."
    args_schema: type[BaseModel] = BaseModel
    
    def __init__(self, validation_engine: ValidationEngine, agent_role: str):
        super().__init__()
        self.validation_engine = validation_engine
        self.agent_role = agent_role
    
    def _run(self) -> str:
        """Get validation statistics"""
        try:
            stats = self.validation_engine.get_validation_stats()
            
            response = [f"=== VALIDATION SYSTEM STATISTICS ==="]
            response.append(f"Total Validations: {stats['total_validations']}")
            response.append(f"Average Score: {stats['average_score']:.1f}/100")
            response.append(f"Pass Rate: {stats['pass_rate']:.1f}%")
            
            if stats['issues_by_type']:
                response.append(f"\\n**Issues by Type:**")
                for issue_type, count in stats['issues_by_type'].items():
                    response.append(f"  {issue_type.replace('_', ' ').title()}: {count}")
            
            if stats['issues_by_severity']:
                response.append(f"\\n**Issues by Severity:**")
                for severity, count in stats['issues_by_severity'].items():
                    response.append(f"  {severity.title()}: {count}")
            
            response.append(f"\\n**System Health:**")
            if stats['pass_rate'] >= 80:
                response.append("  ✅ System performing well")
            elif stats['pass_rate'] >= 60:
                response.append("  ⚠️ System needs attention")
            else:
                response.append("  🚨 System requires immediate attention")
            
            return "\\n".join(response)
        
        except Exception as e:
            return f"Error getting validation stats: {e}"

def create_validation_tools(validation_engine: ValidationEngine, agent_role: str) -> List[BaseTool]:
    """Create validation tools for an agent"""
    return [
        ValidateContentTool(validation_engine, agent_role),
        ValidateRealTimeTool(validation_engine, agent_role),
        GetValidationResultTool(validation_engine, agent_role),
        GetValidationHistoryTool(validation_engine, agent_role),
        ValidationStatsTool(validation_engine, agent_role)
    ]