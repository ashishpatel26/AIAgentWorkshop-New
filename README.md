# 🤖 AI Agent Workshop for Beginners

## Welcome!

**Hello!** This is a simple workshop to learn about AI agents. We'll build smart AI helpers that can work together like a team. No advanced coding experience needed!

## What You'll LearnP

- How AI agents work (like smart assistants)
- How to make multiple AI agents work together
- How AI can remember information between steps
- **🆕 Advanced Features**: Intelligent rate limiting and error handling for production-ready AI applications

## Before We Start

You need:

- **Python** (version 3.8 or higher) - most computers already have this!
- **Basic Python knowledge** - if you can write `print("hello")`, you're ready!
- **Internet connection** - to talk to AI services
- **A computer** - Windows, Mac, or Linux

## 🚀 Quick Setup (5 minutes!)

### Step 1: Get the Code

```bash
# Download this project
git clone <repository-url>
cd ai-agent-workshop
```

### Step 2: Install Tools

```bash
# Install the UV package manager (easy Python installer)
# On Windows:
powershell -c "irm https://astral.sh/uv/install.sh | iex"

# On Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Install Python Packages

```bash
# Install all needed tools (dependencies are now managed in pyproject.toml)
uv sync
```

### Step 4: Get Your AI Key

1. Go to [OpenRouter.ai](https://openrouter.ai) and sign up (it's free!)
2. Get your API key from the keys page
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Open `.env` and replace `your_openrouter_api_key_here` with your real key

### Step 5: Test Everything Works

```bash
python -c "import crewai; print('✅ Ready to start!')"
```

## 🎯 What We'll Build (3 Simple Sessions)

### Session 1: Your First AI Agent (30 minutes)

Learn the basics! We'll create:

- A simple AI that can chat
- An AI that can use tools (like a calculator)
- Your first AI "crew" (team)

**Run it:**

```bash
cd session1
python basics.py          # Learn basic AI chat
python crewai_intro.py    # Learn about AI teams
```

### Session 2: AI Agents Working Together (30 minutes)

Make AI agents collaborate! We'll build:

- Agents with different jobs (researcher, writer)
- A simple content creation team
- How agents share information

**Run it (Command Line):**

```bash
cd session2
python agent_roles.py     # See different AI jobs
python content_crew.py    # Watch AI create content together
```

**🎨 Interactive GUIs Available!**

**Session 2 Agent Roles GUI:**

```bash
# Run the beautiful agent roles workshop GUI
streamlit run session2/agent_roles_gui.py

# Or use the launcher:
python run_session2_gui.py
```

**Session 2 Advanced GUI:**

```bash
# Run the comprehensive multi-team GUI
streamlit run session2_gui.py
```

**GUI Features:**

- 🎨 Beautiful, modern web interfaces
- 👥 Interactive agent team demonstrations
- 📊 Real-time progress tracking
- 💾 Results history and comparison
- 🎯 Educational explanations
- 🔄 Demo mode (works without API keys!)

### Session 3: Smart Workflows (30 minutes)

AI that remembers! We'll create:

- Workflows that pass information between steps
- AI that learns from previous steps
- Simple state management

**Run it:**

```bash
cd session3
python stateful_workflow.py  # See AI remember information
```

## 📁 What's In This Project

```
ai-agent-workshop/
├── README.md              # This guide (you're reading it!)
├── pyproject.toml         # Project configuration and dependencies
├── .env.example          # Template for your settings
├── session2_gui.py       # 🎨 Interactive web GUI for Session 2
├── run_session2_gui.py   # Launcher for the GUI
├── session1/             # Basic AI examples
│   ├── basics.py         # Your first AI agents
│   └── crewai_intro.py   # AI working in teams
├── session2/             # AI collaboration
│   ├── agent_roles.py    # Different AI jobs
│   └── content_crew.py   # AI creating content together
├── session3/             # Smart workflows
│   └── stateful_workflow.py  # AI that remembers
└── utils/                # Helper tools (you don't need to change these)
    ├── config.py         # Configuration management
    ├── helpers.py        # Utility functions
    └── rate_limiter.py   # 🆕 Intelligent API rate limiting
