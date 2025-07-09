from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import sys
import os
from pathlib import Path
import glob
from .llm_manager import LLMManager
from .memory_manager import MemoryManager, MemoryType
from .knowledge_manager import KnowledgeManager
from .knowledge_memory_integration import KnowledgeMemoryIntegration
from .reasoning_engine import ReasoningEngine
from .reasoning_integration import ReasoningIntegration
from .validation_engine import ValidationEngine
from .tools.memory_tools import create_memory_tools
from .tools.knowledge_tools import create_knowledge_tools
from .tools.planning_tools import create_planning_tools
from .tools.validation_tools import create_validation_tools

# Import all default tools from parent soylent_army directory
try:
    # Calculate path to parent soylent_army directory
    soylent_army_root = Path(__file__).parent.parent.parent.parent
    if (soylent_army_root / "tools").exists():
        sys.path.insert(0, str(soylent_army_root))
        from tools.serper_dev_tool.serper_dev_tool import SerperDevTool
        from tools.file_read_tool.file_read_tool import FileReadTool
        from tools.file_writer_tool.file_writer_tool import FileWriterTool
        from tools.directory_read_tool.directory_read_tool import DirectoryReadTool
        from tools.csv_search_tool.csv_search_tool import CSVSearchTool
        from tools.pdf_search_tool.pdf_search_tool import PDFSearchTool
    else:
        # Tools directory not found
        SerperDevTool = None
        FileReadTool = None
        FileWriterTool = None
        DirectoryReadTool = None
        CSVSearchTool = None
        PDFSearchTool = None
except ImportError as e:
    print(f"Warning: Could not import external tools: {e}")
    # Fall back to None if tools unavailable
    SerperDevTool = None
    FileReadTool = None
    FileWriterTool = None
    DirectoryReadTool = None
    CSVSearchTool = None
    PDFSearchTool = None

