"""
Session 3: LangGraph Basics with NVIDIA API
This file demonstrates fundamental LangGraph concepts for building stateful agent workflows using NVIDIA API.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# Load environment variables
load_dotenv()

# NVIDIA API Configuration
NVIDIA_API_KEY = "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"

# Define the state structure
class AgentState(TypedDict):
    """State definition for our agent workflow."""
    user_query: str
    research_result: Optional[str]
    analysis_result: Optional[str]
    final_answer: Optional[str]
    current_step: str

def create_langgraph_workflow():
    """Create a basic LangGraph workflow with nodes and edges."""

    # Initialize the LLM using NVIDIA API
    llm = ChatOpenAI(
        temperature=0.7,
        model="meta/llama3-8b-instruct",
        api_key=NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1"
    )

    def research_node(state: AgentState) -> AgentState:
        """Research node that gathers information."""
        print("🔍 Researching topic...")

        query = state["user_query"]
        research_prompt = f"""Research the following topic comprehensively: {query}

        Provide:
        - Key concepts and definitions
        - Current trends and developments
        - Real-world applications
        - Important considerations

        Be thorough but concise."""

        response = llm.invoke([{"role": "user", "content": research_prompt}])
        research_result = response.content

        # Update state
        new_state = state.copy()
        new_state["research_result"] = research_result
        new_state["current_step"] = "research_complete"

        print(f"✅ Research completed for: {query[:50]}...")
        return new_state

    def analyze_node(state: AgentState) -> AgentState:
        """Analysis node that processes research findings."""
        print("📊 Analyzing research findings...")

        research = state["research_result"]
        analysis_prompt = f"""Analyze the following research and provide insights:

        RESEARCH:
        {research}

        Provide:
        - Key insights and patterns
        - Strengths and limitations
        - Practical implications
        - Recommendations"""

        response = llm.invoke([{"role": "user", "content": analysis_prompt}])
        analysis_result = response.content

        # Update state
        new_state = state.copy()
        new_state["analysis_result"] = analysis_result
        new_state["current_step"] = "analysis_complete"

        print("✅ Analysis completed")
        return new_state

    def answer_node(state: AgentState) -> AgentState:
        """Final answer node that synthesizes everything."""
        print("💡 Generating final answer...")

        query = state["user_query"]
        research = state["research_result"]
        analysis = state["analysis_result"]

        final_prompt = f"""Based on the research and analysis provided, give a comprehensive answer to: {query}

        RESEARCH:
        {research}

        ANALYSIS:
        {analysis}

        Provide a clear, well-structured final answer."""

        response = llm.invoke([{"role": "user", "content": final_prompt}])
        final_answer = response.content

        # Update state
        new_state = state.copy()
        new_state["final_answer"] = final_answer
        new_state["current_step"] = "answer_complete"

        print("✅ Final answer generated")
        return new_state

    def router_function(state: AgentState) -> str:
        """Router function to decide next step based on state."""
        current_step = state.get("current_step", "start")

        if current_step == "start":
            return "research"
        elif current_step == "research_complete":
            return "analyze"
        elif current_step == "analysis_complete":
            return "answer"
        else:
            return END

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("answer", answer_node)

    # Add edges
    workflow.add_conditional_edges(
        "research",
        router_function,
        {"analyze": "analyze", "answer": "answer", END: END}
    )

    workflow.add_conditional_edges(
        "analyze",
        router_function,
        {"answer": "answer", END: END}
    )

    workflow.add_conditional_edges(
        "answer",
        router_function,
        {END: END}
    )

    # Set entry point
    workflow.set_entry_point("research")

    # Compile the graph
    app = workflow.compile()

    return app

def run_basic_langgraph_example():
    """Run a basic LangGraph workflow example."""
    print("=== Basic LangGraph Workflow Example (NVIDIA API) ===")
    print()

    # Create the workflow
    app = create_langgraph_workflow()

    # Initial state
    initial_state = {
        "user_query": "What are the benefits and challenges of implementing AI agents in business processes?",
        "research_result": None,
        "analysis_result": None,
        "final_answer": None,
        "current_step": "start"
    }

    print("Starting workflow execution...")
    print(f"Query: {initial_state['user_query']}")
    print()

    # Execute the workflow
    final_state = app.invoke(initial_state)

    print("\n" + "="*80)
    print("🎉 WORKFLOW EXECUTION COMPLETE!")
    print("="*80)

    print(f"\nFinal Answer:\n{final_state['final_answer']}")

    print("\n📊 Workflow Summary:")
    print(f"  • Research Result Length: {len(final_state.get('research_result', ''))} characters")
    print(f"  • Analysis Result Length: {len(final_state.get('analysis_result', ''))} characters")
    print(f"  • Final Answer Length: {len(final_state.get('final_answer', ''))} characters")

    return final_state

def demonstrate_conditional_routing():
    """Demonstrate conditional routing in LangGraph."""

    print("\n=== Conditional Routing Example (NVIDIA API) ===")
    print()

    class QueryState(TypedDict):
        query: str
        query_type: Optional[str]
        response: Optional[str]

    # Initialize the LLM using NVIDIA API
    llm = ChatOpenAI(
        temperature=0.7,
        model="meta/llama3-8b-instruct",
        api_key=NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1"
    )

    def classify_query(state: QueryState) -> QueryState:
        """Classify the query type."""
        query = state["query"]
        classify_prompt = f"""Classify this query as either 'simple' or 'complex':

        Query: {query}

        Simple queries can be answered directly with basic knowledge.
        Complex queries require research and detailed analysis.

        Respond with only: simple or complex"""

        response = llm.invoke([{"role": "user", "content": classify_prompt}])
        query_type = response.content.strip().lower()

        new_state = state.copy()
        new_state["query_type"] = query_type
        return new_state

    def simple_response(state: QueryState) -> QueryState:
        """Handle simple queries."""
        query = state["query"]
        response_prompt = f"Answer this simple query directly: {query}"

        response = llm.invoke([{"role": "user", "content": response_prompt}])
        answer = response.content

        new_state = state.copy()
        new_state["response"] = f"[SIMPLE] {answer}"
        return new_state

    def complex_response(state: QueryState) -> QueryState:
        """Handle complex queries."""
        query = state["query"]
        response_prompt = f"Provide a detailed analysis for this complex query: {query}"

        response = llm.invoke([{"role": "user", "content": response_prompt}])
        answer = response.content

        new_state = state.copy()
        new_state["response"] = f"[COMPLEX] {answer}"
        return new_state

    def route_based_on_complexity(state: QueryState) -> str:
        """Route to appropriate handler based on query complexity."""
        query_type = state.get("query_type")
        if query_type == "simple":
            return "simple_handler"
        elif query_type == "complex":
            return "complex_handler"
        else:
            return "simple_handler"  # fallback

    # Create conditional workflow
    workflow = StateGraph(QueryState)

    workflow.add_node("classifier", classify_query)
    workflow.add_node("simple_handler", simple_response)
    workflow.add_node("complex_handler", complex_response)

    workflow.set_entry_point("classifier")

    workflow.add_conditional_edges(
        "classifier",
        route_based_on_complexity,
        {
            "simple_handler": "simple_handler",
            "complex_handler": "complex_handler"
        }
    )

    workflow.add_edge("simple_handler", END)
    workflow.add_edge("complex_handler", END)

    app = workflow.compile()

    # Test with different queries
    test_queries = [
        "What is 2 + 2?",
        "Explain quantum computing and its business applications"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = app.invoke({"query": query, "query_type": None, "response": None})
        print(f"Response: {result['response'][:100]}...")

def main():
    """Run LangGraph basics examples."""
    print("AI Agent Workshop - Session 3: LangGraph Basics (NVIDIA API)")
    print("=" * 60)

    try:
        # Run basic workflow example
        run_basic_langgraph_example()

        # Demonstrate conditional routing
        demonstrate_conditional_routing()

        print("\n✅ LangGraph basics with NVIDIA API completed successfully!")
        print("\n💡 Key Concepts Learned:")
        print("   • State management in workflows")
        print("   • Node-based graph construction")
        print("   • Conditional routing logic")
        print("   • Sequential and parallel execution")

    except Exception as e:
        print(f"Error running LangGraph examples: {e}")
        print("Make sure your NVIDIA_API_KEY is set correctly in the .env file.")
        print("Also ensure langgraph is installed: uv pip install langgraph")

if __name__ == "__main__":
    main()