# 1. Imports
import streamlit as st
import json
from langchain_openai import ChatOpenAI

# 2. Setup: Connect to OpenRouter
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    base_url = st.secrets["OPENROUTER_BASE_URL"]
except:
    st.error("🚨 Secrets Missing! Add OPENROUTER_API_KEY and OPENROUTER_BASE_URL to secrets.")
    st.stop()

# 3. Configure the Engine (DeepSeek via OpenRouter)
# We use 'deepseek/deepseek-chat' as it is generally more stable for content generation
llm = ChatOpenAI(
    model="deepseek/deepseek-chat", 
    openai_api_key=api_key,
    openai_api_base=base_url,
    temperature=0.7
)

# --- 🧹 THE ADVANCED CLEANER FUNCTION ---
def clean_text(ai_response):
    """
    Cleans the AI response, handling raw strings, JSON strings, and lists.
    """
    try:
        # Step A: Extract content attribute if it exists
        if hasattr(ai_response, 'content'):
            content = ai_response.content
        else:
            content = ai_response

        # Step B: Check if it's a string that looks like a list (The sneaky bug!)
        if isinstance(content, str):
            content = content.strip()
            # If it starts with [ or {, it might be JSON text. Try to parse it.
            if content.startswith("[") or content.startswith("{"):
                try:
                    # Turn "[{'text':...}]" string into a real Python list
                    content = json.loads(content)
                except:
                    # If it fails, it's just normal text. Keep it.
                    pass

        # Step C: Handle Lists (Extract text from parts)
        if isinstance(content, list):
            full_text = ""
            for part in content:
                if isinstance(part, dict) and 'text' in part:
                    full_text += part['text']
                elif isinstance(part, str):
                    full_text += part
            return full_text
            
        # Step D: Fallback for normal strings
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
        return "Error: Strategy failed."

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
        return "Error: Architecture failed."

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
        response = llm.invoke(writer_prompt )
        return clean_text(response)
    except Exception as e:
        st.error(f"❌ Writer Error: {e}")
        return "Error: Writing failed."

if __name__ == "__main__":
    print("Ready for Streamlit Deployment (DeepSeek Edition).")