@CrewBase
class SoylentRedDivision():
    """SoylentRedDivision Writer Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Get project root path - crew.py is in src/soylent_red_division/, so go up 2 levels to project root
        self.project_root = Path(__file__).parent.parent.parent
        
        # Initialize LLM Manager for centralized LLM configuration and failover
        self.llm_manager = LLMManager()
        
        # Initialize Memory Manager for comprehensive memory system
        self.memory_manager = MemoryManager(self.project_root)
        
        # Initialize Knowledge Manager for comprehensive knowledge system
        self.knowledge_manager = KnowledgeManager(self.project_root)
        
        # Initialize Knowledge-Memory Integration for enhanced learning
        self.km_integration = KnowledgeMemoryIntegration(self.knowledge_manager, self.memory_manager)
        
        # Initialize Reasoning Engine for planning and decision making
        self.reasoning_engine = ReasoningEngine(self.project_root)
        
        # Initialize Reasoning Integration for context-aware planning
        self.reasoning_integration = ReasoningIntegration(
            self.reasoning_engine, 
            self.memory_manager, 
            self.knowledge_manager
        )
        
        # Initialize Validation Engine for brand compliance and quality assurance
        self.validation_engine = ValidationEngine(self.project_root)
        
        # Ensure we're in the correct project root (should contain pyproject.toml)
        if not (self.project_root / "pyproject.toml").exists():
            # Fallback to current working directory if path resolution fails
            self.project_root = Path.cwd()
            
        self.knowledge_path = self.project_root / "knowledge"
        
        # LOAD BRAND KNOWLEDGE AS LAW - This is mandatory for all agents
        # Using the new Knowledge Manager for dynamic brand knowledge loading
        self.brand_knowledge = self.knowledge_manager.get_brand_context('brand_author', 'full')
        
        # Initialize all available default tools
        self.available_tools = []
        
        if SerperDevTool:
            self.serper_tool = SerperDevTool()
            self.available_tools.append(self.serper_tool)
        else:
            self.serper_tool = None
            
        if FileReadTool:
            self.file_read_tool = FileReadTool()
            self.available_tools.append(self.file_read_tool)
        else:
            self.file_read_tool = None
            
        if FileWriterTool:
            self.file_write_tool = FileWriterTool()
            self.available_tools.append(self.file_write_tool)
        else:
            self.file_write_tool = None
            
        if DirectoryReadTool:
            self.directory_read_tool = DirectoryReadTool()
            self.available_tools.append(self.directory_read_tool)
        else:
            self.directory_read_tool = None
            
        if CSVSearchTool:
            self.csv_search_tool = CSVSearchTool()
            self.available_tools.append(self.csv_search_tool)
        else:
            self.csv_search_tool = None
            
        if PDFSearchTool:
            self.pdf_search_tool = PDFSearchTool()
            self.available_tools.append(self.pdf_search_tool)
        else:
            self.pdf_search_tool = None

    def refresh_brand_knowledge(self):
        """Refresh brand knowledge from the Knowledge Manager"""
        self.brand_knowledge = self.knowledge_manager.get_brand_context('brand_author', 'full')

    @agent
    def writer(self) -> Agent:
        """Writer agent with access to all available tools and MANDATORY brand knowledge"""
        # Get base agent config
        agent_config = self.agents_config['writer'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO AGENT CONTEXT
        agent_config['backstory'] = f"{agent_config.get('backstory', '')}\n\n{self.brand_knowledge}"
        
        # Get role-specific LLM with failover (Claude 4 Sonnet primary, Gemini 2.5 Pro backup)
        writer_llm = self.llm_manager.get_llm_for_role('writer')
        
        # Create memory, knowledge, planning, and validation tools for this agent
        memory_tools = create_memory_tools(self.memory_manager, 'writer')
        knowledge_tools = create_knowledge_tools(self.knowledge_manager, 'writer')
        planning_tools = create_planning_tools(self.reasoning_engine, 'writer')
        validation_tools = create_validation_tools(self.validation_engine, 'writer')
        
        return Agent(
            config=agent_config,
            tools=self.available_tools + memory_tools + knowledge_tools + planning_tools + validation_tools,
            llm=writer_llm,
            verbose=True
        )

    @agent
    def brand_author(self) -> Agent:
        """Brand author agent for collaborative drafting and revision with MANDATORY brand knowledge"""
        # Get base agent config
        agent_config = self.agents_config['brand_author'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO AGENT CONTEXT
        agent_config['backstory'] = f"{agent_config.get('backstory', '')}\n\n{self.brand_knowledge}"
        
        # Get role-specific LLM with failover (Claude 4 Sonnet primary for creative collaboration)
        brand_author_llm = self.llm_manager.get_llm_for_role('writer')  # Use same high-quality LLM as writer
        
        # Create memory, knowledge, planning, and validation tools for this agent (brand_author has full admin access)
        memory_tools = create_memory_tools(self.memory_manager, 'brand_author')
        knowledge_tools = create_knowledge_tools(self.knowledge_manager, 'brand_author')
        planning_tools = create_planning_tools(self.reasoning_engine, 'brand_author')
        validation_tools = create_validation_tools(self.validation_engine, 'brand_author')
        
        return Agent(
            config=agent_config,
            tools=self.available_tools + memory_tools + knowledge_tools + planning_tools + validation_tools,
            llm=brand_author_llm,
            verbose=True
        )

    @task
    def writing_task(self) -> Task:
        """Main writing task with MANDATORY brand knowledge injection and LLM override support"""
        # Dynamic output file path
        output_dir = self.project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "written_content.md"
        
        # Get base task config
        task_config = self.tasks_config['writing_task'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO TASK CONTEXT
        task_config['description'] = f"{self.brand_knowledge}\n\n{task_config.get('description', '')}"
        
        # Check for task-level LLM override
        task_llm_config = task_config.get('llm')
        if task_llm_config:
            # Task specifies its own LLM - get it with failover support
            task_llm = self.llm_manager.get_llm_for_role('writer', task_llm_config)
            # Remove llm config from task config since we handle it separately
            task_config_clean = {k: v for k, v in task_config.items() if k != 'llm'}
            return Task(
                config=task_config_clean,
                output_file=str(output_file),
                llm=task_llm  # Task-specific LLM takes precedence
            )
        else:
            # Use role-based LLM (already configured in agent)
            return Task(
                config=task_config,
                output_file=str(output_file)
            )

    @task
    def initial_draft_task(self) -> Task:
        """Initial draft creation task for brand_author collaborative process"""
        # Get base task config
        task_config = self.tasks_config['initial_draft_task'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO TASK CONTEXT
        task_config['description'] = f"{self.brand_knowledge}\n\n{task_config.get('description', '')}"
        
        # Check for task-level LLM override
        task_llm_config = task_config.get('llm')
        if task_llm_config:
            task_llm = self.llm_manager.get_llm_for_role('writer', task_llm_config)
            task_config_clean = {k: v for k, v in task_config.items() if k != 'llm'}
            return Task(
                config=task_config_clean,
                llm=task_llm
            )
        else:
            return Task(
                config=task_config
            )

    @task
    def feedback_revision_task(self) -> Task:
        """Feedback and revision task for iterative collaboration"""
        # Get base task config
        task_config = self.tasks_config['feedback_revision_task'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO TASK CONTEXT
        task_config['description'] = f"{self.brand_knowledge}\n\n{task_config.get('description', '')}"
        
        # Check for task-level LLM override
        task_llm_config = task_config.get('llm')
        if task_llm_config:
            task_llm = self.llm_manager.get_llm_for_role('writer', task_llm_config)
            task_config_clean = {k: v for k, v in task_config.items() if k != 'llm'}
            return Task(
                config=task_config_clean,
                llm=task_llm
            )
        else:
            return Task(
                config=task_config
            )

    @task
    def author_signoff_task(self) -> Task:
        """Author sign-off task for completing collaborative process"""
        # Get base task config
        task_config = self.tasks_config['author_signoff_task'].copy()
        
        # INJECT BRAND KNOWLEDGE AS LAW INTO TASK CONTEXT
        task_config['description'] = f"{self.brand_knowledge}\n\n{task_config.get('description', '')}"
        
        # Check for task-level LLM override
        task_llm_config = task_config.get('llm')
        if task_llm_config:
            task_llm = self.llm_manager.get_llm_for_role('writer', task_llm_config)
            task_config_clean = {k: v for k, v in task_config.items() if k != 'llm'}
            return Task(
                config=task_config_clean,
                llm=task_llm
            )
        else:
            return Task(
                config=task_config
            )

    @crew
    def crew(self) -> Crew:
        """Creates the SoylentRedDivision Writer Crew (default single-agent workflow)"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False  # Disable built-in memory to avoid conflicts
        )

    def brand_author_crew(self) -> Crew:
        """Creates a brand_author collaborative crew for iterative drafting"""
        return Crew(
            agents=[self.brand_author()],
            tasks=[self.initial_draft_task()],
            process=Process.sequential,
            verbose=True,
            memory=False
        )

    def feedback_crew(self, feedback_input: str = "", draft_path: str = "", revision_history: str = "") -> Crew:
        """Creates a feedback/revision crew for iterating on drafts"""
        # Create dynamic task with feedback context
        task = self.feedback_revision_task()
        
        # Inject feedback context into task description
        task_description = task.description
        if feedback_input:
            task_description = f"AUTHOR FEEDBACK: {feedback_input}\n\n{task_description}"
        if draft_path:
            task_description = f"CURRENT DRAFT PATH: {draft_path}\n\n{task_description}"
        if revision_history:
            task_description = f"REVISION HISTORY: {revision_history}\n\n{task_description}"
        
        task.description = task_description
        
        return Crew(
            agents=[self.brand_author()],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )

    def signoff_crew(self, final_draft_path: str = "", signoff_confirmation: str = "") -> Crew:
        """Creates a sign-off crew for finalizing the collaborative process"""
        # Create dynamic task with sign-off context
        task = self.author_signoff_task()
        
        # Inject sign-off context into task description
        task_description = task.description
        if final_draft_path:
            task_description = f"FINAL DRAFT PATH: {final_draft_path}\n\n{task_description}"
        if signoff_confirmation:
            task_description = f"AUTHOR SIGN-OFF CONFIRMATION: {signoff_confirmation}\n\n{task_description}"
        
        task.description = task_description
        
        return Crew(
            agents=[self.brand_author()],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )