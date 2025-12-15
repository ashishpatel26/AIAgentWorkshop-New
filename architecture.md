# AIAgentWorkshop Code Architecture

This document provides a visual representation of the codebase architecture using Mermaid diagrams.

## Project Overview

The AIAgentWorkshop is a Python-based educational project demonstrating progressive AI agent development, from basic interactions to complex multi-agent workflows. It supports multiple AI providers (SambaNova cloud API, Ollama local models, and NVIDIA API) with a simple configuration system.

## Architecture Diagram

```mermaid
flowchart LR
 subgraph subGraph0["External Dependencies"]
        LangChain["LangChain OpenAI<br>ChatOpenAI"]
        CrewAI["CrewAI Framework<br>Agent, Task, Crew"]
        LangGraph["LangGraph<br>StateGraph, TypedDict"]
        SambaNova["SambaNova API<br>Cloud LLM Models"]
        Ollama["Ollama<br>Local LLM Models"]
        NVIDIA["NVIDIA API<br>Cloud LLM Models"]
        DotEnv["python-dotenv<br>Environment Loading"]
  end
 subgraph subGraph1["Simple Configuration"]
        Config["config.py<br>Auto-Configuration<br>- Environment Loading<br>- Provider Selection<br>- Model Configuration"]
  end
 subgraph subGraph2["Testing & Validation"]
        TestScripts["testing/<br>Test Scripts<br>- API Validation<br>- Provider Testing<br>- Integration Tests"]
  end
 subgraph subGraph3["Session 1: Foundations"]
        S1Basics["session1/basics.py<br>Basic AI Interactions<br>- Simple Chat<br>- Math Helper Examples"]
        S1CrewAI["session1/crewai_intro.py<br>CrewAI Introduction<br>- Single Agent Crews<br>- Multi-Agent Teams"]
  end
 subgraph subGraph4["Session 2: Advanced Agents"]
        S2AgentRoles["session2/agent_roles.py<br>Agent Roles &amp; Teams<br>- Specialized Roles<br>- Collaborative Tasks"]
        S2GUI["session2/agent_roles_gui.py<br>GUI Implementation<br>- Agent Role Visualization"]
        S2Content["session2/content_crew.py<br>Content Creation Crew<br>- Content Workflow"]
  end
 subgraph subGraph5["Session 3: Stateful Workflows"]
        S3LangGraph["session3/langgraph_basics.py<br>LangGraph Basics<br>- State Management<br>- Node-Based Graphs<br>- Conditional Routing"]
        S3Stateful["session3/stateful_workflow.py<br>CrewAI Workflows<br>- Complex State Logic"]
        S3Nvidia["session3/langgraph_basics_nvidia.py<br>LangGraph Basics NVIDIA<br>- NVIDIA API Integration"]
        S3LangChain["session3/stateful_workflow_langchain_nvidia.py<br>LangChain NVIDIA<br>- Pure LangChain Approach"]
  end
 subgraph subGraph6["Legacy Utils (Advanced)"]
        LegacyConfig["utils/config.py<br>Legacy Configuration<br>- Complex Config Class"]
        Helpers["utils/helpers.py<br>Utility Functions<br>- Text Processing<br>- Cost Estimation"]
        RateLimiter["utils/rate_limiter.py<br>Rate Limiting<br>- API Throttling"]
  end
    LangChain --> SambaNova & Ollama & NVIDIA & S1Basics & S3LangChain
    CrewAI --> LangChain & S1CrewAI & S2AgentRoles & S2Content & S3Stateful
    LangGraph --> LangChain & S3LangGraph & S3Nvidia
    DotEnv --> Config
    Config --> TestScripts
    Config -. Simple Config .-> S1Basics & S1CrewAI & S2AgentRoles & S2GUI & S2Content & S3LangGraph & S3Stateful & S3Nvidia & S3LangChain
    S1Basics -. Builds Upon .-> S1CrewAI
    S1CrewAI -. Advances To .-> S2AgentRoles
    S2AgentRoles -. Extends To .-> S3LangGraph
    S3LangGraph -. Branches To .-> S3Stateful
    S3Stateful -. Alternative .-> S3Nvidia
    S3Nvidia -. Alternative .-> S3LangChain

     LangChain:::external
     CrewAI:::external
     LangGraph:::external
     SambaNova:::external
     Ollama:::external
     NVIDIA:::external
     DotEnv:::external
     Config:::config
     TestScripts:::testing
     S1Basics:::session1
     S1CrewAI:::session1
     S2AgentRoles:::session2
     S2GUI:::session2
     S2Content:::session2
     S3LangGraph:::session3
     S3Stateful:::session3
     S3Nvidia:::session3
     S3LangChain:::session3
     LegacyConfig:::legacy
     Helpers:::legacy
     RateLimiter:::legacy
    classDef config fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef testing fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef session1 fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef session2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef session3 fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef legacy fill:#f5f5f5,stroke:#616161,stroke-width:1px
    classDef external fill:#fafafa,stroke:#616161,stroke-width:2px
```

