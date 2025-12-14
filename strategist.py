# 1. Imports
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Setup (With Robust Error Handling)
try:
    # Try to get the key from Streamlit Cloud Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# --- CRITICAL FIX: USING THE VERIFIED MODEL NAME ---
# "gemini-flash-latest" is the alias that appeared in your diagnostic test.
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key
)

# --- 🧹 THE CLEANER FUNCTION (Fixes the "[{...}]" mess) ---
def clean_text(ai_response):
    try:
        content = ai_response.content
        
        # Case 1: It's already perfect text
        if isinstance(content, str): 
            return content
            
        # Case 2: It's a list of parts (the "messy" output)
        if isinstance(content, list):
            full_text = ""
            for part in content:
                # Extract text if it exists, otherwise skip
                if isinstance(part, dict) and 'text' in part:
                    full_text += part['text']
                elif isinstance(part, str):
                    full_text += part
            return full_text
            
        # Case 3: Fallback
        return str(content)
    except Exception as e:
        # If cleaning fails, return the raw string so we can at least see it
        return str(ai_response.content)

# --- 🧠 THE NODE FUNCTIONS ---

def strategist_node(niche, audience):
    st.write("...Strategist connecting to Google...")
    prompt = f"Act as a viral content strategist. Generate 3 catchy blog titles about '{niche}' for an audience of '{audience}'."
    
    try:
        response = llm.invoke(prompt)
        return clean_text(response)
    except Exception as e:
        st.error(f"❌ Strategist Error: {e}")
        return "Error: Could not generate strategies."

def architect_node(strategist_output):
    st.write("...Architect analyzing...")
    architect_prompt = f"""
    Act as a senior content editor.
    Here are 3 potential article ideas:
    {strategist_output}
    
    Task:
    1. Select the SINGLE best article idea.
    2. Write a comprehensive outline for that article.
    """
    
    try:
        response = llm.invoke(architect_prompt)
        return clean_text(response)
    except Exception as e:
        st.error(f"❌ Architect Error: {e}")
        return "Error: Could not generate outline."

def writer_node(outline):
    st.write("...Writer drafting...")
    writer_prompt = f"""
    Act as a professional content writer.
    Here is an outline:
    {outline}
    
    Task:
    Write the FULL article based on this outline.
    - Use engaging, professional tone.
    - Use Markdown formatting (headings, bold text).
    - Expand every bullet point into full paragraphs.
    - Use Hashtags and SEO keywords.
    """
    
    try:
        response = llm.invoke(writer_prompt)
        return clean_text(response)
    except Exception as e:
        st.error(f"❌ Writer Error: {e}")
        return "Error: Could not write article."

if __name__ == "__main__":
    print("This script is ready for Streamlit.")
