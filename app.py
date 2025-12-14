import streamlit as st
import strategist  # Importing your backend logic
import time
import json

# 1. Page Configuration
st.set_page_config(
    page_title="ACE Engine",
    page_icon="⚡",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
# This acts as the app's "Short Term Memory"
if "step" not in st.session_state:
    st.session_state.step = "idle" # idle, strategy_done, writing_done
if "generated_ideas" not in st.session_state:
    st.session_state.generated_ideas = []
if "selected_idea_text" not in st.session_state:
    st.session_state.selected_idea_text = ""
if "final_article" not in st.session_state:
    st.session_state.final_article = ""
if "seo_kit" not in st.session_state:
    st.session_state.seo_kit = ""

# --- THEME ENGINE (CSS INJECTOR) ---
def apply_theme(theme_choice):
    if theme_choice == "Hacker Mode":
        st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #00ff41; }
        .stMarkdown, .stText, h1, h2, h3 { color: #00ff41 !important; font-family: 'Courier New', Courier, monospace; }
        .stButton button { border: 1px solid #00ff41; color: #00ff41; background-color: transparent; }
        </style>
        """, unsafe_allow_html=True)
    elif theme_choice == "Paper Writer":
        st.markdown("""
        <style>
        .stApp { background-color: #f4f1ea; color: #2c2c2c; }
        .stMarkdown, p, h1, h2, h3 { font-family: 'Georgia', serif; color: #333; }
        </style>
        """, unsafe_allow_html=True)

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.title("🎛️ ACE Control")
    
    # 1. VISUAL THEME
    theme = st.selectbox("🎨 Interface Theme", ["Standard", "Hacker Mode", "Paper Writer"])
    apply_theme(theme)
    st.divider()

    # 2. INPUTS
    st.subheader("1. Define Target")
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
    audience = st.text_input("Audience", "University Students")
    
    st.subheader("2. Select Pilot Mode")
    pilot_mode = st.radio(
        "How do you want to drive?",
        ["Auto-Pilot 🚀", "Manual Control 🕹️"],
        captions=["AI picks the best idea & writes immediately.", "You review ideas & choose the best one."]
    )
    
    st.divider()
    
    # 3. ACTION BUTTONS
    # The buttons change based on the mode
    if pilot_mode == "Auto-Pilot 🚀":
        action_btn = st.button("🚀 Launch Full Sequence", type="primary", use_container_width=True)
    else:
        # Manual Mode Buttons
        if st.session_state.step == "idle":
            action_btn = st.button("🔍 Scan for Ideas", type="primary", use_container_width=True)
        elif st.session_state.step == "strategy_done":
            action_btn = st.button("✍️ Write Article", type="primary", use_container_width=True)
        else:
            action_btn = st.button("🔄 Reset / Start Over", use_container_width=True)


# --- MAIN LOGIC ENGINE ---

# Title Area
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# LOGIC BRANCH 1: AUTO-PILOT (The "Speed" Route)
if pilot_mode == "Auto-Pilot 🚀" and action_btn:
    
    with st.status("🚀 Auto-Pilot Engaged...", expanded=True) as status:
        st.write("🧠 Strategizing...")
        ideas = strategist.strategist_node(niche, audience)
        
        # In Auto, we just grab the first (best) idea
        if isinstance(ideas, list) and len(ideas) > 0:
            best_idea = ideas[0]
        else:
            best_idea = str(ideas) # Fallback if it's a string
            
        st.write(f"✅ Selected Strategy: {best_idea[:50]}...")
        
        st.write("📐 Architecting & Writing...")
        outline = strategist.architect_node(best_idea)
        title_context = f"{niche} for {audience}"
        
        full_article = strategist.content_factory_node(title_context, outline)
        st.write("✅ Draft Complete.")
        
        st.write("✨ Polishing & SEO...")
        seo = strategist.polish_node(full_article)
        
        # Save to session state so it persists
        st.session_state.final_article = full_article
        st.session_state.seo_kit = seo
        st.session_state.step = "writing_done"
        
        status.update(label="✨ Mission Complete!", state="complete", expanded=False)


# LOGIC BRANCH 2: MANUAL CONTROL (The "Custom" Route)

# Step A: Scan for Ideas
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "idle":
    with st.spinner("🧠 Brainstorming creative angles..."):
        raw_ideas = strategist.strategist_node(niche, audience)
        
        # Ensure it's a list for the radio button
        if isinstance(raw_ideas, list):
            st.session_state.generated_ideas = raw_ideas
        else:
            # Fallback: if AI returned a string, wrap it in a list
            st.session_state.generated_ideas = [raw_ideas]
            
        st.session_state.step = "strategy_done"
        st.rerun() # Refresh to show the selection UI

# Step B: User Selection UI (Only shows if Strategy is Done)
if pilot_mode == "Manual Control 🕹️" and st.session_state.step == "strategy_done":
    st.info("👇 The Strategist found these angles. Select your favorite:")
    
    # THE SELECTION WIDGET
    user_choice = st.radio(
        "Select an Idea Strategy:",
        st.session_state.generated_ideas,
        index=0
    )
    st.session_state.selected_idea_text = user_choice
    
    st.success("Target Locked. Click 'Write Article' in the sidebar to proceed.")


# Step C: Write the Article (Triggered by Sidebar Button in 'strategy_done' state)
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "strategy_done":
    
    with st.status("✍️ Writing your custom selection...", expanded=True) as status:
        target_idea = st.session_state.selected_idea_text
        
        st.write("📐 Architecting...")
        outline = strategist.architect_node(target_idea)
        
        st.write("🏭 Content Factory Running...")
        title_context = f"{niche} for {audience}"
        full_article = strategist.content_factory_node(title_context, outline)
        
        st.write("✨ Polishing...")
        seo = strategist.polish_node(full_article)
        
        # Save results
        st.session_state.final_article = full_article
        st.session_state.seo_kit = seo
        st.session_state.step = "writing_done"
        
        status.update(label="✨ Done!", state="complete", expanded=False)

# Reset Logic
if pilot_mode == "Manual Control 🕹️" and action_btn and st.session_state.step == "writing_done":
    st.session_state.step = "idle"
    st.session_state.final_article = ""
    st.rerun()


# --- DISPLAY RESULTS (Common for both modes) ---
if st.session_state.step == "writing_done":
    
    st.divider()
    
    # AI Cover Image
    image_prompt = f"cinematic high quality editorial photo of {niche}, minimal, 8k, vivid colors"
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
    st.image(image_url, caption=f"Cover Art for {niche}", use_container_width=True)
    
    # Article Display
    st.markdown(st.session_state.final_article)
    
    st.divider()
    st.subheader("📊 SEO & Social Kit")
    st.markdown(st.session_state.seo_kit)
    
    # Download
    final_payload = st.session_state.final_article + "\n\n---\n\n" + st.session_state.seo_kit
    st.download_button(
        label="📥 Download Everything",
        data=final_payload,
        file_name="ace_article.md",
        mime="text/markdown",
        use_container_width=True
    )
