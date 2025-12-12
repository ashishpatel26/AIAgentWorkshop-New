"""
Session 2: Agent Roles and Responsibilities
This file shows how different AI agents can have different jobs and work together.
Just like in a real company, each agent has a special role and expertise.
"""

from crewai import Agent, Task, Crew, LLM
from config import API_KEY, MODEL, API_BASE, TEMPERATURE, MAX_TOKENS, MAX_RETRIES, RETRY_DELAY, PROVIDER

# Step 3: Set up environment for LiteLLM
import os
if PROVIDER == 'sambanova':
    os.environ["SAMBANOVA_API_KEY"] = API_KEY
elif PROVIDER == 'ollama':
    # Ollama doesn't need environment variables
    pass

def get_llm():
    """Get the appropriate LLM configuration based on provider."""
    if PROVIDER == 'ollama':
        return LLM(
            model=f"ollama/{MODEL}",
            base_url="http://localhost:11434"
        )
    elif PROVIDER == 'sambanova':
        return LLM(
            model=f"sambanova/{MODEL}",
            api_key=API_KEY,
            base_url=API_BASE
        )
    else:
        # Default fallback
        return f"{PROVIDER}/{MODEL}"

def demonstrate_agent_roles():
    """Example: Different AI agents with different jobs working together."""
    print("=== Example: Team of AI Agents with Different Roles ===")
    print("This shows how AI agents can be like a team where each has a special job.")
    print()

    # Use configured LLM
    llm = get_llm()

    print("Creating our AI team members...")

    # Agent 1: Data Analyst (like a number cruncher)
    analyst = Agent(
        role="Data Analyst",                           # Job title
        goal="Look at data and find useful patterns",  # What they do
        backstory="I love working with numbers and finding hidden insights in data.",  # Personality
        llm=llm,
        verbose=True                                   # Show thinking
    )

    # Agent 2: Business Strategist (like a business planner)
    strategist = Agent(
        role="Business Strategist",
        goal="Create plans based on data insights",
        backstory="I am good at making business plans and giving advice for growth.",
        llm=llm,
        verbose=True
    )

    print("Giving jobs to our AI team...")

    # Job 1: Analyze some data (for the analyst)
    analysis_task = Task(
        description="Look at this simple sales data: Q1 sales were $10,000, Q2 were $12,000, Q3 were $15,000. Find trends.",
        expected_output="Tell me if sales are going up or down, and by how much.",
        agent=analyst
    )

    # Job 2: Make a business plan (for the strategist - they can see the analyst's work)
    strategy_task = Task(
        description="Based on the sales analysis, suggest 2 ways to increase sales next quarter.",
        expected_output="Two simple suggestions for growing the business.",
        agent=strategist,
        context=[analysis_task]  # Strategist can read analyst's results
    )

    print("Starting the team to work...")
    # Create the team (crew) with both agents and their jobs
    business_crew = Crew(
        agents=[analyst, strategist],           # Team members
        tasks=[analysis_task, strategy_task],   # Jobs to do (in order)
        verbose=True,                          # Show progress
        memory=True,                           # Enable memory
        cache=True,                            # Enable caching
        max_rpm=1                              # Rate limiting
    )

    # Start the work!
    result = business_crew.kickoff()

    print("\nFinal Team Result:")
    print(result)
    print()

def show_simple_roles():
    """Simple example showing just two different roles."""
    print("=== Simple Example: Two Different Jobs ===")
    print("Let's see how two agents with different skills work together.")
    print()

    # Use configured LLM
    llm = get_llm()

    # Create two simple agents
    chef = Agent(
        role="Chef",
        goal="Create and describe recipes",
        backstory="I am a creative chef who loves making delicious food.",
        llm=llm,
        verbose=True
    )

    nutritionist = Agent(
        role="Nutritionist",
        goal="Check if food is healthy",
        backstory="I am a health expert who makes sure food is good for you.",
        llm=llm,
        verbose=True
    )

    # Tasks
    recipe_task = Task(
        description="Create a simple recipe for chocolate chip cookies.",
        expected_output="List ingredients and basic steps.",
        agent=chef
    )

    health_task = Task(
        description="Check if this cookie recipe is healthy and suggest improvements.",
        expected_output="Say if it's healthy and give one healthy tip.",
        agent=nutritionist,
        context=[recipe_task]  # Can see the recipe
    )

    # Create and run crew
    food_crew = Crew(
        agents=[chef, nutritionist],
        tasks=[recipe_task, health_task],
        verbose=True,
        memory=True,                           # Enable memory
        cache=True,                            # Enable caching
        max_rpm=1                              # Rate limiting
    )

    result = food_crew.kickoff()
    print(f"Food Team Result:\n{result}")
    print()

def main():
    """Run the agent roles examples."""
    print("AI Agent Workshop - Session 2: Agent Roles and Team Work")
    print("=" * 70)
    print("Welcome! Today we'll learn about different AI agent roles.")
    print("Just like people in a company, AI agents can have different jobs.")
    print("Let's see how they work together as a team!")
    print()

    try:
        # Run the business example
        demonstrate_agent_roles()

        # Run the simple food example
        show_simple_roles()

        print("Great work! You learned about AI agent roles!")
        print("Each agent has special skills, just like people in a team.")

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        if PROVIDER == 'sambanova':
            print("Make sure your SAMBA_API_KEY is set correctly in the .env file.")
        elif PROVIDER == 'ollama':
            print("Make sure Ollama is running locally on http://localhost:11434")
            print("Install Ollama from https://ollama.ai and run: ollama serve")
        print("Check the README.md for help.")

if __name__ == "__main__":
    main()
