import streamlit as st
import json
import ast  # <--- ONLY CHANGE: Added for fixing the list bug
import re   # <--- ONLY CHANGE: Added for fixing the list bug
from langchain_openai import ChatOpenAI

# 1. SETUP: Connect to OpenRouter / DeepSeek
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("🚨 Secrets Missing! Add OPENROUTER_API_KEY and OPENROUTER_BASE_URL to secrets.")
    st.stop()

# We use DeepSeek Chat for high-quality reasoning
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.7
)

# 2. HELPER: The Text Cleaner (FIXED)
def clean_text(ai_response):
    """Cleans AI response to ensure pure text output."""
    try:
        content = ai_response.content if hasattr(ai_response, 'content') else ai_response
        if isinstance(content, str):
            # Attempt to parse JSON if it looks like a list string
            content = content.strip()
            # REMOVE MARKDOWN (The AI loves to add ```json ... ```)
            content = content.replace("```python", "").replace("```json", "").replace("```", "")
            
            # --- THE FIX FOR LISTS ---
            if content.startswith("[") or content.startswith("{"):
                try:
                    return json.loads(content) # Return object if JSON
                except:
                    try:
                        # Fallback for Python-style lists (single quotes)
                        return ast.literal_eval(content)
                    except:
                        pass
        return str(content)
    except:
        return str(ai_response)

# 3. HELPER: Token Compressor (DISABLED FOR STABILITY)
def smart_compress(context, instruction, target_token=500):
    """
    Pass-through function. We disabled LLMLingua to prevent 
    Streamlit Cloud crashes (Out of Memory errors).
    """
    return context

# =========================================================
# 🧬 STAGE 1: THE STRATEGIC IDEATION ENGINE
# =========================================================
def strategist_node(pain_points, trending_topics):
    st.write("...⚙️ The Strategic Ideation Engine is analyzing...")
    
    # --- PROMPT UNCHANGED ---
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
    return clean_text(response)

# =========================================================
# 📐 STAGE 2: THE STRUCTURAL ARCHITECT
# =========================================================
def architect_node(selected_idea):
    st.write("...📐 The Structural Architect is designing the blueprint...")
    
    # --- PROMPT UNCHANGED ---
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
    return clean_text(response)

# =========================================================
# 🏭 STAGE 3: THE CONTENT FACTORY (Iterative Generation)
# =========================================================
def content_factory_node(article_title, outline):
    full_article = f"# {article_title}\n\n"
    
    # --- Prompt 1: The Introduction ---
    st.write("...🏭 Factory: Forging the Introduction...")
    
    # --- PROMPT UNCHANGED ---
    intro_prompt = f"""
    Role: Act as a professional content writer, SEO expert, and design thinker.
    Think step by step
    Task: Generate a compelling Introduction for the article: "{article_title}".
    Context: {outline}
    Requirement: Hook the reader, define the topic, provide solution preview.
    Avoid: Technical jargon, fluff.
    Output: Professional, bold keywords.
    """
    intro_content = clean_text(llm.invoke(intro_prompt))
    full_article += f"## Introduction\n{intro_content}\n\n"
    
    # --- Prompt 2: Body Section 1 ---
    st.write("...🏭 Factory: Building Section 1 (The Crisis)...")
    context_so_far = f"Title: {article_title}\nIntro: {intro_content}"
    # Compress context if possible
    compressed_context = smart_compress(context_so_far, "Generate Body Section 1")
    
    # --- PROMPT UNCHANGED ---
    body1_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 1 (The Crisis of Data Overload).
    Context to continue from: {compressed_context}
    Output: Start with heading. Bold key concepts.
    """
    body1_content = clean_text(llm.invoke(body1_prompt))
    full_article += f"{body1_content}\n\n"

    # --- Prompt 3: Body Section 2 ---
    st.write("...🏭 Factory: Building Section 2 (Audience)...")
    context_so_far += f"\nSection 1: {body1_content}"
    compressed_context = smart_compress(context_so_far, "Generate Body Section 2")
    
    # --- PROMPT UNCHANGED ---
    body2_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 2 (Audience Intelligence).
    Context to continue from: {compressed_context}
    Output: Start with heading. Bold key concepts. Seamless flow.
    """
    body2_content = clean_text(llm.invoke(body2_prompt))
    full_article += f"{body2_content}\n\n"

    # --- Prompt 4: Body Section 3 ---
    st.write("...🏭 Factory: Building Section 3 (Technical)...")
    context_so_far += f"\nSection 2: {body2_content}"
    compressed_context = smart_compress(context_so_far, "Generate Body Section 3")
    
    # --- PROMPT UNCHANGED ---
    body3_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write Body Section 3 (Advanced Technical Implementation).
    Context to continue from: {compressed_context}
    Output: Start with heading. Bold key concepts. Seamless flow.
    """
    body3_content = clean_text(llm.invoke(body3_prompt))
    full_article += f"{body3_content}\n\n"

    # --- Prompt 5: Conclusion ---
    st.write("...🏭 Factory: Finalizing Conclusion...")
    context_so_far += f"\nSection 3: {body3_content}"
    compressed_context = smart_compress(context_so_far, "Generate Conclusion")
    
    # --- PROMPT UNCHANGED ---
    conc_prompt = f"""
    Role: Professional content writer.
    Think step by step
    Task: Write the Conclusion (The Future is in Your Hands).
    Context to continue from: {compressed_context}
    Requirement: Summarize, Call to Action, Memorable closing.
    Output: Start with heading. Seamless flow.
    """
    conc_content = clean_text(llm.invoke(conc_prompt))
    full_article += f"{conc_content}\n\n"
    
    return full_article

# =========================================================
# ✨ STAGE 4: THE FINAL POLISH
# =========================================================
def polish_node(full_draft):
    st.write("...✨ Applying Final Polish & SEO...")
    
    # We compress the whole article because it's long now
    compressed_draft = smart_compress(full_draft, "Generate SEO keywords and Social Captions", target_token=1000)
    
    # --- PROMPT UNCHANGED ---
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
    return clean_text(response)