## Component Descriptions

### Simple Configuration System
The `config.py` file provides automatic configuration loading:

- **Provider Selection**: Choose between SambaNova (cloud) or Ollama (local)
- **Auto-Loading**: Environment variables loaded automatically on import
- **Easy Imports**: Direct access via `from config import API_KEY, MODEL, etc.`
- **Validation**: Basic key format checking and defaults

### Testing Infrastructure
The `testing/` folder contains validation and testing scripts:

- **test_langchain.py**: LangChain integration tests
- **test_nvidia_langchain.py**: NVIDIA API with LangChain tests
- **test_nvidia_model.py**: Direct NVIDIA model tests
- **test_ollama.py**: Ollama local model tests
- **test_sambanova.py**: SambaNova API tests
- **API Testing**: Validate connections to different providers
- **Integration Tests**: End-to-end workflow testing
- **Provider Validation**: Ensure API keys and models work correctly

### Session Progression
The workshop follows a progressive learning path:

1. **Session 1**: Foundation concepts with basic AI interactions and CrewAI introduction
2. **Session 2**: Advanced agent design with specialized roles and team collaboration
3. **Session 3**: Complex state management with multiple workflow implementations

### Session 3 Variants
Session 3 demonstrates different approaches to stateful workflows:

- **CrewAI Version**: Traditional multi-agent workflows with state
- **NVIDIA Direct**: Direct integration with NVIDIA API
- **LangChain Pure**: Framework-agnostic LangChain implementation

### External Dependencies
- **LangChain**: Framework for building LLM-powered applications
- **CrewAI**: Framework for creating multi-agent workflows
- **LangGraph**: Library for building stateful agent workflows with graph-based logic
- **SambaNova API**: Cloud-based LLM provider with fast inference
- **Ollama**: Local LLM runtime for running models offline
- **NVIDIA API**: Cloud-based LLM provider with high-performance inference
- **python-dotenv**: Environment variable management

## Data Flow

1. Configuration is loaded automatically from `.env` via `config.py`
2. Sessions import configuration variables directly
3. AI providers (SambaNova/Ollama/NVIDIA) are initialized with appropriate settings
4. Agents execute tasks using external LLM APIs through LangChain/CrewAI/LangGraph
5. Results are processed and presented to users

## Design Patterns

- **Simple Imports**: Direct variable imports instead of complex classes
- **Provider Abstraction**: Unified interface for different AI providers
- **Progressive Complexity**: Sessions build upon each other with increasing sophistication
- **Multiple Implementations**: Session 3 shows different approaches to the same problem
- **Configuration as Code**: Settings defined as simple Python variables

## Provider Support

### SambaNova (Cloud)
- Fast inference with enterprise-grade reliability
- Pay-per-use pricing with generous free tier
- Access to multiple model sizes and capabilities

### Ollama (Local)
- Completely free and offline-capable
- Full control over models and data privacy
- No API rate limits or costs
- Requires local hardware resources

### NVIDIA (Cloud)
- High-performance cloud inference
- Access to advanced NVIDIA models
- Scalable and reliable API service
- Suitable for production workloads
