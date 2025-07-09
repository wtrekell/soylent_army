# Claude Guidance for Soylent Red Division

**IMPORTANT**: This file contains lasting instructions and guidance for working with the Soylent Red Division crew. Any Claude session working on this project MUST read and follow these instructions.

## Core Operating Principles

### 1. Step-by-Step Approach (CRITICAL)
- **ALWAYS explain at high level what you plan to do BEFORE doing it**
- Wait for user approval/feedback before executing
- This prevents cascading issues that have occurred in previous attempts
- Never surprise the user with actions taken without explanation

### 2. Brand Knowledge as LAW
- All brand information in `knowledge/` folder is **LAW** - non-negotiable
- Every agent MUST review brand knowledge before performing any task
- Brand compliance is mandatory and enforced at multiple levels:
  - Agent-level: Brand knowledge injected into agent backstory
  - Task-level: Brand knowledge injected into task descriptions
  - System-level: Automatic brand knowledge loading and validation
- **NO exceptions** to brand compliance

### 3. LLM Configuration Requirements
- All agents use role-based LLM assignment with automatic failover
- Writer role: Claude 4 Sonnet (primary) → Gemini 2.5 Pro (backup) → GPT-4o Mini (tertiary)
- Tasks can override role-based LLM configuration when needed
- Central configuration in `config/llm_config.yaml` - environment agnostic
- Failover mechanism handles API failures automatically

### 4. Documentation Standards
- Root README MUST always reflect current state - update after every change
- Documentation must be comprehensive and current
- No feature or change should be undocumented
- Include usage examples, configuration details, and troubleshooting

## Project Structure Requirements

### Mandatory Files and Locations
```
soylent_red_division/
├── CLAUDE_GUIDANCE.md           # THIS FILE - guidance for Claude sessions
├── README.md                    # Always current, comprehensive documentation
├── src/soylent_red_division/
│   ├── crew.py                  # Main crew with brand & LLM integration
│   ├── main.py                  # Entry point with flexible input
│   ├── llm_manager.py           # LLM configuration and failover system
│   └── config/
│       ├── agents.yaml          # Brand-enforced agent configs
│       ├── tasks.yaml           # Brand-validated task definitions
│       └── llm_config.yaml      # Central LLM configuration
├── knowledge/                   # Brand knowledge base (LAW)
│   ├── brand/                   # Brand foundation and personas
│   ├── examples/                # Writing style examples
│   └── templates/               # Article templates
└── output/                      # Generated content
```

### Brand Knowledge Organization
- `knowledge/brand/brand-foundation.md` - Core brand definition (LAW)
- `knowledge/brand/*.md` - Target personas (Strategic Sofia, Adaptive Alex, etc.)
- `knowledge/examples/*.md` - Writing style examples for voice consistency
- `knowledge/templates/article_template.yaml` - Content structure templates

## Technical Implementation Standards

### Brand Enforcement System
1. **Multi-Level Enforcement**:
   - System loads all brand knowledge on crew initialization
   - Agent backstories include complete brand context
   - Task descriptions include brand knowledge and validation requirements
   - Brand violation is "UNACCEPTABLE" and must be corrected

2. **Voice Characteristics** (must be embodied):
   - The Methodical Experimenter
   - The Practical Educator & Translator
   - The Transparent Practitioner
   - The Ethical Realist

3. **Authenticity Protection**:
   - Never fabricate personal experiences
   - Use `[AUTHOR: add personal example]` annotations
   - Only use supplied materials and documented examples

### Brand Author Collaborative Process
1. **Three-Phase Workflow**:
   - **Initial Draft**: AI creates first draft from materials folder
   - **Feedback Iteration**: Conversational feedback and revision cycles
   - **Author Sign-Off**: Explicit approval before personal editing

2. **Collaborative Requirements**:
   - Drafts saved in source materials folder as `DRAFT_[filename].md`
   - Feedback through chat interaction, not structured lists
   - Revision tracking with timestamps and change summaries
   - Brand compliance maintained throughout all iterations

3. **Agent Specialization**:
   - **brand_author** agent handles collaborative process
   - Same LLM configuration as writer (Claude 4 Sonnet primary)
   - Brand knowledge injected at both agent and task levels
   - Expertise in interpreting conversational feedback

