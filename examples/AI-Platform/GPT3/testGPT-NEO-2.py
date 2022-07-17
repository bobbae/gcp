from happytransformer import HappyGeneration
from happytransformer import GENSettings

# Largest GPT2 1.5B
# Largest GPT-Neo 2.7B
# Largest GPT3 175B

# https://happytransformer.com/text-generation/settings/

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-125M")
result = happy_gen.generate_text("my little pony is a unicorn.")
print(result)
print(result.text)

args = GENSettings(no_repeat_ngram_size=2)
result = happy_gen.generate_text("my little pony is a unicorn.", args=args)
print(result.text)

top_k_sampling_settings = GENSettings(do_sample=True, early_stopping=False, top_k=50, temperature=0.7)
result = happy_gen.generate_text("my little pony is a unicorn.", args=top_k_sampling_settings)
print(result.text)

# Training
# https://www.vennify.ai/how-to-generate-harry-potter-text/
# https://happytransformer.com/learning-parameters/

happy_gen.train("train.txt")
from happytransformer import GENTrainArgs
args = GENTrainArgs(num_train_epochs=1)
happy_gen.train("train.txt", args=args)

