import streamlit as st
import strategist  # Importing your backend logic
import time

# 1. Page Configuration (The "Look and Feel")
st.set_page_config(
    page_title="ACE Engine",
    page_icon="⚡",
    layout="centered"
)

# 2. The Header (Center Stage)
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# 3. The Inputs (Center Columns instead of Sidebar)
col1, col2 = st.columns(2)

with col1:
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")

with col2:
    audience = st.text_input("Target Audience", "University Students")

# 4. The "Big Red Button"
if st.button("🚀 Generate Full Article", type="primary", use_container_width=True):
    
    # --- PHASE 1: STRATEGY ---
    with st.status("🧠 ACE is working...", expanded=True) as status:
        
        st.write("Thinking about strategy...")
        # Call the Strategist
        ideas = strategist.strategist_node(niche, audience)
        st.write("✅ Strategy Developed.")
        
        st.write("Architecting the blueprint...")
        # Call the Architect
        outline = strategist.architect_node(ideas)
        st.write("✅ Blueprint Designed.")
        
        st.write("Drafting the content...")
        # Call the Writer
        full_article = strategist.writer_node(outline)
        st.write("✅ Article Written.")
        
        status.update(label="✨ Content Ready!", state="complete", expanded=False)

    # --- PHASE 2: THE REVEAL ---
    
    st.divider()
    
    # 5. The AI Cover Image (Free Pollinations Integration)
    # We create a dynamic prompt for the image based on the user's niche
    image_prompt = f"cinematic high quality editorial photo of {niche}, minimal, 8k, vivid colors"
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
    
    st.image(image_url, caption=f"AI Generated Cover Art for {niche}", use_container_width=True)
    
    # 6. The Article
    st.markdown(full_article)
    
    # 7. Download Button
    st.download_button(
        label="📥 Download Article",
        data=full_article,
        file_name="ace_article.md",
        mime="text/markdown"
    )