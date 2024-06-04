import google.generativeai as genai
from dotenv import load_dotenv
import os 
from IPython.display import Markdown
import pathlib
from PIL import Image
import re
import streamlit as st

import textwrap

load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY,)
model = genai.GenerativeModel('gemini-1.5-flash')

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# # img = input('name of the image file:',)

# img = PIL.Image.open('test.png')
# # response = model.generate_content(['Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)] and then convert it to an html file with tailwind css', img], stream=True)
# print('describing ui')

# response = model.generate_content(['Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)].',img])
# print('generating code')
# response2 = model.generate_content([f'convert the image to react component with tailwind css, make sure to use the full page this is description of the image:\n{response.text}', img],)

# pattern = r'```(.*?)```'
# match = re.search(pattern, response2.text, re.DOTALL)
# html_code = match.group(1).strip()

# response3 = model.generate_content([f'refine the react code according to the image, make sure width and padding is correct. dont use any colors, just do the basic page structure \n: {html_code}', img])
# match = re.search(pattern, response2.text, re.DOTALL)
# html_code = match.group(1).strip()

# with open('output.tsx', 'w') as file:
#   file.write(html_code)
# print('done')
def prompter(prompt, image):
  response = model.generate_content([prompt, image])
  return response.text

def main():
  st.title('UI TO CODE')
  st.subheader('Made by [Hasnain](https://x.com/syeddhasnainn)')

  uploaded_file = st.file_uploader("Choose an image to upload")
  if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image',)
    
    # temp_image_path = pathlib.Path("temp_image.png")
    # image.save(temp_image_path, format="PNG")

  if st.button("Generate"):
    st.write("Generating UI...")
    prompt = """
    Describe this UI in accurate details. When you reference a UI element put its name and bounding box 
    in the format: [object name (y_min, x_min, y_max, x_max)] 
    and then convert it a react component with tailwind css
      """
    ui = prompter(prompt, img)

    st.write('Generating Code...')
    refined_prompt = f"""
convert the image to react component with tailwind css, make sure to use the full page this is description of the image:\n{ui}
"""

  
    refined_ui = prompter(refined_prompt, img)
    st.write('Refining Code...')
    code_prompt = f"""
refine the react code according to the image, make sure width and padding is correct. dont use any colors, just do the basic page structure \n: {refined_ui}
"""
    code = prompter(code_prompt,img)
    st.write(code)
    # with open('index.tsx', 'w') as file:
    #   file.write(html)


if __name__ == "__main__":
  main()