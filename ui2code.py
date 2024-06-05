import google.generativeai as genai
from PIL import Image
import re
import streamlit as st
from config import LLMConfig

# genai.configure(api_key=API_KEY,)
# model = genai.GenerativeModel('gemini-1.5-flash')

model = LLMConfig()
model = model.gemini_config()
# models/gemini-1.0-pro
# models/gemini-1.0-pro-001
# models/gemini-1.0-pro-latest
# models/gemini-1.0-pro-vision-latest
# models/gemini-1.5-flash
# models/gemini-1.5-flash-001
# models/gemini-1.5-flash-latest
# models/gemini-1.5-pro
# models/gemini-1.5-pro-001
# models/gemini-1.5-pro-latest
# models/gemini-pro
# models/gemini-pro-vision

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

def prompter(prompt, image):
  response = model.generate_content([prompt, image])
  return response.text

def use_gemini(img):
    st.write("Generating UI...")
    prompt = """
    Describe this UI in accurate details. When you reference a UI element put its name and bounding box 
    in the format: [object name (y_min, x_min, y_max, x_max)] 
    and then convert it a react component with tailwind css"""

    ui = prompter(prompt, img)

    st.write('Generating Code...')
    refined_prompt = f"""
    convert the image to react component with tailwind css, make sure to use the full page this is description of the image:\n{ui}
    """

    refined_ui = prompter(refined_prompt, img)
    st.write('Refining Code...')
    code_prompt = f"""
    refine the react code according to the image, make sure margin and padding is correct. try to use exactly the same color. Only output the code nothing else, no markdown no text. \n: {refined_ui}
    """
    code = prompter(code_prompt,img)
    st.write(code)
   
    st.download_button(label="Download Code", data=code, file_name="index.tsx")

def main():
  st.title('UI TO CODE')
  st.subheader('Made by [Hasnain](https://x.com/syeddhasnainn)')
  #option to select open ai or gemini
  options = ['Gemini', 'OpenAI']
  label = 'Select the model you want to use'
  selected_options = st.radio(label, options , index=0)
  print(selected_options)

  uploaded_file = st.file_uploader("Choose an image to upload")
  if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image',)
    

  if selected_options == 'Gemini':
    

    if st.button("Generate"):
      use_gemini(img)



if __name__ == "__main__":
  
  
  main()