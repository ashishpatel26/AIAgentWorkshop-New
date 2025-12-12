"""
Session 2: Content Creation Crew
This file demonstrates a complete multi-agent system for content creation using CrewAI.
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

def create_content_creation_crew(topic: str = "AI Agents"):
    """Create a content creation crew with researcher, writer, and editor agents."""

    # Use configured LLM
    llm = get_llm()

    # Create agents with specific roles
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Conduct thorough research and gather comprehensive information on topics",
        backstory="""You are a senior research analyst with years of experience in gathering
        and synthesizing information from various sources. You excel at finding accurate,
        up-to-date information and organizing it in a structured way.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    writer = Agent(
        role="Content Writer",
        goal="Create engaging, well-structured content based on research findings",
        backstory="""You are a skilled content writer who transforms complex research into
        compelling, easy-to-understand narratives. You focus on clarity, engagement,
        and logical flow in your writing.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    editor = Agent(
        role="Content Editor",
        goal="Review, refine, and polish content for accuracy, clarity, and quality",
        backstory="""You are an experienced editor with a keen eye for detail. You ensure
        content is accurate, well-structured, grammatically correct, and engaging for
        the target audience.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    return researcher, writer, editor

def create_content_tasks(topic: str, researcher: Agent, writer: Agent, editor: Agent):
    """Create tasks for the content creation workflow."""

    # Research task
    research_task = Task(
        description=f"""Research the topic '{topic}' comprehensively. Include:
        - Key concepts and definitions
        - Current trends and developments
        - Real-world applications and examples
        - Benefits and challenges
        - Future outlook

        Provide detailed, accurate information with sources where possible.""",
        expected_output="""A comprehensive research report with:
        - Executive summary
        - Key findings organized by category
        - Supporting evidence and examples
        - References to reliable sources""",
        agent=researcher
    )

    # Writing task
    writing_task = Task(
        description=f"""Write a 500-word article about '{topic}' based on the research provided.
        The article should:
        - Have a compelling introduction
        - Cover key concepts clearly
        - Include real-world examples
        - End with future implications
        - Be written in an engaging, accessible style""",
        expected_output="""A complete article with:
        - Title
        - Introduction paragraph
        - 3-4 body paragraphs
        - Conclusion
        - Word count: approximately 500 words""",
        agent=writer,
        context=[research_task]  # Access to research results
    )

    # Editing task
    editing_task = Task(
        description=f"""Review and edit the article about '{topic}'. Focus on:
        - Factual accuracy based on research
        - Clarity and readability
        - Grammar and style
        - Logical flow and structure
        - Engagement and appeal

        Provide the final polished version.""",
        expected_output="""A polished article with:
        - Final title
        - Edited content
        - Brief notes on changes made
        - Quality assurance checklist confirmation""",
        agent=editor,
        context=[research_task, writing_task]  # Access to all previous work
    )

    return research_task, writing_task, editing_task

def run_content_creation_workflow(topic: str = "AI Agents and Multi-Agent Systems"):
    """Run the complete content creation workflow."""
    print(f"=== Content Creation Crew for: {topic} ===")
    print()

    # Create agents
    researcher, writer, editor = create_content_creation_crew(topic)

    # Create tasks
    research_task, writing_task, editing_task = create_content_tasks(
        topic, researcher, writer, editor
    )

    # Create and configure the crew
    content_crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        verbose=True,
        process="sequential",                  # Tasks run in sequence
        memory=True,                           # Enable memory
        cache=True,                            # Enable caching
        max_rpm=1                              # Rate limiting (further reduced)
    )

    # Execute the workflow
    print("🚀 Starting content creation workflow...")
    print()

    result = content_crew.kickoff()

    print("\n" + "="*80)
    print("🎉 CONTENT CREATION COMPLETE!")
    print("="*80)
    print(f"\nFinal Result:\n{result}")

    return result

def main():
    """Run the content creation crew example."""
    print("AI Agent Workshop - Session 2: Content Creation Crew")
    print("=" * 65)

    try:
        # Ask user for topic
        try:
            topic = input("What topic would you like the content creation team to write about? (press Enter for default): ").strip()
            if not topic:
                topic = "The Future of Multi-Agent AI Systems"
        except EOFError:
            # Handle non-interactive environments
            topic = "The Future of Multi-Agent AI Systems"
            print("What topic would you like the content creation team to write about? (press Enter for default): ")
            print("(Using default topic in non-interactive environment)")

        result = run_content_creation_workflow(topic)

        print("\n✅ Content creation workflow completed successfully!")
        print("\n💡 Try modifying the topic variable to create content on different subjects!")

    except Exception as e:
        print(f"❌ Error running content creation crew: {e}")
        if PROVIDER == 'sambanova':
            print("Make sure your SAMBA_API_KEY is set correctly in the .env file.")
        elif PROVIDER == 'ollama':
            print("Make sure Ollama is running locally on http://localhost:11434")
            print("Install Ollama from https://ollama.ai and run: ollama serve")
        print("Also ensure all required packages are installed.")

if __name__ == "__main__":
    main()
