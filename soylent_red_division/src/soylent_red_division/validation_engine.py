"""
Validation Engine - Comprehensive brand compliance and quality validation system
Handles real-time guardrails, content validation, and brand protection
"""

import json
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import difflib

class ValidationSeverity(Enum):
    """Severity levels for validation issues"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ValidationType(Enum):
    """Types of validation checks"""
    BRAND_VOICE = "brand_voice"
    AUTHENTICITY = "authenticity"
    PERSONA_ALIGNMENT = "persona_alignment"
    ETHICAL_INTEGRATION = "ethical_integration"
    TRANSPARENCY = "transparency"
    QUALITY_STANDARDS = "quality_standards"
    TEMPLATE_COMPLIANCE = "template_compliance"
    PROHIBITED_LANGUAGE = "prohibited_language"

class ValidationStatus(Enum):
    """Status of validation results"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    REQUIRES_REVIEW = "requires_review"

@dataclass
class ValidationIssue:
    """Individual validation issue"""
    id: str
    validation_type: ValidationType
    severity: ValidationSeverity
    status: ValidationStatus
    message: str
    description: str
    location: Dict[str, Any]  # line, section, etc.
    suggestions: List[str]
    auto_fixable: bool
    detected_at: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'validation_type': self.validation_type.value,
            'severity': self.severity.value,
            'status': self.status.value,
            'message': self.message,
            'description': self.description,
            'location': self.location,
            'suggestions': self.suggestions,
            'auto_fixable': self.auto_fixable,
            'detected_at': self.detected_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationIssue':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            validation_type=ValidationType(data['validation_type']),
            severity=ValidationSeverity(data['severity']),
            status=ValidationStatus(data['status']),
            message=data['message'],
            description=data['description'],
            location=data['location'],
            suggestions=data['suggestions'],
            auto_fixable=data['auto_fixable'],
            detected_at=datetime.fromisoformat(data['detected_at']),
            metadata=data['metadata']
        )

@dataclass
class ValidationResult:
    """Complete validation result"""
    id: str
    content_id: str
    validation_types: List[ValidationType]
    overall_status: ValidationStatus
    overall_score: float  # 0-100
    issues: List[ValidationIssue]
    suggestions: List[str]
    validated_at: datetime
    validator_version: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'validation_types': [vt.value for vt in self.validation_types],
            'overall_status': self.overall_status.value,
            'overall_score': self.overall_score,
            'issues': [issue.to_dict() for issue in self.issues],
            'suggestions': self.suggestions,
            'validated_at': self.validated_at.isoformat(),
            'validator_version': self.validator_version,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationResult':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            content_id=data['content_id'],
            validation_types=[ValidationType(vt) for vt in data['validation_types']],
            overall_status=ValidationStatus(data['overall_status']),
            overall_score=data['overall_score'],
            issues=[ValidationIssue.from_dict(issue_data) for issue_data in data['issues']],
            suggestions=data['suggestions'],
            validated_at=datetime.fromisoformat(data['validated_at']),
            validator_version=data['validator_version'],
            metadata=data['metadata']
        )

