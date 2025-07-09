from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# Import working tools
import sys
import os
from pathlib import Path

# Try to import external tools from parent soylent_army directory
try:
    # Calculate path to parent soylent_army directory
    soylent_army_root = Path(__file__).parent.parent.parent.parent
    if (soylent_army_root / "tools").exists():
        sys.path.insert(0, str(soylent_army_root))
        from tools.serper_dev_tool.serper_dev_tool import SerperDevTool
        from tools.file_read_tool.file_read_tool import FileReadTool
        from tools.file_writer_tool.file_writer_tool import FileWriterTool
        from tools.directory_read_tool.directory_read_tool import DirectoryReadTool
    else:
        # Tools directory not found
        SerperDevTool = None
        FileReadTool = None
        FileWriterTool = None
        DirectoryReadTool = None
except ImportError as e:
    print(f"Warning: Could not import external tools: {e}")
    # Fall back to None if tools unavailable
    SerperDevTool = None
    FileReadTool = None
    FileWriterTool = None
    DirectoryReadTool = None
from .tools.content_tools import (
    BrandStyleGuideTool, SEOAnalysisTool, 
    ContentQualityTool, SubstackFormatterTool, FactCheckingTool
)

@CrewBase
class SoylentRed():
    """SoylentRed Substack Article Writing Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Configure OpenAI LLM
        self.llm = LLM(model="gpt-4o-mini", temperature=0.1)
        
        # Get project root path - crew.py is in src/soylent_red/, so go up 2 levels to project root
        self.project_root = Path(__file__).parent.parent.parent
        
        # Ensure we're in the correct project root (should contain pyproject.toml)
        if not (self.project_root / "pyproject.toml").exists():
            # Fallback to current working directory if path resolution fails
            self.project_root = Path.cwd()
            
        self.knowledge_path = self.project_root / "knowledge"
        
        # Initialize tools with proper knowledge paths
        BrandStyleGuideTool.set_knowledge_path(str(self.knowledge_path))
        self.brand_tool = BrandStyleGuideTool()
        self.seo_tool = SEOAnalysisTool()
        self.quality_tool = ContentQualityTool()
        self.formatter_tool = SubstackFormatterTool()
        self.fact_checker = FactCheckingTool()
        
        # Initialize external tools if available
        if SerperDevTool:
            self.serper_tool = SerperDevTool()
        else:
            self.serper_tool = None
            
        if FileReadTool:
            self.file_read_tool = FileReadTool()
        else:
            self.file_read_tool = None
            
        if FileWriterTool:
            self.file_write_tool = FileWriterTool()
        else:
            self.file_write_tool = None
            
        if DirectoryReadTool:
            self.directory_read_tool = DirectoryReadTool()
        else:
            self.directory_read_tool = None

    @agent
    def brand_strategist(self) -> Agent:
        tools = [self.brand_tool, self.quality_tool]
        if self.directory_read_tool:
            tools.append(self.directory_read_tool)
        return Agent(
            config=self.agents_config['brand_strategist'],
            tools=tools,
            llm=self.llm,
            verbose=True
        )


    @agent
    def article_writer(self) -> Agent:
        tools = [self.brand_tool, self.quality_tool, self.formatter_tool]
        # Removed file_read_tool - agent should work with provided content only
        if self.file_write_tool:
            tools.append(self.file_write_tool)
        return Agent(
            config=self.agents_config['article_writer'],
            tools=tools,
            llm=self.llm,
            verbose=True
        )

    @agent
    def seo_specialist(self) -> Agent:
        tools = [self.seo_tool, self.quality_tool]
        return Agent(
            config=self.agents_config['seo_specialist'],
            tools=tools,
            llm=self.llm,
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        tools = [self.quality_tool, self.formatter_tool, self.brand_tool, self.fact_checker]
        if self.directory_read_tool:
            tools.append(self.directory_read_tool)
        return Agent(
            config=self.agents_config['editor'],
            tools=tools,
            llm=self.llm,
            verbose=True
        )

    @agent
    def feedback_collector(self) -> Agent:
        tools = []
        if self.file_write_tool:
            tools.append(self.file_write_tool)
        return Agent(
            config=self.agents_config['feedback_collector'],
            tools=tools,
            llm=self.llm,
            verbose=True
        )

    @task
    def brand_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_strategy_task'],
        )


    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
        )

    @task
    def editing_task(self) -> Task:
        # Dynamic output file path
        output_dir = self.project_root / "supplies"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "final_article.md"
        
        return Task(
            config=self.tasks_config['editing_task'],
            output_file=str(output_file)
        )

    @task
    def feedback_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['feedback_collection_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SoylentRed Substack Article Writing Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False  # Disable built-in memory to avoid conflicts
        )