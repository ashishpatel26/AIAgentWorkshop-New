"""
Session 3: Simple Stateful Workflows
This file shows how AI agents can "remember" information and pass it between steps.
Stateful means the workflow remembers what happened in previous steps!
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from utils.config import get_config
from utils.rate_limiter import create_rate_limited_llm

# Step 1: Load our settings
load_dotenv()

# Step 2: Get AI configuration
config = get_config()
agent_config = config.get_agent_config()

# Define what information our workflow will remember (state)
class WorkflowState(TypedDict):
    """This is like a notebook where we write down information as we go."""
    user_question: str                    # The original question
    research_notes: Optional[str]         # What we learned from research
    answer_draft: Optional[str]           # First attempt at answering
    final_answer: Optional[str]           # The polished final answer
    current_step: str                     # Where we are in the process

def research_step(state: WorkflowState) -> WorkflowState:
    """Step 1: Research the topic."""
    print("Step 1: Researching the topic...")

    question = state["user_question"]

    # Create a researcher AI agent with rate limiting
    llm = create_rate_limited_llm(agent_config)

    researcher = Agent(
        role="Researcher",
        goal="Find helpful information about topics",
        backstory="I am a curious researcher who loves learning new things.",
        llm=llm,
        verbose=True
    )

    # Give the researcher a job
    research_task = Task(
        description=f"Research this question and find key facts: {question}",
        expected_output="Write down 3-4 important facts about the topic.",
        agent=researcher
    )

    # Do the research
    crew = Crew(agents=[researcher], tasks=[research_task], verbose=True)
    research_result = crew.kickoff()

    # Save what we learned in our "notebook" (state)
    new_state = state.copy()
    new_state["research_notes"] = str(research_result)
    new_state["current_step"] = "researched"

    print("Research complete! Saved notes for next step.")
    return new_state

def draft_answer_step(state: WorkflowState) -> WorkflowState:
    """Step 2: Use research to create a draft answer."""
    print("Step 2: Writing a draft answer...")

    question = state["user_question"]
    research = state["research_notes"]

    # Create a writer AI agent with rate limiting
    llm = create_rate_limited_llm(agent_config)

    writer = Agent(
        role="Writer",
        goal="Write clear and helpful answers",
        backstory="I am a writer who explains things in simple ways.",
        llm=llm,
        verbose=True
    )

    # Give the writer a job (they can see the research notes!)
    writing_task = Task(
        description=f"Using this research information, write a draft answer to: {question}\n\nResearch: {research}",
        expected_output="Write a clear draft answer in 2-3 sentences.",
        agent=writer
    )

    # Write the draft
    crew = Crew(agents=[writer], tasks=[writing_task], verbose=True)
    draft_result = crew.kickoff()

    # Save the draft in our notebook
    new_state = state.copy()
    new_state["answer_draft"] = str(draft_result)
    new_state["current_step"] = "drafted"

    print("Draft written! Saved for final review.")
    return new_state

def final_answer_step(state: WorkflowState) -> WorkflowState:
    """Step 3: Review and polish the final answer."""
    print("Step 3: Creating the final polished answer...")

    question = state["user_question"]
    research = state["research_notes"]
    draft = state["answer_draft"]

    # Create an editor AI agent with rate limiting
    llm = create_rate_limited_llm(agent_config)

    editor = Agent(
        role="Editor",
        goal="Make answers clear and perfect",
        backstory="I am an editor who polishes writing to make it excellent.",
        llm=llm,
        verbose=True
    )

    # Give the editor a job (they can see everything!)
    editing_task = Task(
        description=f"""Review and improve this draft answer. Make it perfect!

Question: {question}
Research: {research}
Draft: {draft}

Make the final answer clear, accurate, and helpful.""",
        expected_output="Write the final polished answer.",
        agent=editor
    )

    # Create the final answer
    crew = Crew(agents=[editor], tasks=[editing_task], verbose=True)
    final_result = crew.kickoff()

    # Save the final answer
    new_state = state.copy()
    new_state["final_answer"] = str(final_result)
    new_state["current_step"] = "complete"

    print("Final answer ready!")
    return new_state

def decide_next_step(state: WorkflowState) -> str:
    """Decide which step to do next based on where we are."""
    step = state.get("current_step", "start")

    if step == "start":
        return "research"      # Start with research
    elif step == "researched":
        return "draft"         # Research done, now draft
    elif step == "drafted":
        return "final"         # Draft done, now finalize
    else:
        return END             # All done!

def create_simple_workflow():
    """Create our simple 3-step workflow."""
    print("Building our workflow...")

    # Create the workflow
    workflow = StateGraph(WorkflowState)

    # Add our three steps
    workflow.add_node("research", research_step)
    workflow.add_node("draft", draft_answer_step)
    workflow.add_node("final", final_answer_step)

    # Connect the steps (decide which way to go)
    workflow.add_conditional_edges(
        "research",
        decide_next_step,
        {"draft": "draft", END: END}
    )

    workflow.add_conditional_edges(
        "draft",
        decide_next_step,
        {"final": "final", END: END}
    )

    workflow.add_conditional_edges(
        "final",
        decide_next_step,
        {END: END}
    )

    # Start with research
    workflow.set_entry_point("research")

    # Build the workflow
    app = workflow.compile()

    print("Workflow ready!")
    return app

def run_simple_workflow():
    """Run our simple stateful workflow example."""
    print("Running Simple Stateful Workflow")
    print("=" * 50)
    print("This workflow remembers information between steps!")
    print()

    # Create the workflow
    app = create_simple_workflow()

    # Our question
    question = "What are the benefits of eating healthy food?"

    # Start with empty notebook (state)
    starting_state = {
        "user_question": question,
        "research_notes": None,
        "answer_draft": None,
        "final_answer": None,
        "current_step": "start"
    }

    print(f"Question: {question}")
    print("Let's see how the workflow remembers information...")
    print()

    # Run the workflow!
    final_state = app.invoke(starting_state)

    print("\n" + "="*60)
    print("WORKFLOW COMPLETE!")
    print("="*60)

    print("\nWhat the workflow remembered:")
    print(f"  • Research Notes: {len(final_state.get('research_notes', ''))} characters")
    print(f"  • Draft Answer: {len(final_state.get('answer_draft', ''))} characters")
    print(f"  • Final Answer: {len(final_state.get('final_answer', ''))} characters")

    print(f"\nFinal Answer:\n{final_state.get('final_answer', 'No answer available')}")

    return final_state

def main():
    """Run the simple stateful workflow example."""
    print("AI Agent Workshop - Session 3: Simple Stateful Workflows")
    print("=" * 70)
    print("Welcome! Today we'll learn about workflows that remember information.")
    print("This is called 'state' - like how you remember things from step to step.")
    print()

    try:
        # Run our simple workflow
        result = run_simple_workflow()

        print("\nSimple workflow completed successfully!")
        print("\nWhat you learned:")
        print("   • Workflows can remember information between steps")
        print("   • Each step can use what previous steps learned")
        print("   • State helps agents work together better")

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        print("Make sure your OPENROUTER_API_KEY is set correctly in the .env file.")
        print("Check the README.md for setup help.")

if __name__ == "__main__":
    main()
