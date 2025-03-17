import asyncio
from typing import Optional, Dict, Any, Callable
import re
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("session_handler")

class SessionHandler:
    """
    Manipulador de sessão que monitora e resolve problemas de autenticação automaticamente.
    """
    
    def __init__(
        self,
        browser,
        credentials: Optional[Dict[str, str]] = None,
        check_interval: float = 2.0,
        max_retries: int = 3
    ):
        """
        Inicializa o manipulador de sessão.
        
        Args:
            browser: Instância do navegador
            credentials: Dicionário com credenciais (email, password)
            check_interval: Intervalo em segundos para verificar problemas de sessão
            max_retries: Número máximo de tentativas de login
        """
        self.browser = browser
        self.credentials = credentials if credentials is not None else {}
        self.check_interval = check_interval
        self.max_retries = max_retries
        self.monitoring = False
        self.monitor_task = None
        self.pause_callback = None  # Callback para verificar pausa
        
        # Padrões para detectar problemas de sessão
        self.session_expired_patterns = [
            "Sua sessão expirou",
            "Your session has expired",
            "Você não está conectado",
            "You are not connected",
            "Faça login novamente",
            "Sign in again",
            "Tentar novamente",
            "Try again"
        ]
        
        # Botões e elementos para resolver problemas
        self.retry_button_selectors = [
            "button:has-text('Tentar novamente')",
            "button:has-text('Try again')",
            "button:has-text('Retry')",
            "button:has-text('Sign in')",
            "button:has-text('Faça login')"
        ]
        
        # Seletores para formulários de login
        self.email_input_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='identifier']"
        ]
        
        self.password_input_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[name='Passwd']"
        ]
        
        self.next_button_selectors = [
            "button:has-text('Próxima')",
            "button:has-text('Next')",
            "button:has-text('Continue')",
            "button:has-text('Continuar')",
            "button[type='submit']"
        ]
    
    def set_pause_callback(self, callback):
        """
        Define uma função de callback para verificar se a execução deve ser pausada.
        
        Args:
            callback: Função que será chamada periodicamente para verificar se deve pausar
        """
        self.pause_callback = callback
    
    async def start_monitoring(self):
        """Inicia o monitoramento de problemas de sessão."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_task = asyncio.create_task(self._monitor_session())
        logger.info("Monitoramento de sessão iniciado")
    
    async def stop_monitoring(self):
        """Para o monitoramento de problemas de sessão."""
        if not self.monitoring:
            return
        
        self.monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Monitoramento de sessão parado")
    
    async def _monitor_session(self):
        """Monitora continuamente a página em busca de problemas de sessão."""
        while self.monitoring:
            try:
                # Verifica se deve pausar a execução
                if self.pause_callback:
                    self.pause_callback()
                    
                session_problem = await self._check_for_session_problems()
                if session_problem:
                    logger.info("Problema de sessão detectado, tentando resolver...")
                    resolved = await self._resolve_session_problem()
                    if resolved:
                        logger.info("Problema de sessão resolvido com sucesso")
                    else:
                        logger.warning("Não foi possível resolver o problema de sessão")
            except Exception as e:
                logger.error(f"Erro durante o monitoramento de sessão: {str(e)}")
            
            await asyncio.sleep(self.check_interval)
    
    async def _get_active_page(self):
        """
        Obtém a página ativa do navegador.
        
        Returns:
            A página ativa ou None se não houver página disponível
        """
        try:
            # Tenta obter a página do contexto do navegador
            if hasattr(self.browser, 'browser_context') and self.browser.browser_context:
                pages = self.browser.browser_context.pages
                if pages and len(pages) > 0:
                    return pages[0]  # Retorna a primeira página
            
            # Se não conseguir pelo contexto, tenta outros métodos
            if hasattr(self.browser, 'page'):
                return self.browser.page
            
            return None
        except Exception as e:
            logger.error(f"Erro ao obter página ativa: {str(e)}")
            return None
    
    async def _check_for_session_problems(self) -> bool:
        """
        Verifica se há problemas de sessão na página atual.
        
        Returns:
            bool: True se um problema de sessão for detectado, False caso contrário
        """
        try:
            page = await self._get_active_page()
            if not page:
                return False
            
            # Verifica o conteúdo da página
            content = await page.content()
            for pattern in self.session_expired_patterns:
                if pattern in content:
                    return True
            
            # Verifica elementos específicos
            for selector in self.retry_button_selectors:
                button = await page.query_selector(selector)
                if button:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar problemas de sessão: {str(e)}")
            return False
    
    async def _resolve_session_problem(self) -> bool:
        """
        Tenta resolver um problema de sessão detectado.
        
        Returns:
            bool: True se o problema foi resolvido, False caso contrário
        """
        try:
            page = await self._get_active_page()
            if not page:
                return False
            
            # Tenta clicar no botão "Tentar novamente" primeiro
            for selector in self.retry_button_selectors:
                button = await page.query_selector(selector)
                if button:
                    logger.info(f"Clicando no botão: {selector}")
                    await button.click()
                    await asyncio.sleep(3)
                    
                    # Verifica se o problema foi resolvido
                    if not await self._check_for_session_problems():
                        return True
            
            # Se não tiver credenciais, não pode fazer login
            if not self.credentials.get("email") or not self.credentials.get("password"):
                logger.warning("Credenciais não fornecidas, não é possível fazer login")
                return False
            
            # Tenta fazer login
            for attempt in range(self.max_retries):
                logger.info(f"Tentativa de login {attempt + 1}/{self.max_retries}")
                
                # Procura por links de login
                login_link = await page.query_selector("a:has-text('Faça login'), a:has-text('Sign in')")
                if login_link:
                    await login_link.click()
                    await asyncio.sleep(2)
                else:
                    # Se não encontrar o link, tenta navegar diretamente para a página de login
                    current_url = page.url
                    if "google.com" in current_url:
                        await page.goto("https://accounts.google.com/signin")
                    await asyncio.sleep(2)
                
                # Preenche o email
                for selector in self.email_input_selectors:
                    email_input = await page.query_selector(selector)
                    if email_input:
                        await email_input.fill(self.credentials["email"])
                        break
                
                # Clica em próxima
                for selector in self.next_button_selectors:
                    next_button = await page.query_selector(selector)
                    if next_button:
                        await next_button.click()
                        break
                
                await asyncio.sleep(2)
                
                # Preenche a senha
                for selector in self.password_input_selectors:
                    password_input = await page.query_selector(selector)
                    if password_input:
                        await password_input.fill(self.credentials["password"])
                        break
                
                # Clica em próxima novamente
                for selector in self.next_button_selectors:
                    next_button = await page.query_selector(selector)
                    if next_button:
                        await next_button.click()
                        break
                
                await asyncio.sleep(5)
                
                # Verifica se o login foi bem-sucedido
                if not await self._check_for_session_problems():
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao resolver problema de sessão: {str(e)}")
            return False
    
    async def wrap_action(self, action_func: Callable, *args, **kwargs):
        """
        Wrapper para ações do navegador que verifica e resolve problemas de sessão.
        
        Args:
            action_func: Função a ser executada
            *args, **kwargs: Argumentos para a função
            
        Returns:
            Resultado da função
        """
        try:
            result = await action_func(*args, **kwargs)
            
            # Verifica se há problemas de sessão após a ação
            session_problem = await self._check_for_session_problems()
            if session_problem:
                logger.info("Problema de sessão detectado após ação, tentando resolver...")
                resolved = await self._resolve_session_problem()
                if resolved:
                    logger.info("Problema de sessão resolvido, repetindo a ação")
                    result = await action_func(*args, **kwargs)
                else:
                    logger.warning("Não foi possível resolver o problema de sessão")
            
            return result
        except Exception as e:
            logger.error(f"Erro durante a execução da ação: {str(e)}")
            raise 