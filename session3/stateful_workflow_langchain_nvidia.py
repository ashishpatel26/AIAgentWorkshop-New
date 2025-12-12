"""
Session 3: Simple Stateful Workflows with LangChain and NVIDIA API
This file shows how AI agents can "remember" information and pass it between steps using LangChain and NVIDIA API.
Stateful means the workflow remembers what happened in previous steps!
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# NVIDIA API Configuration
NVIDIA_API_KEY = "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"

# Define what information our workflow will remember (state)
class WorkflowState(TypedDict):
    """This is like a notebook where we write down information as we go."""
    user_question: str                    # The original question
    research_notes: Optional[str]         # What we learned from research
    answer_draft: Optional[str]           # First attempt at answering
    final_answer: Optional[str]           # The polished final answer
    current_step: str                     # Where we are in the process

def create_llm():
    """Create NVIDIA LLM using LangChain."""
    return ChatOpenAI(
        model="meta/llama3-8b-instruct",
        api_key=NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.7
    )

def research_step(state: WorkflowState) -> WorkflowState:
    """Step 1: Research the topic using LangChain."""
    print("Step 1: Researching the topic...")

    question = state["user_question"]
    llm = create_llm()

    # Create research prompt
    research_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant. Provide comprehensive information about the given topic."),
        ("human", f"Research this question and find key facts: {question}\n\nProvide 3-4 important facts about the topic.")
    ])

    # Create research chain
    research_chain = research_prompt | llm | StrOutputParser()

    # Do the research
    research_result = research_chain.invoke({})

    # Save what we learned in our "notebook" (state)
    new_state = state.copy()
    new_state["research_notes"] = research_result
    new_state["current_step"] = "researched"

    print("Research complete! Saved notes for next step.")
    return new_state

def draft_answer_step(state: WorkflowState) -> WorkflowState:
    """Step 2: Use research to create a draft answer using LangChain."""
    print("Step 2: Writing a draft answer...")

    question = state["user_question"]
    research = state["research_notes"]
    llm = create_llm()

    # Create drafting prompt
    draft_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a skilled writer who creates clear, helpful answers based on research information."),
        ("human", f"Using this research information, write a draft answer to: {question}\n\nResearch: {research}\n\nWrite a clear draft answer in 2-3 sentences.")
    ])

    # Create drafting chain
    draft_chain = draft_prompt | llm | StrOutputParser()

    # Write the draft
    draft_result = draft_chain.invoke({})

    # Save the draft in our notebook
    new_state = state.copy()
    new_state["answer_draft"] = draft_result
    new_state["current_step"] = "drafted"

    print("Draft written! Saved for final review.")
    return new_state

def final_answer_step(state: WorkflowState) -> WorkflowState:
    """Step 3: Review and polish the final answer using LangChain."""
    print("Step 3: Creating the final polished answer...")

    question = state["user_question"]
    research = state["research_notes"]
    draft = state["answer_draft"]
    llm = create_llm()

    # Create final editing prompt
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert editor who creates polished, accurate, and helpful final answers."),
        ("human", f"""Review and improve this draft answer. Make it perfect!

Question: {question}
Research: {research}
Draft: {draft}

Make the final answer clear, accurate, and helpful.""")
    ])

    # Create final chain
    final_chain = final_prompt | llm | StrOutputParser()

    # Create the final answer
    final_result = final_chain.invoke({})

    # Save the final answer
    new_state = state.copy()
    new_state["final_answer"] = final_result
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
    print("Building our LangChain workflow...")

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

    print("LangChain workflow ready!")
    return app

def run_simple_workflow():
    """Run our simple stateful workflow example."""
    print("Running Simple Stateful Workflow (LangChain + NVIDIA API)")
    print("=" * 60)
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
    print("AI Agent Workshop - Session 3: Simple Stateful Workflows (LangChain + NVIDIA API)")
    print("=" * 85)
    print("Welcome! Today we'll learn about workflows that remember information.")
    print("This is called 'state' - like how you remember things from step to step.")
    print("Using LangChain agents with NVIDIA API!")
    print()

    try:
        # Run our simple workflow
        result = run_simple_workflow()

        print("\nSimple workflow with LangChain + NVIDIA API completed successfully!")
        print("\nWhat you learned:")
        print("   • Workflows can remember information between steps")
        print("   • Each step can use what previous steps learned")
        print("   • LangChain provides powerful agent capabilities")
        print("   • NVIDIA API offers fast, reliable AI models")

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        print("Make sure your NVIDIA_API_KEY is set correctly in the .env file.")
        print("Check the README.md for setup help.")

if __name__ == "__main__":
    main()