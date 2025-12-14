import streamlit as st
import json
import ast 
import re 
from langchain_openai import ChatOpenAI

# 1. SETUP
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("🚨 Secrets Missing! Add OPENROUTER_API_KEY and OPENROUTER_BASE_URL to secrets.")
    st.stop()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.7
)

# 2. HELPER: The Smart Cleaner (UPDATED)
def clean_text(ai_response, parse_json=False):
    """
    Cleans AI response.
    - If parse_json=True: Tries to convert text to a real Python List (For Strategy).
    - If parse_json=False: Forces output to be a String (For Writing).
    """
    try:
        content = ai_response.content if hasattr(ai_response, 'content') else ai_response
        
        # If we just want text, return string immediately
        if not parse_json:
            return str(content)

        # If we WANT a list (Strategy Mode), try to parse it
        if isinstance(content, str):
            content = content.strip()
            content = content.replace("```python", "").replace("```json", "").replace("```", "")
            
            if content.startswith("[") or content.startswith("{"):
                try:
                    return json.loads(content)
                except:
                    try:
                        return ast.literal_eval(content)
                    except:
                        pass
        return str(content)
    except:
        return str(ai_response)

# 3. HELPER: Compressor (Disabled)
def smart_compress(context, instruction, target_token=500):
    return context

# =========================================================
# 🧬 STAGE 1: STRATEGIST (Needs List Output)
# =========================================================
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ The Strategic Ideation Engine is analyzing...")
    
    prompt = f"""
    Role: Act as a viral content strategist and SEO expert for a leading B2B tech publication.
    Think step by step

    Goal: Generate high-performing article ideas that address specific pain points.
    
    Input Data:
    - Pain Points: {pain_points}
    - Trending Topics: {trending_topics}
    
    Task:
    1. Analyze the inputs.
    2. Synthesize the analyze into best 5 unique article ideas.
    3. For each idea, provide a one-sentence rationale explaing it strategic value & why it will resonate with the target Audience.
    
    Output Format:
    Return ONLY a Python List of strings, where each string is an idea + rationale. 
    Example: ["Title: X... Rationale: Y...", "Title: A... Rationale: B..."]

    Final Review : Reasoning your Review.
    """
    
    response = llm.invoke(prompt)
    # ENABLE LIST PARSING HERE
    return clean_text(response, parse_json=True)

# =========================================================
# 📐 STAGE 2: ARCHITECT (Needs String Output)
# =========================================================
def architect_node(selected_idea):
    st.write("...📐 The Structural Architect is designing the blueprint...")
    
    prompt = f"""
    Role: Act as a professional content writer and editor expertise in technical field.
    
    Article Idea: "{selected_idea}"
    
    Task:
    Generate a comprehensive article outline. 
    Structure:
    1. Introduction
    2. Body Section 1: The Problem/Crisis
    3. Body Section 2: Audience/Strategy
    4. Body Section 3: Technical Implementation
    5. Conclusion: Future Outlook
    
    Think step by step:
    - Foundation -> Audience Intelligence -> Narrative Architecture -> Visualization -> Tech Integration -> Delivery -> Impact -> Future Proofing.
    
    Avoid: Extremely difficult jargon, useless keywords.
    Tone: Professional, trustworthy, confidential.
    """
    
    response = llm.invoke(prompt)
    # DISABLE LIST PARSING (Text Only)
    return clean_text(response, parse_json=False)

# =========================================================
# 🏭 STAGE 3: CONTENT FACTORY (Needs String Output)
# =========================================================
def content_factory_node(article_title, outline):
    full_article = f"# {article_title}\n\n"
    
    # Intro
    st.write("...🏭 Factory: Forging the Introduction...")
    intro_prompt = f"""
    Role: Act as a professional content writer, SEO expert, and design thinker.
    Think step by step
    Task: Generate a compelling Introduction for the article: "{article_title}".
    Context: {outline}
    Requirement: Hook the reader, define the topic, provide solution preview.
    Avoid: Technical jargon, fluff.
    Output: Professional, bold keywords.
    """
    # DISABLE LIST PARSING
    intro_content = clean_text(llm.invoke(intro_prompt), parse_json=False)
    full_article += f"## Introduction\n{intro_content}\n\n"
    
    # Body 1
    st.write("...🏭 Factory: Building Section 1...")
    body1_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 1 (The Crisis of Data Overload).
    Context to continue from: {article_title} - {intro_content}
    Output: Start with heading. Bold key concepts.
    """
    body1_content = clean_text(llm.invoke(body1_prompt), parse_json=False)
    full_article += f"{body1_content}\n\n"

    # Body 2
    st.write("...🏭 Factory: Building Section 2...")
    body2_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 2 (Audience Intelligence).
    Context to continue from: {full_article[-500:]}
    Output: Start with heading. Bold key concepts. Seamless flow.
    """
    body2_content = clean_text(llm.invoke(body2_prompt), parse_json=False)
    full_article += f"{body2_content}\n\n"

    # Body 3
    st.write("...🏭 Factory: Building Section 3...")
    body3_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 3 (Advanced Technical Implementation).
    Context to continue from: {full_article[-500:]}
    Output: Start with heading. Bold key concepts. Seamless flow.
    """
    body3_content = clean_text(llm.invoke(body3_prompt), parse_json=False)
    full_article += f"{body3_content}\n\n"

    # Conclusion
    st.write("...🏭 Factory: Finalizing Conclusion...")
    conc_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write the Conclusion (The Future is in Your Hands).
    Context to continue from: {full_article[-500:]}
    Requirement: Summarize, Call to Action, Memorable closing.
    Output: Start with heading. Seamless flow.
    """
    conc_content = clean_text(llm.invoke(conc_prompt), parse_json=False)
    full_article += f"{conc_content}\n\n"
    
    return full_article

# =========================================================
# ✨ STAGE 4: POLISH (Needs String Output)
# =========================================================
def polish_node(full_draft):
    st.write("...✨ Applying Final Polish & SEO...")
    
    compressed_draft = smart_compress(full_draft, "Generate SEO", target_token=1000)
    
    prompt = f"""
    Role: Professional content writer and SEO expert.
    Think step by step
    Task: Review and optimize the article.
    
    Article Content (Compressed Context): 
    {compressed_draft}
    
    Deliverables:
    1. 5 High-Value SEO Keywords.
    2. Meta Description (<160 chars).
    3. Social Media Captions (LinkedIn, Instagram, X).
    
    Format: Use Markdown headings for each deliverable.
    """
    
    response = llm.invoke(prompt)
    # DISABLE LIST PARSING (Text Only)
    return clean_text(response, parse_json=False)
