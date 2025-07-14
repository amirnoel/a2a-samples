import uvicorn


from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from agent_executor import (
    TaskManagerAgentExecutor,
)

def main():
    skill = AgentSkill(
        id='manage_tasks',
        name='Manage Task',
        description='Manages user Tasks',
        tags=['task'],
        examples=['create task','retrieve task','delete task'],
    )

    extended_skill = AgentSkill(
        id='search_tasks',
        name='Returns Task based on query',
        description='Search user Tasks',
        tags=['search'],
        examples=['search task','get task'],
    )

    public_agent_card = AgentCard(
        name='Task Manager Agent',
        description='',
        url='http://localhost:9999/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
        ),
        skills=[skill],
        supportsAuthenicatedExtendedCard=True,
    )

    specific_extended_agent_card = public_agent_card.model_copy(
        update={
            'name': 'Task Manager Agent',
            'description': 'The full-featured task manager agent for authenticated users.',
            'version': '1.0.1',
            'skills': [
                skill,
                extended_skill,
            ],
        }
    )

    request_handler = DefaultRequestHandler(
        agent_executor=TaskManagerAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
        extended_agent_card=specific_extended_agent_card,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9999)

if __name__ == "__main__":
    main()