import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer
import nest_asyncio
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(url):
    """Useful to scrape and summarize a website content, just pass a string with
    only the full url, no need for a final slash `/`, eg: https://google.com or https://clearbit.com/about-us"""
    nest_asyncio.apply()
    articles = [url]

    # Scrapes the blogs above
    loader = AsyncChromiumLoader(articles)
    docs = loader.load()
    transformer = Html2TextTransformer()
    docs_cleaned = transformer.transform_documents(docs)
    content = docs_cleaned[0].dict()['page_content']

    agent = Agent(
        role='Principal Researcher',
        goal=
        'Do amazing researches and summaries based on the content you are working with',
        backstory=
        "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
        llm=ChatOpenAI(model_name="gpt-4o",),
        allow_delegation=False)
    task = Task(
        agent=agent,
        description=
        f'Analyze and make a LONG summary the content bellow, make sure to include the ALL relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{content}',
        expected_output='Website Summary'
    )
    summary = task.execute()
    return f'\nScrapped Content: {summary}\n'
