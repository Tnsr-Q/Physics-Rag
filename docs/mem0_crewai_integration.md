# Mem0.ai and CrewAI Integration

This integration combines CrewAI's agent-based architecture with Mem0's memory capabilities to enable persistent memory across agent interactions and personalized task execution.

## Overview

The integration allows for:
1.  Using CrewAI to manage AI agents and tasks.
2.  Leveraging Mem0 to store and retrieve conversation history.
3.  Creating personalized experiences based on stored user preferences.

## Setup and Configuration

**Installation:**
```bash
pip install crewai crewai-tools mem0ai
```

**Configuration:**
API keys for Mem0 Platform, OpenAI, and Serper Dev are required. Environment variables are used for configuration:

```python
import os
from mem0 import MemoryClient
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["MEM0_API_KEY"] = "your-mem0-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["SERPER_API_KEY"] = "your-serper-api-key"

client = MemoryClient()
```

## Key Integration Steps

1.  **Store User Preferences**: Use `client.add(conversation, user_id=user_id)` to store conversation history and extract user preferences.
2.  **Create CrewAI Agent**: Define an `Agent` with `memory=True` and integrate necessary tools (e.g., `SerperDevTool`).
3.  **Define Tasks**: Create `Task` objects for the agent.
4.  **Set Up Crew**: Configure the `Crew` with `memory=True` and `memory_config` pointing to Mem0:
    ```python
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        memory=True,
        memory_config={
            "provider": "mem0",
            "config": {"user_id": "crew_user_1"},
        }
    )
    ```

## Benefits

*   **Persistent Context & Memory**: Maintains user preferences and interaction history across sessions.
*   **Flexible & Scalable Design**: Easily extendable with new agents, tasks, and capabilities.
