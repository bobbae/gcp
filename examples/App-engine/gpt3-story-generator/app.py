import streamlit as st
import openai
import os
#from google.cloud import secretmanager 

#secret_id = 'openai_api_key'
#project_id = 'my-project-1'
#version = 1    # use the management tools to determine version at runtime

#client = secretmanager.SecretManagerServiceClient()

#name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
#response = client.access_secret_version(request={"name":name})
#api_key = response.payload.data.decode('UTF-8')

#print("api_key", api_key)

st.title("Story Generator App")
st.text("by Nobody Special")

st.markdown(""" 

# About
 
## Play around with the sliders and text fields to generate your very own stories! 

""")

st.markdown("# Generate a story")

with st.form(key="form"):
    api_key = st.text_input("Provide your API key here:")
    prompt = st.text_input("Describe the kind of story you want to be written.")
    st.text(f"(Example: Write me a funny story for children to enjoy)")

    start = st.text_input("Begin writing the first few or several words of your story:")

    slider = st.slider("How many characters do you want your story to be? ", min_value=64, max_value=750)
    st.text("(A typical story is usually 100-500 characters)")

    submit_button = st.form_submit_button(label='Generate story')
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    if submit_button:
        with st.spinner("Generating story..."):
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt + "\n\n" + start,
                temperature=0.71,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.36,
                presence_penalty=0.75
                )
            output = response.get("choices")[0]['text']
        st.markdown("# Story Output:")
        st.subheader(start + output)

        st.markdown("____")
        st.markdown("# Review the story")
        st.subheader("You can press the Generate story Button again if you're unhappy with the model's output")
        
      
