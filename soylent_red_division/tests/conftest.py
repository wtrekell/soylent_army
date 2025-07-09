"""
Test configuration and fixtures for Soylent Red Division
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

from src.soylent_red_division.memory_manager import MemoryManager, MemoryType
from src.soylent_red_division.knowledge_manager import KnowledgeManager, KnowledgeType
from src.soylent_red_division.reasoning_engine import ReasoningEngine
from src.soylent_red_division.validation_engine import ValidationEngine
from src.soylent_red_division.crew import SoylentRedDivision

@pytest.fixture
def temp_project_root():
    """Create a temporary project root for testing"""
    temp_dir = tempfile.mkdtemp()
    project_root = Path(temp_dir)
    
    # Create necessary directories
    (project_root / "knowledge").mkdir(exist_ok=True)
    (project_root / "knowledge" / "brand").mkdir(exist_ok=True)
    (project_root / "knowledge" / "examples").mkdir(exist_ok=True)
    (project_root / "knowledge" / "templates").mkdir(exist_ok=True)
    (project_root / "memory").mkdir(exist_ok=True)
    (project_root / "knowledge_cache").mkdir(exist_ok=True)
    (project_root / "reasoning_cache").mkdir(exist_ok=True)
    (project_root / "validation_cache").mkdir(exist_ok=True)
    (project_root / "output").mkdir(exist_ok=True)
    
    yield project_root
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_brand_foundation(temp_project_root):
    """Create sample brand foundation for testing"""
    brand_content = """# Brand Foundation - Syntax & Empathy

## Mission
Empowering UX designers and creative professionals to effectively integrate AI into their work through practical guidance, transparent knowledge-sharing, and ethical frameworks.

## Voice Characteristics

### The Methodical Experimenter
- Content backed by personal testing and systematic experimentation
- Always show evidence and data
- Include failure cases and iteration counts

### The Practical Educator & Translator
- Complex concepts explained through UX patterns and analogies
- Step-by-step guidance with clear examples
- Focus on actionable insights

### The Transparent Practitioner
- Shows all work including failures and iteration counts
- Documents everything with evidence-based alternatives
- Provides complete transparency in processes

### The Ethical Realist
- Ethics integrated as practical requirements, not afterthoughts
- Addresses bias detection and mitigation
- Considers user agency and control

## Core Values

### Transparency
- Document everything
- Show the work
- Provide evidence-based alternatives

### Curiosity
- Learn by doing
- Question everything
- Follow edge cases

### Continuous Evolution
- Daily practice
- Adapt from evidence
- Share while learning

### Practical Integrity
- Ethical choices
- Refuse bad design
- Actively counter bias
- Design for excluded users

## Target Personas

### Strategic Sofia
- Senior Designer (12+ years experience)
- Seeks strategic frameworks and scaling approaches
- Values comprehensive analysis and leadership guidance

### Adaptive Alex
- Mid-Level Designer (5 years experience)
- Needs practical integration and workflow optimization
- Values actionable steps and proven methods

### Curious Casey
- Junior Designer (2 years experience)
- Building foundational AI skills and understanding
- Values clear explanations and learning resources
"""
    
    brand_file = temp_project_root / "knowledge" / "brand" / "brand-foundation.md"
    brand_file.write_text(brand_content)
    
    return brand_file

@pytest.fixture
def sample_writing_example(temp_project_root):
    """Create sample writing example for testing"""
    example_content = """# Seeking Signal in AI Static

When I started testing AI writing tools six months ago, I expected to find either magic or garbage. Instead, I discovered something more interesting: a new kind of collaboration that demands we rethink how we approach content creation.

## The Methodical Reality

After 127 documented tests across 8 different AI writing tools, here's what the data actually shows:

- **Consistency**: 73% of outputs required substantial revision
- **Brand voice**: Only 23% naturally embodied our voice characteristics
- **Ethical considerations**: 89% failed to integrate ethics throughout

[AUTHOR: add specific tool comparison data]

## The Practical Translation

This isn't about replacing human creativity—it's about augmenting it. Here's the workflow that emerged from our testing:

1. **Human defines the strategic intent** (brand voice, target persona, ethical framework)
2. **AI handles the structural heavy lifting** (research synthesis, first drafts, pattern recognition)
3. **Human refines for brand authenticity** (voice alignment, experience integration, ethical weaving)

## The Transparent Process

Our failures taught us more than our successes. The three biggest mistakes we made:

