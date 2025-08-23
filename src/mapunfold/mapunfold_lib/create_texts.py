import asyncio
import json
import os

import ollama

from .description import Description


# this does not give back valid json
# def get_prompt(info) -> str:
#     return f"""Generate a train station description for the place indicated by bps_name  in four languages: English, German, French and Italian.
#     The result should have the following shape:
#     class Description:
#         bps_name: str
#         en: str
#         de: str
#         fr: str
#         it: str
#
#     'treppen_and_rampen' means stairs and ramps.
#     'billetautomats' are ticket machines.
#     'billetentwerters' are ticket validators.
#     Use following info and especially the geoposition to describe where can be found what inside this station. Create at
#     least 3 paragraphs per language.
#     {info}
#
#     Focus on accessibility and where exactly things are inside this station.
#     """

def get_prompt(info) -> str:
    return f"""Generate a train station description for the place indicated by bps_name  in four languages: English, German, French and Italian.
    The result should have the following shape:
    class Description:
        bps_name: str
        en: str
        de: str
        fr: str
        it: str
    
    'treppen_and_rampen' means stairs and ramps.
    'billetautomats' are ticket machines.
    'billetentwerters' are ticket validators.
    Use following info and especially the geoposition to describe where can be found what inside this station. Create at
    least 2 paragraphs per language.
    {info}
    
    """

# some model that allows schema enforcement is required
def get_json_from_ai_model(prompt: str):

    os.environ["OLLAMA_HOST"] = "http://localhost:11434"

    # probably there should be an async version of this...
    result = ollama.generate(

        model="llama2",
        prompt=prompt,
        format="json"
    )

    json_response = result["response"].strip()
    return json_response

def parse_raw_data(raw):
    try:
        intermediate = json.loads(raw)
        parsed = intermediate["Description"]
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON: {raw}")

    try:
        return Description(**parsed)
    except Exception as e:
        raise ValueError(f"JSON did not match schema: {e}")


async def create_texts(info) -> Description:

    prompt = get_prompt(info)
    maybe_json_response = get_json_from_ai_model(prompt)
    description = parse_raw_data(maybe_json_response)

    return [ prompt, description ]

