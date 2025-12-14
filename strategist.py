import streamlit as st
import json
import ast 
from langchain_openai import ChatOpenAI

# 1. SETUP
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("Secrets Missing.")
    st.stop()

# 2. CONFIGURATION (4k Token Limit)
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.8,
    max_tokens=4000
)

# 3. CLEANER
def clean_text(ai_response, parse_json=False):
    try:
        content = ai_response.content if hasattr(ai_response, 'content') else ai_response
        if not parse_json: return str(content)
        
        if isinstance(content, str):
            content = content.strip().replace("```python", "").replace("```json", "").replace("```", "")
            if content.startswith("[") or content.startswith("{"):
                try: return json.loads(content)
                except: 
                    try: return ast.literal_eval(content)
                    except: pass
        return str(content)
    except:
        return str(ai_response)

# 4. STAGES
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ Strategist: Analyzing...")
    prompt = f"""
    Act as a viral content strategist.
    Goal: Generate 5 high-impact article titles that solve: {pain_points}
    Context: {trending_topics}
    Output Format: ONLY a Python list of strings.
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True)

def architect_node(selected_idea):
    st.write("...📐 Architect: Designing Unique Structure...")
    # DYNAMIC PROMPT: Forces unique headers every time
    prompt = f"""
    Act as a Senior Editor. 
    Article Idea: "{selected_idea}"
    Task: Create a unique outline.
    RULES:
    1. Do NOT use generic headers like "Introduction".
    2. Create 4 descriptive, catchy headers specific to this topic.
    3. Return ONLY the headers as a Python List.
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True) 

def content_factory_node(article_title, outline_headers):
    # Fallback if AI fails to give a list
    if isinstance(outline_headers, str):
        outline_headers = ["The Challenge", "The Solution", "Practical Steps", "Future Outlook"]
        
    full_article = f"# {article_title}\n\n"
    
    # 1. Intro
    st.write("...🏭 Factory: Writing Hook...")
    intro = llm.invoke(f"Write a viral hook introduction for '{article_title}'.")
    full_article += f"### Introduction\n{clean_text(intro)}\n\n"
    
    # 2. Body
    context = str(intro)
    for header in outline_headers:
        st.write(f"...🏭 Factory: Writing section '{header}'...")
        section_prompt = f"""
        Write the article section for the header: "{header}".
        Context: {context[-500:]}
        Tone: Engaging, helpful.
        """
        section_content = clean_text(llm.invoke(section_prompt))
        full_article += f"### {header}\n{section_content}\n\n"
        context += section_content 
        
    return full_article

def polish_node(full_draft):
    st.write("...✨ SEO Expert: Optimizing...")
    prompt = f"""
    Generate an SEO Kit (Keywords, Meta Description,Twitter(x) , LinkedIn Post).
    Context: {full_draft[:1000]}
    """
    return clean_text(llm.invoke(prompt))
