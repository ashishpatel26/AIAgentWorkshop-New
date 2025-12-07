"""
Session 2: Agent Roles and Responsibilities
This file shows how different AI agents can have different jobs and work together.
Just like in a real company, each agent has a special role and expertise.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from utils.config import get_config
from utils.rate_limiter import create_rate_limited_llm

# Step 1: Load our settings
load_dotenv()

# Step 2: Get AI configuration
config = get_config()
agent_config = config.get_agent_config()

def demonstrate_agent_roles():
    """Example: Different AI agents with different jobs working together."""
    print("=== Example: Team of AI Agents with Different Roles ===")
    print("This shows how AI agents can be like a team where each has a special job.")
    print()

    # Create the AI brain for all agents with rate limiting
    llm = create_rate_limited_llm(agent_config)

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
        verbose=True                           # Show progress
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

    # Create AI brain with rate limiting
    llm = create_rate_limited_llm(agent_config)

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
        verbose=True
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
        print("Make sure your OPENROUTER_API_KEY is set correctly in the .env file.")
        print("Check the README.md for help.")

if __name__ == "__main__":
    main()
