import gradio as gr
import asyncio
import threading
import time
from dotenv import load_dotenv
import os
from google_session_browser import GoogleSessionBrowser
import logging
from typing import AsyncGenerator, Tuple, Dict, Any, Union, List

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("google_session_ui")

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis globais para controle
browser_instance = None
execution_paused = False
execution_thread = None
execution_event = threading.Event()  # Evento para controlar a pausa/continuação
browser_visible = False  # Controla se o navegador está visível

def toggle_pause():
    """Alterna entre pausar e continuar a execução."""
    global execution_paused
    
    if execution_paused:
        # Continuar execução
        execution_paused = False
        execution_event.set()
        return "⏸️ Pausar"
    else:
        # Pausar execução
        execution_paused = True
        execution_event.clear()
        return "▶️ Continuar"

def check_pause_status():
    """Verifica se a execução está pausada e aguarda se necessário."""
    if execution_paused:
        logger.info("Execução pausada. Aguardando comando para continuar...")
        execution_event.wait()
        logger.info("Execução continuada!")

async def run_browser_task(
    task: str, 
    google_email: str, 
    google_password: str, 
    openrouter_key: str, 
    model: str, 
    headless: bool, 
    slow_mo: int, 
    check_interval: float, 
    status_box: str
) -> AsyncGenerator[Tuple[str, Dict[str, Any]], None]:
    """Executa uma tarefa no navegador com tratamento de sessão."""
    global browser_instance, browser_visible
    
    try:
        # Atualiza o status
        status_box = status_box + "\nIniciando navegador... Por favor, aguarde."
        yield status_box, {"interactive": True}
        
        # Inicializa o navegador
        browser_instance = GoogleSessionBrowser(
            google_email=google_email,
            google_password=google_password,
            openrouter_api_key=openrouter_key,
            model=model,
            headless=headless,
            slow_mo=slow_mo,
            check_interval=check_interval
        )
        
        # Configura o manipulador de pausa no browser
        browser_instance.set_pause_callback(check_pause_status)
        
        # Atualiza o status
        browser_visible = True
        status_box = status_box + "\n✅ Navegador inicializado com sucesso!"
        status_box = status_box + "\n🔄 Executando tarefa: " + task
        yield status_box, {"interactive": True}
        
        # Executa a tarefa
        result = await browser_instance.run(task)
        
        # Atualiza o status com o resultado
        status_box = status_box + f"\n\n✅ Tarefa concluída com sucesso!\n\nResultado:\n{result}"
        yield status_box, {"interactive": False}
        
    except Exception as e:
        # Em caso de erro, atualiza o status
        error_message = f"\n\n❌ Erro durante a execução: {str(e)}"
        logger.error(error_message)
        status_box = status_box + error_message
        yield status_box, {"interactive": False}
        
    finally:
        # Fecha o navegador
        if browser_instance:
            await browser_instance.close()
            browser_instance = None
            browser_visible = False
            status_box = status_box + "\n\n🔒 Navegador fechado."
            yield status_box, {"interactive": False}

def run_async_task(
    task: str, 
    google_email: str, 
    google_password: str, 
    openrouter_key: str, 
    model: str, 
    headless: bool, 
    slow_mo: int, 
    check_interval: float, 
    status_box: str
) -> Tuple[str, Dict[str, Any]]:
    """Função para executar a tarefa assíncrona em uma thread separada."""
    global execution_thread, execution_paused, execution_event, browser_visible
    
    # Verifica se já existe uma execução em andamento
    if execution_thread and execution_thread.is_alive():
        return status_box + "\n⚠️ Já existe uma tarefa em execução. Aguarde ou reinicie a aplicação.", {"interactive": False}
    
    # Reinicia o evento de pausa
    execution_paused = False
    execution_event.set()
    
    # Cria e inicia a thread
    loop = asyncio.new_event_loop()
    
    def run_in_thread():
        asyncio.set_event_loop(loop)
        try:
            # Executa a tarefa e ignora os resultados (serão processados pela UI)
            asyncio.run(run_browser_task_wrapper())
        except Exception as e:
            logger.error(f"Erro na thread: {str(e)}")
        finally:
            # Garante que o status do navegador seja atualizado
            global browser_visible
            browser_visible = False
    
    async def run_browser_task_wrapper():
        # Esta função é apenas um wrapper para evitar problemas com o asyncio.run
        async for _ in run_browser_task(task, google_email, google_password, openrouter_key, model, headless, slow_mo, check_interval, status_box):
            pass
    
    execution_thread = threading.Thread(target=run_in_thread)
    execution_thread.daemon = True
    execution_thread.start()
    
    # Retorna o status inicial e habilita o botão de pausa
    return status_box + "\n🚀 Iniciando navegador...\n⏳ Por favor, aguarde enquanto o navegador é carregado.", {"interactive": True, "value": "⏸️ Pausar"}

def check_browser_status():
    """Verifica o status do navegador e atualiza a interface."""
    global browser_visible
    return browser_visible, gr.update(interactive=browser_visible)

