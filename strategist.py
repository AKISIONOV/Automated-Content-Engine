import streamlit as st
import json
import ast 
from langchain_openai import ChatOpenAI

# 1. SETUP
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("🚨 Secrets Missing! Add OPENROUTER_API_KEY and OPENROUTER_BASE_URL to secrets.")
    st.stop()

# 2. CONFIGURATION (Safe Token Limit)
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.8,
    max_tokens=3000 # Keeps you within free tier limits
)

# 3. HELPER: Clean Text
def clean_text(ai_response, parse_json=False):
    """Parses AI output into Strings or Lists safely."""
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

# 4. STRATEGY NODE
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ Strategist: Analyzing...")
    prompt = f"""
    Act as a content strategist.
    Goal: Generate 5 unique article titles for: {pain_points} regarding {trending_topics}.
    Output Format: ONLY a Python list of strings.
    Example: ["Title 1", "Title 2"]
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True)

# 5. ARCHITECT NODE
def architect_node(selected_idea):
    st.write("...📐 Architect: Designing...")
    prompt = f"""
    Act as an Editor.
    Idea: "{selected_idea}"
    Task: Create 4 unique, catchy section headers (No 'Introduction' or generic terms).
    Output Format: ONLY a Python list of strings.
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True) 

# 6. WRITING NODE
def content_factory_node(article_title, outline_headers):
    # Fail-safe if headers are broken
    if isinstance(outline_headers, str):
        outline_headers = ["The Core Issue", "Why It Matters", "The Solution", "Key Takeaways"]
        
    full_article = f"# {article_title}\n\n"
    
    # Intro
    st.write("...🏭 Factory: Writing Hook...")
    intro = llm.invoke(f"Write a viral hook introduction for '{article_title}'.")
    full_article += f"### Introduction\n{clean_text(intro)}\n\n"
    
    # Body
    context = str(intro)
    for header in outline_headers:
        st.write(f"...🏭 Factory: Writing section '{header}'...")
        section_prompt = f"""
        Write the section "{header}".
        Context so far: {context[-500:]}
        Tone: Engaging and authoritative.
        """
        section_content = clean_text(llm.invoke(section_prompt))
        full_article += f"### {header}\n{section_content}\n\n"
        context += section_content 
        
    return full_article

# 7. POLISH NODE
def polish_node(full_draft):
    st.write("...✨ SEO Expert: Optimizing...")
    prompt = f"""
    Generate an SEO Kit (5 Keywords, Meta Description, LinkedIn Post).
    Context: {full_draft[:1000]}
    """
    return clean_text(llm.invoke(prompt))
