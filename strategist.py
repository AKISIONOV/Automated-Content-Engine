# 1. Imports
import streamlit as st
from langchain_openai import ChatOpenAI

# 2. Setup: Connect to OpenRouter
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("🚨 Secrets Missing! Add OPENROUTER_API_KEY and OPENROUTER_BASE_URL to secrets.")
    st.stop()

# 3. Configure the Engine (DeepSeek via OpenRouter)
llm = ChatOpenAI(
    model="deepseek/deepseek-r1", # You can also try "deepseek/deepseek-chat"
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.7
)

# --- 🧹 THE CLEANER FUNCTION (Prevents Download Button Crash) ---
def clean_text(ai_response):
    try:
        # Check if response is just a string
        if isinstance(ai_response, str):
            return ai_response
            
        # Check if it is an object with .content
        if hasattr(ai_response, 'content'):
            content = ai_response.content
        else:
            content = ai_response

        # Logic to clean lists or dictionaries
        if isinstance(content, str): 
            return content
        if isinstance(content, list):
            full_text = ""
            for part in content:
                if isinstance(part, dict) and 'text' in part:
                    full_text += part['text']
                elif isinstance(part, str):
                    full_text += part
            return full_text
            
        return str(content)
    except Exception as e:
        return str(ai_response)

# --- 🧠 THE NODE FUNCTIONS ---

def strategist_node(niche, audience):
    st.write(f"...Strategist thinking about {niche}...")
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
        return "Error: Could not generate outline (Introduction, 3 Body Sections, Conclusion)."

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
    print("Ready for Streamlit Deployment (OpenRouter Edition).")