```

## 🏗️ Code Architecture Diagram

```mermaid
flowchart TD
    %% Configuration files
    envFile[📄 .env<br/>Environment Variables]
    pyproject[📄 pyproject.toml<br/>Dependencies]
    configPy[📄 utils/config.py<br/>Configuration Management]

    %% Utility files
    helpers[📄 utils/helpers.py<br/>Helper Functions]
    rateLimiter[📄 utils/rate_limiter.py<br/>API Rate Limiting]

    %% Session 1 files
    basics[📄 session1/basics.py<br/>Basic Chat & Tools]
    crewaiIntro[📄 session1/crewai_intro.py<br/>Agent Teams Intro]

    %% Session 2 files
    agentRoles[📄 session2/agent_roles.py<br/>Agent Roles & Tasks]
    contentCrew[📄 session2/content_crew.py<br/>Content Creation]
    agentRolesGui[📄 session2/agent_roles_gui.py<br/>GUI Interface]

    %% Session 3 files
    statefulWF[📄 session3/stateful_workflow.py<br/>Stateful Workflows]
    langgraphBasics[📄 session3/langgraph_basics.py<br/>Graph Basics]

    %% External frameworks
    langchain[(🤖 LangChain)]
    crewai[(👥 CrewAI)]
    langgraph[(📊 LangGraph)]
    litellm[(🌐 LiteLLM)]
    streamlit[(🎨 Streamlit)]

    %% Connections
    envFile --> configPy
    pyproject --> configPy
    configPy --> helpers
    configPy --> rateLimiter
    configPy --> basics
    configPy --> crewaiIntro
    configPy --> agentRoles
    configPy --> contentCrew
    configPy --> agentRolesGui
    configPy --> statefulWF
    configPy --> langgraphBasics

    rateLimiter --> basics
    rateLimiter --> crewaiIntro
    rateLimiter --> agentRoles
    rateLimiter --> contentCrew
    rateLimiter --> agentRolesGui
    rateLimiter --> statefulWF
    rateLimiter --> langgraphBasics

    basics --> langchain
    crewaiIntro --> crewai
    agentRoles --> crewai
    contentCrew --> crewai
    agentRolesGui --> streamlit
    statefulWF --> langgraph
    langgraphBasics --> langgraph

    langchain --> litellm
    crewai --> litellm
    langgraph --> litellm
```

## 🆘 Having Problems?

### "API Key Not Working"

- Check your `.env` file has the correct key from OpenRouter
- Make sure there are no extra spaces
- Try copying the key again from OpenRouter

### "Rate Limit Exceeded"

The workshop includes **intelligent rate limiting** to handle API limits gracefully:

- **Free accounts**: 50 requests/day limit on OpenRouter
- **Automatic retries**: Scripts retry failed requests with exponential backoff
- **Smart timing**: Extracts exact reset times from API responses

**Solutions:**

- Add $10 credits to OpenRouter for 1000 daily requests
- Wait for the daily reset (usually midnight UTC)
- The rate limiter will automatically handle temporary limits

### "Package Installation Failed"

```bash
# Try reinstalling dependencies
uv sync --reinstall
```

### "Python Not Found"

- Download Python from python.org (version 3.8+)
- Make sure `python` command works in terminal

### Still Stuck?

- Check that all files are in the right folders
- Try running: `python -c "print('Python works!')"`
- Ask for help - you're learning something new! 🚀

## 🎉 You're Done!

**Congratulations!** You've learned about AI agents. What you built:

- 🤖 AI that can chat and use tools
- 👥 AI agents working as a team
- 🧠 AI that remembers information between steps
- ⚡ **Production-ready features**: Intelligent rate limiting, error handling, and API resilience

## Next Steps

Ready for more? Try:

- Change the questions in the examples
- Add your own AI agents
- Build something fun with what you learned!

---

**Happy AI Building!** 🚀🤖
