# RAG Physics Agentic System

This project develops a Rust-based Retrieval-Augmented Generation (RAG) agentic system hyper-specialized for extracting high-level quantum and classical physics information. It integrates with Mem0.ai for persistent memory storage, enabling Reinforcement Learning (RL) data collection. The system also features CrewAI agents, each embodying a renowned physicist persona, to facilitate high-level roundtable discussions on physics topics.

## Project Goal

To design and build a powerful, extensible RAG scraping agentic system with minimal UI, providing a solid scaffolding for further development and training in the domain of quantum and classical physics.

## System Architecture

The system is built with a modular, event-driven architecture, primarily using Rust for performance and reliability. Key components include:

*   **Data Ingestion Layer**: Rust modules for scraping web pages, extracting YouTube transcripts, and parsing PDF documents.
*   **Pre-processing Layer**: Rust modules for cleaning, normalizing, and extracting keywords from ingested text.
*   **Memory Management Layer**: Integration with Mem0.ai for intelligent, persistent memory storage, optimized for RL data.
*   **Agentic Layer**: Python-based CrewAI agents with distinct physicist personas (Einstein, Feynman, Schrödinger, Dirac, Heisenberg) for specialized discussions.
*   **API/Integration Layer**: Rust web server to expose endpoints for system control and facilitate communication between Rust and Python components.
*   **Minimal UI Layer**: A lightweight web interface for basic interaction and monitoring.

For a detailed overview, refer to the [System Architecture and Component Specifications](docs/system_architecture.md).

## Features

*   **Multi-source Data Scraping**: Extracts physics information from academic papers (PDFs), YouTube transcripts, and general web content.
*   **Intelligent Memory Management**: Utilizes Mem0.ai for semantic, episodic, and factual memory, enhancing agent context and learning.
*   **Physicist Personas**: Five distinct AI agents, each embodying a unique physicist (Einstein, Feynman, Schrödinger, Dirac, Heisenberg) with their specific contributions and philosophical views.
*   **High-Level Physics Discussions**: CrewAI agents engage in simulated roundtable discussions, leveraging their persona-specific knowledge and Mem0.ai memories.
*   **RL Data Collection**: Structured storage of extracted physics information and agent interaction history in Mem0.ai for future RL model training.
*   **Rust-based Core**: Emphasizes performance and reliability with a Rust backend.
*   **Minimal Web UI**: A simple interface for triggering data ingestion and agent discussions.

## Setup and Installation

### Prerequisites

*   Rust (with Cargo)
*   Python 3.11+ (with pip)
*   `yt-dlp` (installed via pip)
*   `pdftotext` (usually part of `poppler-utils` on Linux)

### 1. Clone the Repository

```bash
git clone <repository_url>
cd rag_physics_agent
```

### 2. Install Rust Dependencies