def create_ui():
    """Cria a interface do usuário."""
    with gr.Blocks(title="Tratamento Automático de Sessões do Google") as app:
        gr.Markdown("# Tratamento Automático de Sessões do Google")
        gr.Markdown("Esta interface permite executar tarefas no navegador com tratamento automático de sessões do Google.")
        
        with gr.Tab("Configuração"):
            with gr.Row():
                with gr.Column():
                    # Credenciais
                    gr.Markdown("### Credenciais")
                    google_email = gr.Textbox(
                        label="Email do Google", 
                        placeholder="seu_email@gmail.com",
                        value=os.getenv("GOOGLE_EMAIL", "")
                    )
                    google_password = gr.Textbox(
                        label="Senha do Google", 
                        placeholder="sua_senha_aqui",
                        type="password",
                        value=os.getenv("GOOGLE_PASSWORD", "")
                    )
                    openrouter_key = gr.Textbox(
                        label="Chave da API OpenRouter", 
                        placeholder="sua_chave_openrouter_aqui",
                        type="password",
                        value=os.getenv("OPENROUTER_API_KEY", "")
                    )
                
                with gr.Column():
                    # Configurações do navegador
                    gr.Markdown("### Configurações do Navegador")
                    model = gr.Dropdown(
                        label="Modelo de IA",
                        choices=[
                            "openai/gpt-4o-mini",  # Destacando o GPT-4o Mini
                            "openai/gpt-4o-mini-search-preview",
                            "openai/gpt-4o",
                            "openai/gpt-4-turbo",
                            "openai/gpt-3.5-turbo",
                            "anthropic/claude-3-opus",
                            "anthropic/claude-3-sonnet",
                            "anthropic/claude-3-haiku"
                        ],
                        value="openai/gpt-4o-mini"  # Definindo como padrão
                    )
                    headless = gr.Checkbox(
                        label="Executar em segundo plano",
                        value=False,
                        info="Se marcado, o navegador não será visível durante a execução"
                    )
                    slow_mo = gr.Slider(
                        label="Atraso entre ações (ms)",
                        minimum=0,
                        maximum=500,
                        value=100,
                        step=10,
                        info="Quanto maior o valor, mais lenta será a execução"
                    )
                    check_interval = gr.Slider(
                        label="Intervalo de verificação de sessão (s)",
                        minimum=0.5,
                        maximum=10,
                        value=2.0,
                        step=0.5,
                        info="Intervalo para verificar problemas de sessão"
                    )
        
        with gr.Tab("Execução"):
            # Tarefa
            task = gr.Textbox(
                label="Tarefa a ser executada",
                placeholder="Ex: Acesse meus arquivos no Google Drive e liste os 5 mais recentes",
                lines=3
            )
            
            # Status do navegador
            with gr.Row():
                browser_status = gr.Checkbox(
                    label="Status do Navegador",
                    value=False,
                    interactive=False,
                    info="Indica se o navegador está em execução"
                )
                
                # Indicador visual
                browser_indicator = gr.HTML(
                    value="<div style='text-align: center; padding: 10px;'><span style='color: red; font-weight: bold;'>⚫ Navegador inativo</span></div>"
                )
                
                # Botão de atualização
                refresh_button = gr.Button("🔄 Atualizar Status")
            
            # Botões
            with gr.Row():
                start_button = gr.Button("▶️ Iniciar", variant="primary")
                pause_button = gr.Button("⏸️ Pausar", interactive=False)
            
            # Status
            status_box = gr.Textbox(
                label="Status da execução",
                placeholder="Aguardando início da execução...",
                lines=10,
                interactive=False
            )
        
        # Eventos
        start_button.click(
            fn=run_async_task,
            inputs=[task, google_email, google_password, openrouter_key, model, headless, slow_mo, check_interval, status_box],
            outputs=[status_box, pause_button]
        )
        
        pause_button.click(
            fn=toggle_pause,
            inputs=[],
            outputs=[pause_button]
        )
        
        # Função para atualizar o status do navegador
        def update_browser_status():
            global browser_visible
            if browser_visible:
                return True, "<div style='text-align: center; padding: 10px;'><span style='color: green; font-weight: bold;'>🟢 Navegador ativo</span></div>", gr.update(interactive=True)
            else:
                return False, "<div style='text-align: center; padding: 10px;'><span style='color: red; font-weight: bold;'>⚫ Navegador inativo</span></div>", gr.update(interactive=False)
        
        # Inicializa o status do navegador
        app.load(
            fn=update_browser_status,
            inputs=None,
            outputs=[browser_status, browser_indicator, pause_button]
        )
        
        # Botão de atualização
        refresh_button.click(
            fn=update_browser_status,
            inputs=None,
            outputs=[browser_status, browser_indicator, pause_button]
        )
        
        # Instruções
        with gr.Tab("Instruções"):
            gr.Markdown("""
            ## Como usar o Tratamento Automático de Sessões do Google
            
            ### 1. Configure suas credenciais
            - Insira seu email e senha do Google
            - Adicione sua chave da API OpenRouter
            
            ### 2. Ajuste as configurações do navegador
            - Escolha o modelo de IA desejado (recomendamos o GPT-4o Mini para melhor custo-benefício)
            - Defina se o navegador deve ser executado em segundo plano
            - Ajuste o atraso entre ações e o intervalo de verificação de sessão
            
            ### 3. Execute sua tarefa
            - Digite a tarefa que deseja realizar
            - Clique em "Iniciar" para começar a execução
            - Use o botão "Pausar" quando precisar intervir manualmente
            - Clique em "Continuar" para retomar a execução após uma pausa
            
            ### Exemplos de tarefas
            - "Acesse meus arquivos no Google Drive e liste os 5 mais recentes"
            - "Verifique meus emails não lidos no Gmail"
            - "Crie um novo documento no Google Docs com o título 'Relatório Mensal'"
            
            ### Segurança
            ⚠️ **IMPORTANTE**: Suas credenciais do Google são informações sensíveis.
            - Use uma senha de aplicativo específica para o Google em vez de sua senha principal
            - Use este sistema apenas em dispositivos pessoais e seguros
            """)
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(share=False, server_port=7861) 