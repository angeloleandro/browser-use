import os
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Union

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from pydantic import SecretStr

# Local module imports
from browser_use import Agent

load_dotenv()


@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool


@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[dict]


def parse_agent_history(history_str: str) -> None:
    console = Console()

    # Split the content into sections based on ActionResult entries
    sections = history_str.split('ActionResult(')

    for i, section in enumerate(sections[1:], 1):  # Skip first empty section
        # Extract relevant information
        content = ''
        if 'extracted_content=' in section:
            content = section.split('extracted_content=')[1].split(',')[0].strip("'")

        if content:
            header = Text(f'Step {i}', style='bold blue')
            panel = Panel(content, title=header, border_style='blue')
            console.print(panel)
            console.print()


async def run_browser_task(
    task: str,
    api_key: str,
    model: str = 'openai/gpt-4o',
    headless: bool = True,
    use_openrouter: bool = True,
) -> str:
    if not api_key.strip():
        return 'Por favor, forneça uma chave de API'

    if use_openrouter:
        os.environ['OPENROUTER_API_KEY'] = api_key
        base_url = "https://openrouter.ai/api/v1"
        
        # Configurar o modelo para OpenRouter
        llm = ChatOpenAI(
            model=model,
            api_key=SecretStr(api_key or ""),
            base_url=base_url,
            default_headers={
                "HTTP-Referer": "https://localhost",
                "X-Title": "Browser-use Gradio UI"
            }
        )
    else:
        os.environ['OPENAI_API_KEY'] = api_key
        llm = ChatOpenAI(model=model, api_key=SecretStr(api_key or ""))

    try:
        agent = Agent(
            task=task,
            llm=llm,
        )
        result = await agent.run()
        # Converter o resultado para string se não for
        if not isinstance(result, str):
            return str(result)
        return result
    except Exception as e:
        return f'Erro: {str(e)}'


def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# Browser Use - Automação de Tarefas no Navegador')

        with gr.Row():
            with gr.Column():
                use_openrouter = gr.Checkbox(label='Usar OpenRouter', value=True)
                api_key = gr.Textbox(
                    label='Chave de API (OpenRouter ou OpenAI)', 
                    placeholder='sk-...',
                    type='password',
                    value=os.getenv("OPENROUTER_API_KEY", "")  # Pré-preencher com a chave do .env
                )
                task = gr.Textbox(
                    label='Descrição da Tarefa',
                    placeholder='Ex: Encontre voos de São Paulo para o Rio de Janeiro para a próxima semana',
                    lines=3,
                )
                model_choices = gr.Dropdown(
                    choices=[
                        # OpenAI
                        'openai/gpt-4o', 
                        'openai/gpt-4-turbo',
                        'openai/gpt-4o-mini',
                        
                        # Anthropic
                        'anthropic/claude-3-opus', 
                        'anthropic/claude-3-sonnet',
                        
                        # Google
                        'google/gemini-pro',
                        'google/gemini-2.0-flash-001',
                        'google/gemini-1.5-pro',
                        
                        # Meta
                        'meta-llama/llama-3-70b-instruct',
                        
                        # Qwen
                        'qwen/qwen-vl-plus',
                        'qwen/qwen-vl-max',
                        
                        # Microsoft
                        'microsoft/phi-3-mini'
                    ], 
                    label='Modelo (OpenRouter)', 
                    value='openai/gpt-4o',
                    visible=True,
                    allow_custom_value=True
                )
                openai_model_choices = gr.Dropdown(
                    choices=['gpt-4o', 'gpt-4', 'gpt-3.5-turbo'], 
                    label='Modelo (OpenAI)', 
                    value='gpt-4o',
                    visible=False
                )
                headless = gr.Checkbox(label='Executar em segundo plano', value=True)
                submit_btn = gr.Button('Executar Tarefa')

            with gr.Column():
                output = gr.Textbox(label='Resultado', lines=10, interactive=False)

        # Alternar entre modelos OpenRouter e OpenAI
        def toggle_model_dropdown(use_or):
            return gr.update(visible=use_or), gr.update(visible=not use_or)
        
        use_openrouter.change(
            toggle_model_dropdown, 
            inputs=[use_openrouter], 
            outputs=[model_choices, openai_model_choices]
        )
        
        # Função para determinar qual modelo usar
        def get_model(use_or, or_model, openai_model):
            return or_model if use_or else openai_model
        
        submit_btn.click(
            fn=lambda task, api_key, use_or, or_model, openai_model, headless: 
                asyncio.run(run_browser_task(
                    task, 
                    api_key, 
                    get_model(use_or, or_model, openai_model), 
                    headless,
                    use_or
                )),
            inputs=[task, api_key, use_openrouter, model_choices, openai_model_choices, headless],
            outputs=output,
        )

    return interface


if __name__ == '__main__':
    demo = create_ui()
    demo.launch() 