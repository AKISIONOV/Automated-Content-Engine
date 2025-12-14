import streamlit as st
import strategist
import urllib.parse
import requests
import io
from PIL import Image

# 1. CONFIGURATION
st.set_page_config(
    page_title="ACE Engine",
    page_icon="⚡",
    layout="wide"
)

# 2. THEME ENGINE
def apply_theme(theme_choice):
    if theme_choice == "Dark Mode":
        st.markdown("""<style>.stApp { background-color: #0e1117; color: white; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Light Mode":
        st.markdown("""<style>.stApp { background-color: #ffffff; color: black; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Hacker Green":
        st.markdown("""<style>.stApp { background-color: #002b36; color: #859900; }</style>""", unsafe_allow_html=True)

# 3. IMAGE GENERATOR (Hugging Face API)
def generate_image(prompt):
    """
    Generates an image using Hugging Face's Free Inference API.
    Model: StabilityAI Stable Diffusion XL (High Quality, No Watermark)
    """
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    # Try to get token, but allow running without it (fallback to pollinations if needed)
    try:
        hf_token = st.secrets["HF_TOKEN"]
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Enhanced prompt for better quality
        full_prompt = f"editorial style photo of {prompt}, 8k resolution, highly detailed, professional photography, cinematic lighting, minimal style"
        
        response = requests.post(API_URL, headers=headers, json={"inputs": full_prompt})
        
        if response.status_code == 200:
            image_bytes = response.content
            return Image.open(io.BytesIO(image_bytes))
        else:
            return None
    except:
        return None

# 4. SIDEBAR CONTROLS
with st.sidebar:
    st.title("🎛️ ACE Control")
    theme = st.selectbox("🎨 Interface Theme", ["Default (System)", "Dark Mode", "Light Mode", "Hacker Green"])
    apply_theme(theme)
    st.divider()

    st.subheader("📍 Target Parameters")
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
    audience = st.text_input("Target Audience", "University Students")
    
    st.divider()
    generate_btn = st.button("🚀 Launch Auto-Pilot", type="primary", use_container_width=True)

# 5. MAIN INTERFACE
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# 6. EXECUTION LOGIC
if generate_btn:
    result_container = st.container()
    
    with st.status("🚀 ACE Systems Engaged...", expanded=True) as status:
        
        # --- STEP 1: STRATEGY ---
        st.write("🧠 PHASE 1: Strategic Analysis...")
        try:
            ideas = strategist.strategist_node(niche, audience)
            if isinstance(ideas, list) and len(ideas) > 0:
                best_idea = ideas[0]
            else:
                best_idea = str(ideas)
            st.info(f"Selected Angle: {str(best_idea)[:80]}...")
        except Exception as e:
            st.error(f"Strategy Error: {e}")
            st.stop()

        # --- STEP 2: ARCHITECTURE ---
        st.write("📐 PHASE 2: Structural Blueprinting...")
        try:
            outline = strategist.architect_node(best_idea)
        except Exception as e:
            st.error(f"Architect Error: {e}")
            st.stop()
            
        # --- STEP 3: WRITING ---
        st.write("🏭 PHASE 3: Content Generation...")
        try:
            title_context = f"{niche} for {audience}"
            full_article = strategist.content_factory_node(title_context, outline)
        except Exception as e:
            st.error(f"Writing Error: {e}")
            st.stop()

        # --- STEP 4: POLISHING ---
        st.write("✨ PHASE 4: SEO & Final Polish...")
        try:
            seo_kit = strategist.polish_node(full_article)
        except Exception as e:
            st.error(f"Polish Error: {e}")
            st.stop()
            
        # --- STEP 5: IMAGE GENERATION (Running in background) ---
        st.write("🎨 PHASE 5: Generating Visuals...")
        generated_img = generate_image(niche)

        status.update(label="✅ Mission Complete!", state="complete", expanded=False)

    # 7. DISPLAY RESULTS
    with result_container:
        
        # Display Image (Hugging Face or Fallback)
        if generated_img:
            st.image(generated_img, caption=f"AI Generated Art for {niche}", use_container_width=True)
        else:
            # Fallback to Pollinations if HF fails or no token
            safe_prompt = urllib.parse.quote(f"editorial photo of {niche}")
            st.image(f"https://image.pollinations.ai/prompt/{safe_prompt}", caption="Visuals (Fallback)", use_container_width=True)

        st.subheader("📄 The Article")
        st.markdown(str(full_article))
        st.divider()
        st.subheader("📊 SEO Strategy Kit")
        st.markdown(str(seo_kit))
        
        final_payload = str(full_article) + "\n\n---\n\n" + str(seo_kit)
        st.download_button("📥 Download Full Package", final_payload, "ace_content.md", "text/markdown", type="primary", use_container_width=True)

else:
    st.info("👈 Enter your topic in the sidebar and click 'Launch Auto-Pilot' to begin.")