### LLM Management System
1. **Priority Hierarchy**:
   - Task-level LLM definition (highest)
   - Role-based LLM definition (standard)
   - Crew-level default LLM (emergency fallback)

2. **Failover Requirements**:
   - Automatic health checks before execution
   - Seamless switching between primary/backup/tertiary
   - Comprehensive error handling and logging
   - Support for connection errors, timeouts, rate limits

3. **Configuration Standards**:
   - Central `llm_config.yaml` for all LLM definitions
   - Environment-agnostic (use environment variables for keys)
   - Role-specific optimization
   - Clear documentation of override capabilities

## Development Workflow Standards

### When Making Changes
1. **Explain the plan** at high level before implementation
2. **Update components** in logical order:
   - Core functionality first
   - Configuration files second
   - Documentation last
3. **Test integration** between components
4. **Update README** to reflect all changes made
5. **Maintain todo lists** to track progress transparently

### File Modification Protocol
1. **Read existing files** before making changes
2. **Understand current patterns** and maintain consistency
3. **Follow established conventions** for naming, structure, and style
4. **Preserve existing functionality** while adding new features
5. **Test configuration validity** after changes

### Error Prevention
- **Never assume** file locations or structures
- **Always verify** paths and dependencies before referencing
- **Check imports** and module relationships
- **Validate YAML syntax** in configuration files
- **Test failover scenarios** for LLM configurations

## Content Creation Standards

### Brand Compliance Requirements
- All content must embody the four voice characteristics
- Target appropriate personas based on content type
- Include ethical considerations as design requirements
- Demonstrate transparency through documented processes
- Provide actionable, evidence-based recommendations
- Never fabricate personal experiences or testing results

### Quality Standards
- Publication-ready output (no brand revisions needed)
- Template-based structure when applicable
- Professional tone with conversational warmth
- Clear, actionable takeaways
- Proper markdown formatting

## Communication Standards

### With User
- **Be concise and direct** - avoid unnecessary preamble/postamble
- **Answer the specific question** asked
- **Minimize output tokens** while maintaining quality
- **Ask for clarification** when requirements are unclear
- **Provide options** when multiple approaches are possible

### In Documentation
- **Use clear headings** and structured organization
- **Include practical examples** for all features
- **Provide troubleshooting guidance** for common issues
- **Maintain consistent terminology** throughout
- **Update version information** when making changes

## Important Context

### Project History
- This is the 4th attempt at creating this crew
- Previous attempts had cascading issues due to lack of step-by-step approach
- User expects explanation before action to prevent problems
- Brand enforcement and LLM management are critical requirements

### User Expectations
- **Quality over speed** - take time to do it right
- **Transparency in process** - explain what you're doing and why
- **Comprehensive documentation** - everything must be documented
- **Production-ready output** - this is not a prototype
- **Brand fidelity** - brand knowledge is non-negotiable

### Key Success Factors
1. **Follow the step-by-step approach** religiously
2. **Treat brand knowledge as LAW** with no exceptions
3. **Maintain comprehensive documentation** at all times
4. **Implement robust failover systems** for reliability
5. **Focus on production-ready quality** not prototypes

## Emergency Procedures

### If Brand Knowledge Changes
1. Update the knowledge files
2. Reload brand context in crew initialization
3. Verify agent and task configurations still align
4. Update documentation to reflect changes
5. Test content generation for brand compliance

### If LLM Configuration Needs Updates
1. Update `config/llm_config.yaml`
2. Test failover scenarios
3. Verify agent and task LLM assignments
4. Update documentation with new configurations
5. Test end-to-end content generation

### If System Architecture Changes
1. Update file structure as needed
2. Maintain backward compatibility where possible
3. Update import statements and paths
4. Test all integration points
5. Update README and architecture documentation

---

## Instructions for Future Claude Sessions

1. **READ THIS FILE FIRST** before making any changes
2. **Understand the brand enforcement system** and its requirements
3. **Follow the step-by-step approach** - explain before implementing
4. **Maintain documentation standards** - update README after changes
5. **Respect the LLM configuration system** and failover requirements
6. **Ask questions** if any guidance is unclear
7. **Preserve production-ready quality** in all work

**Remember**: This is a production system with specific requirements. Quality, brand fidelity, and comprehensive documentation are non-negotiable.