Ensure Rust and Cargo are installed. If not, follow the instructions [here](https://www.rust-lang.org/tools/install).

```bash
cargo build
```

### 3. Install Python Dependencies

Create a Python virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

*(Note: A `requirements.txt` file will be generated in the next steps.)*

### 4. Install System Dependencies

Ensure `yt-dlp` and `pdftotext` are available:

```bash
pip install yt-dlp
sudo apt-get update && sudo apt-get install -y poppler-utils # For pdftotext
```

### 5. Configure API Keys

Set your API keys as environment variables. You can use the provided `set_env.py` script as a template:

```bash
python set_env.py
# Or manually set:
export MEM0_API_KEY="your_mem0_api_key"
export CEREBRAS_API_KEY="your_cerebras_api_key" # Or OPENAI_API_KEY
```

## Usage

### Running the Rust Backend

```bash
cargo run
```

This will start the Rust API server and the minimal web UI. You can then access the UI in your browser at `http://127.0.0.1:8081` (or the configured UI port).

### Running CrewAI Agents (via Python)

The CrewAI agents are designed to be orchestrated by the Rust backend. However, for testing or standalone execution, you can run the Python script directly:

```bash
source venv/bin/activate
python agents/crewai_agents.py
```

This will simulate a discussion on a predefined topic and store the summary in Mem0.ai.

## Project Structure

```
rag_physics_agent/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── data_ingestion/
│   │   ├── mod.rs
│   │   ├── scraper.rs         # Web scraping logic
│   │   ├── youtube_parser.rs  # YouTube transcript extraction
│   │   └── pdf_parser.rs      # PDF text extraction
│   ├── pre_processing/
│   │   ├── mod.rs
│   │   └── text_processor.rs  # Text cleaning, normalization, keyword extraction
│   ├── mem0_client/
│   │   ├── mod.rs
│   │   ├── python_bridge.rs   # Rust-Python bridge for Mem0.ai
│   │   └── mem0_python_client.py # Python script for Mem0.ai interaction
│   ├── api/
│   │   ├── mod.rs
│   │   └── server.rs          # REST API endpoints
│   ├── ui/
│   │   ├── mod.rs
│   │   └── web_app.rs         # Minimal UI serving
│   └── utils/
│       └── mod.rs
├── agents/
│   ├── crewai_agents.py       # Python script for CrewAI agents
│   └── personas.json          # Physicist persona definitions
├── data/
│   └── personas/              # Detailed persona data (Markdown files)
├── config/
│   └── settings.toml          # Configuration settings
├── docs/
│   ├── system_architecture.md
│   ├── mem0_core_concepts.md
│   ├── mem0_crewai_integration.md
│   └── mem0_rl_data_best_practices.md
├── static/
│   └── index.html             # Minimal web UI HTML
├── set_env.py                 # Example script to set environment variables
└── README.md                  # This file
```

## Development Roadmap

### Phase 1: Core System Development (Current)

*   **Rust Backend**: Complete implementation of data ingestion (web, YouTube, PDF), text pre-processing, and Mem0.ai Python bridge.
*   **API Layer**: Develop REST endpoints in Rust to trigger data ingestion, manage Mem0.ai interactions, and initiate CrewAI agent discussions.
*   **CrewAI Agents**: Refine agent personas, define core tasks, and ensure seamless integration with Mem0.ai for memory and context.
*   **Minimal UI**: Implement basic UI elements to interact with the Rust backend (trigger scraping, start discussions, view status).

### Phase 2: Advanced Data Acquisition and Processing

*   **Targeted Scraping**: Implement more sophisticated and configurable scraping rules for specific academic databases (e.g., arXiv categories for quantum physics, classical mechanics).
*   **YouTube API Integration**: Utilize the official YouTube Data API for more robust transcript extraction and video metadata retrieval.
*   **Advanced NLP**: Integrate advanced NLP techniques in Rust (or via Python bridge) for Named Entity Recognition (NER) of physics concepts, relation extraction, and abstractive summarization.
*   **PDF Layout Analysis**: Improve PDF parsing to handle complex layouts, tables, and figures more effectively.

### Phase 3: Enhanced Memory and RL Integration

*   **Mem0.ai Graph Memory**: Fully leverage Mem0.ai's graph memory capabilities to build a rich knowledge graph of physics concepts and their interconnections.
*   **RL Feedback Loop**: Implement a feedback mechanism where the outcomes of agent discussions (e.g., consensus, unresolved questions, new insights) are used to refine Mem0.ai memories or trigger further data acquisition.
*   **RL Model Training**: Develop and integrate RL models that learn from the structured data in Mem0.ai to optimize agent behavior, discussion strategies, or knowledge retrieval processes.

### Phase 4: UI/UX and Observability Improvements

*   **Interactive Knowledge Graph Visualization**: Develop a dynamic web visualization of the physics knowledge graph stored in Mem0.ai.
*   **Agent Dashboard**: Create a comprehensive dashboard to monitor agent activity, memory usage, discussion progress, and key metrics.
*   **Advanced Query Interface**: Implement a natural language query interface allowing users to ask complex physics questions to the agent collective and visualize their reasoning process.
*   **Real-time Discussion Viewer**: Enhance the UI to display agent discussions in real-time, highlighting contributions from each persona.

### Phase 5: Deployment and Scalability

*   **Containerization**: Package the Rust backend and Python components into Docker containers for easier deployment and scalability.
*   **Cloud Deployment**: Provide guidance and scripts for deploying the system on cloud platforms (e.g., AWS, GCP, Azure).
*   **Performance Optimization**: Further optimize Rust code for concurrent scraping and processing, and fine-tune Mem0.ai and CrewAI configurations for large-scale operations.

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` (to be created) for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` (to be created) file for details.

## Acknowledgments

*   Mem0.ai for providing the intelligent memory layer.
*   CrewAI for the agent orchestration framework.
*   Cerebras for the powerful LLM capabilities.

