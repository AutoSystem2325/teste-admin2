#!/bin/bash

echo "🚀 Instalando dependências dos Mini Apps OctavioSync..."

echo ""
echo "📦 Atualizando pip..."
python3 -m pip install --upgrade pip

echo ""
echo "📦 Instalando dependências básicas..."
pip3 install requests
pip3 install python-socketio
pip3 install pyautogui

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🎯 Para executar:"
echo "   App Mãe: cd mae && python3 app_mae.py"
echo "   App Filho: cd filho && python3 app_filho.py"
echo ""



