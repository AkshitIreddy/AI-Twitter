import base64
import cohere 
from random_word import RandomWords
import random
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import datetime
import names
from fastapi import FastAPI, HTTPException, Request, Depends, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json

app = FastAPI()
security = HTTPBasic()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = RandomWords()

co = cohere.Client(open("cohere_api_key.txt", 'r').read()) 

model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

@app.post("/inference")
async def create_insights(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "myusername" or credentials.password != "mypassword":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    data = await request.json()
    mydata = tweet_list_generator()
    tweet_list = []
    for tweet in mydata:
        tweet_data = {
            "text": tweet[0],
            "image": tweet[2] if tweet[2] != "empty" else None,  # Store image filename
            "author": tweet[3]
        }
        if tweet_data["image"]:
            # Load image data and encode it as base64
            with open("../Database/Image/"+tweet_data["image"], "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode("utf-8")
            tweet_data["image_data"] = image_data
        tweet_list.append(tweet_data)

    return tweet_list


def tweet_list_generator():

    tweet_list = []
    for i in range(5):
        random_word = r.get_random_word()
        tweet = tweet_generator(random_word)
        user_name = names.get_full_name()

        image_probability = random.random()
        if image_probability < 0.5:
            tweet_list.append([tweet, random_word, 'empty', user_name])
            continue

        image_filename = image_generate(random_word, tweet)
        tweet_list.append([tweet, random_word, image_filename, user_name])

    return tweet_list
        
def image_generate(random_word, tweet):

    prompt =  random_word + "beautiful, photorealistic, high quality, realism, ultra quality, 4k, artistic, masterpiece, beautiful" + tweet
    negative_prompt = "ugly, bad, deformed face, deformed eyes, deformed lips, deformation, malformations, extra limbs, dismembered limbs, bodiless hands, bodiless legs, deformed fingers, deformed face, missing body parts, twisted legs, twisted hands, missing feets, missing palms, low quality"

    image = pipe(prompt, negative_prompt=negative_prompt).images[0]

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"file_{formatted_time}.png"  
    filepath = f"../Database/Image/{filename}"

    image.save(filepath)
    return filename

def tweet_generator(random_word):

    response = co.chat( 
    model='command-r',
    message=f'Create a twitter tweet which may talk about the latest news or an opinion about the following word\n{random_word}',
    temperature=0.3,
    chat_history=[],
    prompt_truncation='auto',
    connectors=[{"id":"web-search"}],
    documents=[]
    ) 
    return response.text
