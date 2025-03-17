from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from pydantic import SecretStr
load_dotenv()

async def main():
    # Configurando o modelo da OpenRouter
    # Você pode escolher diferentes modelos disponíveis na OpenRouter
    # Exemplos: "openai/gpt-4-turbo", "anthropic/claude-3-opus", "meta-llama/llama-3-70b-instruct"
    modelo = "openai/gpt-4o"  # Substitua pelo modelo que deseja usar
    
    llm = ChatOpenAI(
        model=modelo,
        api_key=SecretStr(os.getenv("OPENROUTER_API_KEY", "")),
        base_url=os.getenv("OPENAI_API_BASE"),
        # Adicione os headers necessários para a OpenRouter
        default_headers={
            "HTTP-Referer": "https://localhost",  # Substitua pelo seu site se necessário
            "X-Title": "Browser-use Test"
        }
    )
    
    agent = Agent(
        task="Compare o preço do gpt-4o e DeepSeek-V3",
        llm=llm,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main()) 