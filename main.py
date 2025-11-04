import anyio
from os.path import join, dirname
from dotenv import load_dotenv
from basic_query import basic_query

print('§ Claude Agent SDK Lab 1')

dotenv_path = join(dirname(__file__), '.env.local') # .env
load_dotenv(dotenv_path)

anyio.run(basic_query) 
