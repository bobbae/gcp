import streamlit as st
import socket
from PIL import Image
#import openai
import os
#from google.cloud import secretmanager 
import transformers
from transformers import BloomTokenizerFast, BloomModel
from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
import torch

#tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-350m")
#model = BloomModel.from_pretrained("bigscience/bloom-350m")
model = BloomForCausalLM.from_pretrained("bigscience/bloom-1b3")
tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-1b3")
result_length = 150

#secret_id = 'openai_api_key'
#project_id = 'acto-su-1'
#version = 1    # use the management tools to determine version at runtime

#client = secretmanager.SecretManagerServiceClient()

#name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
#response = client.access_secret_version(request={"name":name})
#api_key = response.payload.data.decode('UTF-8')

max_length = 1440
port =  5000
address = '127.0.0.1'

client_socket = socket.socket()
client_socket.connect((address,port))
#client_socket.close()

st.title("Image Generator App")
st.markdown("#### by Nobody Special")

st.markdown(""" 

### About
 
#### Provide some prompts and generate images

""")

st.markdown("### Input")
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
        message = '{ "story_prompt": "' + story_prompt + '", "filename": "' + filename + '"}'
        story = ''
        if len(message) < max_length:
            with st.spinner("Generating image..."):
                data = message.encode()
                client_socket.send(data)
                inputs = tokenizer(story_prompt, return_tensors="pt")
                story = tokenizer.decode(model.generate(inputs["input_ids"],
                       max_length=result_length,
                       num_beams=2,
                       no_repeat_ngram_size=2,
                       early_stopping=True
                      )[0])
                client_socket.recv(max_length)

            st.markdown("### Generated images:")
            st.markdown("#### " + filename)
            st.markdown("____")
            st.markdown("### story prompt")
            st.markdown("#### " + story_prompt)
            st.markdown(story)
            st.markdown("____")
            for i in range(4):
                fn = filename + str(i) + ".jpg"
                image = Image.open(fn)
                st.image(image, caption=fn)
                #st.markdown("____")

            st.markdown("#### You can try again if you're unhappy with the model's output")
