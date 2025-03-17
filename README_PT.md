# Browser-use - Automação de Navegador com IA

Este repositório contém a configuração para usar o Browser-use, uma ferramenta que permite conectar agentes de IA com o navegador.

## Requisitos

- Python 3.11 ou superior
- Chave de API da OpenAI ou OpenRouter

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Instale o Playwright:

```bash
playwright install
```

3. Configure o arquivo `.env` com sua chave de API:

Para OpenAI:
```
OPENAI_API_KEY=sua_chave_aqui
```

Para OpenRouter:
```
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

## Uso

### Exemplo Simples

Execute o script de exemplo:

```bash
python test_browser_use.py
```

### Interface Gráfica com Gradio

Execute a interface Gradio:

```bash
python run_gradio_ui.py
```

Na interface, você pode:
- Escolher entre usar OpenAI ou OpenRouter
- Inserir sua chave de API
- Descrever a tarefa que deseja que o agente execute
- Selecionar o modelo de IA a ser usado
- Escolher se deseja executar o navegador em segundo plano

## Modelos Disponíveis na OpenRouter

A OpenRouter permite acesso a vários modelos de diferentes provedores:

- OpenAI: gpt-4o, gpt-4-turbo
- Anthropic: claude-3-opus, claude-3-sonnet
- Meta: llama-3-70b-instruct
- Google: gemini-pro
- E muitos outros

## Exemplos de Tarefas

- "Compare o preço do gpt-4o e DeepSeek-V3"
- "Encontre voos de São Paulo para o Rio de Janeiro para a próxima semana"
- "Pesquise as últimas notícias sobre inteligência artificial"
- "Encontre receitas de bolo de chocolate e salve os ingredientes"

## Solução de Problemas

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme que sua chave de API está correta
3. Certifique-se de que o Playwright está instalado corretamente
4. Para a OpenRouter, verifique se você tem créditos suficientes para o modelo escolhido

Para mais informações, consulte a [documentação oficial do Browser-use](https://github.com/browser-use/browser-use) ou a [documentação da OpenRouter](https://openrouter.ai/docs). 