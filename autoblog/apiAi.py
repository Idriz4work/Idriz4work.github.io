import os
import shutil
import logging
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import text,create_engine
from llamaapi import LlamaAPI
from openai import OpenAI
import pandas as pd
import pyinputplus as pyip
import replicate, webbrowser, requests
import requests
from git import Repo
from pathlib import Path

import argparse

load_dotenv

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
api = os.getenv("API_KEY")

client = OpenAI(
    api_key=api,
    base_url="https://api.llama-api.com"
)

def main(title):

    prompt = """Atilla's Website
    Biography
    I am a Python instructor teaching people machine learning!


    Blog

    Jan 31, 2023
    Title: Why AI will never replace the radiologist
    tags: tech, machine-learning, radiology
    Summary:  I talk about the cons of machine learning in radiology. I explain why I think that AI will never replace the radiologist.
    Full text:"""
    
    response = client.chat.completions.create(
                            model="llama-13b-chat",
                            messages=[
                                {"role": "system", "content":"You are a helpful assistant to write blogposts."},
                                {"role": "user", "content": prompt},
                            ],
                                temperature=0.7
)

    print(response.choices[0].message.content)

    prompt = f"Create a pixel art based on: '{title}'."
    
    # Initialize the Replicate client with the API token
    clientReplicate = replicate.Client(api_token=REPLICATE_API_TOKEN)

    input = {
        "width": 768,
        "height": 768,
        "prompt": title,
        "refine": "expert_ensemble_refiner",
        "apply_watermark": False,
        "num_inference_steps": 25
    }

    output = clientReplicate.run(
        "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
        input=input,
    )
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

    # Open the URL in a new Chrome window
    webbrowser.get(chrome_path).open_new(str(output))
    print(output)
    
    image_res = requests.get(str(output), stream = True)
    
    if image_res.status_code == 200:
        with open('str(output)1','wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-title", type=str, help="enter title of image")
    args = parser.parse_args()
    main(args.title)
