"""
Session 1: CrewAI Introduction
This file shows how to use CrewAI to create teams of AI agents that work together.
CrewAI helps multiple AI agents collaborate on tasks, just like a real team!
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from utils.config import get_config

# Step 1: Load our settings
load_dotenv()

# Step 2: Get AI configuration
config = get_config()
agent_config = config.get_agent_config()

# Step 3: Set up environment for LiteLLM
os.environ["OPENROUTER_API_KEY"] = agent_config['api_key']

def simple_crew_example():
    """Example 1: Single AI Agent (like having one team member)"""
    print("=== Example 1: Single Agent Crew ===")
    print("This shows how one AI agent can complete a task.")
    print()

    # Ask user what topic they want researched
    research_topic = input("What topic would you like the AI researcher to explain? (press Enter for default): ").strip()
    if not research_topic:
        research_topic = "AI agents"

    # Use OpenRouter model format that LiteLLM understands
    # CrewAI will automatically use LiteLLM with this format
    llm = f"openrouter/{agent_config['model']}"

    print("Creating an AI researcher agent...")
    # Create one agent (like hiring one employee)
    researcher = Agent(
        role="Researcher",                                    # Job title
        goal="Find and explain information about topics",     # What they should do
        backstory="I am a helpful researcher who loves learning and sharing knowledge.",  # Their personality
        llm=llm,                                              # Their brain
        verbose=True                                          # Show their thinking process
    )

    print(f"Creating a research task about: {research_topic}")
    # Give the agent a job to do
    research_task = Task(
        description=f"Explain what {research_topic} are/is in simple terms that anyone can understand.",  # What to do
        expected_output="A simple explanation in 2-3 sentences.",  # What the result should look like
        agent=researcher  # Which agent does this task
    )

    print("Starting the crew (team) to work...")
    # Create a "crew" (team) with our agent and task
    crew = Crew(
        agents=[researcher],      # Team members
        tasks=[research_task],    # Jobs to do
        verbose=True             # Show progress
    )

    # Start the work!
    result = crew.kickoff()

    print(f"\nFinal Result about {research_topic}:")
    print(result)
    print()

def multi_agent_crew_example():
    """Example 2: Multiple AI Agents Working Together (like a real team)"""
    print("=== Example 2: Multi-Agent Crew (Team Work) ===")
    print("This shows how multiple AI agents can work together on a bigger project.")
    print()

    # Ask user what topic they want the team to work on
    team_topic = input("What topic would you like the AI team to research and write about? (press Enter for default): ").strip()
    if not team_topic:
        team_topic = "AI agents"

    # Use OpenRouter model format that LiteLLM understands
    # CrewAI will automatically use LiteLLM with this format
    llm = f"openrouter/{agent_config['model']}"

    print("Creating two AI agents for our team...")
    # Create two agents (like hiring two employees)
    researcher = Agent(
        role="Researcher",
        goal="Find information about topics",
        backstory="I am a curious researcher who gathers facts and information.",
        llm=llm,
        verbose=True
    )

    writer = Agent(
        role="Writer",
        goal="Write clear and interesting content",
        backstory="I am a creative writer who makes information easy to read.",
        llm=llm,
        verbose=True
    )

    print(f"Creating tasks for the team about: {team_topic}")
    # Task 1: Research (first job)
    research_task = Task(
        description=f"Find 3 benefits and 2 challenges of using {team_topic}.",
        expected_output="A simple list of benefits and challenges.",
        agent=researcher
    )

    # Task 2: Write article (second job - uses research results)
    writing_task = Task(
        description=f"Write a short paragraph about {team_topic} using the research information.",
        expected_output="One paragraph explaining the topic.",
        agent=writer,
        context=[research_task]  # Writer can see what researcher found
    )

    print("Starting the team to work together...")
    # Create crew with both agents and both tasks
    crew = Crew(
        agents=[researcher, writer],           # Our team
        tasks=[research_task, writing_task],   # Jobs in order
        verbose=True
    )

    # Start the team work!
    result = crew.kickoff()

    print(f"\nFinal Team Result about {team_topic}:")
    print(result)
    print()

def main():
    """Run the CrewAI examples."""
    print("AI Agent Workshop - Session 1: Learning About CrewAI")
    print("=" * 65)
    print("Welcome! CrewAI lets us create teams of AI agents.")
    print("Each agent has a special role, just like people in a company.")
    print("Let's see how they work alone and together!")
    print()

    try:
        # Run first example (single agent)
        simple_crew_example()

        # Run second example (team work)
        multi_agent_crew_example()

        print("Excellent! You learned about CrewAI!")
        print("Now you know how AI agents can work as a team.")

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        print("Make sure your OPENROUTER_API_KEY is set correctly in the .env file.")
        print("Check the README.md for setup help.")

if __name__ == "__main__":
    main()
