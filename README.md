<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./static/browser-use-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./static/browser-use.png">
  <img alt="Shows a black Browser Use Logo in light color mode and a white one in dark color mode." src="./static/browser-use.png"  width="full">
</picture>

<h1 align="center">Enable AI to control your browser 🤖</h1>

[![GitHub stars](https://img.shields.io/github/stars/gregpr07/browser-use?style=social)](https://github.com/gregpr07/browser-use/stargazers)
[![Discord](https://img.shields.io/discord/1303749220842340412?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://link.browser-use.com/discord)
[![Cloud](https://img.shields.io/badge/Cloud-☁️-blue)](https://cloud.browser-use.com)
[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://docs.browser-use.com)
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
[![Weave Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fapp.workweave.ai%2Fapi%2Frepository%2Fbadge%2Forg_T5Pvn3UBswTHIsN1dWS3voPg%2F881458615&labelColor=#EC6341)](https://app.workweave.ai/reports/repository/org_T5Pvn3UBswTHIsN1dWS3voPg/881458615)

🌐 Browser-use is the easiest way to connect your AI agents with the browser.

💡 See what others are building and share your projects in our [Discord](https://link.browser-use.com/discord)! Want Swag? Check out our [Merch store](https://browsermerch.com).

🌤️ Skip the setup - try our <b>hosted version</b> for instant browser automation! <b>[Try the cloud ☁︎](https://cloud.browser-use.com)</b>.

# Quick start

With pip (Python>=3.11):

```bash
pip install browser-use
```

install playwright:

```bash
playwright install
```

Spin up your agent:

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())
```

Add your API keys for the provider you want to use to your `.env` file.

```bash
OPENAI_API_KEY=
```

For other settings, models, and more, check out the [documentation 📕](https://docs.browser-use.com).

### Test with UI

You can test [browser-use with a UI repository](https://github.com/browser-use/web-ui)

Or simply run the gradio example:

```
uv pip install gradio
```

```bash
python examples/ui/gradio_demo.py
```

# Demos

<br/><br/>

[Task](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py): Add grocery items to cart, and checkout.

[![AI Did My Groceries](https://github.com/user-attachments/assets/d9359085-bde6-41d4-aa4e-6520d0221872)](https://www.youtube.com/watch?v=L2Ya9PYNns8)

<br/><br/>

Prompt: Add my latest LinkedIn follower to my leads in Salesforce.

![LinkedIn to Salesforce](https://github.com/user-attachments/assets/1440affc-a552-442e-b702-d0d3b277b0ae)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/find_and_apply_to_jobs.py): Read my CV & find ML jobs, save them to a file, and then start applying for them in new tabs, if you need help, ask me.'

https://github.com/user-attachments/assets/171fb4d6-0355-46f2-863e-edb04a828d04

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/browser/real_browser.py): Write a letter in Google Docs to my Papa, thanking him for everything, and save the document as a PDF.

![Letter to Papa](https://github.com/user-attachments/assets/242ade3e-15bc-41c2-988f-cbc5415a66aa)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/custom-functions/save_to_file_hugging_face.py): Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.

https://github.com/user-attachments/assets/de73ee39-432c-4b97-b4e8-939fd7f323b3

<br/><br/>

## More examples

For more examples see the [examples](examples) folder or join the [Discord](https://link.browser-use.com/discord) and show off your project.

# Vision

Tell your computer what to do, and it gets it done.

## Roadmap

### Agent

- [ ] Improve agent memory (summarize, compress, RAG, etc.)
- [ ] Enhance planning capabilities (load website specific context)
- [ ] Reduce token consumption (system prompt, DOM state)

### DOM Extraction

- [ ] Improve extraction for datepickers, dropdowns, special elements
- [ ] Improve state representation for UI elements

### Rerunning tasks

- [ ] LLM as fallback
- [ ] Make it easy to define workfows templates where LLM fills in the details
- [ ] Return playwright script from the agent

### Datasets

- [ ] Create datasets for complex tasks
- [ ] Benchmark various models against each other
- [ ] Fine-tuning models for specific tasks

### User Experience

- [ ] Human-in-the-loop execution
- [ ] Improve the generated GIF quality
- [ ] Create various demos for tutorial execution, job application, QA testing, social media, etc.

## Contributing

We love contributions! Feel free to open issues for bugs or feature requests. To contribute to the docs, check out the `/docs` folder.

## Local Setup

To learn more about the library, check out the [local setup 📕](https://docs.browser-use.com/development/local-setup).

## Cooperations

We are forming a commission to define best practices for UI/UX design for browser agents.
Together, we're exploring how software redesign improves the performance of AI agents and gives these companies a competitive advantage by designing their existing software to be at the forefront of the agent age.

Email [Toby](mailto:tbiddle@loop11.com?subject=I%20want%20to%20join%20the%20UI/UX%20commission%20for%20AI%20agents&body=Hi%20Toby%2C%0A%0AI%20found%20you%20in%20the%20browser-use%20GitHub%20README.%0A%0A) to apply for a seat on the committee.

## Swag

Want to show off your Browser-use swag? Check out our [Merch store](https://browsermerch.com). Good contributors will receive swag for free 👀.

## Citation

If you use Browser Use in your research or project, please cite:

```bibtex
@software{browser_use2024,
  author = {Müller, Magnus and Žunič, Gregor},
  title = {Browser Use: Enable AI to control your browser},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/browser-use/browser-use}
}
```

 <div align="center"> <img src="https://github.com/user-attachments/assets/402b2129-b6ac-44d3-a217-01aea3277dce" width="400"/> 
 
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
 
 </div>

<div align="center">
Made with ❤️ in Zurich and San Francisco
 </div>

# Browser-use com Tratamento Automático de Sessões

Este projeto estende a ferramenta [Browser-use](https://github.com/browser-use/browser-use) para lidar automaticamente com problemas de sessão ao acessar serviços do Google e outros sites que exigem autenticação.

## Funcionalidades

- 🔄 **Tratamento automático de sessões expiradas** - Detecta e resolve problemas de sessão sem intervenção manual
- 🤖 **Integração com modelos de IA** - Utiliza modelos como GPT-4o Mini via OpenRouter para automação inteligente e econômica
- 🌐 **Suporte a múltiplos serviços Google** - Gmail, Drive, Docs, Sheets, etc.
- 🔒 **Gestão segura de credenciais** - Armazena credenciais localmente no arquivo .env
- ⏯️ **Controle de pausa** - Permite pausar a execução para intervenção manual quando necessário

## Componentes Principais

- **SessionHandler** (`session_handler.py`) - Monitora e resolve problemas de sessão
- **GoogleSessionBrowser** (`google_session_browser.py`) - Navegador com tratamento automático de sessões do Google
- **Interface Gráfica** (`google_session_ui.py`) - Interface gráfica com botão de pausa para execução de tarefas

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/browser-use.git
   cd browser-use
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. Configure o arquivo `.env`:
   ```
   OPENROUTER_API_KEY=sua_chave_openrouter_aqui
   GOOGLE_EMAIL=seu_email@gmail.com
   GOOGLE_PASSWORD=sua_senha_aqui
   ```

## Uso

### Interface Gráfica (Recomendado)

Execute a interface gráfica:
```bash
python google_session_ui.py
```

A interface gráfica oferece:
- Configuração fácil de credenciais e parâmetros
- Seleção de modelos da OpenRouter, com destaque para o GPT-4o Mini
- Botão de pausa para intervenção manual quando necessário
- Visualização em tempo real do status da execução

### Interface Gradio

Execute a interface Gradio:
```bash
python run_gradio_ui.py
```

### Linha de Comando

Execute o navegador com tratamento automático de sessões:
```bash
python google_session_browser.py
```

### Uso Programático

```python
import asyncio
from google_session_browser import GoogleSessionBrowser

async def main():
    browser = GoogleSessionBrowser(
        model="openai/gpt-4o-mini",  # Usando o modelo GPT-4o Mini (padrão)
        headless=False
    )
    
    try:
        result = await browser.run("Acesse meus arquivos no Google Drive e liste os 5 mais recentes")
        print(result)
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentação

- [Instruções para Tratamento de Sessões do Google](GOOGLE_SESSION_INSTRUCOES.md) - Guia detalhado sobre o tratamento automático de sessões
- [Como Usar](COMO_USAR.md) - Guia geral de uso da ferramenta Browser-use

## Modelos Suportados

Nossa interface suporta os seguintes modelos da OpenRouter:

| Modelo | Descrição | Recomendação |
|--------|-----------|--------------|
| **openai/gpt-4o-mini** | Versão mais leve e econômica do GPT-4o | ⭐ Recomendado para uso diário |
| openai/gpt-4o | Modelo completo com excelente desempenho | Para tarefas complexas |
| openai/gpt-4-turbo | Versão turbo do GPT-4 | Alternativa ao GPT-4o |
| openai/gpt-3.5-turbo | Modelo mais econômico | Para tarefas simples |
| anthropic/claude-3-opus | Modelo mais avançado da Anthropic | Para tarefas que exigem raciocínio avançado |
| anthropic/claude-3-sonnet | Versão intermediária do Claude | Bom equilíbrio entre custo e desempenho |
| anthropic/claude-3-haiku | Versão mais leve do Claude | Para tarefas simples |

## Recursos Especiais

### Botão de Pausa

A interface gráfica inclui um botão de pausa que permite:
1. **Pausar a execução** - Quando você precisa intervir manualmente
2. **Continuar a execução** - Após realizar as alterações necessárias

Este recurso é especialmente útil quando:
- Você precisa resolver captchas manualmente
- Precisa fazer login com verificação em duas etapas
- Deseja ajustar algo na página antes de continuar

### Detecção Inteligente de Sessões

O sistema detecta automaticamente problemas de sessão através de:
- Análise do conteúdo da página
- Detecção de botões específicos como "Tentar novamente"
- Monitoramento contínuo durante a execução

## Segurança

⚠️ **IMPORTANTE**: Este sistema requer suas credenciais do Google para funcionar. Para maior segurança:

1. Use uma senha de aplicativo específica para o Google em vez de sua senha principal
2. Nunca compartilhe seu arquivo `.env` ou suas credenciais
3. Use este script apenas em dispositivos pessoais e seguros
4. Considere criar uma conta Google separada para testes

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
