import os
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from mem0 import MemoryClient
# Import your new custom tools
from agents.tools.rtx_ppf_tools import (
    analyze_rtx_ppf_parquet,
    generate_floquet_cli_command,
    ppf_probe_eigenvalues,
    launch_inspector_gui
)
# Load API keys from environment variables
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY") # Assuming Cerebras uses OpenAI-compatible API

if not MEM0_API_KEY:
    raise ValueError("MEM0_API_KEY environment variable not set.")
if not OPENAI_API_KEY and not CEREBRAS_API_KEY:
    raise ValueError("Either OPENAI_API_KEY or CEREBRAS_API_KEY environment variable must be set.")

# Initialize Mem0 client
mem0_client = MemoryClient(api_key=MEM0_API_KEY)

# Configure LLM for CrewAI agents
# Prioritize Cerebras if available, otherwise use OpenAI
llm_config = {
    "model": "gpt-oss-120b", # Assuming Cerebras model name
    "api_key": CEREBRAS_API_KEY,
    "base_url": "https://api.cerebras.ai/v1" # Placeholder, adjust if Cerebras has a different base URL
} if CEREBRAS_API_KEY else {
    "model": "gpt-4-turbo", # Default OpenAI model
    "api_key": OPENAI_API_KEY,
}

# --- Tools for Agents ---

@tool("Mem0 Add Memory Tool")
def mem0_add_memory(data: str, user_id: str, metadata: dict = None, category: str = None) -> str:
    """Adds a new memory to Mem0.ai for a specific user_id. Useful for storing facts, observations, or discussion points.
    data: The content of the memory to store.
    user_id: The ID of the user/agent associated with this memory.
    metadata: Optional dictionary of metadata (e.g., source, topic, timestamp).
    category: Optional category for the memory (e.g., 'quantum_mechanics', 'classical_physics', 'discussion_point').
    """
    try:
        mem0_client.add(data, user_id=user_id, metadata=metadata, category=category)
        return f"Memory added successfully for user {user_id}."
    except Exception as e:
        return f"Failed to add memory: {e}"

@tool("Mem0 Search Memory Tool")
def mem0_search_memory(query: str, user_id: str = None, category: str = None, limit: int = 5) -> str:
    """Searches for relevant memories in Mem0.ai based on a query. Can be filtered by user_id and category.
    query: The search query.
    user_id: Optional ID of the user/agent to search memories for.
    category: Optional category to filter search results.
    limit: Maximum number of search results to return.
    """
    try:
        results = mem0_client.search(query, user_id=user_id, category=category, limit=limit)
        if results:
            formatted_results = []
            for mem in results:
                formatted_results.append(f"Memory ID: {mem.id}\nData: {mem.data}\nMetadata: {mem.metadata}\nCategory: {mem.category}")
            return "\n---\n".join(formatted_results)
        else:
            return "No relevant memories found."
    except Exception as e:
        return f"Failed to search memories: {e}"

# --- Agent Definitions ---

def load_persona_data(persona_data_path):
    with open(persona_data_path, 'r') as f:
        return f.read()

 Enhanced agent creation with RTX-PPF tools
def create_physicist_agent_with_ppf(persona_config):
    """Create agents with both Mem0 AND PPF tools"""
    
    persona_data = load_persona_data(persona_config["persona_data_path"])
    
    # Base tools (Mem0)
    base_tools = [mem0_add_memory, mem0_search_memory]
    
    # Specialized tools per physicist
    specialized_tools = {
        "Albert Einstein": [
            analyze_rtx_ppf_parquet,  # Topology theorist
            launch_inspector_gui
        ],
        "Richard Feynman": [
            ppf_probe_eigenvalues,    # Hands-on experimentalist
            generate_floquet_cli_command
        ],
        "Erwin Schrödinger": [
            analyze_rtx_ppf_parquet,  # Wave mechanics analyst
            ppf_probe_eigenvalues
        ],
        "Paul Dirac": [
            ppf_probe_eigenvalues,    # Mathematical rigor
        ],
        "Werner Heisenberg": [
            analyze_rtx_ppf_parquet,  # Uncertainty / measurement
        ]
    }
    
    tools = base_tools + specialized_tools.get(persona_config["name"], [])
    
    full_backstory = f"""
    {persona_config["backstory"]}
    
    --- Persona Data ---
    {persona_data}
    
    --- Available Tools ---
    You have access to:
    - Mem0 memory system for storing/retrieving insights
    - RTX-PPF analysis tools for Floquet topology data
    - PPF bridge for instant eigenvalue classification
    - CLI generator for proposing new experiments
    
    Your role is to analyze quantum topological data through the lens of your
    historical contributions and philosophical views. Use tools proactively.
    """
    
    return Agent(
        role=persona_config["role"],
        goal=persona_config["goal"],
        backstory=full_backstory,
        allow_delegation=True,
        verbose=True,
        memory=True,
        tools=tools,
        llm={
            "model": "llama-3.3-70b",  # Cerebras model
            "api_key": os.getenv("CEREBRAS_API_KEY"),
            "base_url": "https://api.cerebras.ai/v1"
        }
    )

