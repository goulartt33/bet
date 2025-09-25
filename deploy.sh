@echo off
REM ===================================================
REM Deploy automático via CMD (Windows)
REM ===================================================

SET BRANCH=main
SET COMMIT_MSG=Atualização automática do bot
SET RENDER_SERVICE_ID=srv-COLOQUE_SEU_ID_AQUI
SET RENDER_API_TOKEN=COLOQUE_SEU_TOKEN_AQUI

echo 📦 Adicionando alterações ao Git...
git add .

echo 📝 Criando commit...
git commit -m "%COMMIT_MSG%"

echo 🚀 Enviando para o GitHub...
git push origin %BRANCH%

echo ⚡ Iniciando deploy no Render...
powershell -Command "Invoke-RestMethod -Uri 'https://api.render.com/deploy/%RENDER_SERVICE_ID%' -Method POST -Headers @{ Authorization = 'Bearer %RENDER_API_TOKEN%' }"

echo ✅ Deploy iniciado!
pause
