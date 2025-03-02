import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time

# App title and description
st.set_page_config(page_title="Advice Rater", page_icon="🧠")

st.title("Advice Quality Rater 🧠")
st.markdown("### Rate the quality of advice from 1-10")

# Session state to store API key
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# Section for API key input
with st.expander("Configure Gemini API Key", expanded=not st.session_state.api_key_configured):
    # Preview section
    st.markdown("### 📱 App Preview")
    st.markdown("""
    Once configured, you'll be able to:
    1. Enter a piece of advice
    2. Describe the circumstances it was given in
    3. Get an AI-powered rating from 1-10
    4. Receive detailed feedback on why the advice is good/bad
    
    **Example Rating:**
    
    *Advice: "Just quit your job if you're not happy"*  
    *Circumstances: "Person is facing mild workplace stress but has a family to support and no savings"*
    
    **Rating: 2/10** ❌  
    *This advice fails to consider financial responsibilities and lacks a planned approach to career transition...*
    """)
    
    api_key = st.text_input("Enter your Gemini API Key", type="password", 
                           help="Get your API key from https://makersuite.google.com/app/apikey")
    
    if st.button("Save API Key"):
        if api_key:
            # Configure the API
            genai.configure(api_key=api_key)
            st.session_state.api_key = api_key
            st.session_state.api_key_configured = True
            st.success("API Key configured successfully!")
        else:
            st.error("Please enter a valid API Key")

# Main app functionality - only show if API key is configured
if st.session_state.get('api_key_configured'):
    genai.configure(api_key=st.session_state.api_key)
    
    advice = st.text_area("Enter the piece of advice:", 
                         placeholder="Example: You should invest all your money in crypto")
    
    circumstances = st.text_area("Describe the circumstances:", 
                               placeholder="Example: Advice given to a 65-year-old retiree with limited savings")
    
    if st.button("Rate This Advice"):
        if advice and circumstances:
            with st.spinner("Analyzing the advice..."):
                try:
                    # Get available models
                    models = genai.list_models()
                    gemini_models = [m.name for m in models if 'gemini' in m.name]
                    
                    # Use the first available Gemini model (or specific one if found)
                    model_name = 'models/gemini-1.0-pro'
                    for m in gemini_models:
                        if 'gemini-pro' in m:
                            model_name = m
                            break
                    
                    # Call Gemini API with correct model name
                    model = genai.GenerativeModel(model_name)
                    
                    prompt = f"""
                    Analyze this piece of advice: "{advice}"
                    
                    Given under these circumstances: "{circumstances}"
                    
                    Rate this advice on a scale of 1 to 10, where:
                    - 1 means terrible, potentially harmful advice
                    - 10 means excellent, well-considered advice
                    
                    Provide your numerical rating first, followed by a detailed explanation of why you gave this rating.
                    Format your response as:
                    
                    Rating: [number]/10
                    
                    Analysis: [your detailed explanation]
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # Display results
                    st.markdown("## Results")
                    st.markdown(response.text)
                    
                    # Extract the numerical rating if possible
                    try:
                        rating_text = response.text.split("Rating:")[1].split("/10")[0].strip()
                        rating = int(rating_text)
                        
                        # Visual indicator based on rating
                        if rating <= 3:
                            st.error(f"⚠️ This is poor advice - rated {rating}/10")
                        elif rating <= 6:
                            st.warning(f"⚠️ This advice is questionable - rated {rating}/10")
                        elif rating <= 8:
                            st.info(f"✅ This is decent advice - rated {rating}/10")
                        else:
                            st.success(f"🌟 This is excellent advice - rated {rating}/10")
                    except:
                        pass
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.error("If you're seeing a model error, the Gemini API may have changed. Try using a different model.")
                    
                    # Show available models for debugging
                    try:
                        models = genai.list_models()
                        st.write("Available models:")
                        for m in models:
                            st.write(f"- {m.name}")
                    except Exception as model_err:
                        st.error(f"Couldn't list models: {str(model_err)}")
        else:
            st.warning("Please enter both advice and circumstances.")
