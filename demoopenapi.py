import main
from secretkey import openai_key
from openai import OpenAI
import json
import pandas as pd

clent = OpenAI(
    api_key=openai_key
)

def extract_finacial_data(text):
    prompt = get_prompt_financial()+text
    response = clent.chat.completions.create(
    messages = [
       {'role': 'user','content': prompt}],
    model = 'gpt-3.5-turbo',
    
)
    # content = response.choices[0]['message']['content']
    content = response
    print(content)
    
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=['Measure','value'])
    except (json.JSONDecodeError, IndexError):
        pass
    
    return pd.DataFrame({
        "Measure":["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "value": ["","","",""]
    })
    
    
    
def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a EPS)
from the following news article. If you can't find the information from this article then return "".
Do make things up. Then retrieve a stock symbol corresponding to that company. For this you can use your general knowledge (it doesn't have to be from this article). Always return your
response as a valid JSON string. The format of that string should be this
{
    "company": "Walmart",
    "Stock Symbol": "WMT",
    "Revenue":"12.34 million",
    "Net income":"34.78 million",
    "EPS":"2.1 $"
}

News Article:
=============


'''
response = clent.chat.completions.create(
    messages = [
       {'role': 'user','content': 'write a poem on samosa . only 4 line please'}
            ],
    model = 'gpt-3.5-turbo',
    
)

# print(response['choices'][0]['message']['content'])
print(response)


if __name__ == '__main__':
    
    text = '''
    Tesla's Earing news in text format: Tesla's earning this quarter blew all the estimates. They
    '''
    df = extract_finacial_data(text)
    print(df.to_string())