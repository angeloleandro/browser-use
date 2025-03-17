from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv
import os
from pydantic import SecretStr
import sys
import logging
from typing import Optional, Dict, Any, Callable

# Importa o manipulador de sessão
from session_handler import SessionHandler

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("google_session_browser")

load_dotenv()

class GoogleSessionBrowser:
    """
    Navegador com tratamento automático de sessões do Google.
    """
    
    def __init__(
        self,
        google_email: Optional[str] = None,
        google_password: Optional[str] = None,
        openrouter_api_key: Optional[str] = None,
        model: str = "openai/gpt-4o-mini",
        headless: bool = False,
        slow_mo: int = 100,
        check_interval: float = 2.0,
    ):
        """
        Inicializa o navegador com tratamento de sessão.
        
        Args:
            google_email: Email da conta Google
            google_password: Senha da conta Google
            openrouter_api_key: Chave da API da OpenRouter
            model: Modelo de IA a ser usado (padrão: openai/gpt-4o-mini)
            headless: Se o navegador deve ser executado em segundo plano
            slow_mo: Atraso em milissegundos entre ações
            check_interval: Intervalo em segundos para verificar problemas de sessão
        """
        # Carrega credenciais do .env se não fornecidas
        self.google_email = google_email or os.getenv("GOOGLE_EMAIL", "")
        self.google_password = google_password or os.getenv("GOOGLE_PASSWORD", "")
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY", "")
        
        # Configurações do navegador
        self.model = model
        self.headless = headless
        self.slow_mo = slow_mo
        self.check_interval = check_interval
        
        # Instâncias
        self.agent = None
        self.browser = None
        self.session_handler = None
        
        # Callback para verificar pausa
        self.pause_callback = None
        
        # Configuração do LLM
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=SecretStr(self.openrouter_api_key),
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://localhost",
                "X-Title": "Browser-use Google Session"
            }
        )
        
        # Instruções para o agente
        self.task_prefix = f"""
        Você é um assistente especializado em navegação web que pode lidar com problemas de sessão do Google.
        
        Se você encontrar mensagens como "Sua sessão expirou" ou "Você não está conectado", tente:
        1. Clicar no botão "Tentar novamente" se estiver disponível
        2. Se não funcionar, procurar um link "Faça login" e clicar nele
        3. Fazer login usando o email: {self.google_email} e senha: {self.google_password}
        
        Sempre informe ao usuário quando encontrar e resolver problemas de sessão.
        
        Agora, execute a seguinte tarefa:
        """
    
    def set_pause_callback(self, callback: Callable[[], None]):
        """
        Define uma função de callback para verificar se a execução deve ser pausada.
        
        Args:
            callback: Função que será chamada para verificar se deve pausar
        """
        self.pause_callback = callback
    
    async def setup(self):
        """Configura o agente e o manipulador de sessão."""
        # Cria o browser com as configurações
        browser_config = BrowserConfig(
            headless=self.headless,
            extra_chromium_args=[f"--slow-mo={self.slow_mo}"]
        )
        self.browser = Browser(config=browser_config)
        
        # Cria o agente com a tarefa inicial
        task_inicial = "Inicializando..."
        self.agent = Agent(
            task=task_inicial,
            llm=self.llm,
            browser=self.browser
        )
        
        # Configura o manipulador de sessão
        self.session_handler = SessionHandler(
            browser=self.browser,
            credentials={"email": self.google_email, "password": self.google_password},
            check_interval=self.check_interval
        )
        
        # Inicia o monitoramento de sessão
        await self.session_handler.start_monitoring()
        logger.info("Navegador e manipulador de sessão configurados com sucesso")
    
    async def run(self, task: str) -> str:
        """
        Executa uma tarefa com tratamento automático de sessão.

        Args:
            task: Descrição da tarefa a ser executada

        Returns:
            Resultado da execução da tarefa
        """
        if self.agent is None:
            await self.setup()
        
        # Adiciona o prefixo à tarefa
        full_task = f"{self.task_prefix}\n\n{task}"
        
        # Cria um novo agente com a tarefa completa
        new_agent = Agent(
            task=full_task,
            llm=self.llm,
            browser=self.browser
        )
        
        # Configura o manipulador de sessão para usar o callback de pausa
        if self.session_handler and self.pause_callback:
            self.session_handler.set_pause_callback(self.pause_callback)
            
        try:
            # Executa a tarefa com verificação de pausa
            result = await self._run_with_pause_check(new_agent)
            return result
        except Exception as e:
            logging.error(f"Erro ao executar tarefa: {str(e)}")
            raise
        finally:
            # Para o monitoramento de sessão
            if self.session_handler:
                await self.session_handler.stop_monitoring()

    async def _run_with_pause_check(self, agent) -> str:
        """
        Executa o agente com verificação de pausa.
        
        Args:
            agent: Instância do agente a ser executado
            
        Returns:
            Resultado da execução do agente
        """
        # Substitui o método run original do agente para incluir verificação de pausa
        original_take_step = agent.take_step
        
        async def take_step_with_pause_check():
            # Verifica se deve pausar
            if self.pause_callback and callable(self.pause_callback):
                self.pause_callback()
                
            # Executa o passo original
            return await original_take_step()
        
        # Substitui o método
        agent.take_step = take_step_with_pause_check
        
        # Executa o agente
        result = await agent.run()
        
        # Converte o resultado para string se necessário
        if not isinstance(result, str):
            result = str(result)
            
        return result
    
    async def close(self):
        """Fecha o navegador e libera recursos."""
        if self.session_handler:
            await self.session_handler.stop_monitoring()
        
        if self.browser:
            await self.browser.close()
        
        logger.info("Navegador fechado e recursos liberados")


async def main():
    """Função principal para executar o navegador com tratamento de sessão."""
    # Solicita a tarefa a ser executada
    task = input("Digite a tarefa que deseja realizar (ex: 'Acesse meus arquivos no Google Drive'): ")
    if not task:
        task = "Acesse meus arquivos no Google Drive e liste os 5 mais recentes"
    
    # Cria e executa o navegador
    browser = GoogleSessionBrowser(headless=False)
    
    try:
        result = await browser.run(task)
        print("\nResultado:", result)
    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main()) 