class BrandVoiceValidator:
    """Validates content against brand voice characteristics"""
    
    def __init__(self):
        # Voice characteristic patterns
        self.voice_patterns = {
            'methodical_experimenter': {
                'required_patterns': [
                    r'\btested?\b', r'\bexperiment', r'\bresults?\b', r'\bdata\b',
                    r'\bmeasur', r'\bcompare', r'\btried?\b', r'\banalyz'
                ],
                'negative_patterns': [
                    r'\bI think\b', r'\bI believe\b', r'\bprobably\b', r'\bmight work\b'
                ]
            },
            'practical_educator': {
                'required_patterns': [
                    r'\bstep\b', r'\bhow to\b', r'\bexample\b', r'\bpattern\b',
                    r'\bworkflow\b', r'\bprocess\b', r'\bpractical\b'
                ],
                'negative_patterns': [
                    r'\btheoretical\b', r'\bacademic\b', r'\babstract\b'
                ]
            },
            'transparent_practitioner': {
                'required_patterns': [
                    r'\bshowing?\b', r'\bdocument', r'\btrack', r'\brecord',
                    r'\bevidence\b', r'\bproof\b', r'\bdemonstrat'
                ],
                'negative_patterns': [
                    r'\bhidden\b', r'\bsecret\b', r'\bbehind the scenes\b'
                ]
            },
            'ethical_realist': {
                'required_patterns': [
                    r'\bethic', r'\bbias\b', r'\bfair', r'\binclus', r'\baccess',
                    r'\brespons', r'\bimpact\b', r'\bconsequence'
                ],
                'negative_patterns': [
                    r'\bdon\'t worry about\b', r'\bignore\b', r'\bskip.*ethic'
                ]
            }
        }
        
        # Prohibited language patterns
        self.prohibited_patterns = {
            'hype_language': [
                r'\brevolutionary\b', r'\bgame.?chang', r'\bmagic\b', r'\bmiracle\b',
                r'\bunbelievable\b', r'\bamazing\b', r'\bincredible\b', r'\bawesome\b'
            ],
            'corporate_buzzwords': [
                r'\bsynerg', r'\bleverag', r'\boptimiz.*ROI\b', r'\bdisrupt',
                r'\bgrowth.?hack', r'\bthought.?leader', r'\bbest.?practice'
            ],
            'ai_mysticism': [
                r'\bAI.*sentient\b', r'\bAI.*conscious\b', r'\bAI.*think',
                r'\bAI.*understand', r'\bAI.*feel', r'\bAI.*want'
            ]
        }
    
    def validate_voice_characteristics(self, content: str) -> List[ValidationIssue]:
        """Validate content against voice characteristics"""
        issues = []
        content_lower = content.lower()
        
        for voice_type, patterns in self.voice_patterns.items():
            # Check for required patterns
            required_found = any(re.search(pattern, content_lower) 
                               for pattern in patterns['required_patterns'])
            
            if not required_found:
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.BRAND_VOICE,
                    severity=ValidationSeverity.HIGH,
                    status=ValidationStatus.FAILED,
                    message=f"Missing {voice_type.replace('_', ' ')} voice patterns",
                    description=f"Content should embody the {voice_type.replace('_', ' ')} voice characteristic",
                    location={'voice_type': voice_type},
                    suggestions=[
                        f"Add language that demonstrates {voice_type.replace('_', ' ')} approach",
                        "Include specific examples or evidence",
                        "Show methodical process or practical application"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'voice_type': voice_type, 'patterns_checked': patterns['required_patterns'][:3]}
                ))
            
            # Check for negative patterns
            negative_found = [pattern for pattern in patterns['negative_patterns'] 
                            if re.search(pattern, content_lower)]
            
            for pattern in negative_found:
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.BRAND_VOICE,
                    severity=ValidationSeverity.MEDIUM,
                    status=ValidationStatus.WARNING,
                    message=f"Detected anti-pattern for {voice_type.replace('_', ' ')}",
                    description=f"Found language that conflicts with {voice_type.replace('_', ' ')} voice",
                    location={'voice_type': voice_type, 'pattern': pattern},
                    suggestions=[
                        "Replace speculative language with evidence-based statements",
                        "Add concrete examples or data",
                        "Strengthen with specific results"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'voice_type': voice_type, 'detected_pattern': pattern}
                ))
        
        return issues
    
    def validate_prohibited_language(self, content: str) -> List[ValidationIssue]:
        """Validate content against prohibited language patterns"""
        issues = []
        content_lower = content.lower()
        
        for category, patterns in self.prohibited_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    issues.append(ValidationIssue(
                        id=str(uuid.uuid4()),
                        validation_type=ValidationType.PROHIBITED_LANGUAGE,
                        severity=ValidationSeverity.HIGH,
                        status=ValidationStatus.FAILED,
                        message=f"Prohibited {category.replace('_', ' ')} detected",
                        description=f"Found language that violates brand voice guidelines",
                        location={'category': category, 'position': match.span(), 'text': match.group()},
                        suggestions=[
                            "Replace with evidence-based language",
                            "Use practical, specific terms",
                            "Focus on concrete benefits"
                        ],
                        auto_fixable=True,
                        detected_at=datetime.now(),
                        metadata={'category': category, 'pattern': pattern, 'matched_text': match.group()}
                    ))
        
        return issues

