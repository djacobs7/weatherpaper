
from openai import OpenAI

def write_weather_poem(detailed_forecast):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Write a poem about this forecast. Each line should be less than 20 characters.  The poem should be less than 20 words: ${detailed_forecast}"},
        ]
    )

    

    return response.choices[0].message.content