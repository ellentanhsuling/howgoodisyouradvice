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
    
    *Advice: "Just take it like any normal day and deal with it."*  
    *Circumstances: "Person is facing an emergency situation that is out of their control and is on the verge of mental and emotional breakdown"*
    
    **Rating: 2/10** ❌  
    *
The advice "just take it like a normal day" can be problematic for someone experiencing an emotional breakdown. Here's why:
Emotional intensity: Emotional breakdowns are characterized by intense emotions, which can't simply be "taken as usual." The individual may feel overwhelmed, anxious, or despairing, making it challenging to function normally.
Lack of understanding: This advice might imply that the person is overreacting or being too sensitive, which can lead to feelings of shame, guilt, and isolation. Emotional breakdowns are not a sign of weakness; they're a natural response to overwhelming situations.
Inadequate support: The "just take it like a normal day" approach might discourage individuals from seeking help or talking about their emotions. This can perpetuate the stigma surrounding mental health issues and prevent people from getting the support they need.
Unrealistic expectations: Emotional breakdowns often require more than just "taking things as usual." They may necessitate taking time to process, reflect, and recharge.
Instead of this advice, consider these alternatives:
Acknowledge your emotions: Recognize that emotional breakdowns are a normal response to intense situations.
Seek support: Reach out to trusted friends, family members, or mental health professionals for guidance and validation.
Practice self-care: Engage in activities that promote relaxation, stress relief, and overall well-being (e.g., exercise, meditation, creative pursuits).
Take small steps: Break down overwhelming tasks into smaller, manageable chunks to help regain control and confidence.
Remember, emotional breakdowns are not a sign of weakness; they're an opportunity for growth, self-awareness, and healing.*
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
                    # Call Gemini API
                    model = genai.GenerativeModel('gemini-pro')
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
        else:
            st.warning("Please enter both advice and circumstances.")
