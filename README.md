# Advice Quality Rater

A Streamlit application that uses Google's Gemini AI to rate advice quality on a scale of 1-10.

![Advice Rater Screenshot](https://i.imgur.com/example.png)

## Overview

This application allows users to:
- Input a piece of advice
- Describe the circumstances in which the advice was given
- Get an AI-powered rating from 1-10
- Receive detailed feedback on the quality of the advice

## Features

- Simple, intuitive interface
- Secure API key handling with session state
- Detailed analysis of advice quality
- Visual indicators for different rating levels
- Mobile-friendly UI

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI Python SDK
- A Gemini API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/advice-quality-rater.git
cd advice-quality-rater
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and go to the URL shown in the terminal (typically http://localhost:8501)

3. Enter your Gemini API key (get one at https://makersuite.google.com/app/apikey)

4. Input advice and circumstances, then click "Rate This Advice"

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it into the app when prompted

## Privacy Note

This application does not store your API key permanently. It's kept only in the session state while the app is running.

## Examples

**Example 1:**
- Advice: "Just invest all your money in cryptocurrency"
- Circumstances: "Given to a retired person living on fixed income"
- Rating: 2/10 - High risk advice that could jeopardize financial security

**Example 2:**
- Advice: "Apply for multiple positions and prepare well for interviews"
- Circumstances: "Recent graduate looking for their first job"
- Rating: 9/10 - Practical advice that improves chances of employment

## License

MIT

