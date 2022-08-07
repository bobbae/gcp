#import gradio as gr
from aitextgen import aitextgen

print("downloading GPT-NEO model")
ai = aitextgen(model="EleutherAI/gpt-neo-125M",to_gpu=True)


def ai_text(inp):
  generated_text = ai.generate_one(max_length = 1000, prompt = inp, no_repeat_ngram_size = 3) #repetition_penalty = 1.9)
  print("===============")
  print(generated_text)
  print("===============")
  return generated_text


#ai_text("USA is a leading manufacturer in smartphone and that is ")
ai_text("My little pony is a unicorn and it looks like a dog on a rainbow.")

#output_text = gr.outputs.Textbox()
#gr.Interface(ai_text,"textbox", output_text, title="ai generated Blog with GPT-Neo",
#   description="AI Generated Blog Content with GPT-Neo - via {aitextgen}").launch()