class AuthenticityValidator:
    """Validates content authenticity and experience claims"""
    
    def __init__(self):
        # Patterns that indicate personal experience claims
        self.experience_patterns = [
            r'\bI\s+(tried|tested|used|found|discovered|learned|realized)\b',
            r'\bIn my experience\b', r'\bI\'ve (seen|noticed|observed)\b',
            r'\bWhen I (was|worked|did)\b', r'\bI remember\b',
            r'\bMy (team|company|project)\b', r'\bWe (implemented|tried|used)\b'
        ]
        
        # Patterns for proper annotation
        self.annotation_patterns = [
            r'\[AUTHOR:\s*add\s+personal\s+example\]',
            r'\[AUTHOR:\s*insert\s+experience\]',
            r'\[AUTHOR:\s*add\s+story\]'
        ]
    
    def validate_experience_claims(self, content: str, source_materials: str = "") -> List[ValidationIssue]:
        """Validate that personal experiences are properly annotated"""
        issues = []
        
        # Find all experience claims
        experience_matches = []
        for pattern in self.experience_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            experience_matches.extend(matches)
        
        # Check each experience claim
        for match in experience_matches:
            # Extract surrounding context
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end]
            
            # Check if this claim is supported by source materials
            if source_materials:
                # Simple similarity check - in production, use more sophisticated NLP
                claim_words = set(match.group().lower().split())
                source_words = set(source_materials.lower().split())
                overlap = len(claim_words.intersection(source_words))
                
                if overlap < 2:  # Threshold for unsupported claims
                    issues.append(ValidationIssue(
                        id=str(uuid.uuid4()),
                        validation_type=ValidationType.AUTHENTICITY,
                        severity=ValidationSeverity.CRITICAL,
                        status=ValidationStatus.FAILED,
                        message="Unsupported personal experience claim",
                        description="Found personal experience claim not supported by source materials",
                        location={'position': match.span(), 'context': context},
                        suggestions=[
                            "Add [AUTHOR: add personal example] annotation",
                            "Remove personal claim and use general statement",
                            "Provide source material supporting this experience"
                        ],
                        auto_fixable=True,
                        detected_at=datetime.now(),
                        metadata={'claim': match.group(), 'context': context}
                    ))
            else:
                # No source materials - all personal claims should be annotated
                # Check if proper annotation exists nearby
                annotation_nearby = any(re.search(ann_pattern, context, re.IGNORECASE) 
                                      for ann_pattern in self.annotation_patterns)
                
                if not annotation_nearby:
                    issues.append(ValidationIssue(
                        id=str(uuid.uuid4()),
                        validation_type=ValidationType.AUTHENTICITY,
                        severity=ValidationSeverity.CRITICAL,
                        status=ValidationStatus.FAILED,
                        message="Personal experience claim without annotation",
                        description="Personal experience claim requires [AUTHOR: add personal example] annotation",
                        location={'position': match.span(), 'context': context},
                        suggestions=[
                            "Add [AUTHOR: add personal example] annotation",
                            "Replace with general statement",
                            "Provide specific source material"
                        ],
                        auto_fixable=True,
                        detected_at=datetime.now(),
                        metadata={'claim': match.group(), 'context': context}
                    ))
        
        return issues

