from typing import Dict, Any, Optional
import asyncio
import re

# Definição de uma classe base simplificada para nossas funções
class CustomBrowserFunction:
    """Classe base para funções personalizadas do navegador."""
    name = ""
    description = ""
    
    async def execute(self, **kwargs):
        """Método para executar a função."""
        pass

class HandleGoogleSessionExpired(CustomBrowserFunction):
    """
    Função personalizada para lidar com erros de sessão expirada do Google.
    Detecta mensagens de erro como "Sua sessão expirou" e tenta fazer login novamente.
    """
    name = "handle_google_session_expired"
    description = "Detecta e resolve problemas de sessão expirada do Google, fazendo login novamente automaticamente."
    
    async def execute(
        self,
        browser,
        google_email: Optional[str] = None,
        google_password: Optional[str] = None,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa a função para lidar com sessões expiradas do Google.
        
        Args:
            browser: Instância do navegador
            google_email: Email da conta Google (opcional)
            google_password: Senha da conta Google (opcional)
            max_retries: Número máximo de tentativas
            
        Returns:
            Dicionário com o resultado da operação
        """
        # Acessa a página atual do navegador
        page = browser.page if hasattr(browser, 'page') else None
        if not page:
            return {"success": False, "message": "Não foi possível acessar a página do navegador"}
        
        # Verifica se há mensagem de sessão expirada
        session_expired_texts = [
            "Sua sessão expirou",
            "Your session has expired",
            "Você não está conectado",
            "You are not connected",
            "Faça login novamente"
        ]
        
        page_content = await page.content()
        session_expired = any(text in page_content for text in session_expired_texts)
        
        if not session_expired:
            # Verifica elementos específicos que podem indicar sessão expirada
            try:
                expired_element = await page.query_selector("text=Sua sessão expirou")
                if not expired_element:
                    expired_element = await page.query_selector("text=Your session has expired")
                if not expired_element:
                    expired_element = await page.query_selector("button:has-text('Tentar novamente')")
                
                session_expired = expired_element is not None
            except Exception:
                pass
        
        if not session_expired:
            return {"success": True, "message": "Nenhum problema de sessão detectado"}
        
        # Tenta clicar no botão "Tentar novamente" primeiro
        try:
            retry_button = await page.query_selector("button:has-text('Tentar novamente')")
            if retry_button:
                await retry_button.click()
                await asyncio.sleep(3)
                
                # Verifica se o problema foi resolvido
                new_content = await page.content()
                if not any(text in new_content for text in session_expired_texts):
                    return {"success": True, "message": "Sessão restaurada com sucesso usando o botão 'Tentar novamente'"}
        except Exception as e:
            pass
        
        # Se não tiver credenciais, não pode fazer login automaticamente
        if not google_email or not google_password:
            return {
                "success": False, 
                "message": "Sessão expirada detectada, mas não foram fornecidas credenciais para login automático"
            }
        
        # Tenta fazer login novamente
        for attempt in range(max_retries):
            try:
                # Clica no link de login se disponível
                try:
                    login_link = await page.query_selector("a:has-text('Faça login')")
                    if login_link:
                        await login_link.click()
                        await asyncio.sleep(2)
                except Exception:
                    # Se não encontrar o link, tenta navegar diretamente para a página de login
                    await page.goto("https://accounts.google.com/signin")
                
                # Preenche o email
                await page.fill("input[type='email']", google_email)
                await page.click("button:has-text('Próxima'), button:has-text('Next')")
                await asyncio.sleep(2)
                
                # Preenche a senha
                await page.fill("input[type='password']", google_password)
                await page.click("button:has-text('Próxima'), button:has-text('Next')")
                await asyncio.sleep(5)
                
                # Verifica se o login foi bem-sucedido
                current_url = page.url
                if "myaccount.google.com" in current_url or "accounts.google.com/signin/v2/challenge" in current_url:
                    # Pode ser necessário lidar com verificação em duas etapas aqui
                    pass
                
                # Retorna à página original
                await page.go_back()
                
                # Verifica se o problema foi resolvido
                new_content = await page.content()
                if not any(text in new_content for text in session_expired_texts):
                    return {"success": True, "message": f"Login realizado com sucesso na tentativa {attempt + 1}"}
            
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"success": False, "message": f"Falha ao fazer login após {max_retries} tentativas: {str(e)}"}
                
                await asyncio.sleep(2)  # Espera antes de tentar novamente
        
        return {"success": False, "message": "Não foi possível resolver o problema de sessão expirada"}


class CheckAndFixGoogleSession(CustomBrowserFunction):
    """
    Função para verificar e corrigir problemas de sessão do Google durante a navegação.
    """
    name = "check_and_fix_google_session"
    description = "Verifica se há problemas de sessão do Google durante a navegação e tenta corrigi-los automaticamente."
    
    async def execute(
        self,
        browser,
        google_email: Optional[str] = None,
        google_password: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa a verificação e correção de sessão do Google.
        
        Args:
            browser: Instância do navegador
            google_email: Email da conta Google (opcional)
            google_password: Senha da conta Google (opcional)
            
        Returns:
            Dicionário com o resultado da operação
        """
        handle_session = HandleGoogleSessionExpired()
        result = await handle_session.execute(
            browser=browser,
            google_email=google_email,
            google_password=google_password
        )
        
        return result

# Registra as funções personalizadas para uso com o Browser-use
custom_functions = {
    "handle_google_session_expired": HandleGoogleSessionExpired(),
    "check_and_fix_google_session": CheckAndFixGoogleSession()
} 