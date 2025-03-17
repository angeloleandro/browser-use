# Instruções para Tratamento Automático de Sessões do Google

## Visão Geral

Este sistema foi desenvolvido para lidar automaticamente com problemas de sessão ao acessar serviços do Google através da ferramenta Browser-use. Ele monitora continuamente a página em busca de mensagens de expiração de sessão e resolve esses problemas automaticamente, permitindo que suas tarefas sejam executadas sem interrupções.

## Problemas Comuns de Sessão

Ao acessar serviços do Google como Gmail, Drive, Docs, etc., você pode encontrar mensagens como:
- "Sua sessão expirou"
- "Você não está conectado"
- "Faça login novamente"
- "Tentar novamente"

Estas mensagens interrompem o fluxo normal de execução das tarefas e exigem intervenção manual para continuar.

## Nossa Solução

Desenvolvemos um sistema que:
1. Monitora continuamente a página em busca de mensagens de expiração de sessão
2. Detecta automaticamente quando esses problemas ocorrem
3. Resolve os problemas clicando em "Tentar novamente" ou fazendo login novamente com suas credenciais
4. Permite que suas tarefas continuem sem interrupção
5. Oferece a possibilidade de pausar a execução quando necessário para intervenção manual

## Como Configurar

### 1. Configure o arquivo .env

Adicione suas credenciais do Google ao arquivo `.env`:

```
GOOGLE_EMAIL=seu_email@gmail.com
GOOGLE_PASSWORD=sua_senha_aqui
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
```

**Importante sobre segurança**: 
- Recomendamos usar uma senha de aplicativo específica para o Google em vez de sua senha principal
- Nunca compartilhe seu arquivo `.env` ou suas credenciais
- Use este script apenas em dispositivos pessoais e seguros

## Como Usar

### Opção 1: Interface Gráfica (Recomendado)

Execute a interface gráfica:

```bash
python google_session_ui.py
```

A interface gráfica oferece:
- Configuração fácil de credenciais e parâmetros
- Seleção de modelos da OpenRouter, com destaque para o GPT-4o Mini
- Botão de pausa para intervenção manual quando necessário
- Visualização em tempo real do status da execução
- Instruções detalhadas de uso

#### Como usar a interface:

1. Na aba **Configuração**, insira suas credenciais e ajuste as configurações do navegador
2. Selecione o modelo de IA (recomendamos o **GPT-4o Mini** para melhor custo-benefício)
3. Na aba **Execução**, digite a tarefa que deseja realizar
4. Clique em **Iniciar** para começar a execução
5. Use o botão **Pausar** quando precisar intervir manualmente
6. Clique em **Continuar** para retomar a execução após uma pausa

### Opção 2: Linha de Comando

Execute o navegador com tratamento de sessão:

```bash
python google_session_browser.py
```

Quando solicitado, digite a tarefa que deseja realizar, como:
- "Acesse meus arquivos no Google Drive e liste os 5 mais recentes"
- "Verifique meus emails não lidos no Gmail"
- "Crie um novo documento no Google Docs"

## Modelos Disponíveis

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

## Como Funciona

O sistema consiste em três componentes principais:

### 1. SessionHandler (session_handler.py)

Esta classe é responsável por:
- Monitorar a página em busca de problemas de sessão
- Detectar mensagens de expiração
- Resolver problemas clicando em botões de retry ou fazendo login novamente
- Fornecer um wrapper para ações que verifica problemas após cada ação

### 2. GoogleSessionBrowser (google_session_browser.py)

Esta classe:
- Configura o agente Browser-use com instruções específicas para lidar com problemas de sessão
- Inicializa o SessionHandler para monitoramento contínuo
- Executa tarefas com tratamento automático de sessão
- Gerencia o ciclo de vida do navegador e do manipulador de sessão
- Suporta pausa e continuação da execução

### 3. Interface Gráfica (google_session_ui.py)

Esta interface:
- Fornece uma forma amigável de configurar e executar tarefas
- Permite selecionar entre diferentes modelos da OpenRouter
- Permite pausar e continuar a execução quando necessário
- Exibe o status da execução em tempo real
- Oferece instruções detalhadas de uso

## Personalização

Você pode personalizar o comportamento do sistema ajustando os seguintes parâmetros ao criar uma instância de `GoogleSessionBrowser`:

```python
browser = GoogleSessionBrowser(
    google_email="email@gmail.com",  # Sobrescreve o valor do .env
    google_password="senha",         # Sobrescreve o valor do .env
    openrouter_api_key="chave_api",  # Sobrescreve o valor do .env
    model="openai/gpt-4o-mini",      # Modelo de IA a ser usado (recomendado)
    headless=False,                  # Se o navegador deve ser executado em segundo plano
    slow_mo=100,                     # Atraso em milissegundos entre ações
    check_interval=2.0               # Intervalo em segundos para verificar problemas de sessão
)
```

## Resolução de Problemas

### O sistema não está detectando problemas de sessão
- Verifique se o `check_interval` não está muito alto
- Confirme que as mensagens de expiração estão em português ou inglês (os padrões suportados)
- Adicione padrões personalizados se necessário

### Falha ao fazer login novamente
- Verifique se suas credenciais estão corretas
- Confirme que sua conta não tem verificação em duas etapas ativa
- Use uma senha de aplicativo se estiver usando 2FA

### O navegador fecha inesperadamente
- Aumente o valor de `slow_mo` para dar mais tempo para as páginas carregarem
- Verifique se há erros nos logs

### Preciso intervir manualmente
- Na interface gráfica, clique no botão **Pausar**
- Faça as alterações necessárias manualmente
- Clique em **Continuar** para retomar a execução

## Segurança

**IMPORTANTE**: Este sistema requer suas credenciais do Google para funcionar. Para maior segurança:

1. Use uma senha de aplicativo específica para o Google em vez de sua senha principal
2. Nunca compartilhe seu arquivo `.env` ou suas credenciais
3. Use este script apenas em dispositivos pessoais e seguros
4. Considere criar uma conta Google separada para testes

## Exemplo de Uso Avançado

```python
import asyncio
from google_session_browser import GoogleSessionBrowser

async def executar_tarefas():
    browser = GoogleSessionBrowser(
        model="openai/gpt-4o-mini",  # Usando o modelo recomendado
        headless=False
    )
    
    try:
        # Tarefa 1: Verificar emails
        resultado1 = await browser.run("Verifique meus emails não lidos no Gmail")
        print("Resultado 1:", resultado1)
        
        # Tarefa 2: Acessar Drive
        resultado2 = await browser.run("Liste meus arquivos recentes no Google Drive")
        print("Resultado 2:", resultado2)
        
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(executar_tarefas()) 