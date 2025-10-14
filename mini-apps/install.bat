@echo off
echo 🚀 Instalando dependências dos Mini Apps OctavioSync...

echo.
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

echo.
echo 📦 Instalando dependências básicas...
pip install requests
pip install python-socketio
pip install pyautogui

echo.
echo ✅ Instalação concluída!
echo.
echo 🎯 Para executar:
echo    App Mãe: cd mae && python app_mae.py
echo    App Filho: cd filho && python app_filho.py
echo.
pause



