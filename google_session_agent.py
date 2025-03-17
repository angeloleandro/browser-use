from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from pydantic import SecretStr
import sys
import json

# Importa as funções personalizadas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import browser_use_custom_functions

load_dotenv()

class GoogleSessionAgent:
    """
    Agente personalizado do Browser-use que lida automaticamente com problemas de sessão do Google.
    """
    
    def __init__(
        self,
        google_email=None,
        google_password=None,
        openrouter_api_key=None,
        model="openai/gpt-4o",
    ):
        """
        Inicializa o agente com credenciais do Google e configurações da API.
        
        Args:
            google_email: Email da conta Google
            google_password: Senha da conta Google
            openrouter_api_key: Chave da API da OpenRouter
            model: Modelo de IA a ser usado
        """
        self.google_email = google_email
        self.google_password = google_password
        
        # Usa a chave da API do .env se não for fornecida
        if not openrouter_api_key:
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # Configura o modelo LLM
        self.llm = ChatOpenAI(
            model=model,
            api_key=SecretStr(openrouter_api_key or ""),
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://localhost",
                "X-Title": "Browser-use Google Session Agent"
            }
        )
        
        # Instruções personalizadas para o agente
        self.task_prefix = f"""
        Você é um assistente especializado em navegação web que pode lidar com problemas de sessão do Google.
        
        Quando encontrar mensagens como "Sua sessão expirou" ou "Você não está conectado", você deve:
        1. Clicar no botão "Tentar novamente" se estiver disponível
        2. Se não funcionar, procurar um link "Faça login" e clicar nele
        3. Fazer login usando o email: {google_email} e senha: {google_password}
        
        Após cada ação de navegação em sites do Google (como Gmail, Drive, Docs), verifique se há problemas 
        de sessão e resolva-os conforme as instruções acima.
        
        Sempre informe ao usuário quando encontrar e resolver problemas de sessão.
        
        Agora, execute a seguinte tarefa:
        """
    
    async def run(self, task):
        """
        Executa uma tarefa com tratamento automático de sessões do Google.
        
        Args:
            task: Descrição da tarefa a ser executada
            
        Returns:
            Resultado da execução da tarefa
        """
        # Adiciona o prefixo à tarefa
        full_task = f"{self.task_prefix}\n\n{task}"
        
        # Cria o agente com as configurações básicas
        agent = Agent(
            task=full_task,
            llm=self.llm,
        )
        
        # Executa o agente
        result = await agent.run()
        return result


async def main():
    """Função principal para executar o agente."""
    # Solicita as credenciais do Google se não estiverem no .env
    google_email = os.getenv("GOOGLE_EMAIL")
    if not google_email:
        google_email = input("Digite seu email do Google: ")
    
    google_password = os.getenv("GOOGLE_PASSWORD")
    if not google_password:
        import getpass
        google_password = getpass.getpass("Digite sua senha do Google: ")
    
    # Cria e executa o agente
    agent = GoogleSessionAgent(
        google_email=google_email,
        google_password=google_password
    )
    
    # Define a tarefa a ser executada
    task = input("Digite a tarefa que deseja realizar (ex: 'Acesse meus arquivos no Google Drive'): ")
    if not task:
        task = "Acesse meus arquivos no Google Drive e liste os 5 mais recentes"
    
    # Executa o agente
    result = await agent.run(task)
    print("\nResultado:", result)


if __name__ == "__main__":
    asyncio.run(main()) 