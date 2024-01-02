import os
import openai
import streamlit as st

# Set your OpenAI API key
openaikey = os.environ["openaikey"]
openai.api_key = openaikey

def get_openai_response(prompt, history):
    try:
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        # Append the history to the messages
        for message in history:
            # Split each message into role and content
            role, content = message.split(': ', 1)
            if "You" in role:
                role = "user"
            elif "Chatbot" in role:
                role = "assistant"
            else:
                continue  # Skip any messages with unrecognized roles
            messages.append({"role": role, "content": content})
        
        # Add the current prompt to the messages
        messages.append({"role": "user", "content": prompt})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


def format_response(response_text, max_line_length=80):
    words = response_text.split()
    line = ''
    formatted_text = ''

    for word in words:
        if len(line + word) > max_line_length:
            formatted_text += line.rstrip() + '\n'
            line = ''
        line += word + ' '

    # Add the last line
    formatted_text += line.rstrip()

    return formatted_text

def main():
    # Replace 'YOUR_IMAGE_URL' with the actual URL of your image
    #background_url = "https://drive.google.com/uc?export=view&id=1mOtyD3Ml2TE_d-WJu69vVRYvVDos3SiH"

    st.markdown(
    """
    <style>
        body {
            background-image: url("https://drive.google.com/uc?export=view&id=1mOtyD3Ml2TE_d-WJu69vVRYvVDos3SiH");
            background-size: cover;
            color: #333333;  /* Adjust text color for readability if necessary */
            font-family: 'Georgia', serif;
        }
        h1 {
            color: #01579b;  /* Dark blue for titles */
            font-family: 'Raleway', sans-serif;
        }
        .widget label, .stTextInput > label, .st-bb, .st-at, .st-ae {
            color: #01579b;  /* Dark blue for widget labels */
        }
        .css-2trqyj {
            background-color: #e0f2f1;  /* Match the body background */
        }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    st.title("Hospital Chatbot")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    user_input = st.text_input("Type your message here and press Enter:")

    if user_input:
           # Add user input to history with bold labels
           st.session_state['history'].append(f"**You**: {user_input}")
           
           # Get response from OpenAI with conversation history
           response = get_openai_response(user_input, st.session_state['history'])
    
           # Format and add response to history with bold labels
           formatted_response = format_response(response)
           st.session_state['history'].append(f"**Chatbot**: {formatted_response}")
    
           # Display conversation history using markdown for bold formatting
           for message in st.session_state['history']:
               st.markdown(message, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
