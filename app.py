import streamlit as st
import strategist  # Importing your backend logic
import time

# 1. Page Configuration
st.set_page_config(
    page_title="ACE Engine",
    page_icon="⚡",
    layout="centered"
)

# 2. The Header
st.title("⚡ ACE: Automated Content Engine")
st.markdown("### Build viral, expert-level articles in seconds.")
st.markdown("---")

# 3. The Inputs
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("Topic / Niche", "Artificial Intelligence")
with col2:
    audience = st.text_input("Target Audience", "University Students")

# 4. The "Big Red Button"
if st.button("🚀 Generate Full Article", type="primary", use_container_width=True):
    
    # --- PHASE 1: STRATEGY & WRITING ---
    with st.status("🧠 ACE is working...", expanded=True) as status:
        
        st.write("Thinking about strategy...")
        # 1. Strategy
        ideas = strategist.strategist_node(niche, audience)
        st.write("✅ Strategy Developed.")
        
        st.write("Architecting the blueprint...")
        # 2. Architect
        outline = strategist.architect_node(ideas)
        st.write("✅ Blueprint Designed.")
        
        st.write("Drafting the content (This may take a minute)...")
        # 3. Content Factory (UPDATED FUNCTION NAME)
        # We create a title context for the factory
        article_title = f"{niche} for {audience}"
        full_article = strategist.content_factory_node(article_title, outline)
        st.write("✅ Article Written.")
        
        st.write("Polishing and SEO...")
        # 4. Polish (NEW STEP)
        seo_content = strategist.polish_node(full_article)
        st.write("✅ Content Polished.")
        
        status.update(label="✨ Content Ready!", state="complete", expanded=False)

    # --- PHASE 2: THE REVEAL ---
    st.divider()
    
    # 5. AI Cover Image
    image_prompt = f"cinematic high quality editorial photo of {niche}, minimal, 8k, vivid colors, style : photorealistic"
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
    st.image(image_url, caption=f"AI Generated Cover Art for {niche}", use_container_width=True)
    
    # 6. The Article
    st.subheader("📄 The Article")
    st.markdown(full_article)
    
    st.divider()
    
    # 7. SEO & Socials (New Section)
    st.subheader("📊 SEO & Social Media Kit")
    st.markdown(seo_content)
    
    # 8. Download Button (Downloads EVERYTHING)
    final_text = full_article + "\n\n---\n\n" + seo_content
    st.download_button(
        label="📥 Download Article & SEO Kit",
        data=final_text,
        file_name="ace_article.md",
        mime="text/markdown"
    )
