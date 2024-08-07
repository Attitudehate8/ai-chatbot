import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to generate AI image from prompt
def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "256x256"  # Smaller size for faster generation
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    image_url = response.json()['data'][0]['url']
    return image_url

# Streamlit app interface
st.title('AI Image Generator')

prompt = st.text_input('Enter the prompt for the AI image:')
num_images = st.number_input('Enter the number of images you want to generate:', min_value=1, max_value=10, value=1)

if st.button('Generate Images'):
    if not prompt:
        st.error('Please enter a prompt.')
    else:
        st.write("Generating images...")
        if not os.path.exists('generated_images'):
            os.makedirs('generated_images')

        for i in range(num_images):
            image_url = generate_image(prompt)
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join('generated_images', f'image_{i+1}.png'))
            st.image(img, caption=f'Image {i+1}', use_column_width=True)

        st.success(f'{num_images} images generated successfully.')

        # Create a zip file for download
        zip_file_path = 'generated_images.zip'
        os.system(f'zip -r {zip_file_path} generated_images')

        with open(zip_file_path, 'rb') as f:
            st.download_button('Download All Images', f, file_name=zip_file_path)