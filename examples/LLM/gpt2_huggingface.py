import torch
import transformers
from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id = tokenizer.eos_token_id)

input_string = "Yesterday I spent several hours in the library, studying"
input_tokens = tokenizer.encode(input_string, return_tensors = "pt")

output = model.generate(input_tokens, max_length = 256)

output_string = tokenizer.decode(output[0], \
        skip_special_tokens=True)

print(f"Input sequence: {input_string}")

print(f"Output sequence: {output_string}")

