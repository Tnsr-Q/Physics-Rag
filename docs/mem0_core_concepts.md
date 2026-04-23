# Mem0.ai Core Concepts and Features

Mem0 is a memory layer designed for modern AI agents, providing persistent memory capabilities. It enables agents to recall past interactions, store user preferences and factual context, and learn from successes and failures, making them stateful.

## Stateless vs. Stateful Agents

*   **Stateless Agents**: Process queries, generate responses, and forget everything, even with large context windows.
*   **Stateful Agents (powered by Mem0)**: Retain context, recall relevant information, and behave more intelligently over time.

## Mem0 vs. RAG

Mem0 is not a wrapper around a vector store and differs from Retrieval-Augmented Generation (RAG):

| Aspect | RAG | Mem0 Memory |
|---|---|---|
| Statefulness | Stateless | Stateful |
| Recall Type | Document lookup | Evolving user context |
| Use Case | Ground answers in data | Guide behavior across time |

Together, RAG informs the LLM, while Mem0 shapes its memory.

## Types of Memory in Mem0

Mem0 supports various memory types:

*   **Working Memory**: Short-term session awareness.
*   **Factual Memory**: Long-term structured knowledge (e.g., preferences, settings).
*   **Episodic Memory**: Records specific past conversations.
*   **Semantic Memory**: Builds general knowledge over time.

## Why Developers Choose Mem0 (Key Features)

Mem0 is a full memory engine with:

*   **LLM-based extraction**: Intelligently decides what to remember.
*   **Filtering & decay**: Avoids memory bloat and forgets irrelevant information.
*   **Cost Reduction**: Saves compute costs through smart prompt injection of only relevant memories.
*   **Dashboards & APIs**: Provides observability and fine-grained control.
*   **Cloud and OSS**: Available as a managed service or an open-source SDK.
*   **Reduced token usage and faster responses**: Sub-50 ms lookups.
*   **Multimodal support**: Handles both text and images.
*   **Graph memory**: Connects insights and entities across sessions.

## Getting Started

Mem0 offers both a managed platform and an open-source solution.
