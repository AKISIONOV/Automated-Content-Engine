import streamlit as st
import strategist  # Importing your backend logic
import time

# 1. Page Configuration
# We use 'wide' layout so the article has more space in the center
st.set_page_config(
    page_title="ACE Engine",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR: CONTROLS & PROCESS ---
with st.sidebar:
    st.header("🎮 Control Panel")
    st.markdown("Define your content strategy here.")
    
    # Inputs moved to Sidebar
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
    audience = st.text_input("Target Audience", "University Students")
    
    st.markdown("---")
    
    # The Button moved to Sidebar
    generate_btn = st.button("🚀 Generate Full Article", type="primary", use_container_width=True)

    # Placeholder for the "Thinking" logs
    # We will populate this ONLY when the button is clicked
    status_container = st.container()

# --- MAIN AREA: DISPLAY ---
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# Main Logic
if generate_btn:
    
    # 1. SHOW PROCESS IN SIDEBAR
    with st.sidebar:
        with st.status("🧠 ACE is working...", expanded=True) as status:
            
            st.write("Thinking about strategy...")
            # 1. Strategy
            ideas = strategist.strategist_node(niche, audience)
            st.write("✅ Strategy Developed.")
            
            st.write("Architecting the blueprint...")
            # 2. Architect
            outline = strategist.architect_node(ideas)
            st.write("✅ Blueprint Designed.")
            
            st.write("Drafting content (this takes time)...")
            # 3. Content Factory
            article_title = f"{niche} for {audience}"
            full_article = strategist.content_factory_node(article_title, outline)
            st.write("✅ Article Written.")
            
            st.write("Polishing & SEO...")
            # 4. Polish
            seo_content = strategist.polish_node(full_article)
            st.write("✅ Done.")
            
            status.update(label="✨ Content Ready!", state="complete", expanded=False)

    # 2. SHOW RESULT IN CENTER (Main Area)
    
    # AI Cover Image
    image_prompt = f"cinematic high quality editorial photo of {niche}, minimal, 8k, vivid colors"
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
    
    # Create a nice layout for the result
    st.image(image_url, caption=f"Cover Art for {niche}", use_container_width=True)
    
    st.markdown(full_article)
    
    st.markdown("---")
    st.subheader("📊 SEO & Social Media Kit")
    st.markdown(seo_content)
    
    # Download Button (Bottom of Main Area)
    final_text = full_article + "\n\n---\n\n" + seo_content
    st.download_button(
        label="📥 Download Article & SEO Kit",
        data=final_text,
        file_name="ace_article.md",
        mime="text/markdown",
        use_container_width=True
    )

else:
    # Initial State (Before clicking button)
    st.info("👈 Enter your topic in the sidebar and click Generate to start.")
