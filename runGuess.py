# Convenience libraries
import os
import time
import re

# API call helpers
from anthropic import Anthropic
from openai import OpenAI
from mistralai import Mistral
import replicate
# Grok and Gemini will use openai library

# Environmental variables
from dotenv import load_dotenv
load_dotenv()

# Working directory for project taken from env vars; write in an output folder 'out'
os.chdir(os.environ.get("ROOT_DIR") + "out\\")

# Tested query
query = "I am thinking of a random integer number between 1 and 50. Try to guess what number I am thinking of. You will only get one guess and please return the answer as a plain number."

# Sleep after each query (seconds)
sleepTime = 2

# Keep on trying until we've successfully gone through the try-catch, iterating all combinations
while True:
    try:
        # Repeat the query 100 times
        for rep in range(100):
            # Test determinism'ish (~0) and more freedom (0.2) for temperature
            for temp in [0.0, 0.2, 1.0]:
                # Pad replicates to 00#, 0##, etc
                rep = str(rep).rjust(3, '0')

                # Reset the client objects for each call

                # Claude section
                for modelname in [
                    # 3.* Haiku
                    "claude-3-5-haiku-20241022",
                    # 3.* Sonnet(s)
                    "claude-3-5-sonnet-20240620",
                    "claude-3-5-sonnet-20241022",
                    "claude-3-7-sonnet-20250219",
                    # 4s
                    "claude-sonnet-4-20250514",
                    "claude-opus-4-20250514"
                ]:
                    client = Anthropic(
                        api_key=os.environ.get("ANTHROPIC_API_TOKEN"),
                    )
                    filename = (modelname
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        # Run the actual prompt itself
                        message = client.messages.create(
                            model=modelname,
                            max_tokens=4096,
                            temperature=temp,
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": query
                                        }
                                    ]
                                }
                            ]
                        )
                        response = "".join(message.content[0].text)
                        # Write output to a suitable file
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        f.write(response)
                        f.close()
                        time.sleep(7)  # Sleep a bit

                # GPT section
                gpts = [
                    # 4o*
                    "gpt-4o-2024-05-13",
                    "gpt-4o-2024-08-06",
                    "gpt-4o-2024-11-20",
                    # 4.1*
                    "gpt-4.1-nano-2025-04-14",
                    "gpt-4.1-mini-2025-04-14",
                    "gpt-4.1-2025-04-14",
                ]
                # Reasoning models o1 and o3 are only runnable with temperature 1 (default)
                if temp == 1.0:
                    gpts = gpts + ["o1-2024-12-17", "o3-2025-04-16"]
                for modelname in gpts:
                    client = OpenAI(
                        api_key=os.environ.get("OPENAI_API_KEY")
                    )
                    filename = (modelname
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        response = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": query,
                                }
                            ],
                            model=modelname,
                            temperature=temp
                        )
                        # Write output to a suitable file
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        f.write(response.choices[0].message.content)
                        f.close()
                        time.sleep(sleepTime)  # Sleep a bit

                # Mistral section
                for modelname in [
                    "mistral-large-2411",
                    "mistral-medium-2505",
                    "mistral-small-2503"
                ]:
                    client = Mistral(
                        api_key=os.environ.get("MISTRAL_API_KEY")
                    )
                    filename = (modelname
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        response = client.chat.complete(
                            messages=[
                                {
                                    "role": "user",
                                    "content": query,
                                }
                            ],
                            model=modelname,
                            temperature=temp
                        )
                        # Write output to a suitable file
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        f.write(response.choices[0].message.content)
                        f.close()
                        time.sleep(sleepTime)  # Sleep a bit

                # Replicate section (Llama, DeepSeek, ...)
                for modelname in [
                    # Llamas
                    "meta/llama-4-maverick-instruct",
                    "meta/llama-4-scout-instruct",
                    # DeepSeeks
                    "deepseek-ai/deepseek-r1",
                    "deepseek-ai/deepseek-v3",
                    # Google Deepmind's Gemma 3
                    #"google-deepmind/gemma-3-4b-it:00139d2960396352b671f7b5c2ece5313bf6d45fe0a052efe14f023d2a81e196",
                    #"google-deepmind/gemma-3-12b-it:5a0df3fa58c87fbd925469a673fdb16f3dd08e6f4e2f1a010970f07b7067a81c",
                    #"google-deepmind/gemma-3-27b-it:c0f0aebe8e578c15a7531e08a62cf01206f5870e9d0a67804b8152822db58c54"
                ]:
                    filename = (re.sub("/", "_", modelname)
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        input = {
                            "prompt": query,
                            "temperature": temp
                        }
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        out = ""
                        for iterator in replicate.run(
                                modelname,
                                input=input
                        ):
                            out = out + "".join(iterator)
                            print("".join(iterator), end="", file=f)
                        f.close()
                        time.sleep(sleepTime)  # Sleep a bit

                # Gemini section
                for modelname in [
                        "gemini-2.5-pro-preview-03-25",
                        "gemini-2.5-pro-preview-06-05",
                        "gemini-2.5-pro-preview-05-06",
                        "gemini-2.0-flash-001",
                        "gemini-2.0-flash-lite-001"
                    ]:
                    client = OpenAI(
                        api_key=os.environ.get("GEMINI_API_TOKEN"),
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                    )
                    filename = (modelname
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        response = client.chat.completions.create(
                            model=modelname,
                            n=1,
                            messages=[
                                {
                                    "role": "user",
                                    "content": query,
                                }
                            ],
                            temperature=temp
                        )
                        # Write output to a suitable file
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        f.write(response.choices[0].message.content)
                        f.close()
                        time.sleep(sleepTime)  # Sleep a bit

                # Grok section
                for modelname in [
                    "grok-3-beta",
                    "grok-2-1212"
                ]:
                    client = OpenAI(
                        api_key=os.environ.get("XAI_API_KEY"),
                        base_url="https://api.x.ai/v1"
                    )
                    filename = (modelname
                                + "_temp" + str(temp)
                                + "_rep" + str(rep)
                                )
                    # Run only if the output file doesn't exist yet
                    if not os.path.isfile(os.path.realpath(filename + ".out")):
                        print("Running " + filename)
                        response = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": query,
                                }
                            ],
                            model=modelname,
                            temperature=temp,
                        )
                        f = open(filename + ".out", 'w', encoding="utf-8")
                        f.write(response.choices[0].message.content)
                        f.close()
                        time.sleep(sleepTime)  # Sleep a bit
        break
    except Exception as e:
        print("Exception:\n " + str(e) + "\n\n")
        time.sleep(120)