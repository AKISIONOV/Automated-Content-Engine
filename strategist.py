# 1. Imports
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Setup (With Robust Error Handling)
try:
    # Try to get the key from Streamlit Cloud Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # If secrets are missing, try a local fallback or stop
    # This prevents the app from crashing immediately if the key is wrong
    st.error("🚨 API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Use the specific 1.5 Flash model (More stable for free tier)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=api_key
)

# --- 🧹 THE CLEANER FUNCTION (Fixes formatting issues) ---
def clean_text(ai_response):
    try:
        content = ai_response.content
        # If it's already a clean string, return it
        if isinstance(content, str): 
            return content
        # If it's a list (the "messy" output), extract just the text
        if isinstance(content, list):
            full_text = ""
            for part in content:
                if 'text' in part: 
                    full_text += part['text']
            return full_text
        # Fallback
        return str(content)
    except:
        return str(ai_response)

# --- 🧠 THE NODE FUNCTIONS (With Debugging) ---

def strategist_node(niche, audience):
    st.write("...Strategist connecting to Google...")
    prompt = f"Act as a viral content strategist. Generate 3 catchy blog titles about '{niche}' for an audience of '{audience}'."
    
    try:
        response = llm.invoke(prompt)
        return clean_text(response)
    except Exception as e:
        # THIS IS THE FIX: Print the actual error to the screen
        st.error(f"❌ Strategist Error: {e}")
        return "Error: Could not generate strategies. Please check API Quota."

def architect_node(strategist_output):
    st.write("...Architect analyzing...")
    architect_prompt = f"""
    Act as a senior content editor.
    Here are 3 potential article ideas:
    {strategist_output}
    
    Task:
    1. Select the SINGLE best article idea.
    2.  Write a comprehensive outline for that article (Introduction, 3 Body Sections, Conclusion).
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
    - Use Hashtags and SEO keywords to enhance the article visibility.
    """
    
    try:
        response = llm.invoke(writer_prompt)
        return clean_text(response)
    except Exception as e:
        st.error(f"❌ Writer Error: {e}")
        return "Error: Could not write article."

if __name__ == "__main__":
    print("This script is ready for Streamlit.")