class PersonaAlignmentValidator:
    """Validates content alignment with target personas"""
    
    def __init__(self):
        # Persona requirements
        self.persona_requirements = {
            'Strategic Sofia': {
                'complexity': 'high',
                'focus': ['frameworks', 'strategy', 'leadership', 'scaling'],
                'language_level': 'senior',
                'content_depth': 'comprehensive'
            },
            'Adaptive Alex': {
                'complexity': 'medium',
                'focus': ['practical', 'implementation', 'workflow', 'tools'],
                'language_level': 'mid-level',
                'content_depth': 'balanced'
            },
            'Curious Casey': {
                'complexity': 'low',
                'focus': ['basics', 'learning', 'getting started', 'fundamentals'],
                'language_level': 'beginner',
                'content_depth': 'foundational'
            }
        }
        
        # Language complexity indicators
        self.complexity_indicators = {
            'high': ['strategic', 'framework', 'methodology', 'paradigm', 'architecture'],
            'medium': ['practical', 'workflow', 'process', 'integration', 'implementation'],
            'low': ['basic', 'simple', 'start', 'begin', 'learn', 'introduction']
        }
    
    def validate_persona_alignment(self, content: str, target_personas: List[str]) -> List[ValidationIssue]:
        """Validate content alignment with target personas"""
        issues = []
        
        if not target_personas:
            issues.append(ValidationIssue(
                id=str(uuid.uuid4()),
                validation_type=ValidationType.PERSONA_ALIGNMENT,
                severity=ValidationSeverity.HIGH,
                status=ValidationStatus.FAILED,
                message="No target personas specified",
                description="Content must specify target personas for proper alignment",
                location={'section': 'metadata'},
                suggestions=[
                    "Specify target personas (Strategic Sofia, Adaptive Alex, Curious Casey)",
                    "Analyze content complexity to determine appropriate personas",
                    "Review persona requirements in brand foundation"
                ],
                auto_fixable=False,
                detected_at=datetime.now(),
                metadata={'target_personas': target_personas}
            ))
            return issues
        
        content_lower = content.lower()
        
        for persona in target_personas:
            if persona not in self.persona_requirements:
                continue
                
            requirements = self.persona_requirements[persona]
            
            # Check complexity alignment
            complexity_score = self._analyze_complexity(content_lower)
            expected_complexity = requirements['complexity']
            
            if not self._complexity_matches(complexity_score, expected_complexity):
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.PERSONA_ALIGNMENT,
                    severity=ValidationSeverity.MEDIUM,
                    status=ValidationStatus.WARNING,
                    message=f"Content complexity mismatch for {persona}",
                    description=f"Content complexity doesn't match {persona}'s expected level",
                    location={'persona': persona, 'expected': expected_complexity, 'actual': complexity_score},
                    suggestions=[
                        f"Adjust content complexity for {persona}",
                        "Add appropriate examples and explanations",
                        "Review persona requirements"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'persona': persona, 'complexity_expected': expected_complexity, 'complexity_actual': complexity_score}
                ))
            
            # Check focus alignment
            focus_areas = requirements['focus']
            focus_found = any(focus in content_lower for focus in focus_areas)
            
            if not focus_found:
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.PERSONA_ALIGNMENT,
                    severity=ValidationSeverity.MEDIUM,
                    status=ValidationStatus.WARNING,
                    message=f"Missing focus areas for {persona}",
                    description=f"Content should address {persona}'s focus areas",
                    location={'persona': persona, 'focus_areas': focus_areas},
                    suggestions=[
                        f"Include content relevant to {persona}'s interests",
                        f"Address {', '.join(focus_areas[:3])} aspects",
                        "Review persona requirements and adjust content"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'persona': persona, 'focus_areas': focus_areas}
                ))
        
        return issues
    
    def _analyze_complexity(self, content: str) -> str:
        """Analyze content complexity level"""
        high_indicators = sum(1 for indicator in self.complexity_indicators['high'] if indicator in content)
        medium_indicators = sum(1 for indicator in self.complexity_indicators['medium'] if indicator in content)
        low_indicators = sum(1 for indicator in self.complexity_indicators['low'] if indicator in content)
        
        if high_indicators >= medium_indicators and high_indicators >= low_indicators:
            return 'high'
        elif medium_indicators >= low_indicators:
            return 'medium'
        else:
            return 'low'
    
    def _complexity_matches(self, actual: str, expected: str) -> bool:
        """Check if complexity levels are compatible"""
        compatibility_matrix = {
            'high': ['high', 'medium'],  # High can work for medium too
            'medium': ['medium', 'low', 'high'],  # Medium is most flexible
            'low': ['low', 'medium']  # Low can stretch to medium
        }
        return actual in compatibility_matrix.get(expected, [])

