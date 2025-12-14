# 1. Imports
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Setup the "Chef" (Connect to Gemini via Cloud Secrets)
# This looks for the key in Streamlit Cloud settings
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Fallback for local testing (optional, but good for safety)
    # If you want to run locally, make sure you have a .streamlit/secrets.toml file
    # Or just ignore this if you are deploying to cloud immediately.
    api_key = "YOUR_LOCAL_KEY_HERE_IF_NEEDED" 

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key
)

# 3. Define the Function (The Node)
def strategist_node(niche, audience):
    print(f"--- 🧠 The Strategist is thinking about {niche}... ---")
    
    # This is the prompt template
    prompt = f"Act as a viral content strategist. Generate 3 catchy blog titles about '{niche}' for an audience of '{audience}'."
    
    # Ask the AI
    response = llm.invoke(prompt)
    return response.content

# 4. Define the Architect Function (Node 2)
def architect_node(strategist_output):
    print("\n--- 📐 The Architect is analyzing the ideas... ---")
    
    # The Prompt
    architect_prompt = f"""
    Act as a senior content editor.
    
    Here are 3 potential article ideas:
    {strategist_output}
    
    Task:
    1. Select the SINGLE best article idea from the list above.
    2. Write a comprehensive outline for that article (Introduction, 3 Body Sections, Conclusion).
    """
    
    # Ask the AI
    response = llm.invoke(architect_prompt)
    return response.content

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
    
    # Ask the AI
    response = llm.invoke(writer_prompt)
    return response.content

# 6. Local Testing Block (Optional)
if __name__ == "__main__":
    print("⚠️ NOTE: This script expects to be run by the Streamlit App.")
    # This part will fail locally if you don't have secrets.toml set up
    # But it is fine for the Cloud Deployment.