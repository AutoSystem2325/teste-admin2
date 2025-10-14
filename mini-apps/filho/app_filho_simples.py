#!/usr/bin/env python3
"""
App Filho Simplificado - Funcional sem dependências extras
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import threading
from datetime import datetime
import pyautogui

# Adicionar o diretório shared ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from config import SERVER_URL, WEBSOCKET_URL, DETECTION_CONFIG
from api_client import OctavioSyncAPIClient
from websocket_client import OctavioSyncWebSocketClient

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OctavioSync - Filho Login")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        
        self.center_window()
        self.api_client = OctavioSyncAPIClient(SERVER_URL)
        self.setup_ui()
        
        self.login_success = False
        self.user_token = None
        self.filho_id = None
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.root.winfo_screenheight() // 2) - (250 // 2)
        self.root.geometry(f"300x250+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="OctavioSync - Filho", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=25)
        self.email_entry.pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Senha:").pack(anchor=tk.W)
        self.senha_entry = ttk.Entry(main_frame, width=25, show="*")
        self.senha_entry.pack(pady=(0, 20))
        
        ttk.Button(main_frame, text="Login", command=self.login).pack()
        
        self.root.bind('<Return>', lambda e: self.login())
        self.email_entry.focus()
    
    def login(self):
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha email e senha")
            return
        
        def login_thread():
            if self.api_client.login_filho(email, senha):
                self.user_token = self.api_client.get_token()
                self.filho_id = self.api_client.get_filho_id()
                self.login_success = True
                self.root.after(0, self.close_window)
            else:
                self.root.after(0, lambda: messagebox.showerror("Erro", "Login falhou"))
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def close_window(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
        return self.login_success, self.user_token, self.filho_id

class ControlWindow:
    def __init__(self, token, filho_id):
        self.token = token
        self.filho_id = filho_id
        self.ws_client = None
        self.is_connected = False
        self.floating_buttons = {}  # Armazenar botões flutuantes
        
        self.root = tk.Tk()
        self.root.title("OctavioSync - Filho Controle")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.center_window()
        self.setup_ui()
        self.setup_pyautogui()
        self.connect_websocket()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Monitoramento de Comandos", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Status da Conexão
        self.status_label = ttk.Label(main_frame, text="Conexão: Desconectado", 
                                     font=("Arial", 10), foreground="red")
        self.status_label.pack(anchor=tk.W, pady=(0, 5))

        # Último Comando
        self.last_command_label = ttk.Label(main_frame, text="Último Comando: Nenhum",
                                            font=("Arial", 10))
        self.last_command_label.pack(anchor=tk.W, pady=(0, 5))

        # Log
        ttk.Label(main_frame, text="Log de Atividades:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = tk.Text(main_frame, height=10, state='disabled', wrap='word')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões para criar botões flutuantes
        floating_frame = ttk.Frame(main_frame)
        floating_frame.pack(pady=(5, 0))
        
        ttk.Button(floating_frame, text="Criar Botões Flutuantes", 
                  command=self.create_floating_buttons).pack(pady=5)
        
        # Botões de teste manual
        test_frame = ttk.Frame(main_frame)
        test_frame.pack(pady=(5, 0))
        
        ttk.Button(test_frame, text="Teste 1C", 
                  command=lambda: self.execute_command("1C")).pack(side=tk.LEFT, padx=2)
        ttk.Button(test_frame, text="Teste -1V", 
                  command=lambda: self.execute_command("-1V")).pack(side=tk.LEFT, padx=2)
        ttk.Button(test_frame, text="Teste -", 
                  command=lambda: self.execute_command("-")).pack(side=tk.LEFT, padx=2)
        
        # Mapeamento de teclas
        ttk.Label(main_frame, text="Mapeamento: 1C→F5 | -1V→F6 | -→F11", 
                 font=("Arial", 8), foreground="gray").pack()

    def setup_pyautogui(self):
        """Configura PyAutoGUI com failsafe e debug"""
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1  # Pausa maior para garantir execução
        
        # Informações de debug
        pos = pyautogui.position()
        size = pyautogui.size()
        
        self.add_log(f"PyAutoGUI configurado - Mouse: {pos}, Tela: {size}")
        self.add_log("FAILSAFE ativo: mova mouse para canto superior esquerdo para parar")

    def add_log(self, message, level='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.root.after(0, lambda: self._insert_log(f"[{timestamp}] {message}\n"))

    def _insert_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def connect_websocket(self):
        self.add_log("Conectando ao WebSocket...")
        self.ws_client = OctavioSyncWebSocketClient(WEBSOCKET_URL, self.token)
        
        # Configurar callback para receber comandos
        self.ws_client.on_filho_sync(self.on_websocket_message)

        def connect_thread():
            try:
                if self.ws_client.connect():
                    self.on_websocket_connect()
                else:
                    self.add_log("Falha na conexão WebSocket")
            except Exception as e:
                self.add_log(f"Erro na conexão: {e}")
        
        threading.Thread(target=connect_thread, daemon=True).start()

    def on_websocket_connect(self):
        self.is_connected = True
        self.root.after(0, lambda: self.status_label.config(text="Conexão: Conectado", foreground="green"))
        self.add_log("Conectado ao WebSocket!")
        
        # Enviar status online
        if self.ws_client.connected:
            self.ws_client.send_filho_status("online")
            self.add_log("Status online enviado")

    def on_websocket_message(self, data):
        """Recebe comando da mãe e executa tecla"""
        command = data.get('padrao') or data.get('pattern')
        if command:
            self.add_log(f"Comando recebido: {command}")
            self.root.after(0, lambda c=command: self.last_command_label.config(text=f"Último: {c}"))
            self.execute_command(command)
        else:
            self.add_log(f"Mensagem sem padrão: {data}")

    def execute_command(self, command):
        """Executa clique no botão flutuante correspondente"""
        button_mapping = {
            "1C": "f5_button",    # Amarelo → Botão F5
            "-1V": "f6_button",   # Verde → Botão F6  
            "-": "f11_button"     # Neutro → Botão F11
        }
        
        button_name = button_mapping.get(command)
        if button_name and hasattr(self, 'floating_buttons'):
            try:
                self.add_log(f"🎯 Comando recebido: {command}")
                
                # Encontrar o botão correspondente
                button_window = self.floating_buttons.get(button_name)
                if button_window and button_window.winfo_exists():
                    # Pegar posição do botão
                    x = button_window.winfo_x() + button_window.winfo_width() // 2
                    y = button_window.winfo_y() + button_window.winfo_height() // 2
                    
                    self.add_log(f"🖱️ Clicando no botão {command} em ({x}, {y})")
                    
                    # Clicar no botão
                    pyautogui.click(x, y)
                    
                    self.add_log(f"✅ Botão {command} clicado!")
                    
                else:
                    self.add_log(f"⚠️ Botão {command} não encontrado ou não visível")
                    
            except Exception as e:
                self.add_log(f"❌ ERRO ao clicar botão {command}: {e}")
        else:
            self.add_log(f"⚠️ Comando desconhecido: {command}")

    def create_floating_buttons(self):
        """Cria botões flutuantes para F5, F6 e F11"""
        try:
            self.add_log("🎯 Criando botões flutuantes...")
            
            # Posições iniciais (lado direito da tela)
            screen_width = self.root.winfo_screenwidth()
            positions = [
                (screen_width - 120, 100),   # F5
                (screen_width - 120, 160),   # F6  
                (screen_width - 120, 220),   # F11
            ]
            
            buttons_info = [
                ("f5_button", "F5\n(1C)", "#FFD700", positions[0]),   # Amarelo
                ("f6_button", "F6\n(-1V)", "#32CD32", positions[1]),  # Verde
                ("f11_button", "F11\n(-)", "#808080", positions[2]),  # Cinza
            ]
            
            for button_id, text, color, (x, y) in buttons_info:
                # Criar janela flutuante
                button_window = tk.Toplevel(self.root)
                button_window.title(f"Botão {text.split()[0]}")
                button_window.geometry(f"80x60+{x}+{y}")
                button_window.resizable(True, True)
                button_window.attributes('-topmost', True)
                button_window.attributes('-alpha', 0.9)
                
                # Botão dentro da janela
                button = tk.Button(button_window, 
                                 text=text,
                                 font=("Arial", 10, "bold"),
                                 bg=color,
                                 fg="black" if color != "#808080" else "white",
                                 command=lambda bid=button_id: self.click_floating_button(bid))
                button.pack(fill=tk.BOTH, expand=True)
                
                # Tornar arrastável
                self.make_draggable(button_window)
                
                # Armazenar referência
                self.floating_buttons[button_id] = button_window
                
                self.add_log(f"✅ Botão {text.split()[0]} criado em ({x}, {y})")
            
            self.add_log("🎉 Botões flutuantes criados!")
            self.add_log("📍 Posicione os botões onde quiser e teste!")
            
        except Exception as e:
            self.add_log(f"❌ Erro ao criar botões: {e}")

    def make_draggable(self, window):
        """Torna uma janela arrastável"""
        def start_drag(event):
            window.x = event.x
            window.y = event.y

        def drag_window(event):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")

        window.bind("<Button-1>", start_drag)
        window.bind("<B1-Motion>", drag_window)

    def click_floating_button(self, button_id):
        """Callback quando um botão flutuante é clicado"""
        button_names = {
            "f5_button": "1C (F5)",
            "f6_button": "-1V (F6)", 
            "f11_button": "- (F11)"
        }
        
        button_name = button_names.get(button_id, button_id)
        self.add_log(f"🖱️ Botão {button_name} clicado manualmente!")

    def create_floating_buttons(self):
        """Cria botões flutuantes para F5, F6 e F11"""
        try:
            self.add_log("🎯 Criando botões flutuantes...")
            
            # Posições iniciais (lado direito da tela)
            screen_width = self.root.winfo_screenwidth()
            positions = [
                (screen_width - 120, 100),   # F5
                (screen_width - 120, 160),   # F6  
                (screen_width - 120, 220),   # F11
            ]
            
            buttons_info = [
                ("f5_button", "F5\n(1C)", "#FFD700", positions[0]),   # Amarelo
                ("f6_button", "F6\n(-1V)", "#32CD32", positions[1]),  # Verde
                ("f11_button", "F11\n(-)", "#808080", positions[2]),  # Cinza
            ]
            
            for button_id, text, color, (x, y) in buttons_info:
                # Criar janela flutuante
                button_window = tk.Toplevel(self.root)
                button_window.title(f"Botão {text.split()[0]}")
                button_window.geometry(f"80x60+{x}+{y}")
                button_window.resizable(True, True)
                button_window.attributes('-topmost', True)
                button_window.attributes('-alpha', 0.9)
                
                # Botão dentro da janela
                button = tk.Button(button_window, 
                                 text=text,
                                 font=("Arial", 10, "bold"),
                                 bg=color,
                                 fg="black" if color != "#808080" else "white",
                                 command=lambda bid=button_id: self.click_floating_button(bid))
                button.pack(fill=tk.BOTH, expand=True)
                
                # Tornar arrastável
                self.make_draggable(button_window)
                
                # Armazenar referência
                self.floating_buttons[button_id] = button_window
                
                self.add_log(f"✅ Botão {text.split()[0]} criado em ({x}, {y})")
            
            self.add_log("🎉 Botões flutuantes criados!")
            self.add_log("📍 Posicione os botões onde quiser e teste!")
            
        except Exception as e:
            self.add_log(f"❌ Erro ao criar botões: {e}")

    def make_draggable(self, window):
        """Torna uma janela arrastável"""
        def start_drag(event):
            window.x = event.x
            window.y = event.y

        def drag_window(event):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")

        window.bind("<Button-1>", start_drag)
        window.bind("<B1-Motion>", drag_window)

    def click_floating_button(self, button_id):
        """Callback quando um botão flutuante é clicado"""
        button_names = {
            "f5_button": "1C (F5)",
            "f6_button": "-1V (F6)", 
            "f11_button": "- (F11)"
        }
        
        button_name = button_names.get(button_id, button_id)
        self.add_log(f"🖱️ Botão {button_name} clicado manualmente!")

    def on_closing(self):
        self.add_log("Fechando aplicativo...")
        
        # Fechar botões flutuantes
        for button_window in self.floating_buttons.values():
            try:
                if button_window.winfo_exists():
                    button_window.destroy()
            except:
                pass
        
        if self.ws_client:
            self.ws_client.disconnect()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

def main():
    print("🚀 OctavioSync - App Filho Simplificado")
    
    # Login
    login_window = LoginWindow()
    success, token, filho_id = login_window.run()
    
    if not success:
        print("❌ Login cancelado")
        return
    
    print(f"✅ Login bem-sucedido! Filho ID: {filho_id}")
    
    # Controle
    control_window = ControlWindow(token, filho_id)
    control_window.run()

if __name__ == "__main__":
    main()