# Recreate agents with PPF tools
einstein_agent = create_physicist_agent_with_ppf(personas_config[0])
feynman_agent = create_physicist_agent_with_ppf(personas_config[1])
schrodinger_agent = create_physicist_agent_with_ppf(personas_config[2])
dirac_agent = create_physicist_agent_with_ppf(personas_config[3])
heisenberg_agent = create_physicist_agent_with_ppf(personas_config[4])

# Load all persona configurations
with open("agents/personas.json", 'r') as f:
    personas_config = json.load(f)

# Create agents dynamically
physicist_agents = {}
for persona in personas_config:
    agent_name = persona["name"].replace(" ", "_").lower()
    physicist_agents[agent_name] = create_physicist_agent(persona, [mem0_add_memory, mem0_search_memory])

# Assign agents to individual variables for easier access (optional, but good for clarity)
einstein_agent = physicist_agents["albert_einstein"]
feynman_agent = physicist_agents["richard_feynman"]
schrodinger_agent = physicist_agents["erwin_schrödinger"]
dirac_agent = physicist_agents["paul_dirac"]
heisenberg_agent = physicist_agents["werner_heisenberg"]

# --- Task Definitions ---

def create_discussion_task(agent, topic):
    return Task(
        description=f"Engage in a high-level discussion about {topic}, drawing upon your expertise and philosophical views. Remember to leverage your memory for context and to store new insights.",
        expected_output=f"A detailed contribution to the discussion on {topic}, reflecting the agent's unique perspective and knowledge.",
        agent=agent,
        async_execution=True
    )

# --- Crew Definition ---

def setup_physics_roundtable_crew(topic: str):
    # Create tasks for each agent to discuss the topic
    einstein_task = create_discussion_task(einstein_agent, topic)
    feynman_task = create_discussion_task(feynman_agent, topic)
    schrodinger_task = create_discussion_task(schrodinger_agent, topic)
    dirac_task = create_discussion_task(dirac_agent, topic)
    heisenberg_task = create_discussion_task(heisenberg_agent, topic)

    # The crew will execute tasks sequentially, allowing agents to build on each other's contributions
    # and store their insights in Mem0.ai.
    crew = Crew(
        agents=list(physicist_agents.values()), # Use all created agents
        tasks=[
            einstein_task,
            feynman_task,
            schrodinger_task,
            dirac_task,
            heisenberg_task
        ],
        process=Process.sequential,
        memory=True,
        memory_config={
            "provider": "mem0",
            "config": {"user_id": "physics_roundtable"} # A shared user_id for the discussion context
        },
        verbose=True
    )
    return crew

if __name__ == "__main__":
    # Example usage: Simulate a discussion on the interpretation of quantum mechanics
    discussion_topic = "the interpretation of quantum mechanics"
    physics_crew = setup_physics_roundtable_crew(discussion_topic)

    print("\n\n########### Starting Physics Roundtable Discussion ###########")
    result = physics_crew.kickoff()
    print("\n\n########### Discussion Concluded ###########")
    print(result)

    # You can also add a task to summarize the discussion and store it in Mem0
    summary_agent = Agent(
        role="Discussion Summarizer",
        goal="Summarize the key points and conclusions of the physics discussion.",
        backstory="An impartial academic who excels at synthesizing complex discussions into concise summaries.",
        allow_delegation=False,
        verbose=True,
        llm=llm_config,
        tools=[mem0_search_memory, mem0_add_memory]
    )

    summary_task = Task(
        description=f"Summarize the recent discussion on {discussion_topic}. Retrieve all relevant memories from Mem0.ai for user 'physics_roundtable' to inform your summary.",
        expected_output="A comprehensive summary of the discussion, highlighting each physicist's main arguments and any points of agreement or disagreement.",
        agent=summary_agent
    )

    summary_crew = Crew(
        agents=[summary_agent],
        tasks=[summary_task],
        process=Process.sequential,
        memory=True,
        memory_config={
            "provider": "mem0",
            "config": {"user_id": "physics_roundtable"}
        },
        verbose=True
    )

    print("\n\n########### Generating Discussion Summary ###########")
    summary_result = summary_crew.kickoff()
    print("\n\n########### Summary ###########")
    print(summary_result)

    # Store the final summary in Mem0
    mem0_add_memory(summary_result, user_id="physics_roundtable", category="discussion_summary", metadata={"topic": discussion_topic})
    print("Discussion summary stored in Mem0.ai.")

