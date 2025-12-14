import streamlit as st
import strategist
import urllib.parse
import requests
import io
from PIL import Image

# 1. CONFIG
st.set_page_config(page_title="ACE Engine", page_icon="⚡", layout="wide")

# 2. IMAGE ENGINE (Robust Download)
def get_image(prompt_text):
    """
    Downloads image bytes directly to prevent Streamlit URL crashes.
    """
    safe_prompt = urllib.parse.quote(prompt_text[:100])
    
    # OPTION A: Hugging Face (Best Quality)
    if "HF_TOKEN" in st.secrets:
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
            payload = {"inputs": f"editorial photo of {prompt_text}, high quality, minimal"}
            response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
        except:
            pass # Fail silently to fallback

    # OPTION B: Pollinations (Fallback)
    try:
        # We DOWNLOAD the image here instead of letting Streamlit guess
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        return None
    
    return None

# 3. SIDEBAR
with st.sidebar:
    st.title("🎛️ ACE Control")
    niche = st.text_input("Niche", "Artificial Intelligence")
    audience = st.text_input("Audience", "University Students")
    st.divider()
    btn = st.button("🚀 Auto-Pilot Launch", type="primary", use_container_width=True)

# 4. MAIN APP
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")

if btn:
    with st.status("🚀 System Running...", expanded=True) as status:
        
        # 1. Strategy
        try:
            ideas = strategist.strategist_node(niche, audience)
            best_idea = ideas[0] if isinstance(ideas, list) else str(ideas)
            st.info(f"Selected Angle: {best_idea}")
        except:
            st.error("Strategy Failed. Try a simpler topic.")
            st.stop()
            
        # 2. Architecture (Dynamic)
        try:
            headers = strategist.architect_node(best_idea)
            st.write(f"Blueprint: {headers}")
        except:
            headers = ["The Challenge", "The Solution", "Key Examples", "Conclusion"]
            
        # 3. Writing
        full_article = strategist.content_factory_node(best_idea, headers)
        
        # 4. Polish
        seo_kit = strategist.polish_node(full_article)
        
        # 5. Image (Parallel)
        st.write("🎨 Generating Visuals...")
        img_result = get_image(niche)
        
        status.update(label="Done!", state="complete", expanded=False)

    # 5. RESULTS DISPLAY
    if img_result:
        st.image(img_result, caption="Cover Art", use_container_width=True)
    else:
        st.warning("⚠️ Cover image could not be generated (Network Timeout).")
        
    st.markdown(full_article)
    st.divider()
    st.markdown(seo_kit)
    
    payload = str(full_article) + "\n\n" + str(seo_kit)
    st.download_button("📥 Download", payload, "article.md")
