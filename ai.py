import os
import openai
import uuid
import time
import json
import time
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Openai set
openai.api_key = st.secrets['OPENAI_API_KEY'] # os.getenv('OPENAI_API_KEY')  

# Naver clova set
clova_ocr_apigw_url = st.secrets['CLOVA_OCR_APIGW_URL'] # os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = st.secrets['CLOVA_OCR_SECRET_KEY'] # os.getenv('CLOVA_OCR_SECRET_KEY')

# Naver api set
naver_client_id = st.secrets['NAVER_CLIENT_ID'] # os.getenv('NAVER_CLIENT_ID')
naver_secret = st.secrets['NAVER_SECRET'] # os.getenv('NAVER_SECRET')

def getKeywords(text):
    prompt = f'''
        여러 책 표지 이미지 속 텍스트를 OCR로 추출한 결과를 줄 테니까, 
        지은이, 출판사, 오타 정보를 제외하고
        '책 제목'을 추출해줘
        텍스트가 없으면 아무것도 출력하지 마
        [텍스트]
        {text}
        [책 제목]
    '''
    msgs = [{'role': 'user', 'content': prompt}]
    answer, _ = getGPT(msgs)
    return answer
        
def bookSearch(text):
    params = {
        'query' : text,
        'display' : 10,
        'sort' : 'sim'
    }
    headers = {
        'X-Naver-Client-Id': naver_client_id,
        'X-Naver-Client-Secret': naver_secret,
        'Content-Type': 'application/json'
    }
    response = requests.get('https://openapi.naver.com/v1/search/book.json', params = params, headers=headers)
    return response.json()

def directocr(data):
    request_json = {
        'images': [
            {
                'format': 'png',
                'name': 'demo',
                'data': data
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time()*1000))
    }
    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': clova_ocr_secret_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(clova_ocr_apigw_url, headers=headers, data = payload)
    result = response.json()
    texts = result['images'][0]['fields']
    context = ''
    for text in texts:
        ### whole
        context += text['inferText']
        if (text['lineBreak']):
            context += '\n'
        else: 
            context += ' '
    return context, texts
    
def getGPT(msgs, model = 'gpt-3.5-turbo-0613', temperature = 0.1):
        try:
            response = openai.ChatCompletion.create(
                model = model,
                messages = msgs,
                temperature = temperature
            )
        except:
            return False, False
        answer = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens
        return answer, tokens

    
if __name__ == '__main__':
    bookSearch('100대 호기심')