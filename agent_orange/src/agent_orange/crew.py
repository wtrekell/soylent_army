from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.design_system_tools import (
    GitHubSourceExtractorTool, ComponentCSSAnalyzerTool, 
    DesignPatternExtractorTool, VisualReferenceGeneratorTool
)

@CrewBase
class AgentOrange():
    """AgentOrange - Cloudscape Design System Analysis and Reskinning Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Configure LLM explicitly for OpenAI
        self.llm = LLM(model="gpt-4o-mini", temperature=0.1)
        
        # Initialize design system tools
        self.github_extractor = GitHubSourceExtractorTool()
        self.css_analyzer = ComponentCSSAnalyzerTool()
        self.pattern_extractor = DesignPatternExtractorTool()
        self.reference_generator = VisualReferenceGeneratorTool()

    @agent
    def design_system_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['design_system_analyst'], # type: ignore[index]
            tools=[self.github_extractor],
            llm=self.llm,
            verbose=True
        )

    @agent
    def css_pattern_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['css_pattern_expert'], # type: ignore[index]
            tools=[self.css_analyzer, self.pattern_extractor],
            llm=self.llm,
            verbose=True
        )

    @agent
    def visual_reference_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_reference_creator'], # type: ignore[index]
            tools=[self.reference_generator, self.css_analyzer],
            llm=self.llm,
            verbose=True
        )

    @agent
    def reskinning_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['reskinning_strategist'], # type: ignore[index]
            tools=[self.pattern_extractor, self.css_analyzer],
            llm=self.llm,
            verbose=True
        )

    @task
    def github_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['github_extraction_task'], # type: ignore[index]
        )

    @task
    def pattern_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['pattern_analysis_task'], # type: ignore[index]
        )

    @task
    def visual_reference_task(self) -> Task:
        return Task(
            config=self.tasks_config['visual_reference_task'], # type: ignore[index]
        )

    @task
    def reskinning_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['reskinning_strategy_task'], # type: ignore[index]
            output_file='refined_materials/cloudscape_reskinning_strategy.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgentOrange crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
