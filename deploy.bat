@echo off
echo Atualizando repositório Git...
git add .
git commit -m "Atualização do bot"
git push origin main

echo Deploy iniciado no Render...
powershell -Command "bash deploy.sh"

pause
