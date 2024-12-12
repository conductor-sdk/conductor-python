import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ConfigDict
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_chat_complete import LlmChatComplete, ChatMessage
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models.SkillRegistryService import SkillRegistryService, InMemorySkillRegistry
from conductor.client.http.models.Skill import SkillDocument
from conductor.client.workflow.task.timeout_policy import TimeoutPolicy
import logging
import asyncio
from datetime import datetime, UTC

class PlanStep(BaseModel):
    id: str
    description: str
    required_capabilities: list[str]
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class PlanLevel(BaseModel):
    overview: str
    detailed_steps: list[PlanStep]
    skill_mapping: dict[str, SkillDocument]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Plan(BaseModel):
    query: str
    levels: PlanLevel
    workflow_def: Optional[dict[str, Any]] = None
    metadata: dict[str, Any] = {}
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class AgentConfig(BaseModel):
    name: str
    description: str
    planner_model: str = "gpt-4o"
    response_model: str = "gpt-3.5-turbo"
    llm_provider: str = "openai_savant"
    prompt_templates: dict[str, str]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Agent:
    def __init__(self, 
                 config: AgentConfig, 
                 orchestrator: AIOrchestrator,
                 skill_registry: Optional[SkillRegistryService] = None):
        """
        Initialize an agent with a configuration and shared orchestrator
        
        Args:
            config: AgentConfig object containing agent-specific settings
            orchestrator: Shared AIOrchestrator instance for LLM interactions
            skill_registry: Optional SkillRegistryService instance (defaults to InMemorySkillRegistry)
        """
        self.config = config
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(f"agent.{config.name}")
        self.conductor_config = Configuration()
        self.clients = OrkesClients(configuration=self.conductor_config)
        self.skill_registry = skill_registry or InMemorySkillRegistry()
        
        # Register this agent's prompt templates
        self._register_prompt_templates()

    def _register_prompt_templates(self):
        """Register agent-specific prompt templates with shared orchestrator"""
        for name, template in self.config.prompt_templates.items():
            template_name = f"{self.config.name}_{name}"  # Namespace the template
            try:
                self.orchestrator.add_prompt_template(template_name, template, f"{name} instructions")
                self.orchestrator.associate_prompt_template(
                    template_name,
                    self.config.llm_provider,
                    [self.config.planner_model, self.config.response_model]
                )
            except Exception as e:
                self.logger.warning(f"Template {template_name} already exists: {str(e)}")

    async def process_query(self, query: str) -> str:
        """Main entry point - processes query and returns human-friendly response"""
        execution_id = datetime.now(UTC).isoformat()
        self.logger.info(f"Starting query processing {execution_id}: {query}")
        
        try:
            # Generate plan at all levels
            plan = await self.generate_plan(query)
            self.logger.info(f"Generated plan: {plan}")
            
            # Create workflow from plan
            workflow = self._create_workflow_from_plan(plan)
            
            # Execute workflow
            result = await self._execute_workflow(workflow)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query {execution_id}: {str(e)}", exc_info=True)
            raise

    async def generate_plan(self, query: str) -> Plan:
        """Generate plan at all three levels"""
        # Use planner_model to generate overview
        overview = await self._generate_overview(query)
        
        # Generate detailed steps
        detailed_steps = await self._generate_detailed_steps(overview)
        
        # Map steps to skills using RAG
        skill_mapping = await self._map_steps_to_skills(detailed_steps)
        
        return Plan(
            query=query,
            levels=PlanLevel(
                overview=overview,
                detailed_steps=detailed_steps,
                skill_mapping=skill_mapping
            )
        )

    async def _generate_overview(self, query: str) -> str:
        """Generate high-level overview of what needs to be done"""
        messages = [
            {
                "role": "system",
                "content": "Generate a high-level overview of how to answer this query. Focus on the main steps needed."
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        result = await self.orchestrator.chat_complete(
            provider=self.config.llm_provider,
            model=self.config.planner_model,
            messages=messages,
            template_name=f"{self.config.name}_planner_instructions"
        )
        
        return result.content

    async def _generate_detailed_steps(self, overview: str) -> List[PlanStep]:
        """Break down overview into detailed executable steps"""
        messages = [
            {
                "role": "system",
                "content": """Break down this overview into detailed steps. For each step specify:
                1. A unique ID
                2. Clear description of what needs to be done
                3. Required capabilities
                4. Input requirements
                5. Expected outputs"""
            },
            {
                "role": "user",
                "content": f"Overview: {overview}"
            }
        ]
        
        result = await self.orchestrator.chat_complete(
            provider=self.config.llm_provider,
            model=self.config.planner_model,
            messages=messages,
            template_name=f"{self.config.name}_planner_instructions"
        )
        
        steps_data = json.loads(result.content)
        return [PlanStep(**step) for step in steps_data['steps']]

    async def _map_steps_to_skills(self, steps: List[PlanStep]) -> Dict[str, SkillDocument]:
        """Map each step to available skills"""
        skill_mapping = {}
        
        for step in steps:
            search_desc = f"{step.description} {' '.join(step.required_capabilities)}"
            matching_skills = self.skill_registry.find_relevant_skills(
                description=search_desc,
                k=1
            )
            
            if matching_skills:
                skill_mapping[step.id] = matching_skills[0]
                self.logger.info(f"Mapped step {step.id} to skill {matching_skills[0].skill_name}")
            else:
                self.logger.warning(f"No matching skill found for step {step.id}")
        
        return skill_mapping

    def _create_workflow_from_plan(self, plan: Plan) -> ConductorWorkflow:
        """Create a Conductor workflow from the completed plan"""
        workflow_executor = self.clients.get_workflow_executor()
        wf = ConductorWorkflow(
            name=f"{self.config.name}_query_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}",
            version=1,
            executor=workflow_executor
        )

        previous_task = None
        for step in plan.levels.detailed_steps:
            skill = plan.levels.skill_mapping.get(step.id)
            if not skill:
                self.logger.warning(f"No skill mapping found for step {step.id}")
                continue

            task = skill.to_conductor_task(
                task_ref_name=f"step_{step.id}",
                inputs=step.inputs
            )

            if previous_task:
                previous_task >> task
            else:
                wf >> task
            
            previous_task = task

        return wf

    async def _execute_workflow(self, workflow: ConductorWorkflow) -> Any:
        """Execute the workflow and return results"""
        self.logger.info("Executing workflow...")
        workflow_client = self.clients.get_workflow_client()
        workflow_run = workflow.execute()
        workflow_id = workflow_run.workflow_id
        
        # Poll for completion
        self.logger.info(f"Polling workflow {workflow_id}...")
        while True:
            status = workflow_client.get_workflow_status(
                workflow_id=workflow_id,
                include_output=True
            )
            if not status.is_running():
                result = status.output.get('result', {})
                self.logger.info(f"Workflow completed with result: {result}")
                return result
            await asyncio.sleep(1)
    
    def _format_response(self, result: Any) -> str:
        """Format the workflow result for human consumption"""
        if isinstance(result, dict):
            return json.dumps(result, indent=2)
        return str(result)
    def _create_planning_workflow(self, query: str) -> ConductorWorkflow:
        """Creates a workflow for the planning process"""
        workflow_executor = self.clients.get_workflow_executor()
        wf = ConductorWorkflow(
            name=f"{self.config.name}_planning_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}",
            version=1,
            executor=workflow_executor
        )

        # Overview generation task
        overview_task = LlmChatComplete(
            task_ref_name='generate_overview',
            llm_provider=self.config.llm_provider,
            model=self.config.planner_model,
            instructions_template=f"{self.config.name}_planner_instructions",
            messages=[ChatMessage(role='user', message=query)],
            max_tokens=2048
        )

        # Detailed steps generation task
        detailed_steps_task = LlmChatComplete(
            task_ref_name='generate_steps',
            llm_provider=self.config.llm_provider,
            model=self.config.planner_model,
            instructions_template=f"{self.config.name}_planner_instructions",
            messages=[ChatMessage(
                role='user',
                message=f"Generate detailed steps for this overview: ${overview_task.output('result')}"
            )],
            max_tokens=2048
        )

        # Skills mapping task using RAG
        skill_mapping_task = SimpleTask(
            task_reference_name='map_skills',
            task_def_name='map_skills_to_plan'
        )
        skill_mapping_task.input_parameter('steps', detailed_steps_task.output('result'))

        # Chain the tasks
        wf >> overview_task >> detailed_steps_task >> skill_mapping_task

        return wf

    async def generate_plan(self, query: str) -> Plan:
        """Generate plan using a Conductor workflow"""
        planning_workflow = self._create_planning_workflow(query)
        
        # Execute planning workflow
        workflow_run = planning_workflow.execute()
        workflow_id = workflow_run.workflow_id
        
        # Get workflow client
        workflow_client = self.clients.get_workflow_client()
        
        # Poll for completion
        while True:
            status = workflow_client.get_workflow_status(
                workflow_id=workflow_id,
                include_output=True
            )
            if not status.is_running():
                # Extract results from workflow output
                overview = status.output.get('generate_overview', {}).get('result', '')
                detailed_steps = status.output.get('generate_steps', {}).get('result', [])
                skill_mapping = status.output.get('map_skills', {}).get('result', {})
                
                return Plan(
                    query=query,
                    levels=PlanLevel(
                        overview=overview,
                        detailed_steps=detailed_steps,
                        skill_mapping=skill_mapping
                    )
                )
            await asyncio.sleep(1)







def create_default_prompt_templates() -> dict[str, str]:
    """Create default prompt templates for agents"""
    return {
        "planner_instructions": """
        You are a planning assistant that breaks down user queries into executable steps.
        Given the query, create a plan that:
        1. Identifies required capabilities
        2. Breaks down the task into concrete steps
        3. Specifies inputs and outputs for each step

        Format your response as a JSON object with the following structure:
        {
            "overview": "Brief description of the plan",
            "steps": [
                {
                    "id": "unique_step_id",
                    "description": "What this step does",
                    "required_capabilities": ["capability1", "capability2"],
                    "inputs": {"input1": "description1"},
                    "outputs": {"output1": "description1"}
                }
            ]
        }
        """,
        
        "response_generation": """
        Given the execution results, generate a clear and concise response for the user.
        Focus on:
        1. What was accomplished
        2. Any relevant metrics or outcomes
        3. Next steps or recommendations if applicable
        """
    }

class AgentPool:
    """Manages a collection of agents sharing an orchestrator"""
    
    def __init__(self):
        self.conductor_config = Configuration()
        self.orchestrator = AIOrchestrator(api_configuration=self.conductor_config)
        self.skill_registry = InMemorySkillRegistry()
        self.agents: Dict[str, Agent] = {}
        self.logger = logging.getLogger("agent_pool")

    def create_agent(self, config: AgentConfig) -> Agent:
        """Create and register a new agent"""
        if config.name in self.agents:
            raise ValueError(f"Agent with name {config.name} already exists")
            
        agent = Agent(
            config=config, 
            orchestrator=self.orchestrator,
            skill_registry=self.skill_registry
        )
        self.agents[config.name] = agent
        return agent
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)

    async def process_query(self, agent_name: str, query: str) -> str:
        """Process a query using the specified agent"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"No agent found with name {agent_name}")
        return await agent.process_query(query)

async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create agent pool
    pool = AgentPool()

    # Create different types of agents
    agents_config = [
        AgentConfig(
            name="sales_agent",
            description="Agent for sales-related queries",
            prompt_templates=create_default_prompt_templates()
        ),
        AgentConfig(
            name="support_agent",
            description="Agent for customer support queries",
            prompt_templates=create_default_prompt_templates()
        )
    ]

    # Register agents
    for config in agents_config:
        pool.create_agent(config)

    # Test queries for different agents
    test_cases = [
        ("sales_agent", "Find our top 10 customers by revenue"),
        ("support_agent", "List all open support tickets"),
        ("sales_agent", "Generate Q4 sales forecast")
    ]

    # Run test cases
    for agent_name, query in test_cases:
        print(f"\nProcessing query with {agent_name}: {query}")
        try:
            result = await pool.process_query(agent_name, query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())