import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv('TOKEN_AI'))
model = genai.GenerativeModel('gemini-2.5-flash',
                              system_instruction="Ты — помощник по Python. Отвечай кратко и по делу. Это твоя основная задача, дальше контекст того, где ты работаешь." \
                              "Ты используешься в телеграм боте, поэтому не форматируй свои ответы, перед каждым запросом тебе будет отправляться история чата с опередленным" \
                              "пользователем в формате: два списка, в первом списке каждый элемент - это запрос пользователя, во втором списке каждый элемент - это твой ответ.")



