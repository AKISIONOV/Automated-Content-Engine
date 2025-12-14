import streamlit as st
import strategist
import urllib.parse
import time

# 1. CONFIG
st.set_page_config(page_title="ACE Engine", page_icon="⚡", layout="wide")

# 2. THEME ENGINE
def apply_theme(theme_choice):
    if theme_choice == "Dark Mode":
        st.markdown("""<style>.stApp { background-color: #0e1117; color: white; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Light Mode":
        st.markdown("""<style>.stApp { background-color: #ffffff; color: black; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Hacker Green":
        st.markdown("""<style>.stApp { background-color: #002b36; color: #859900; } .stButton button {border: 1px solid #859900;}</style>""", unsafe_allow_html=True)

# 3. ROBUST IMAGE GENERATOR (Pollinations Only)
def get_safe_image_url(prompt_text):
    """
    Creates a safe, simple URL for Pollinations AI to prevent crashes.
    """
    try:
        # 1. Simplify the prompt to just key nouns (prevents URL errors)
        # We take the first 40 chars which is usually the core subject
        short_prompt = prompt_text[:40] 
        
        # 2. Encode it for web (turn spaces into %20)
        safe_prompt = urllib.parse.quote(f"editorial photo of {short_prompt}")
        
        # 3. Construct URL with No-Logo flag
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?nologo=true&width=800&height=400"
        return image_url
    except:
        # Ultimate fallback image if everything breaks
        return "https://image.pollinations.ai/prompt/technology?nologo=true"

# 4. SIDEBAR
with st.sidebar:
    st.title("🎛️ ACE Control")
    
    # Theme Selector
    theme = st.selectbox("🎨 Interface Theme", ["Default (System)", "Dark Mode", "Light Mode", "Hacker Green"])
    apply_theme(theme)
    st.divider()

    niche = st.text_input("Niche / Topic", "Artificial Intelligence")
    audience = st.text_input("Audience", "University Students")
    st.divider()
    
    btn = st.button("🚀 Auto-Pilot Launch", type="primary", use_container_width=True)

# 5. MAIN APP
st.title("⚡ ACE: Automated Content Engine")

if btn:
    with st.status("🚀 System Running...", expanded=True) as status:
        
        # 1. Strategy
        try:
            ideas = strategist.strategist_node(niche, audience)
            best_idea = ideas[0] if isinstance(ideas, list) else str(ideas)
            st.info(f"Selected Angle: {best_idea[:80]}...")
        except:
            st.error("Strategy Failed. Retrying...")
            best_idea = f"{niche} strategies for {audience}"
            
        # 2. Architecture
        try:
            headers = strategist.architect_node(best_idea)
            st.write("Blueprint Designed.")
        except:
            headers = ["The Challenge", "The Solution", "Key Examples", "Conclusion"]
            
        # 3. Writing
        full_article = strategist.content_factory_node(best_idea, headers)
        
        # 4. Polish
        seo_kit = strategist.polish_node(full_article)
        
        status.update(label="Done!", state="complete", expanded=False)

    # 6. RESULTS DISPLAY
    
    # --- IMAGE FIX IS HERE ---
    image_url = get_safe_image_url(niche)
    st.image(image_url, caption=f"Visual: {niche}", use_container_width=True)
    # -------------------------
        
    st.markdown(full_article)
    st.divider()
    st.markdown(seo_kit)
    
    payload = str(full_article) + "\n\n" + str(seo_kit)
    st.download_button("📥 Download", payload, "article.md", use_container_width=True)
