import transformers
from transformers import BloomTokenizerFast, BloomModel
from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
import torch

#tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-350m")
#model = BloomModel.from_pretrained("bigscience/bloom-350m")
model = BloomForCausalLM.from_pretrained("bigscience/bloom-1b3")
tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-1b3")

prompt = "A dog and a cat and a unicorn were racing on the rainbow clouds."
result_length = 150
inputs = tokenizer(prompt, return_tensors="pt")

print("=========================")
# Greedy Search
print(tokenizer.decode(model.generate(inputs["input_ids"],
                       max_length=result_length
                      )[0]))

print("=========================")
# Beam Search
print(tokenizer.decode(model.generate(inputs["input_ids"],
                       max_length=result_length,
                       num_beams=2,
                       no_repeat_ngram_size=2,
                       early_stopping=True
                      )[0]))

print("=========================")
# Sampling Top-k + Top-p
print(tokenizer.decode(model.generate(inputs["input_ids"],
                       max_length=result_length,
                       do_sample=True,
                       top_k=50,
                       top_p=0.9
                      )[0]))
