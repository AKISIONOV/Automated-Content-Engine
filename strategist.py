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

# 2. CONFIGURATION (4k Token Limit to prevent Cost Errors)
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.85, # Higher creativity for viral content
    max_tokens=4000
)

# 3. HELPER: Clean Text
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

# =========================================================
# 🧬 STAGE 1: STRATEGIST
# =========================================================
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ Strategist: Analyzing Market Angles...")
    prompt = f"""
    Act as a viral content strategist.
    Goal: Generate 5 high-impact article titles that solve: {pain_points}
    Context: {trending_topics}
    
    Output Format: ONLY a Python list of strings.
    Example: ["Title 1...", "Title 2..."]
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True)

# =========================================================
# 📐 STAGE 2: DYNAMIC ARCHITECT (Unique Headers)
# =========================================================
def architect_node(selected_idea):
    st.write("...📐 Architect: Designing Unique Structure...")
    prompt = f"""
    Act as a Senior Editor. 
    Article Idea: "{selected_idea}"
    
    Task: Create a unique, engaging outline.
    RULES:
    1. Do NOT use generic headers like "Introduction" or "Body Section 1".
    2. Create 4-5 catchy, descriptive headers that tell a story.
    3. Return ONLY the headers as a Python List.
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True) 

# =========================================================
# 🏭 STAGE 3: CONTENT FACTORY (Real Content)
# =========================================================
def content_factory_node(article_title, outline_headers):
    # Fallback if AI fails to give a list
    if isinstance(outline_headers, str):
        outline_headers = ["The Challenge", "The Solution", "Practical Steps", "Future Outlook"]
        
    full_article = f"# {article_title}\n\n"
    
    # 1. Intro
    st.write("...🏭 Factory: Writing Viral Hook...")
    intro = llm.invoke(f"Write a viral hook introduction for '{article_title}'. Use a Storytelling approach.")
    full_article += f"### Introduction\n{clean_text(intro)}\n\n"
    
    # 2. Body Sections
    context = str(intro)
    for header in outline_headers:
        st.write(f"...🏭 Factory: Writing section '{header}'...")
        section_prompt = f"""
        Write the article section for the header: "{header}".
        Context so far: {context[-500:]}
        Tone: Engaging, helpful, authoritative.
        """
        section_content = clean_text(llm.invoke(section_prompt))
        full_article += f"### {header}\n{section_content}\n\n"
        context += section_content 
        
    return full_article

# =========================================================
# ✨ STAGE 4: POLISH
# =========================================================
def polish_node(full_draft):
    st.write("...✨ SEO Expert: Optimizing...")
    prompt = f"""
    Generate an SEO Kit for this article.
    1. 5 High-Traffic Keywords
    2. Meta Description
    3. LinkedIn Post
    """
    return clean_text(llm.invoke(prompt))
