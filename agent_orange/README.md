# Agent Orange - Cloudscape Design System Analysis

Agent Orange is a specialized CrewAI project designed to help the original creator of the Cloudscape Design System reconnect with and analyze the evolved state of their design system. This crew extracts, analyzes, and creates comprehensive reference materials for reskinning and extending the Cloudscape Design System.

## Purpose

As the original designer of Cloudscape from over a decade ago, this tool helps you:
- Extract actual CSS/SCSS source files from the current GitHub repositories
- Analyze how your design system has evolved over time
- Identify reusable design patterns and tokens
- Create browsable reference documentation
- Develop strategies for reskinning and creating new component variations

## What Agent Orange Does

The crew consists of 4 specialized agents working in sequence:

1. **Design System Analyst** - Extracts CSS/SCSS source files from GitHub repos
2. **CSS Pattern Expert** - Analyzes styling patterns, variables, and architecture  
3. **Visual Reference Creator** - Builds comprehensive, browsable documentation
4. **Reskinning Strategist** - Develops practical strategies for customization

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system.

```bash
# Install dependencies
crewai install
```

**Add your `OPENAI_API_KEY` into the `.env` file**

## Running the Analysis

To start the complete Cloudscape analysis:

```bash
crewai run
```

This will:
1. Extract source files from key Cloudscape repositories
2. Analyze CSS patterns and design tokens
3. Generate visual reference documentation  
4. Create a comprehensive reskinning strategy guide

## Output Locations

After running, check these locations:
- `raw_materials/github_sources/` - Extracted CSS/SCSS source files
- `refined_materials/visual_reference/` - Interactive component documentation
- `refined_materials/cloudscape_reskinning_strategy.md` - Strategic implementation guide

## Target Repositories

Agent Orange extracts styling from these key Cloudscape repositories:
- `cloudscape-design/components` - Main component styling
- `cloudscape-design/global-styles` - Global design tokens and themes
- `cloudscape-design/board-components` - Specialized board components  
- `cloudscape-design/chart-components` - Chart-specific styling

## Support

For support, questions, or feedback regarding the AgentOrange Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