class EthicalIntegrationValidator:
    """Validates ethical considerations integration"""
    
    def __init__(self):
        self.ethical_patterns = {
            'bias_consideration': [r'\bbias\b', r'\bfair', r'\bequit', r'\bdiscriminat'],
            'inclusion_focus': [r'\binclus', r'\baccess', r'\bdiversit', r'\bequal'],
            'user_agency': [r'\buser.*control\b', r'\buser.*choice\b', r'\buser.*agency\b'],
            'transparency': [r'\btranspar', r'\bopen', r'\bclear', r'\bhonest'],
            'responsibility': [r'\bresponsib', r'\baccountab', r'\bimpact', r'\bconsequence']
        }
        
        self.afterthought_patterns = [
            r'\bAlso.*ethic', r'\bFinally.*ethic', r'\bBy the way.*ethic',
            r'\bOh.*and.*ethic', r'\bDon\'t forget.*ethic'
        ]
    
    def validate_ethical_integration(self, content: str) -> List[ValidationIssue]:
        """Validate that ethics are woven throughout, not afterthoughts"""
        issues = []
        content_lower = content.lower()
        
        # Check for ethical considerations presence
        ethical_mentions = []
        for category, patterns in self.ethical_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                ethical_mentions.extend([(category, match) for match in matches])
        
        if not ethical_mentions:
            issues.append(ValidationIssue(
                id=str(uuid.uuid4()),
                validation_type=ValidationType.ETHICAL_INTEGRATION,
                severity=ValidationSeverity.HIGH,
                status=ValidationStatus.FAILED,
                message="No ethical considerations found",
                description="Content must integrate ethical considerations throughout",
                location={'section': 'entire_content'},
                suggestions=[
                    "Add bias detection and mitigation considerations",
                    "Include accessibility and inclusion aspects",
                    "Address user agency and control",
                    "Consider potential negative impacts"
                ],
                auto_fixable=False,
                detected_at=datetime.now(),
                metadata={'ethical_categories_missing': list(self.ethical_patterns.keys())}
            ))
        
        # Check for afterthought patterns
        for pattern in self.afterthought_patterns:
            matches = list(re.finditer(pattern, content_lower))
            for match in matches:
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.ETHICAL_INTEGRATION,
                    severity=ValidationSeverity.MEDIUM,
                    status=ValidationStatus.WARNING,
                    message="Ethics appear as afterthought",
                    description="Ethical considerations should be woven throughout, not added at the end",
                    location={'position': match.span(), 'text': match.group()},
                    suggestions=[
                        "Integrate ethical considerations throughout the content",
                        "Address ethics as part of main discussion",
                        "Make ethics integral to recommendations"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'afterthought_pattern': pattern, 'matched_text': match.group()}
                ))
        
        # Check distribution of ethical mentions
        if ethical_mentions:
            content_length = len(content)
            positions = [match.start() / content_length for _, match in ethical_mentions]
            
            # Check if ethics are distributed throughout (not clustered)
            if len(set(int(pos * 3) for pos in positions)) < 2:  # Clustered in one third
                issues.append(ValidationIssue(
                    id=str(uuid.uuid4()),
                    validation_type=ValidationType.ETHICAL_INTEGRATION,
                    severity=ValidationSeverity.MEDIUM,
                    status=ValidationStatus.WARNING,
                    message="Ethical considerations clustered in one section",
                    description="Ethics should be distributed throughout the content",
                    location={'positions': positions},
                    suggestions=[
                        "Spread ethical considerations throughout all sections",
                        "Address ethics in each major recommendation",
                        "Integrate ethics into examples and case studies"
                    ],
                    auto_fixable=False,
                    detected_at=datetime.now(),
                    metadata={'positions': positions, 'distribution': 'clustered'}
                ))
        
        return issues

