# SoylentRed Crew

A specialized CrewAI-powered multi-agent system for creating on-brand Substack articles. SoylentRed serves as a production-ready coding assistant crew that can take natural language inputs and provide guidance, author code, and handle content creation workflows. The crew is designed to learn from interactions over time and improve future outputs through experience.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your API keys into the `.env` file:**
- `OPENAI_API_KEY` - Required for LLM operations
- `SERPER_API_KEY` - Required for web search functionality

**Configuration:**
- `src/soylent_red/config/agents.yaml` - Agent definitions and roles
- `src/soylent_red/config/tasks.yaml` - Task workflows and outputs  
- `src/soylent_red/crew.py` - Crew logic and tool integrations
- `src/soylent_red/main.py` - Entry point and input handling

## Integrated Tools

This crew includes the following production-ready tools:
- **SerperDevTool** - Real internet search capabilities
- **FileReadTool** - Read files and CSV data
- **FileWriterTool** - Create and write output files
- **DirectoryReadTool** - Browse directory structures
- **Brand & Content Tools** - Specialized tools for on-brand content creation

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the soylent_red Crew, assembling the agents and assigning them tasks as defined in your configuration.

The crew will execute a sequential workflow to create publication-ready Substack articles, outputting a final `final_article.md` file.

## Crew Architecture

The SoylentRed crew consists of specialized agents working in sequence:

1. **Brand Strategist** - Ensures content aligns with brand guidelines and audience preferences
2. **Content Researcher** - Performs web research and gathers supporting data using SerperDevTool
3. **Article Writer** - Creates the main content following brand guidelines and quality standards
4. **SEO Specialist** - Optimizes content for search and audience engagement
5. **Editor** - Performs final review, formatting, and quality assurance

Each agent has access to specialized tools appropriate for their role, with file operations handled through the integrated FileRead/Write tools and research conducted via SerperDevTool.

## Support

For support, questions, or feedback regarding the SoylentRed Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
