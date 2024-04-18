import json
import tqdm
import os
import random
import openai
from datetime import datetime
import argparse
import time

import requests
from utils import deprecated, dump_dataclass, AttrDict

try:
    from openai import OpenAI
except ImportError:
    print("[WARNING] `openai` package has not been installed or with incorrect version.")
    pass

# api_base = "https://api.openai.com/v1"
api_base = "https://lonlie.plus7.plus/v1"
    
def make_requests_http(
        prompts, *args,
        model="gpt-3.5-turbo", max_tokens=1024, temperature=0.7, top_p=0.5, 
        frequency_penalty=0, presence_penalty=0, stop_sequences=["\n\n"], logprobs=5, n=1, best_of=1, retries=3, 
        api_key=None, organization=None, **kwargs
    ):
    """
    Communicate with OpenAI GPT3.5 API via HTTP requests.
    """

    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "Please provide an API key for OpenAI GPT3."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": x} for x in prompts],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop": stop_sequences,
        "n": n,
        # "logprobs": logprobs,
        # "best_of": best_of,
    }
    
    retry = 0
    while retry < retries:
        try:
            response = requests.post(
                f"{api_base}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to get response from OpenAI: {e}. Retry {retry}/{retries}.")
            retry += 1
            time.sleep(5)
        else:
            break

    assert retry < retries, "Failed to get response from OpenAI."
    response = response.json()

    if isinstance(prompts, list):
        results = []
        for i, prompt in enumerate(prompts):
            # print(len(response.choices), (i*n,(i+1)*n), response.choices[i * n: (i + 1) * n])
            data = {
                "prompt": prompt,
                "response": {"choices": response["choices"][i * n: (i + 1) * n]} if response else None,
                "created_at": str(datetime.now()),
            }
            results.append(data)
        return results
    else:
        data = {
            "prompt": prompts,
            "response": response,
            "created_at": str(datetime.now()),
        }
        return [data]

@deprecated
def make_requests(
        prompts, model="gpt-3.5-turbo", max_tokens=1024, temperature=0.7, top_p=0.5, 
        frequency_penalty=0, presence_penalty=0, stop_sequences=["\n\n"], logprobs=5, n=1, best_of=1, retries=3, 
        api_key=None, organization=None,
    ):
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "Please provide an API key for OpenAI GPT3."

    client = OpenAI(
        api_key=api_key,
        base_url="https://lonlie.plus7.plus/v1"
    )
    
    retry_cnt = 0
    backoff_time = 30
    while retry_cnt <= retries:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{'role': 'user', 'content': x} for x in prompts],
                temperature=temperature,
            )
            break
        except openai.BadRequestError as e:
            print(f"OpenAIError: {e}.")
            if "Please reduce your prompt" in str(e):
                target_length = int(target_length * 0.8)
                print(f"Reducing target length to {target_length}, retrying...")
            else:
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                backoff_time *= 1.5
            retry_cnt += 1
    
    if isinstance(prompts, list):
        results = []
        for j, prompt in enumerate(prompts):
            data = {
                "prompt": prompt,
                "response": {"choices": response.choices[j * n: (j + 1) * n]} if response else None,
                "created_at": str(datetime.now()),
            }
            results.append(data)
        return results
    else:
        data = {
            "prompt": prompts,
            "response": response,
            "created_at": str(datetime.now()),
        }
        return [data]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        type=str,
        help="The input file that contains the prompts to GPT3.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output file to save the responses from GPT3.",
    )
    parser.add_argument(
        "--engine",
        type=str,
        help="The openai GPT3 engine to use.",
    )
    parser.add_argument(
        "--max_tokens",
        default=500,
        type=int,
        help="The max_tokens parameter of GPT3.",
    )
    parser.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="The temprature of GPT3.",
    )
    parser.add_argument(
        "--top_p",
        default=0.5,
        type=float,
        help="The `top_p` parameter of GPT3.",
    )
    parser.add_argument(
        "--frequency_penalty",
        default=0,
        type=float,
        help="The `frequency_penalty` parameter of GPT3.",
    )
    parser.add_argument(
        "--presence_penalty",
        default=0,
        type=float,
        help="The `presence_penalty` parameter of GPT3.",
    )
    parser.add_argument(
        "--stop_sequences",
        default=["\n\n"],
        nargs="+",
        help="The `stop_sequences` parameter of GPT3.",
    )
    parser.add_argument(
        "--logprobs",
        default=5,
        type=int,
        help="The `logprobs` parameter of GPT3"
    )
    parser.add_argument(
        "--n",
        type=int,
        help="The `n` parameter of GPT3. The number of responses to generate."
    )
    parser.add_argument(
        "--best_of",
        type=int,
        help="The `best_of` parameter of GPT3. The beam size on the GPT3 server."
    )
    parser.add_argument(
        "--use_existing_responses",
        action="store_true",
        help="Whether to use existing responses from the output file if it exists."
    )
    parser.add_argument(
        "--request_batch_size",
        default=20,
        type=int,
        help="The number of requests to send to GPT3 at a time."
    )
    return parser.parse_args()

    
if __name__ == "__main__":
    random.seed(123)
    args = parse_args()
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)

    # read existing file if it exists
    existing_responses = {}
    if os.path.exists(args.output_file) and args.use_existing_responses:
        with open(args.output_file, "r") as fin:
            for line in fin:
                data = json.loads(line)
                existing_responses[data["prompt"]] = data

    # do new prompts
    with open(args.input_file, "r") as fin:
        if args.input_file.endswith(".jsonl"):
            all_prompts = [json.loads(line)["prompt"] for line in fin]
        else:
            all_prompt = [line.strip().replace("\\n", "\n") for line in fin]

    with open(args.output_file, "w") as fout:
        for i in tqdm.tqdm(range(0, len(all_prompts), args.request_batch_size)):
            batch_prompts = all_prompts[i: i + args.request_batch_size]
            if all(p in existing_responses for p in batch_prompts):
                for p in batch_prompts:
                    fout.write(json.dumps(existing_responses[p]) + "\n")
            else:
                results = make_requests(
                    engine=args.engine,
                    prompts=batch_prompts,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    top_p=args.top_p,
                    frequency_penalty=args.frequency_penalty,
                    presence_penalty=args.presence_penalty,
                    stop_sequences=args.stop_sequences,
                    logprobs=args.logprobs,
                    n=args.n,
                    best_of=args.best_of,
                )
                for data in results:
                    fout.write(json.dumps(data) + "\n")