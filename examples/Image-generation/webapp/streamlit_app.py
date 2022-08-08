import streamlit as st
from RealESRGAN import RESRGAN
from PIL import Image
#import openai
import os
#from google.cloud import secretmanager 

#secret_id = 'openai_api_key'
#project_id = 'acto-su-1'
#version = 1    # use the management tools to determine version at runtime

#client = secretmanager.SecretManagerServiceClient()

#name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
#response = client.access_secret_version(request={"name":name})
#api_key = response.payload.data.decode('UTF-8')

#print("api_key", api_key)

st.title("Image Generator App")
st.text("by Nobody Special")

st.markdown(""" 

# About
 
## Provide some prompts and generate images

""")

reg = RESRGAN()
print('initializing realESRGAN')
with st.spinner("Reticulating splines ..."):
    reg.get_ready()

st.markdown("# Input")
with st.form(key="form"):
    story_prompt = st.text_input("story prompt")
    filename = st.text_input("file name root")

    #start = st.text_input("Begin writing the first few or several words of your story:")

    #slider = st.slider("How many characters do you want your story to be? ", min_value=64, max_value=750)
    #st.text("(A typical story is usually 100-500 characters)")

    submit_button = st.form_submit_button(label='Generate')
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    #openai.api_key = api_key

    if submit_button:
        with st.spinner("Generating image..."):
            reg.gen_images(story_prompt, filename)

        st.markdown("# Generated images:")
        st.subheader(filename)
        st.markdown("____")
        st.markdown("# story prompt")
        st.text(story_prompt)
        st.markdown("____")
        for i in range(4):
            fn = filename + str(i) + ".jpg"
            image = Image.open(fn)
            st.image(image, caption=fn)
            #st.markdown("____")

        st.subheader("You can try again if you're unhappy with the model's output")
