# Meta Translate

Meta Translate is a Python wrapper designed to streamline the utilization of Meta AI's Seamless text and speech translation model. This wrapper simplifies complex operations into a single Python code line, enabling users to effortlessly translate texts and speech into multiple languages.

## Key Features

- **Efficiency:** Meta Translate combines multiple line operations into a concise Python code call, making translation tasks more straightforward.
  
- **Local Model Loading:** Unlike other Python libraries such as Bark and Google TTS engines, Meta Translate loads models natively on your local system before performing the translation process.

- **Privacy:** Meta Translate provides a superior solution by ensuring that models operate locally, offering both free unlimited translation tasks and enhanced privacy.

## CODENAME

Meta Translate is developed under the THUNDERSTORM PROJECT.

## Quickstart

Install the library using pip:

```bash
pip install meta_translate
```

```Python 
from meta_translate import load_seamless_m4t_model
from meta_translate import text_to_translated_text

# Load the model
model_name = "facebook/hf-seamless-m4t-medium"
processor, model = load_seamless_m4t_model(model_name)

# Perform translation
text_to_translate = """Technology has transformed the way we communicate and access information. In today's interconnected world, the rapid advancement of digital tools has made communication more instantaneous and information more accessible than ever before."""
translated_result = text_to_translated_text(model, processor, text_to_translate, tgt_lang="spa")

# Print the output
print(translated_result)
```

## LICENCE
ALL RIGHTS RESERVED UNDER MIT LICENSE AND META AI TERMS AND CONDITIONS
