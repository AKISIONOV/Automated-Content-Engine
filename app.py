import streamlit as st
import strategist
import ast 
import urllib.parse # <--- NEW IMPORT: For fixing the image URL

# 1. CONFIG
st.set_page_config(page_title="ACE Engine", page_icon="⚡", layout="wide")

# 2. SESSION STATE
if "step" not in st.session_state: st.session_state.step = "idle"
if "generated_ideas" not in st.session_state: st.session_state.generated_ideas = []
if "selected_idea_text" not in st.session_state: st.session_state.selected_idea_text = ""
if "final_article" not in st.session_state: st.session_state.final_article = ""
if "seo_kit" not in st.session_state: st.session_state.seo_kit = ""

# 3. THEME ENGINE
def apply_theme(theme_choice):
    if theme_choice == "Dark Mode":
        st.markdown("""<style>.stApp { background-color: #0e1117; color: white; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Light Mode":
        st.markdown("""<style>.stApp { background-color: #ffffff; color: black; }</style>""", unsafe_allow_html=True)
    elif theme_choice == "Custom (Green)":
        st.markdown("""<style>.stApp { background-color: #002b36; color: #859900; }</style>""", unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🎛️ ACE Control")
    theme = st.selectbox("🎨 Theme", ["Default (System)", "Dark Mode", "Light Mode", "Custom (Green)"])
    apply_theme(theme)
    st.divider()

    st.subheader("1. Strategy Inputs")
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
    audience = st.text_input("Audience", "University Students")
    
    st.subheader("2. Pilot Mode")
    pilot_mode = st.radio("Mode:", ["Auto-Pilot 🚀", "Manual Control 🕹️"])
    st.divider()
    
    if pilot_mode == "Auto-Pilot 🚀":
        action_btn = st.button("🚀 Launch Sequence", type="primary", use_container_width=True)
    else:
        if st.session_state.step == "idle":
            action_btn = st.button("🔍 Scan for Ideas", type="primary", use_container_width=True)
        elif st.session_state.step == "strategy_done":
            action_btn = st.button("✍️ Write Article", type="primary", use_container_width=True)
        else:
            action_btn = st.button("🔄 Start Over", use_container_width=True)

# 5. MAIN CONTENT
st.title("⚡ ACE: Automated Content Engine")
st.markdown("---")

# AUTO PILOT LOGIC
if pilot_mode == "Auto-Pilot 🚀" and action_btn:
    with st.status("🚀 Auto-Pilot Engaged...", expanded=True) as status:
        st.write("🧠 Strategizing...")
        ideas = strategist.strategist_node(niche, audience)
        
        if isinstance(ideas, list) and len(ideas) > 0:
            best_idea = ideas[0]
        else:
            best_idea = str(ideas)
            
        st.write(f"✅ Selected: {str(best_idea)[:50]}...")
        st.write("📐 Architecting...")
        outline = strategist.architect_node(best_idea)
        
        full_article = strategist.content_factory_node(f"{niche} for {audience}", outline)
        seo = strategist.polish_node(full_article)
        
        st.session_state.final_article = full_article
        st.session_state.seo_kit = seo
        st.session_state.step = "writing_done"
        status.update(label="✨ Done!", state="complete", expanded=False)

# MANUAL LOGIC - Step A: Scan
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "idle":
    with st.spinner("🧠 Scanning..."):
        raw_ideas = strategist.strategist_node(niche, audience)
        
        final_list = []
        if isinstance(raw_ideas, list):
            final_list = raw_ideas
        elif isinstance(raw_ideas, str):
            try:
                import re
                list_match = re.search(r"\[.*\]", raw_ideas, re.DOTALL)
                if list_match:
                    clean_str = list_match.group(0)
                    final_list = ast.literal_eval(clean_str)
                else:
                    final_list = [raw_ideas]
            except:
                final_list = [raw_ideas]
        
        st.session_state.generated_ideas = final_list
        st.session_state.step = "strategy_done"
        st.rerun()

# MANUAL LOGIC - Step B: Selection
if pilot_mode == "Manual Control 🕹️" and st.session_state.step == "strategy_done":
    st.info("👇 Select your content strategy:")
    
    if st.session_state.generated_ideas and isinstance(st.session_state.generated_ideas, list):
        user_choice = st.radio(
            "Available Angles:",
            st.session_state.generated_ideas,
            index=0
        )
        st.session_state.selected_idea_text = user_choice
        st.success("Target Locked. Click 'Write Article' in the sidebar.")
    else:
        st.error("Error with ideas format. Please Reset.")
        if st.button("Reset"):
            st.session_state.step = "idle"
            st.rerun()

# MANUAL LOGIC - Step C: Write
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "strategy_done":
    with st.status("✍️ Writing...", expanded=True) as status:
        target_idea = st.session_state.selected_idea_text
        
        st.write("📐 Architecting...")
        outline = strategist.architect_node(target_idea)
        
        # Pass title + audience as simple context string
        full_article = strategist.content_factory_node(f"{niche} for {audience}", outline)
        
        st.write("✨ Polishing...")
        seo = strategist.polish_node(full_article)
        
        st.session_state.final_article = full_article
        st.session_state.seo_kit = seo
        st.session_state.step = "writing_done"
        status.update(label="✨ Done!", state="complete", expanded=False)

# Reset
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "writing_done":
    st.session_state.step = "idle"
    st.rerun()

# DISPLAY RESULT
if st.session_state.step == "writing_done":
    
    # --- THE FIX FOR THE IMAGE ---
    # We clean the prompt so it fits in a URL (replace spaces with %20)
    raw_prompt = f"editorial photo of {niche}, minimal, high quality"
    encoded_prompt = urllib.parse.quote(raw_prompt) 
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    try:
        st.image(image_url, caption="Cover Art", use_container_width=True)
    except:
        st.warning("Could not generate image due to high traffic.")
    # -----------------------------
    
    # SAFETY: Ensure we display Strings, not Lists
    safe_article = str(st.session_state.final_article)
    safe_seo = str(st.session_state.seo_kit)
    
    st.markdown(safe_article)
    st.divider()
    st.markdown(safe_seo)
    
    final_payload = safe_article + "\n\n---\n\n" + safe_seo
    st.download_button("📥 Download Full Kit", final_payload, "ace_article.md", "text/markdown", use_container_width=True)
