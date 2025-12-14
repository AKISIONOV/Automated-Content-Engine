import streamlit as st
import strategist
import urllib.parse  # <--- CRITICAL FIX: Helps fix broken URLs

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

# 3. SIDEBAR CONTROLS
with st.sidebar:
    st.title("🎛️ ACE Control")
    
    # Theme Selection
    theme = st.selectbox("🎨 Interface Theme", ["Default (System)", "Dark Mode", "Light Mode", "Hacker Green"])
    apply_theme(theme)
    st.divider()

    # Inputs
    st.subheader("📍 Target Parameters")
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
    audience = st.text_input("Target Audience", "University Students")
    
    st.divider()
    
    # The One Button
    generate_btn = st.button("🚀 Launch Auto-Pilot", type="primary", use_container_width=True)
    
    st.caption("ACE will analyze, structure, write, and optimize content automatically.")

# 4. MAIN INTERFACE
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# 5. EXECUTION LOGIC
if generate_btn:
    
    # Create a container for the final result
    result_container = st.container()
    
    # Use a status container for the live "Thinking" logs
    with st.status("🚀 ACE Systems Engaged...", expanded=True) as status:
        
        # --- STEP 1: STRATEGY ---
        st.write("🧠 PHASE 1: Strategic Analysis...")
        try:
            # We fetch ideas, but since it's auto-pilot, we just grab the best one automatically
            ideas = strategist.strategist_node(niche, audience)
            
            # Smart Selection: If it's a list, take the first. If string, take it all.
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
            
        # --- STEP 3: WRITING (THE FACTORY) ---
        st.write("🏭 PHASE 3: Content Generation (This may take 30-60s)...")
        try:
            # Create a specific title context for the writer
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

        status.update(label="✅ Mission Complete!", state="complete", expanded=False)

    # 6. DISPLAY RESULTS (In the main container)
    with result_container:
        
        # --- THE FIX FOR THE IMAGE CRASH ---
        try:
            # We "Clean" the prompt so it fits in a URL (replace spaces with %20)
            raw_prompt = f"editorial photo of {niche}, minimal, high quality"
            encoded_prompt = urllib.parse.quote(raw_prompt) 
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            st.image(image_url, caption=f"AI Generated Art for {niche}", use_container_width=True)
        except:
            st.warning("⚠️ Could not generate cover image (Network or URL error).")
        # -----------------------------------

        # The Main Article
        st.subheader("📄 The Article")
        st.markdown(str(full_article))
        
        st.divider()
        
        # The SEO Kit
        st.subheader("📊 SEO Strategy Kit")
        st.markdown(str(seo_kit))
        
        # Download Button
        final_payload = str(full_article) + "\n\n---\n\n" + str(seo_kit)
        st.download_button(
            label="📥 Download Full Article Package",
            data=final_payload,
            file_name="ace_content_package.md",
            mime="text/markdown",
            type="primary",
            use_container_width=True
        )

else:
    # Idle State Display
    st.info("👈 Enter your topic in the sidebar and click 'Launch Auto-Pilot' to begin.")
