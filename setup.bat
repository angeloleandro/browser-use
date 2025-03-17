@echo off
echo Instalando dependencias do Browser-use...
pip install -r requirements.txt
echo.
echo Instalando Playwright...
playwright install
echo.
echo Configuracao concluida! Agora voce pode executar:
echo - python test_browser_use.py (para o exemplo simples)
echo - python run_gradio_ui.py (para a interface grafica)
echo.
echo Lembre-se de configurar sua chave de API da OpenAI no arquivo .env
pause 