# Como Usar o Browser-use com OpenRouter

Este guia rápido explica como usar o Browser-use com a OpenRouter para automatizar tarefas no navegador usando diferentes modelos de IA.

## Configuração Inicial

1. **Obtenha uma chave da API da OpenRouter**:
   - Crie uma conta em [OpenRouter](https://openrouter.ai/)
   - Gere uma chave de API no painel de controle

2. **Configure o arquivo .env**:
   ```
   OPENROUTER_API_KEY=sua_chave_openrouter_aqui
   OPENAI_API_BASE=https://openrouter.ai/api/v1
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Usando a Interface Gráfica

1. **Inicie a interface Gradio**:
   ```bash
   python run_gradio_ui.py
   ```

2. **Na interface**:
   - Mantenha a opção "Usar OpenRouter" marcada
   - Cole sua chave da API da OpenRouter
   - Escreva a tarefa que deseja automatizar
   - Selecione o modelo de IA desejado
   - Clique em "Executar Tarefa"

## Usando o Script de Exemplo

1. **Edite o arquivo test_browser_use.py** para escolher o modelo desejado:
   ```python
   modelo = "anthropic/claude-3-opus"  # Substitua pelo modelo que deseja usar
   ```

2. **Execute o script**:
   ```bash
   python test_browser_use.py
   ```

## Modelos Disponíveis na OpenRouter

### OpenAI
- `openai/gpt-4o`
- `openai/gpt-4-turbo`
- `openai/gpt-4o-mini`

### Anthropic
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku`

### Google
- `google/gemini-pro`
- `google/gemini-2.0-flash-001`
- `google/gemini-1.5-pro`

### Meta
- `meta-llama/llama-3-70b-instruct`
- `meta-llama/llama-3-8b-instruct`

### Qwen
- `qwen/qwen-vl-plus`
- `qwen/qwen-vl-max`

### Microsoft
- `microsoft/phi-3-mini`

## Exemplos de Tarefas

- "Pesquise os preços de passagens aéreas de São Paulo para o Rio de Janeiro para o próximo mês"
- "Encontre as 5 melhores receitas de bolo de chocolate e liste os ingredientes"
- "Compare os preços do iPhone 15 em diferentes lojas online"
- "Pesquise as últimas notícias sobre inteligência artificial no Brasil"
- "Encontre tutoriais sobre como aprender Python para iniciantes"

## Solução de Problemas

- **Erro de autenticação**: Verifique se sua chave da API está correta
- **Erro de modelo**: Confirme se o modelo escolhido está disponível na OpenRouter
- **Erro de créditos**: Verifique se você tem créditos suficientes na sua conta OpenRouter
- **Erro do Playwright**: Execute `playwright install` novamente

Para mais informações, consulte a [documentação da OpenRouter](https://openrouter.ai/docs). 