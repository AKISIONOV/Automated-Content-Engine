import streamlit as st
import strategist
import urllib.parse
import requests
import io

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

# 3. SAFE IMAGE DOWNLOADER (The Fix)
def get_image_bytes(prompt_text):
    """
    Downloads the image data directly. 
    This prevents Streamlit from crashing on URL timeouts.
    """
    try:
        # Simplify prompt to avoid URL errors
        short_prompt = prompt_text[:40]
        safe_prompt = urllib.parse.quote(f"editorial photo of {short_prompt}, high quality")
        
        # Pollinations URL (No Logo)
        url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){safe_prompt}?nologo=true&width=1024&height=512"
        
        # Download with a strict timeout
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.content # Return the raw image data
    except:
        pass
    return None

# 4. SIDEBAR
with st.sidebar:
    st.title("🎛️ ACE Control")
    theme = st.selectbox("🎨 Interface Theme", ["Default (System)", "Dark Mode", "Light Mode", "Hacker Green"])
    apply_theme(theme)
    st.divider()

    niche = st.text_input("Niche / Topic", "Artificial Intelligence")
    audience = st.text_input("Audience", "University Students")
    st.divider()
    
    # ONE BUTTON TO RULE THEM ALL
    btn = st.button("🚀 Auto-Pilot Launch", type="primary", use_container_width=True)

# 5. MAIN APP
st.title("⚡ ACE: Automated Content Engine")

if btn:
    with st.status("🚀 System Running...", expanded=True) as status:
        
        # 1. Strategy
        try:
            ideas = strategist.strategist_node(niche, audience)
            # Pick the first idea automatically
            best_idea = ideas[0] if isinstance(ideas, list) else str(ideas)
            st.info(f"Selected Angle: {best_idea[:80]}...")
        except:
            st.error("Strategy Failed. Using fallback.")
            best_idea = f"The Future of {niche} for {audience}"
            
        # 2. Architecture
        try:
            headers = strategist.architect_node(best_idea)
            st.write("Blueprint Designed.")
        except:
            headers = ["The Challenge", "The Solution", "Practical Steps", "Conclusion"]
            
        # 3. Writing
        full_article = strategist.content_factory_node(best_idea, headers)
        
        # 4. Polish
        seo_kit = strategist.polish_node(full_article)
        
        # 5. Image Generation (Parallel)
        st.write("🎨 Generating Visuals...")
        image_bytes = get_image_bytes(niche)
        
        status.update(label="Done!", state="complete", expanded=False)

    # 6. RESULTS DISPLAY
    
    # Display Image from Bytes (Safe Mode)
    if image_bytes:
        st.image(image_bytes, caption=f"Visual: {niche}", use_container_width=True)
    else:
        st.warning("⚠️ Image could not be generated (Network Timeout).")
        
    st.markdown(full_article)
    st.divider()
    with st.expander("View SEO Strategy Kit"):
        st.markdown(seo_kit)
    
    # 7. DOWNLOAD
    payload = str(full_article) + "\n\n---\n\n" + str(seo_kit)
    st.download_button(
        label="📥 Download Article (Markdown)",
        data=payload,
        file_name="ace_article.md",
        type="primary",
        use_container_width=True
    )
