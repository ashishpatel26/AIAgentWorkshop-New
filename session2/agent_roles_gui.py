"""
Agent Roles GUI - Interactive AI Agent Workshop
A beautiful Streamlit interface for exploring agent roles and collaboration from session2/agent_roles.py
"""

import streamlit as st
import time
from typing import Dict, List
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
    llm = get_llm()
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

def create_food_team_agents(language="English"):
    """Create food preparation team agents."""
    llm = get_llm()

    if "Gujarati" in language:
        chef_backstory = "I am a master Gujarati chef specializing in traditional Gujarati cuisine, farsan, and festive dishes. I know all about Gujarati flavors, spices, and cooking techniques."
        nutritionist_backstory = "I am a nutrition expert familiar with Gujarati dietary traditions, Ayurvedic principles, and the nutritional value of traditional Gujarati ingredients."
    else:
        chef_backstory = "I am a creative chef who loves making delicious food."
        nutritionist_backstory = "I am a health expert who makes sure food is good for you."

    chef = Agent(
        role="Chef",
        goal="Create and describe recipes",
        backstory=chef_backstory,
        llm=llm,
        verbose=False
    )
    nutritionist = Agent(
        role="Nutritionist",
        goal="Check if food is healthy",
        backstory=nutritionist_backstory,
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

        crew = Crew(
            agents=[analyst, strategist],
            tasks=[analysis_task, strategy_task],
            verbose=False,
            memory=True,
            cache=True,
            max_rpm=1
        )
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

                    *Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

def run_food_team_analysis(recipe_request, language="English"):
    """Run food team analysis with fallback for demo."""
    try:
        chef, nutritionist = create_food_team_agents(language)

        # Adjust prompts based on language
        if "Gujarati" in language:
            recipe_description = f"Create a simple Gujarati recipe for {recipe_request}. Include traditional Gujarati ingredients and cooking methods. Provide the recipe in Gujarati language with English translations."
            recipe_output = "List ingredients in Gujarati with English translations and provide cooking steps in both languages."
            health_description = "Check if this Gujarati recipe is healthy according to traditional Gujarati dietary principles and suggest improvements."
        else:
            recipe_description = f"Create a simple recipe for {recipe_request}."
            recipe_output = "List ingredients and basic steps."
            health_description = "Check if this recipe is healthy and suggest improvements."

        recipe_task = Task(
            description=recipe_description,
            expected_output=recipe_output,
            agent=chef
        )

        health_task = Task(
            description=health_description,
            expected_output="Say if it's healthy and give one healthy tip.",
            agent=nutritionist,
            context=[recipe_task]
        )

        crew = Crew(
            agents=[chef, nutritionist],
            tasks=[recipe_task, health_task],
            verbose=False,
            memory=True,
            cache=True,
            max_rpm=1
        )
        result = crew.kickoff()
        return f"Food Team Analysis Complete!\n\nRecipe Request: {recipe_request}\nLanguage: {language}\n\nResult:\n{str(result)}"
    except Exception as e:
        # Fallback demo response - intelligent analysis of request
        recipe_lower = recipe_request.lower()

        if "Gujarati" in language:
            # Gujarati cuisine - analyze request context and provide thoughtful response

            # First, understand what the user is asking for
            request_analysis = ""

            # Check for specific traditional Gujarati dish names
            if any(word in recipe_lower for word in ['dhokla', 'dhoklaa', 'ઢોકળા']):
                request_analysis = "User is requesting Dhokla - a traditional Gujarati steamed snack"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ પૂર્ણ! (Gujarati Culinary Analysis Complete!)

Recipe Request: {recipe_request}
Language: {language}

👨‍🍳 રસોઇયાની રેસીપી - ઢોકળા (Chef's Recipe - Dhokla)

સામગ્રી (Ingredients - Serves 4):
- 1 કપ ચણાનો લોટ (1 cup chana flour/besan)
- 1/2 કપ દહીં (1/2 cup yogurt)
- 1 ટીસ્પૂન લીંબુનો રસ (1 tsp lemon juice)
- 1/2 ટીસ્પૂન હિંગ (1/2 tsp hing/asafoetida)
- 1 ટીસ્પૂન રાઇ (1 tsp mustard seeds)
- 2-3 લીલા મરચા (2-3 green chilies)
- ખાંડ અને મીઠું સ્વાદ મુજબ (Sugar and salt to taste)
- તલ અને ધાણા પાઉડર માટે (For garnish: sesame seeds and coriander)

સૂચનાઓ (Instructions):
1. ચણાનો લોટ, દહીં, ખાંડ, મીઠું અને પાણી મિક્સ કરો
2. લીંબુનો રસ નાખીને ફેફસો જેટલું પાતળું બેટર બનાવો
3. ગ્રીઝ કરેલી થાલીમાં નાખીને સ્ટીમ કરો 15-20 મિનિટ
4. ઠંડુ થાય પછી કટિંગ કરો
5. રાઇ, હિંગ અને લીલા મરચા ઘીમાં તડકો
6. ઢોકળા પર નાખો અને ધાણા-તલથી ગાર્નિશ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
ઢોકળા સ્ટીમ કરેલી વાનગી છે જે સ્વાસ્થ્યપ્રદ છે. પોષણ મૂલ્ય:
- ચણાનો લોટ પ્રોટીન અને આયર્નથી ભરપૂર
- દહીં કેલ્શિયમ અને પ્રોબાયોટિક્સ આપે છે
- ઓઈલ-ફ્રી સ્ટીમિંગ હાર્ટ-હેલ્ધી છે
- લીંબુ વિટામિન C નો સારો સ્ત્રોત

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

            elif any(word in recipe_lower for word in ['thepla', 'thhepla', 'થેપલા']):
                request_analysis = "User is requesting Thepla - traditional Gujarati methi flatbread"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ પૂર્ણ! (Gujarati Culinary Analysis Complete!)

Recipe Request: {recipe_request}
Language: {language}

👨‍🍳 રસોઇયાની રેસીપી - થેપલા (Chef's Recipe - Thepla)

સામગ્રી (Ingredients - Makes 8-10 theplas):
- 1 કપ ગોળ મેદો (1 cup wheat flour)
- 1/2 કપ મેથીના પાન (1/2 cup fenugreek leaves)
- 2 ટેબલસ્પૂન બેસન (2 tbsp besan/chickpea flour)
- 1 ટીસ્પૂન લાલ મરચું પાઉડર (1 tsp red chili powder)
- 1/2 ટીસ્પૂન હળદર (1/2 tsp turmeric)
- 1 ટીસ્પૂન રાઇ પાઉડર (1 tsp mustard powder)
- મીઠું અને તલ સ્વાદ મુજબ (Salt and sesame seeds to taste)
- તેલ રોટલી બનાવવા માટે (Oil for making rotis)

સૂચનાઓ (Instructions):
1. મેથીના પાન ધોઈને સૂકા કરો અને બારીક કાપો
2. બધી સામગ્રી મિક્સ કરીને મટીર જેવું લોટ બનાવો
3. ૧૫-૨૦ મિનિટ રહેવા દો
4. નાની રોટલી બનાવીને તેલમાં શેકો
5. બંને બાજુ સોનેરી થાય ત્યાં સુધી શેકો
6. ગરમ ગરમ સર્વ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
થેપલા ગુજરાતી ટ્રેડિશનલ સ્નેક છે જે ખૂબ આરોગ્યપ્રદ છે. આહાર મૂલ્ય:
- મેથીના પાન ફાઇબર અને આયર્નથી ભરપૂર
- ગોળ મેદો કોમ્પ્લેક્સ કાર્બોહાઇડ્રેટ્સ આપે છે
- મસાલા પાચન સુધારે છે
- લાંબા સમય સુધી ભૂખ ન મરે તેવું રાખે છે

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

            elif any(word in recipe_lower for word in ['khandoi', 'khandvi', 'ખંડવી']):
                request_analysis = "User is requesting Khandoi - traditional Gujarati steamed sweet"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ પૂર્ણ! (Gujarati Culinary Analysis Complete!)

Recipe Request: {recipe_request}
Language: {language}

👨‍🍳 રસોઇયાની રેસીપી - ખંડવી (Chef's Recipe - Khandoi)

સામગ્રી (Ingredients - Serves 4):
- 1 કપ ચણાનો લોટ (1 cup chana flour/besan)
- 1/2 કપ દહીં (1/2 cup yogurt)
- 1/2 કપ ખાંડ (1/2 cup sugar)
- 1/4 કપ ઘી (1/4 cup ghee)
- 1/4 ટીસ્પૂન હળદર (1/4 tsp turmeric)
- 1/4 ટીસ્પૂન એલચી પાઉડર (1/4 tsp cardamom powder)
- ચારોળી અને કાજુ માટે (For garnish: pistachios and cashews)

સૂચનાઓ (Instructions):
1. ચણાનો લોટ, દહીં, હળદર અને પાણી મિક્સ કરીને બેટર બનાવો
2. ૨ કલાક રહેવા દો (Let batter rest for 2 hours)
3. ઘીમાં ખાંડ ગોલ્ડન થાય ત્યાં સુધી ગરમ કરો
4. બેટર નાખીને હલાવતા રહો જ્યાં સુધી ઘટ્ટ ન થાય
5. થાલીમાં પાથરીને ઠંડુ કરો
6. એલચી પાઉડર અને ચારોળીથી ગાર્નિશ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
ખંડવી ગુજરાતી મીઠાઈ છે જે પ્રોટીન અને કાર્બોહાઇડ્રેટ્સથી ભરપૂર છે. આરોગ્યપ્રદ લાભ:
- ચણાનો લોટ પ્રોટીનનો સારો સ્ત્રોત છે
- દહીં પાચન સુધારે છે
- મર્યાદિત ખાંડ રાખો ડાયાબિટીસ માટે સલામત
- એલચી પાચન સહાય કરે છે

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

            # Chocolate chip cookies request
            elif any(word in recipe_lower for word in ['chocolate', 'chip', 'cookie']):
                request_analysis = "User is requesting chocolate chip cookies - a Western sweet treat"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ - વિનંતીની સમજ (Gujarati Culinary Analysis - Understanding Request)

Recipe Request: {recipe_request}
Language: {language}

🔍 વિનંતી વિશ્લેષણ (Request Analysis):
{request_analysis}

💭 વિચાર પ્રક્રિયા (Thought Process):
- ચોકલેટ ચીપ કુકીઝ એ પાશ્ચાત્ય મીઠાઈ છે (Chocolate chip cookies are a Western sweet)
- ગુજરાતી સંસ્કૃતિમાં આનું સમાણ શોધીએ (Let's find an equivalent in Gujarati culture)
- ખંડવી અથવા લાડુ જેવી મીઠાઈ વધુ યોગ્ય રહેશે (Khandoi or Laddu would be more appropriate)
- પરંતુ વિનંતી મુજબ ચોકલેટ સ્વાદ આપવો જોઈએ (But we should provide chocolate flavor as requested)

👨‍🍳 રસોઇયાની રેસીપી - ચોકલેટ ખંડવી (Chef's Recipe - Chocolate Khandoi)

સામગ્રી (Ingredients - Serves 4):
- 1 કપ ચણાનો લોટ (1 cup chana flour/besan)
- 1/2 કપ દહીં (1/2 cup yogurt)
- 1/2 કપ ખાંડ (1/2 cup sugar)
- 1/4 કપ ચોકલેટ ચીપ્સ અથવા કોકો પાઉડર (1/4 cup chocolate chips or cocoa powder)
- 1/4 કપ ઘી (1/4 cup ghee)
- 1/4 ટીસ્પૂન હળદર (1/4 tsp turmeric)
- 1/4 ટીસ્પૂન એલચી પાઉડર (1/4 tsp cardamom powder)

સૂચનાઓ (Instructions):
1. ચણાનો લોટ, દહીં, હળદર અને પાણી મિક્સ કરો
2. ચોકલેટ ચીપ્સ ગલાવીને નાખો
3. ૨ કલાક રહેવા દો
4. ઘીમાં ખાંડ ગોલ્ડન કરો
5. બેટર નાખીને ઘટ્ટ કરો
6. થાલીમાં પાથરીને ચોકલેટ ચીપ્સથી ગાર્નિશ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
આ ગુજરાતી-શૈલીની ચોકલેટ મીઠાઈ છે જે પરંપરાગત સ્વાદ સાથે મળે છે. લાભ:
- ચણાનો લોટ પ્રોટીન આપે છે
- દહીં પાચન સુધારે છે
- ચોકલેટનું મર્યાદિત પ્રમાણ આરોગ્યપ્રદ રહે છે

*Note: This is a demo response. Set up your API key for real AI analysis.*"""

            # Pizza or bread request
            elif any(word in recipe_lower for word in ['pizza', 'bread', 'pasta', 'pasta', 'noodle']):
                request_analysis = "User is requesting pizza/bread/pasta - Western comfort food"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ - વિનંતીની સમજ (Gujarati Culinary Analysis - Understanding Request)

Recipe Request: {recipe_request}
Language: {language}

🔍 વિનંતી વિશ્લેષણ (Request Analysis):
{request_analysis}

💭 વિચાર પ્રક્રિયા (Thought Process):
- પિઝા એ ઈટાલિયન વાનગી છે જે રોટલી જેવી લાગે છે (Pizza is Italian dish that resembles roti)
- ગુજરાતીમાં રોટલી અને શાક એ સમાન છે (In Gujarat, roti and shaak are similar)
- મેથી થેપલા અથવા ભાખરી વધુ યોગ્ય રહેશે (Methi thepla or bhakhri would be more appropriate)
- પરંતુ વિનંતી મુજબ ટોપિંગ્સ સાથે રોટલી બનાવી શકાય (But we can make roti with toppings as requested)

👨‍🍳 રસોઇયાની રેસીપી - ગુજરાતી પિઝા રોટલી (Chef's Recipe - Gujarati Pizza Roti)

સામગ્રી (Ingredients - Serves 2):
- 1 કપ ગોળ મેદો (1 cup wheat flour)
- 1/2 કપ દહીં (1/2 cup yogurt)
- 1 ટીસ્પૂન રાઇ પાઉડર (1 tsp mustard powder)
- 1/2 ટીસ્પૂન હળદર (1/2 tsp turmeric)
- મીઠું સ્વાદ મુજબ (Salt to taste)
- ટોપિંગ માટે: શાક, પનીર, મસાલા (For topping: vegetables, paneer, spices)

સૂચનાઓ (Instructions):
1. મેદો, દહીં, મસાલા મિક્સ કરીને રોટલી બનાવો
2. રોટલી શેકીને સોનેરી કરો
3. ઉપર શાક અને પનીર નાખો
4. ઘીમાં તડકો અને ધાણા-લીંબુથી ગાર્નિશ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
આ ગુજરાતી-શૈલીની પિઝા છે જે પરંપરાગત રોટલી જેવી છે. લાભ:
- ગોળ મેદો કોમ્પ્લેક્સ કાર્બોહાઇડ્રેટ્સ આપે છે
- શાક વિટામિન્સ અને ફાઇબર આપે છે
- દહીં પ્રોટીન અને કેલ્શિયમ આપે છે

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

            # General sweet/dessert
            elif any(word in recipe_lower for word in ['sweet', 'mithai', 'dessert', 'cake']):
                request_analysis = "User is requesting a sweet/dessert dish"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ - વિનંતીની સમજ (Gujarati Culinary Analysis - Understanding Request)

Recipe Request: {recipe_request}
Language: {language}

🔍 વિનંતી વિશ્લેષણ (Request Analysis):
{request_analysis}

💭 વિચાર પ્રક્રિયા (Thought Process):
- મીઠાઈ માટે ગુજરાતી ખંડવી યોગ્ય છે (Khandoi is perfect for sweets in Gujarat)
- તે પરંપરાગત ગુજરાતી મીઠાઈ છે (It's a traditional Gujarati sweet)
- ચણાનો લોટ અને દહીંથી બને છે (Made from chana flour and yogurt)
- આરોગ્યપ્રદ અને સ્વાદિષ્ટ છે (Healthy and delicious)

👨‍🍳 રસોઇયાની રેસીપી - ખંડવી (Chef's Recipe - Khandoi)

સામગ્રી (Ingredients - Serves 4):
- 1 કપ ચણાનો લોટ (1 cup chana flour/besan)
- 1/2 કપ દહીં (1/2 cup yogurt)
- 1/2 કપ ખાંડ (1/2 cup sugar)
- 1/4 કપ ઘી (1/4 cup ghee)
- 1/4 ટીસ્પૂન હળદર (1/4 tsp turmeric)
- 1/4 ટીસ્પૂન એલચી પાઉડર (1/4 tsp cardamom powder)

સૂચનાઓ (Instructions):
1. ચણાનો લોટ, દહીં, હળદર મિક્સ કરો
2. ૨ કલાક રહેવા દો
3. ઘીમાં ખાંડ ગોલ્ડન કરો
4. બેટર નાખીને ઘટ્ટ કરો
5. થાલીમાં પાથરીને એલચીથી ગાર્નિશ કરો

🥗 પોષણ વિશેષજ્ઞનું વિશ્લેષણ (Nutritionist's Analysis):
ખંડવી ગુજરાતી મીઠાઈ છે જે પ્રોટીન અને કાર્બોહાઇડ્રેટ્સથી ભરપૂર છે.

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

            # Default Gujarati response
            else:
                request_analysis = f"User is requesting: {recipe_request} - analyzing for Gujarati adaptation"
                return f"""ગુજરાતી કુલિનરી વિશ્લેષણ - વિનંતીની સમજ (Gujarati Culinary Analysis - Understanding Request)

Recipe Request: {recipe_request}
Language: {language}

🔍 વિનંતી વિશ્લેષણ (Request Analysis):
{request_analysis}

💭 વિચાર પ્રક્રિયા (Thought Process):
- વિનંતીને સમજીને ગુજરાતી સંસ્કૃતિમાં ફિટ કરવાનો પ્રયાસ કરું છું
- જો વાનગી સ્નેક છે તો ઢોકળા અથવા ખંડવી સૂચવી શકું છું
- જો મુખ્ય ભોજન છે તો શાક-ભાખરી સૂચવી શકું છું
- હંમેશા પરંપરાગત ગુજરાતી સ્વાદ અને આરોગ્ય ધ્યાનમાં રાખું છું

👨‍🍳 રસોઇયાની સૂચન (Chef's Recommendation):
આ વિનંતી માટે ગુજરાતી રીતે ઢોકળા અથવા થેપલા જેવી વાનગી વધુ યોગ્ય રહેશે.

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""
        else:
            # English fallback - analyze request type
            if any(word in recipe_lower for word in ['sweet', 'dessert', 'cookie', 'cake', 'pie']):
                return f"""Culinary Analysis Complete!

Recipe Request: {recipe_request}
Language: {language}

👨‍🍳 Chef's Recipe - Classic Chocolate Chip Cookies:

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
These cookies are a sweet treat but high in sugar and fats. Suggestions:
- Use whole wheat flour instead of all-purpose
- Reduce sugar by 1/4 cup and add applesauce
- Include nuts for healthy fats and protein
- Portion control: 1-2 cookies per serving

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""
            else:
                return f"""Culinary Analysis Complete!

Recipe Request: {recipe_request}
Language: {language}

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

*Note: This is a demo response. Set up your SAMBA_API_KEY for real AI analysis.*"""

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
                    sub_status_text = st.empty()

                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 20:
                            status_text.text("📊 Data Analyst: Initializing analysis...")
                            sub_status_text.text("Loading sales data and preparing datasets...")
                        elif i < 40:
                            status_text.text("📊 Data Analyst: Analyzing quarterly trends...")
                            sub_status_text.text("Calculating growth rates and identifying patterns...")
                        elif i < 60:
                            status_text.text("📊 Data Analyst: Computing key metrics...")
                            sub_status_text.text("Analyzing sales velocity and market indicators...")
                        elif i < 80:
                            status_text.text("🎯 Business Strategist: Reviewing analysis...")
                            sub_status_text.text("Evaluating data insights and market conditions...")
                        elif i < 90:
                            status_text.text("🎯 Business Strategist: Developing strategies...")
                            sub_status_text.text("Creating actionable recommendations and growth plans...")
                        else:
                            status_text.text("✅ Finalizing comprehensive business report...")
                            sub_status_text.text("Compiling analysis results and strategic recommendations...")
                        time.sleep(0.03)

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
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.text_area(
                "What would you like to cook?",
                placeholder="Example: chocolate chip cookies",
                height=100,
                key="food_input",
                help="Enter a recipe request and the AI team will create and analyze it!"
            )
        with col2:
            language = st.selectbox(
                "Recipe Language",
                ["English", "Gujarati (ગુજરાતી)"],
                key="language_select",
                help="Choose the language for your recipe"
            )

        if st.button("🍳 Create & Analyze Recipe", type="primary", use_container_width=True):
            if not user_input.strip():
                st.warning("Please enter a recipe request!")
            else:
                with st.spinner("🤖 Chef and nutritionist are collaborating..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    sub_status_text = st.empty()

                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 25:
                            status_text.text("👨‍🍳 Chef: Researching recipe foundations...")
                            sub_status_text.text("Analyzing ingredients and cooking techniques...")
                        elif i < 45:
                            status_text.text("👨‍🍳 Chef: Crafting recipe structure...")
                            sub_status_text.text("Developing cooking methods and flavor profiles...")
                        elif i < 65:
                            status_text.text("👨‍🍳 Chef: Refining ingredient balance...")
                            sub_status_text.text("Optimizing measurements and cooking times...")
                        elif i < 80:
                            status_text.text("🥗 Nutritionist: Analyzing nutritional content...")
                            sub_status_text.text("Evaluating calorie content and macronutrients...")
                        elif i < 90:
                            status_text.text("🥗 Nutritionist: Assessing health impact...")
                            sub_status_text.text("Checking vitamins, minerals, and dietary balance...")
                        else:
                            status_text.text("✅ Finalizing healthy recipe with improvements...")
                            sub_status_text.text("Compiling final recipe with nutritional recommendations...")
                        time.sleep(0.03)

                    result = run_food_team_analysis(user_input, language)
                    st.session_state.results_history.append({
                        "team": "Food Preparation",
                        "input": user_input,
                        "language": language,
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
            language_info = f" - {result.get('language', 'English')}" if 'language' in result else ""
            with st.expander(f"{result['team']}{language_info} - {result['input'][:40]}..."):
                st.write(f"**Team:** {result['team']}")
                st.write(f"**Input:** {result['input']}")
                if 'language' in result:
                    st.write(f"**Language:** {result['language']}")
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