1. **Assuming AI understood our brand** (it doesn't, without explicit guidance)
2. **Expecting consistent quality** (it varies dramatically based on prompt quality)
3. **Treating it like a magic wand** (it's a tool that requires skilled operation)

## The Ethical Reality

This collaboration raises questions we can't ignore:

- How do we maintain authenticity when AI generates first drafts?
- What's our responsibility to disclose AI involvement?
- How do we ensure diverse perspectives aren't filtered out?

We're building systems that address these concerns, not sidestep them.

## The Continuous Evolution

Six months of testing has taught us this is just the beginning. We're sharing our methods, data, and failures because the design community needs to figure this out together.

What we're learning today will be obsolete tomorrow. That's exactly why we need to document everything.
"""
    
    example_file = temp_project_root / "knowledge" / "examples" / "seeking-signal-in-ai-static.md"
    example_file.write_text(example_content)
    
    return example_file

@pytest.fixture
def sample_persona(temp_project_root):
    """Create sample persona for testing"""
    persona_content = """# Adaptive Alex - Mid-Level UX Designer

## Background
- **Experience**: 5 years in UX design
- **Current Role**: UX Designer at mid-size tech company
- **Education**: HCI or Design degree
- **Team**: Works in cross-functional product teams

## Goals & Motivations
- Integrate AI tools into existing workflows efficiently
- Improve design process speed without sacrificing quality
- Stay current with AI developments relevant to UX
- Build reputation as someone who "gets" AI in design

## Pain Points
- Overwhelmed by AI tool options and hype
- Uncertain about which tools provide real value
- Struggling to convince stakeholders of AI tool ROI
- Worried about AI replacing human creativity

## Preferred Content Style
- Practical, step-by-step implementation guides
- Real workflow examples and case studies
- Tool comparisons with clear pros/cons
- Honest assessment of AI limitations

## Success Metrics
- Can successfully integrate 2-3 AI tools into daily workflow
- Reduces routine task time by 30% within 6 months
- Feels confident explaining AI benefits to team/stakeholders
- Maintains design quality while increasing output
"""
    
    persona_file = temp_project_root / "knowledge" / "brand" / "alex_rodriguez.md"
    persona_file.write_text(persona_content)
    
    return persona_file

@pytest.fixture
def sample_template(temp_project_root):
    """Create sample template for testing"""
    template_content = """# Article Template - Core Body Guide

## Structure Requirements

### Introduction (Hook + Context)
- **Hook**: Compelling opening that demonstrates relevance
- **Context**: Why this matters now for target personas
- **Promise**: What specific value readers will get

### Main Body (Problem + Solution + Evidence)
- **Problem Definition**: Clear problem statement with evidence
- **Solution Framework**: Step-by-step approach or methodology
- **Evidence**: Data, examples, or case studies supporting the solution
- **Ethical Considerations**: Woven throughout, not tacked on

### Conclusion (Summary + Next Steps)
- **Key Takeaways**: 3-5 main points to remember
- **Next Steps**: Specific actions readers can take
- **Evolution Note**: How this guidance may change over time

## Voice Requirements
- Embody all four voice characteristics
- Include [AUTHOR: add personal example] for experience claims
- Show transparent process and methodology
- Integrate ethical considerations throughout

## Brand Compliance
- Serve appropriate target personas
- Follow brand values (Transparency, Curiosity, Evolution, Integrity)
- Avoid prohibited language (hype, buzzwords, AI mysticism)
- Maintain practical, evidence-based approach
"""
    
    template_file = temp_project_root / "knowledge" / "templates" / "article_template.yaml"
    template_file.write_text(template_content)
    
    return template_file

@pytest.fixture
def memory_manager(temp_project_root):
    """Create memory manager for testing"""
    return MemoryManager(temp_project_root)

@pytest.fixture
def knowledge_manager(temp_project_root, sample_brand_foundation, sample_writing_example, sample_persona, sample_template):
    """Create knowledge manager for testing"""
    km = KnowledgeManager(temp_project_root)
    km.refresh_knowledge()  # Load sample knowledge
    return km

@pytest.fixture
def reasoning_engine(temp_project_root):
    """Create reasoning engine for testing"""
    return ReasoningEngine(temp_project_root)

@pytest.fixture
def validation_engine(temp_project_root):
    """Create validation engine for testing"""
    return ValidationEngine(temp_project_root)

@pytest.fixture
def sample_content():
    """Sample content for testing validation"""
    return """# AI in UX Design: A Practical Guide

After testing 15 AI tools over 6 months, I've learned that successful AI integration requires methodical experimentation and transparent documentation.

## The Methodical Approach

Here's the systematic process I developed:

1. **Define Success Metrics**: What specific outcomes do you want?
2. **Test Systematically**: Document every iteration and result
3. **Measure Real Impact**: Track time savings, quality improvements
4. **Share Transparently**: Include failures and lessons learned

## Practical Implementation

Based on my testing, here's what actually works:

- **Start small**: Begin with one tool, one workflow
- **Document everything**: Track what works and what doesn't
- **Include ethics from day one**: Don't add ethics as an afterthought
- **Design for excluded users**: Consider accessibility and inclusion

## The Ethical Reality

We must address these concerns directly:

- **Bias detection**: AI tools can perpetuate existing biases
- **User agency**: People should control AI involvement in their experience
- **Transparency**: We need clear disclosure of AI usage
- **Accessibility**: AI tools must work for everyone

## Evidence-Based Results

From my 6-month study:
- 73% reduction in initial research time
- 45% improvement in ideation speed
- 12% increase in design quality scores
- 89% of stakeholders supported continued AI integration

[AUTHOR: add specific tool comparison data]

## Continuous Evolution

This field changes daily. What works today may not work tomorrow. That's why we document everything and share our methods openly.

The goal isn't to replace human creativity—it's to augment it responsibly.
"""

@pytest.fixture
def sample_invalid_content():
    """Sample content with validation issues for testing"""
    return """# Revolutionary AI Will Transform UX Design Forever!

This amazing, game-changing technology is absolutely incredible and will disrupt everything we know about design!

I think AI is magical and can solve any problem. In my experience working with AI for years, I've seen it perform miracles that defy explanation.

My team has used AI to completely revolutionize our workflow and achieve unprecedented results.

The AI understands everything and can think creatively like humans. It's truly sentient and knows exactly what users want.

Don't worry about ethics or bias - AI is perfect and will handle everything automatically.

This is the best practice for leveraging AI synergies to optimize your design ROI through disruptive innovation.

Finally, here are some ethical considerations to think about...
"""

@pytest.fixture
def sample_task_context():
    """Sample task context for testing"""
    return {
        'title': 'AI Integration Guide',
        'context': 'Creating practical guide for UX designers',
        'target_personas': ['Adaptive Alex', 'Curious Casey'],
        'requirements': 'Step-by-step implementation guide with real examples',
        'format': 'markdown'
    }

@pytest.fixture
def mock_llm_responses():
    """Mock LLM responses for testing"""
    return {
        'content_creation': "This is a sample AI-generated content response for testing purposes.",
        'brand_validation': "Content appears to meet brand guidelines based on analysis.",
        'revision': "Here is a revised version of the content with improvements."
    }

# Test data fixtures
@pytest.fixture
def sample_memory_entries():
    """Sample memory entries for testing"""
    return [
        {
            'content': 'Successfully integrated AI tool X into workflow',
            'tags': ['ai-integration', 'workflow', 'success'],
            'importance': 8,
            'metadata': {'tool': 'AI Tool X', 'result': 'positive'}
        },
        {
            'content': 'Brand voice validation failed on first attempt',
            'tags': ['brand-validation', 'failure', 'learning'],
            'importance': 7,
            'metadata': {'issue': 'voice_alignment', 'resolution': 'added_examples'}
        },
        {
            'content': 'Persona targeting improved user engagement by 34%',
            'tags': ['persona-targeting', 'metrics', 'success'],
            'importance': 9,
            'metadata': {'persona': 'Adaptive Alex', 'improvement': '34%'}
        }
    ]

@pytest.fixture
def sample_knowledge_items():
    """Sample knowledge items for testing"""
    return [
        {
            'title': 'Brand Foundation',
            'knowledge_type': KnowledgeType.BRAND_FOUNDATION,
            'content': 'Core brand guidelines and voice characteristics...',
            'tags': ['brand', 'foundation', 'voice'],
            'metadata': {'version': '1.0', 'mandatory': True}
        },
        {
            'title': 'Writing Example - AI Guide',
            'knowledge_type': KnowledgeType.WRITING_EXAMPLES,
            'content': 'Sample writing that demonstrates brand voice...',
            'tags': ['writing', 'example', 'ai'],
            'metadata': {'quality_score': 9.2, 'persona': 'Adaptive Alex'}
        }
    ]

@pytest.fixture
def sample_validation_issues():
    """Sample validation issues for testing"""
    return [
        {
            'type': 'brand_voice',
            'severity': 'high',
            'message': 'Missing methodical experimenter patterns',
            'location': {'section': 'methodology'},
            'suggestions': ['Add data and testing evidence', 'Include failure cases']
        },
        {
            'type': 'authenticity',
            'severity': 'critical',
            'message': 'Unsupported personal experience claim',
            'location': {'line': 15, 'text': 'In my experience...'},
            'suggestions': ['Add [AUTHOR: add personal example]', 'Provide source material']
        }
    ]

class MockLLMManager:
    """Mock LLM manager for testing"""
    
    def __init__(self):
        self.responses = {}
    
    def get_llm_for_role(self, role, task_config=None):
        return MockLLM()
    
    def set_response(self, key, response):
        self.responses[key] = response

class MockLLM:
    """Mock LLM for testing"""
    
    def __init__(self):
        self.model = "mock-model"
        self.temperature = 0.1
    
    def invoke(self, prompt):
        return "Mock LLM response for testing"

@pytest.fixture
def mock_llm_manager():
    """Mock LLM manager for testing"""
    return MockLLMManager()

# Test configuration
pytest_plugins = []