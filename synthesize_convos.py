import os
import openai
from time import time,sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_convo(text, topic):
    with open('convos/%s_%s.txt' % (topic, time()), 'w', encoding='utf-8') as outfile:
        outfile.write(text)


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.85, top_p=1.0, tokens=1000, freq_pen=0.5, pres_pen=0.0, stop=['<<END>>']):  # NOTE: original temp was 0.7 and freq_pen was 0.0 - I turned these up to reduce repetition
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    for i in range(0, 4):
        topics = open_file('topics.txt').splitlines()
        for topic in topics:
            print(topic)
            prompt = open_file('prompt.txt').replace('<<TOPIC>>', topic)
            response = gpt3_completion(prompt)
            outtext = 'User: Hey TIM%s' % response
            print(outtext)
            tpc = topic.replace(' ', '')[0:15]
            save_convo(outtext, tpc)
            #exit()
            