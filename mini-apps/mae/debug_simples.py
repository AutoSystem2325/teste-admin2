#!/usr/bin/env python3
"""
Debug ultra-simples para entender o que está acontecendo
"""
try:
    from PIL import ImageGrab
    import tkinter as tk
    from tkinter import messagebox
    
    def capturar_e_analisar():
        """Captura uma região pequena da tela e analisa"""
        print("Clique OK e posicione o mouse sobre o campo Qtd")
        input("Pressione ENTER quando estiver posicionado...")
        
        # Capturar uma região pequena ao redor do mouse
        import pyautogui
        x, y = pyautogui.position()
        
        # Capturar região 50x30 ao redor do mouse
        screenshot = ImageGrab.grab(bbox=(x-25, y-15, x+25, y+15))
        screenshot.save("debug_captura.png")
        
        width, height = screenshot.size
        print(f"Capturado: {width}x{height} pixels")
        
        # Analisar todas as cores
        cores = {}
        for px in range(width):
            for py in range(height):
                r, g, b = screenshot.getpixel((px, py))
                cor_key = f"({r},{g},{b})"
                cores[cor_key] = cores.get(cor_key, 0) + 1
        
        # Mostrar as 10 cores mais comuns
        cores_ordenadas = sorted(cores.items(), key=lambda x: x[1], reverse=True)
        
        print("\n🎨 CORES MAIS COMUNS:")
        for i, (cor, count) in enumerate(cores_ordenadas[:10]):
            pct = (count / (width * height)) * 100
            print(f"{i+1}. {cor} - {count} pixels ({pct:.1f}%)")
        
        # Análise simples
        print(f"\n📊 ANÁLISE:")
        print(f"Total de cores únicas: {len(cores)}")
        print(f"Imagem salva como: debug_captura.png")
        
        # Tentar detectar padrão
        cor_mais_comum = cores_ordenadas[0][0] if cores_ordenadas else "N/A"
        print(f"Cor dominante: {cor_mais_comum}")
        
    if __name__ == "__main__":
        print("🔍 DEBUG ULTRA-SIMPLES")
        print("=" * 40)
        capturar_e_analisar()
        
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Instale: pip install Pillow pyautogui")
except Exception as e:
    print(f"❌ Erro: {e}")