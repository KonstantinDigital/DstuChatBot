import openai
import logging
import config

openai.api_key = config.PROXY_OPENAI_TOKEN
openai.api_base = config.PROXY_OPENAI_STARTPOINT


async def gen_txt(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            # max_tokens=20
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def gen_img(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            model="dall-e-3",
            prompt=prompt,
            n=n,
            size=size,
            # quality="hd",
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls
