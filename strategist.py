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

# 2. CONFIGURATION
# Optimized for high-quality, long-form content
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.85, # Slightly higher for creativity
    max_tokens=15000  # Maximized for length
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

# =========================================================
# 🧬 STAGE 1: ADVANCED STRATEGIST
# =========================================================
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ Strategist: Analyzing Market Angles...")
    
    # OPTIMIZATION: Asking for specific "Angles" (Contrarian, Listicle, How-to)
    prompt = f"""
    Act as a world-class Content Strategist.
    
    Target Topic: {trending_topics}
    User Pain Point: {pain_points}
    
    Task: Generate 5 high-viral potential article headlines.
    Strategy:
    - Mix "How-to" guides with "Contrarian/Opinion" pieces.
    - Focus on curiosity and high value.
    - Avoid generic AI titles.
    
    Output Format: ONLY a Python list of strings.
    Example: ["Why Most Students Fail at X", "The Ultimate Guide to Y"]
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True)

# =========================================================
# 📐 STAGE 2: NARRATIVE ARCHITECT
# =========================================================
def architect_node(selected_idea):
    st.write("...📐 Architect: Designing Narrative Arc...")
    
    # OPTIMIZATION: Forcing a "Story Structure" instead of a flat list
    prompt = f"""
    Act as a Senior Editor at a top publication.
    
    Article Title: "{selected_idea}"
    
    Task: Design a powerful 4-part structure.
    Rules:
    1. Header 1 must define the 'Crisis' or 'Problem'.
    2. Header 2 must offer a 'New Perspective' or 'Strategy'.
    3. Header 3 must be 'Actionable Steps'.
    4. Header 4 must be the 'Future Outlook'.
    
    Do NOT use the words "Introduction" or "Conclusion". Use catchy, descriptive headers.
    Output Format: ONLY a Python list of 4 strings.
    """
    response = llm.invoke(prompt)
    return clean_text(response, parse_json=True) 

# =========================================================
# 🏭 STAGE 3: CONTENT FACTORY (DEEP WORK MODE)
# =========================================================
def content_factory_node(article_title, outline_headers):
    # Fail-safe
    if isinstance(outline_headers, str):
        outline_headers = ["The Core Problem", "The Smart Solution", "Action Plan", "The Future"]
        
    full_article = f"# {article_title}\n\n"
    
    # 1. The Hook (Intro)
    st.write("...🏭 Factory: Crafting the Hook...")
    # OPTIMIZATION: Asking for a "Hook" specifically
    intro_prompt = f"""
    Write a viral opening hook for the article: "{article_title}".
    Style: Storytelling, punchy, engaging. Start with a bold statement or question.
    Length: 150-200 words.
    """
    intro = llm.invoke(intro_prompt)
    full_article += f"### Introduction\n{clean_text(intro)}\n\n"
    
    # 2. Body Sections (Iterative Context)
    context = str(intro)
    
    for i, header in enumerate(outline_headers):
        st.write(f"...🏭 Factory: Writing Section {i+1} ('{header}')...")
        
        # OPTIMIZATION: Giving specific instructions per section type
        if i == 0: focus = "Focus on the pain point and why current solutions fail."
        elif i == 1: focus = "Introduce the new strategy/solution clearly."
        elif i == 2: focus = "Provide a step-by-step list or technical examples."
        else: focus = "Summarize and give a visionary outlook."
        
        section_prompt = f"""
        Write the section: "{header}".
        Context so far: {context[-1500:]}
        
        Instructions:
        - {focus}
        - Use short paragraphs.
        - Use bolding for key terms.
        - Tone: Expert, Authoritative, yet Accessible.
        - Length: 300-400 words.
        """
        
        section_content = clean_text(llm.invoke(section_prompt))
        full_article += f"### {header}\n{section_content}\n\n"
        context += section_content 
        
    return full_article

# =========================================================
# ✨ STAGE 4: SEO & VIRALITY POLISH
# =========================================================
def polish_node(full_draft):
    st.write("...✨ SEO Expert: Final Polish...")
    
    # OPTIMIZATION: Asking for Platform-Specific content
    prompt = f"""
    Analyze this article: {full_draft[:2000]}...
    
    Generate a "Growth Kit":
    1. 5 High-Volume SEO Keywords.
    2. A click-worthy Meta Description (160 chars).
    3. A LinkedIn Post (Professional tone, emojis, bullet points).
    4. A Twitter Thread starter (Punchy, thread hook).
    
    Format: Markdown.
    """
    return clean_text(llm.invoke(prompt))