class ValidationEngine:
    """
    Main validation engine that coordinates all validation checks
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.validation_cache_dir = project_root / "validation_cache"
        self.validation_cache_dir.mkdir(exist_ok=True)
        
        # Storage files
        self.validation_results_file = self.validation_cache_dir / "validation_results.json"
        self.validation_log_file = self.validation_cache_dir / "validation_operations.log"
        
        # Initialize validators
        self.brand_voice_validator = BrandVoiceValidator()
        self.authenticity_validator = AuthenticityValidator()
        self.persona_alignment_validator = PersonaAlignmentValidator()
        self.ethical_integration_validator = EthicalIntegrationValidator()
        
        # Storage
        self.validation_results: Dict[str, ValidationResult] = {}
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Load existing results
        self._load_validation_results()
        
        # Version
        self.validator_version = "1.0.0"
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for validation operations"""
        logger = logging.getLogger("ValidationEngine")
        if not logger.handlers:
            handler = logging.FileHandler(self.validation_log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_validation_results(self):
        """Load validation results from storage"""
        if not self.validation_results_file.exists():
            return
        
        try:
            with open(self.validation_results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for result_data in data:
                    result = ValidationResult.from_dict(result_data)
                    self.validation_results[result.id] = result
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Error loading validation results: {e}")
    
    def _save_validation_results(self):
        """Save validation results to storage"""
        try:
            with open(self.validation_results_file, 'w', encoding='utf-8') as f:
                json.dump([result.to_dict() for result in self.validation_results.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving validation results: {e}")
    
    def validate_content(self, content: str, content_id: str = None, 
                        target_personas: List[str] = None, 
                        source_materials: str = "",
                        validation_types: List[ValidationType] = None) -> ValidationResult:
        """Comprehensive content validation"""
        
        if content_id is None:
            content_id = str(uuid.uuid4())
        
        if validation_types is None:
            validation_types = list(ValidationType)
        
        if target_personas is None:
            target_personas = []
        
        all_issues = []
        
        # Run each validation type
        if ValidationType.BRAND_VOICE in validation_types:
            all_issues.extend(self.brand_voice_validator.validate_voice_characteristics(content))
        
        if ValidationType.PROHIBITED_LANGUAGE in validation_types:
            all_issues.extend(self.brand_voice_validator.validate_prohibited_language(content))
        
        if ValidationType.AUTHENTICITY in validation_types:
            all_issues.extend(self.authenticity_validator.validate_experience_claims(content, source_materials))
        
        if ValidationType.PERSONA_ALIGNMENT in validation_types:
            all_issues.extend(self.persona_alignment_validator.validate_persona_alignment(content, target_personas))
        
        if ValidationType.ETHICAL_INTEGRATION in validation_types:
            all_issues.extend(self.ethical_integration_validator.validate_ethical_integration(content))
        
        # Calculate overall status and score
        overall_status, overall_score = self._calculate_overall_assessment(all_issues)
        
        # Generate overall suggestions
        suggestions = self._generate_overall_suggestions(all_issues)
        
        # Create validation result
        result = ValidationResult(
            id=str(uuid.uuid4()),
            content_id=content_id,
            validation_types=validation_types,
            overall_status=overall_status,
            overall_score=overall_score,
            issues=all_issues,
            suggestions=suggestions,
            validated_at=datetime.now(),
            validator_version=self.validator_version,
            metadata={
                'content_length': len(content),
                'target_personas': target_personas,
                'has_source_materials': bool(source_materials),
                'validation_types_count': len(validation_types)
            }
        )
        
        # Store result
        self.validation_results[result.id] = result
        self._save_validation_results()
        
        self.logger.info(f"Validated content {content_id} with status {overall_status.value} and score {overall_score}")
        
        return result
    
    def _calculate_overall_assessment(self, issues: List[ValidationIssue]) -> Tuple[ValidationStatus, float]:
        """Calculate overall validation status and score"""
        if not issues:
            return ValidationStatus.PASSED, 100.0
        
        # Count issues by severity
        critical_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.CRITICAL)
        high_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.HIGH)
        medium_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.MEDIUM)
        low_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.LOW)
        
        # Calculate score (start at 100, deduct points)
        score = 100.0
        score -= critical_count * 25  # Critical issues are severe
        score -= high_count * 15
        score -= medium_count * 8
        score -= low_count * 3
        
        score = max(0.0, score)
        
        # Determine status
        if critical_count > 0:
            status = ValidationStatus.FAILED
        elif high_count > 2:
            status = ValidationStatus.FAILED
        elif high_count > 0 or medium_count > 3:
            status = ValidationStatus.WARNING
        elif medium_count > 0 or low_count > 0:
            status = ValidationStatus.REQUIRES_REVIEW
        else:
            status = ValidationStatus.PASSED
        
        return status, score
    
    def _generate_overall_suggestions(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate high-level suggestions based on issues"""
        suggestions = []
        
        # Group issues by type
        issues_by_type = defaultdict(list)
        for issue in issues:
            issues_by_type[issue.validation_type].append(issue)
        
        # Generate type-specific suggestions
        if ValidationType.BRAND_VOICE in issues_by_type:
            suggestions.append("Review brand voice characteristics and ensure content embodies all four voice aspects")
        
        if ValidationType.AUTHENTICITY in issues_by_type:
            suggestions.append("Add [AUTHOR: add personal example] annotations for all personal experience claims")
        
        if ValidationType.PERSONA_ALIGNMENT in issues_by_type:
            suggestions.append("Adjust content complexity and focus to better serve target personas")
        
        if ValidationType.ETHICAL_INTEGRATION in issues_by_type:
            suggestions.append("Integrate ethical considerations throughout content, not as afterthoughts")
        
        if ValidationType.PROHIBITED_LANGUAGE in issues_by_type:
            suggestions.append("Replace prohibited language with evidence-based, practical alternatives")
        
        # Add priority suggestions based on severity
        critical_issues = [issue for issue in issues if issue.severity == ValidationSeverity.CRITICAL]
        if critical_issues:
            suggestions.insert(0, "Address critical brand compliance issues before proceeding")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def get_validation_result(self, result_id: str) -> Optional[ValidationResult]:
        """Get validation result by ID"""
        return self.validation_results.get(result_id)
    
    def get_content_validation_history(self, content_id: str) -> List[ValidationResult]:
        """Get validation history for specific content"""
        return [result for result in self.validation_results.values() 
                if result.content_id == content_id]
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation system statistics"""
        total_validations = len(self.validation_results)
        
        if total_validations == 0:
            return {
                'total_validations': 0,
                'average_score': 0,
                'pass_rate': 0,
                'issues_by_type': {},
                'issues_by_severity': {}
            }
        
        scores = [result.overall_score for result in self.validation_results.values()]
        passed_count = sum(1 for result in self.validation_results.values() 
                          if result.overall_status == ValidationStatus.PASSED)
        
        # Count issues by type and severity
        issues_by_type = defaultdict(int)
        issues_by_severity = defaultdict(int)
        
        for result in self.validation_results.values():
            for issue in result.issues:
                issues_by_type[issue.validation_type.value] += 1
                issues_by_severity[issue.severity.value] += 1
        
        return {
            'total_validations': total_validations,
            'average_score': sum(scores) / len(scores),
            'pass_rate': (passed_count / total_validations) * 100,
            'issues_by_type': dict(issues_by_type),
            'issues_by_severity': dict(issues_by_severity),
            'recent_validations': total_validations  # Could be time-filtered
        }
    
    def validate_real_time(self, partial_content: str, context: Dict[str, Any] = None) -> List[ValidationIssue]:
        """Real-time validation for content being written"""
        # Lighter validation for real-time use
        issues = []
        
        # Quick brand voice check
        issues.extend(self.brand_voice_validator.validate_prohibited_language(partial_content))
        
        # Quick authenticity check
        if context and context.get('source_materials'):
            issues.extend(self.authenticity_validator.validate_experience_claims(
                partial_content, context['source_materials']
            ))
        
        # Return only high and critical issues for real-time
        return [issue for issue in issues 
                if issue.severity in [ValidationSeverity.CRITICAL, ValidationSeverity.HIGH]]