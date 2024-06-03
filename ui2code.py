import google.generativeai as genai
from dotenv import load_dotenv
import os 
from IPython.display import Markdown
import pathlib
import PIL.Image
import re

import textwrap

load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = genai.GenerativeModel('gemini-1.5-flash')
# img = input('name of the image file:',)

img = PIL.Image.open('test.png')
# response = model.generate_content(['Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)] and then convert it to an html file with tailwind css', img], stream=True)
print('describing ui')

response = model.generate_content(['Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)].',img])
print('generating code')
response2 = model.generate_content([f'convert the image to react component with tailwind css, this is description of the image:\n{response.text}', img],)

pattern = r'```(.*?)```'
match = re.search(pattern, response2.text, re.DOTALL)
html_code = match.group(1).strip()

response3 = model.generate_content([f'refine the react code according to the image, make sure width and padding is correct. colors are correct, if you cant find the bg image add any image that fits best \n: {html_code}', img])
match = re.search(pattern, response2.text, re.DOTALL)
html_code = match.group(1).strip()

with open('output.tsx', 'w') as file:
  file.write(html_code)
print('done')



