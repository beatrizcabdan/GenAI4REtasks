import openai
import time


def init_openai(key=None):
    if not key:
        key = open("openai_key.txt", 'r').read()
    openai.api_key = key


def gpt3_prompt(prompt, engine='text-davinci-003', max_tokens=500, temperature=0.4, maxiter=5):
    while maxiter > 0:
        try:
            response = openai.ChatCompletion.create(model=engine, messages=[{"role": "user", "content": prompt}], max_tokens=max_tokens, temperature=temperature)
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            maxiter -= 1
            print(f"API not ready. Error: {str(e)}")
            print("Trying again:", maxiter, "attempts left")
            time.sleep(20)
    return "API not ready"
