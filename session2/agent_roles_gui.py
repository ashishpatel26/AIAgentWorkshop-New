"""
Agent Roles GUI - Interactive AI Agent Workshop
A beautiful Streamlit interface for exploring agent roles and collaboration from session2/agent_roles.py
"""

import streamlit as st
import time
from typing import Dict, List
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from utils.config import get_config

# Load environment
load_dotenv()
config = get_config()
agent_config = config.get_agent_config()

# Custom CSS for beautiful design
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    .agent-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }

    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }

    .team-member {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .result-container {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .progress-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem;
        border: 1px solid #f0f0f0;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .floating-animation {
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    .stTextArea>div>textarea {
        border-radius: 8px !important;
        border: 2px solid #e1e8ed !important;
        transition: border-color 0.3s ease !important;
    }

    .stTextArea>div>textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Agent creation functions
def create_business_team_agents():
    """Create business analysis team agents."""
    llm = f"openrouter/{agent_config['model']}"
    analyst = Agent(
        role="Data Analyst",
        goal="Look at data and find useful patterns",
        backstory="I love working with numbers and finding hidden insights in data.",
        llm=llm,
        verbose=False
    )
    strategist = Agent(
        role="Business Strategist",
        goal="Create plans based on data insights",
        backstory="I am good at making business plans and giving advice for growth.",
        llm=llm,
        verbose=False
    )
    return analyst, strategist

def create_food_team_agents():
    """Create food preparation team agents."""
    llm = f"openrouter/{agent_config['model']}"
    chef = Agent(
        role="Chef",
        goal="Create and describe recipes",
        backstory="I am a creative chef who loves making delicious food.",
        llm=llm,
        verbose=False
    )
    nutritionist = Agent(
        role="Nutritionist",
        goal="Check if food is healthy",
        backstory="I am a health expert who makes sure food is good for you.",
        llm=llm,
        verbose=False
    )
    return chef, nutritionist

# Analysis functions
def run_business_team_analysis(sales_data):
    """Run business team analysis with fallback for demo."""
    try:
        analyst, strategist = create_business_team_agents()

        analysis_task = Task(
            description=f"Look at this simple sales data: {sales_data}. Find trends.",
            expected_output="Tell me if sales are going up or down, and by how much.",
            agent=analyst
        )

        strategy_task = Task(
            description="Based on the sales analysis, suggest 2 ways to increase sales next quarter.",
            expected_output="Two simple suggestions for growing the business.",
            agent=strategist,
            context=[analysis_task]
        )

        crew = Crew(agents=[analyst, strategist], tasks=[analysis_task, strategy_task], verbose=False)
        result = crew.kickoff()
        return f"Business Team Analysis Complete!\n\nSales Data: {sales_data}\n\nResult:\n{str(result)}"
    except Exception as e:
        # Fallback demo response
        return f"""Business Team Analysis Complete!

Sales Data: {sales_data}

Result:
📊 Data Analyst Findings:
- Sales show an upward trend over the quarters
- Growth rate: Approximately 25-30% quarter over quarter
- Strong performance in Q3 and Q4

🎯 Business Strategist Recommendations:
1. Continue marketing campaigns that drove Q3-Q4 growth
2. Expand successful product lines identified in the analysis
3. Consider seasonal promotions to maintain momentum

*Note: This is a demo response. Set up your OPENROUTER_API_KEY for real AI analysis.*"""

def run_food_team_analysis(recipe_request):
    """Run food team analysis with fallback for demo."""
    try:
        chef, nutritionist = create_food_team_agents()

        recipe_task = Task(
            description=f"Create a simple recipe for {recipe_request}.",
            expected_output="List ingredients and basic steps.",
            agent=chef
        )

        health_task = Task(
            description="Check if this cookie recipe is healthy and suggest improvements.",
            expected_output="Say if it's healthy and give one healthy tip.",
            agent=nutritionist,
            context=[recipe_task]
        )

        crew = Crew(agents=[chef, nutritionist], tasks=[recipe_task, health_task], verbose=False)
        result = crew.kickoff()
        return f"Food Team Analysis Complete!\n\nRecipe Request: {recipe_request}\n\nResult:\n{str(result)}"
    except Exception as e:
        # Fallback demo response
        return f"""Culinary Analysis Complete!

Recipe Request: {recipe_request}

👨‍🍳 Chef's Recipe:
Ingredients:
- 2 cups all-purpose flour
- 1 cup butter, softened
- 3/4 cup granulated sugar
- 1 cup chocolate chips
- 1 tsp vanilla extract
- 1/2 tsp baking soda
- 1/4 tsp salt

Instructions:
1. Preheat oven to 375°F (190°C)
2. Cream together butter and sugars
3. Beat in eggs and vanilla
4. Combine flour, baking soda, and salt
5. Stir in chocolate chips
6. Drop spoonfuls onto baking sheet
7. Bake for 9-11 minutes

🥗 Nutritionist's Analysis:
These cookies are a treat but high in sugar and fats. Suggestions:
- Use whole wheat flour instead of all-purpose
- Reduce sugar by 1/4 cup and add applesauce
- Include nuts for healthy fats and protein
- Portion control: 1-2 cookies per serving

*Note: This is a demo response. Set up your OPENROUTER_API_KEY for real AI analysis.*"""

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Agent Roles Workshop",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css()

    # Initialize session state
    if 'results_history' not in st.session_state:
        st.session_state.results_history = []

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/user-group-man-woman.png", width=80)
        st.title("Agent Roles Workshop")
        st.markdown("---")

        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Teams", "2")
        with col2:
            st.metric("Runs", len(st.session_state.results_history))

        st.markdown("---")
        st.markdown("### About")
        st.write("Explore how AI agents with different roles collaborate on tasks!")

        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.results_history = []
            st.success("History cleared!")

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">👥 Agent Roles Workshop</h1>
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem;">AI Agents Working Together</h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">See how different AI agents collaborate like a real team!</p>
    </div>
    """, unsafe_allow_html=True)

    # Team selection
    st.markdown("## 🎯 Choose Your AI Agent Team")

    team_choice = st.radio(
        "Select a team to explore:",
        ["📊 Business Analysis Team", "🍳 Food Preparation Team"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Business Team Section
    if team_choice == "📊 Business Analysis Team":
        st.markdown("### 📊 Business Intelligence Team")
        st.write("**Data Analyst + Business Strategist** working together to analyze business data and create growth strategies.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="team-member">
                <h4>📈 Data Analyst</h4>
                <p>Analyzes sales data and finds patterns</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="team-member">
                <h4>🎯 Business Strategist</h4>
                <p>Creates growth strategies from insights</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 💼 Enter Your Sales Data")
        user_input = st.text_area(
            "Sales data to analyze:",
            placeholder="Example: Q1 sales were $10,000, Q2 were $12,000, Q3 were $15,000",
            height=100,
            key="business_input",
            help="Enter sales data and the AI team will analyze trends and suggest strategies!"
        )

        if st.button("🚀 Analyze Business Data", type="primary", use_container_width=True):
            if not user_input.strip():
                st.warning("Please enter some sales data to analyze!")
            else:
                with st.spinner("🤖 AI agents are analyzing your business data..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 40:
                            status_text.text("Data Analyst examining patterns...")
                        elif i < 80:
                            status_text.text("Business Strategist developing strategies...")
                        else:
                            status_text.text("Finalizing business recommendations...")
                        time.sleep(0.02)

                    result = run_business_team_analysis(user_input)
                    st.session_state.results_history.append({
                        "team": "Business Analysis",
                        "input": user_input,
                        "result": result,
                        "timestamp": time.time()
                    })

                st.success("✅ Business Analysis Complete!")
                st.markdown("### 📄 Analysis Results")
                st.markdown(result)

    # Food Team Section
    else:
        st.markdown("### 🍳 Culinary Innovation Team")
        st.write("**Chef + Nutritionist** collaborating to create healthy, delicious recipes.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="team-member">
                <h4>👨‍🍳 Master Chef</h4>
                <p>Creates delicious recipes</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="team-member">
                <h4>🥗 Nutrition Expert</h4>
                <p>Ensures recipes are healthy</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🍽️ Enter Your Recipe Request")
        user_input = st.text_area(
            "What would you like to cook?",
            placeholder="Example: chocolate chip cookies",
            height=100,
            key="food_input",
            help="Enter a recipe request and the AI team will create and analyze it!"
        )

        if st.button("🍳 Create & Analyze Recipe", type="primary", use_container_width=True):
            if not user_input.strip():
                st.warning("Please enter a recipe request!")
            else:
                with st.spinner("🤖 Chef and nutritionist are collaborating..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 45:
                            status_text.text("Chef crafting the perfect recipe...")
                        elif i < 90:
                            status_text.text("Nutritionist analyzing nutritional balance...")
                        else:
                            status_text.text("Finalizing healthy recipe recommendations...")
                        time.sleep(0.02)

                    result = run_food_team_analysis(user_input)
                    st.session_state.results_history.append({
                        "team": "Food Preparation",
                        "input": user_input,
                        "result": result,
                        "timestamp": time.time()
                    })

                st.success("✅ Recipe Complete!")
                st.markdown("### 📄 Recipe & Analysis")
                st.markdown(result)

    # Results History
    if st.session_state.results_history:
        st.markdown("---")
        st.markdown("## 📈 Recent Results")

        for i, result in enumerate(reversed(st.session_state.results_history[-3:])):  # Show last 3
            with st.expander(f"{result['team']} - {result['input'][:40]}..."):
                st.write(f"**Team:** {result['team']}")
                st.write(f"**Input:** {result['input']}")
                st.write(f"**Time:** {time.strftime('%H:%M:%S', time.localtime(result['timestamp']))}")
                st.code(result['result'], language=None)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Session 2:</strong> Learning about AI agent roles and team collaboration</p>
        <p>Each agent has specialized skills, just like people in a real team!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()