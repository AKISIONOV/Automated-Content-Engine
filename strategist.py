# 1. Imports
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Setup the "Chef" (Connect to Gemini via Cloud Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = "LOCAL_KEY_IF_NEEDED"

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key
)

# --- 🧹 THE CLEANER FUNCTION (Fixes the "Messy" Output) ---
def clean_text(ai_response):
    """
    Takes the raw AI response and extracts just the clean text string.
    Removes the [{'type': 'text'}] garbage.
    """
    content = ai_response.content
    
    # If it's already a clean string, just return it
    if isinstance(content, str):
        return content
        
    # If it's a list (the messy part), extract the text
    if isinstance(content, list):
        full_text = ""
        for part in content:
            if 'text' in part:
                full_text += part['text']
        return full_text
        
    # Fallback
    return str(content)
# -----------------------------------------------------------

# 3. Define the Function (The Node)
def strategist_node(niche, audience):
    print(f"--- 🧠 The Strategist is thinking about {niche}... ---")
    prompt = f"Act as a viral content strategist. Generate 3 catchy blog titles about '{niche}' for an audience of '{audience}'."
    
    response = llm.invoke(prompt)
    # USE THE CLEANER HERE
    return clean_text(response)

# 4. Define the Architect Function (Node 2)
def architect_node(strategist_output):
    print("\n--- 📐 The Architect is analyzing the ideas... ---")
    architect_prompt = f"""
    Act as a senior content editor.
    Here are 3 potential article ideas:
    {strategist_output}
    
    Task:
    1. Select the SINGLE best article idea from the list above.
    2. Write a comprehensive outline for that article (Introduction, 3 Body Sections, Conclusion).
    """
    
    response = llm.invoke(architect_prompt)
    # USE THE CLEANER HERE
    return clean_text(response)

# 5. Define the Writer Function (Node 3)
def writer_node(outline):
    print("\n--- ✍️ The Writer is drafting the story... ---")
    writer_prompt = f"""
    Act as a professional content writer.
    
    Here is an outline for an article:
    {outline}
    
    Task:
    Write the FULL article based on this outline.
    - Use engaging, professional tone.
    - Use Markdown formatting (headings, bold text).
    - Expand every bullet point into full paragraphs.
    - Use Hashtags and SEO keywords to enhance the article visibility.
    """
    
    response = llm.invoke(writer_prompt)
    # USE THE CLEANER HERE
    return clean_text(response)

if __name__ == "__main__":
    print("⚠️ NOTE: This script expects to be run by the Streamlit App.")

