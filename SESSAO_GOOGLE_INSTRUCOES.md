# Tratamento Automático de Sessões do Google

Este guia explica como usar o sistema de tratamento automático de sessões do Google que desenvolvemos para o Browser-use.

## O Problema

Quando você usa o Browser-use para acessar serviços do Google (Drive, Gmail, etc.), pode encontrar mensagens como:
- "Sua sessão expirou"
- "Você não está conectado"
- "Faça login novamente"

Essas mensagens interrompem a automação e exigem intervenção manual.

## Nossa Solução

Desenvolvemos um sistema que:
1. **Monitora continuamente** a página em busca de problemas de sessão
2. **Detecta automaticamente** mensagens de sessão expirada
3. **Resolve o problema** clicando em "Tentar novamente" ou fazendo login novamente
4. **Continua a tarefa** de onde parou

## Como Usar

### 1. Configure o arquivo `.env`

```
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
GOOGLE_EMAIL=seu_email@gmail.com
GOOGLE_PASSWORD=sua_senha_aqui
```

### 2. Execute o navegador com tratamento de sessão

```bash
python google_session_browser.py
```

O script irá:
- Solicitar a tarefa que você deseja realizar
- Iniciar o navegador com monitoramento de sessão
- Executar a tarefa
- Resolver automaticamente problemas de sessão

## Como Funciona

O sistema consiste em dois componentes principais:

### 1. `session_handler.py`

Um manipulador de sessão que:
- Monitora continuamente a página em busca de problemas de sessão
- Detecta mensagens de erro específicas
- Tenta clicar em botões como "Tentar novamente"
- Faz login novamente usando suas credenciais

### 2. `google_session_browser.py`

Um wrapper para o Browser-use que:
- Integra o manipulador de sessão com o agente do Browser-use
- Adiciona instruções específicas para o agente
- Gerencia o ciclo de vida do navegador e do manipulador de sessão

## Personalização

Você pode personalizar o comportamento do sistema editando:

- **Padrões de detecção**: Adicione ou remova padrões de texto que indicam problemas de sessão
- **Seletores de botões**: Modifique os seletores CSS para botões e campos de formulário
- **Intervalo de verificação**: Ajuste a frequência com que o sistema verifica problemas de sessão

## Solução de Problemas

- **Erro de autenticação**: Verifique se suas credenciais do Google estão corretas
- **Verificação em duas etapas**: Este sistema não lida com verificação em duas etapas. Recomendamos desativar temporariamente a verificação em duas etapas ou usar um dispositivo confiável
- **Captcha**: Se o Google mostrar um captcha, você precisará resolvê-lo manualmente

## Segurança

⚠️ **IMPORTANTE**: Suas credenciais do Google são informações sensíveis. Nunca compartilhe o arquivo .env ou exponha suas credenciais.

Para maior segurança:
- Use este script apenas em dispositivos pessoais e seguros
- Considere criar uma senha de aplicativo específica para este uso
- Exclua suas credenciais do arquivo .env quando não estiver usando o script 