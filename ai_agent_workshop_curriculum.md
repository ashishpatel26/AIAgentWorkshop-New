# AI Agent Workshop Curriculum: Building Multi-Agent Systems with CrewAI and LangGraph

## Workshop Overview
**Target Audience:** College engineering students with basic programming knowledge
**Duration:** 3 hours (3 sessions of 1 hour each)
**Format:** Hands-on workshop with theory sessions, live coding demonstrations, and individual/group projects
**Prerequisites:**
- Basic Python programming (variables, functions, classes)
- Familiarity with command line/terminal
- Basic understanding of AI/ML concepts (optional but helpful)
- Laptop with internet connection

**Learning Objectives:**
By the end of this workshop, students will be able to:
- Understand the concepts of AI agents and multi-agent systems
- Implement basic autonomous agents using CrewAI framework
- Build simple multi-agent workflows with CrewAI
- Get an introduction to stateful workflows with LangGraph
- Design basic collaborative agent systems for real-world problems

## Required Software Setup
**Before the Workshop:**
1. Install Python 3.8+
2. Install required packages using UV:
   ```bash
   uv pip install crewai langchain langgraph openai python-dotenv
   ```
3. Set up OpenAI API key (for LLM access)
4. Install VS Code or preferred IDE
5. Git for version control

## Workshop Schedule

### Session 1: Introduction to AI Agents and CrewAI Basics (1 hour)
**Objectives:** Understand agent fundamentals and get started with CrewAI

**Topics Covered:**
- What are AI agents? Definition and characteristics
- Single vs Multi-agent systems
- Overview of CrewAI framework
- Brief introduction to LangGraph

**Hands-on Activities:**
1. **Environment Setup (20 mins)**
   - Install required packages
   - Configure API keys
   - Test basic setup

2. **CrewAI Basics (40 mins)**
   - Create simple agents with roles
   - Define basic tasks
   - Run a simple crew workflow

### Session 2: Hands-on CrewAI Project (1 hour)
**Objectives:** Build a functional multi-agent system with CrewAI

**Topics Covered:**
- Agent roles and responsibilities
- Task delegation and collaboration
- Tool integration basics

**Hands-on Activities:**
- **Collaborative Project: Content Creation Crew (1 hour)**
  - Build a 3-agent system: Researcher, Writer, Editor
  - Assign tasks for topic research and content generation
  - Test the workflow and iterate

### Session 3: LangGraph Introduction and Integration (1 hour)
**Objectives:** Learn basics of LangGraph and combine with CrewAI concepts

**Topics Covered:**
- LangGraph concepts: nodes, edges, state
- Basic stateful workflows
- Integrating CrewAI with LangGraph ideas

**Hands-on Activities:**
1. **LangGraph Fundamentals (30 mins)**
   - Build a simple graph-based workflow
   - Implement basic state management

2. **Integration Project (30 mins)**
   - Create a hybrid simple agent system
   - Discuss real-world applications and next steps

## Detailed Module Breakdown

### Module 1: Agent Fundamentals and Setup
**Duration:** 20 minutes
**Content:**
- Agent = AI + Tools + Memory + Reasoning
- Single vs Multi-agent systems
- Overview of CrewAI and LangGraph

**Activity:** Environment setup and basic agent creation

### Module 2: CrewAI Hands-on
**Duration:** 1 hour
**Content:**
- Agent creation with roles
- Task definition and delegation
- Basic collaboration patterns

**Activity:** Build a content creation crew (Researcher, Writer, Editor)

### Module 3: LangGraph Introduction
**Duration:** 1 hour
**Content:**
- Graph concepts for agents
- Basic stateful workflows
- Integration possibilities

**Activity:** Create a simple stateful agent workflow

## Assessment and Evaluation
- **Formative:** Code reviews during hands-on sessions
- **Summative:** Final project presentation (optional)
- **Peer Learning:** Code sharing and debugging sessions

## Resources and Materials
- Workshop GitHub repository with starter code
- Official documentation links:
  - CrewAI: https://www.crewai.com/
  - LangGraph: https://langchain-ai.github.io/langgraph/
- Additional reading: "Human Compatible" by Stuart Russell

## Instructor Preparation Notes
- Prepare demo environments for each session
- Have backup solutions for API rate limits
- Prepare troubleshooting guides for common issues
- Arrange for adequate computing resources (cloud credits if needed)

## Expected Challenges and Solutions
- API key management: Provide sandbox environments
- Complex debugging: Include error handling examples
- Time management: Have modular exercises that can be shortened
- Varying skill levels: Offer advanced extensions for experienced students

This curriculum provides a comprehensive, hands-on introduction to AI agent development suitable for engineering students, balancing theoretical concepts with practical implementation.
