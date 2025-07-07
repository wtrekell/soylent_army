from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool, WebsiteSearchTool
from .tools.content_tools import (
    BrandStyleGuideTool, WebResearchTool, SEOAnalysisTool, 
    ContentQualityTool, SubstackFormatterTool
)

@CrewBase
class SoylentRed():
    """SoylentRed Substack Article Writing Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Configure OpenAI LLM
        self.llm = LLM(model="gpt-4o-mini", temperature=0.1)
        
        # Initialize tools
        self.brand_tool = BrandStyleGuideTool()
        self.research_tool = WebResearchTool()
        self.serper_tool = SerperDevTool()
        self.website_search_tool = WebsiteSearchTool()
        self.seo_tool = SEOAnalysisTool()
        self.quality_tool = ContentQualityTool()
        self.formatter_tool = SubstackFormatterTool()

    @agent
    def brand_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['brand_strategist'],
            tools=[self.brand_tool, self.quality_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['content_researcher'],
            tools=[self.research_tool, self.serper_tool, self.website_search_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tools=[self.brand_tool, self.quality_tool, self.formatter_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            tools=[self.seo_tool, self.quality_tool, self.serper_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            tools=[self.quality_tool, self.formatter_tool, self.brand_tool],
            llm=self.llm,
            verbose=True
        )

    @task
    def brand_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_strategy_task'],
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
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
        return Task(
            config=self.tasks_config['editing_task'],
            output_file='final_article.md'
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