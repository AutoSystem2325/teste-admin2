#!/usr/bin/env python3
"""
App Filho com Botões Flutuantes - Versão Completa e Funcional
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
        self.floating_buttons = {}
        
        self.root = tk.Tk()
        self.root.title("OctavioSync - Filho com Botões Flutuantes")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        self.center_window()
        self.setup_ui()
        self.setup_pyautogui()
        self.connect_websocket()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"450x400+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Controle com Botões Flutuantes", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Status Frame - Mais organizado
        status_frame = ttk.LabelFrame(main_frame, text="Status do Sistema", padding="8")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status da conexão
        conn_frame = ttk.Frame(status_frame)
        conn_frame.pack(fill=tk.X, pady=2)
        ttk.Label(conn_frame, text="Conexão:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.status_label = ttk.Label(conn_frame, text="Desconectado", 
                                     font=("Arial", 9), foreground="red")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Status da mãe
        mae_frame = ttk.Frame(status_frame)
        mae_frame.pack(fill=tk.X, pady=2)
        self.mae_status_label = ttk.Label(mae_frame, text="Aguardando mãe...", 
                                         font=("Arial", 9), foreground="gray")
        self.mae_status_label.pack(side=tk.LEFT)
        
        # Último comando
        cmd_frame = ttk.Frame(status_frame)
        cmd_frame.pack(fill=tk.X, pady=2)
        ttk.Label(cmd_frame, text="Último:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.last_command_label = ttk.Label(cmd_frame, text="Nenhum", font=("Arial", 9))
        self.last_command_label.pack(side=tk.LEFT, padx=(5, 0))

        # BOTÃO PRINCIPAL - CRIAR BOTÕES FLUTUANTES
        create_frame = ttk.LabelFrame(main_frame, text="Botões Flutuantes", padding="10")
        create_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(create_frame, text="🎯 CRIAR BOTÕES FLUTUANTES", 
                  command=self.create_floating_buttons,
                  style="Accent.TButton").pack(pady=5)
        
        ttk.Label(create_frame, text="Cria 3 marcadores invisíveis para posicionar sobre botões reais",
                 font=("Arial", 8), foreground="gray").pack()
        ttk.Label(create_frame, text="Posicione cada marcador SOBRE o botão que quer automatizar",
                 font=("Arial", 8), foreground="blue").pack()

        # Botões de teste
        test_frame = ttk.LabelFrame(main_frame, text="Testes Manuais", padding="10")
        test_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons_row1 = ttk.Frame(test_frame)
        buttons_row1.pack(pady=2)
        
        ttk.Button(buttons_row1, text="🟡 Teste 1C", 
                  command=lambda: self.execute_command("1C")).pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="🟢 Teste -1V", 
                  command=lambda: self.execute_command("-1V")).pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="⚫ Teste -", 
                  command=lambda: self.execute_command("-")).pack(side=tk.LEFT, padx=3)
        
        buttons_row2 = ttk.Frame(test_frame)
        buttons_row2.pack(pady=2)
        
        ttk.Button(buttons_row2, text="🧪 Teste PyAutoGUI", 
                  command=self.test_pyautogui).pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row2, text="📍 Mostrar Posições", 
                  command=self.show_button_positions).pack(side=tk.LEFT, padx=3)

        # Log
        ttk.Label(main_frame, text="Log de Atividades:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = tk.Text(main_frame, height=12, state='disabled', wrap='word',
                               bg='#f0f0f0', font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Info
        ttk.Label(main_frame, text="Mapeamento: 1C→F5🟡 | -1V→F6🟢 | -→F11⚫", 
                 font=("Arial", 8), foreground="blue").pack()

    def setup_pyautogui(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.add_log("🔧 PyAutoGUI configurado com failsafe")

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.root.after(0, lambda: self._insert_log(f"[{timestamp}] {message}\n"))

    def _insert_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def connect_websocket(self):
        self.add_log("🔌 Conectando ao WebSocket...")
        self.ws_client = OctavioSyncWebSocketClient(WEBSOCKET_URL, self.token)
        
        # Configurar callbacks
        self.ws_client.on_filho_sync(self.on_websocket_message)
        self.ws_client.on_mae_status_broadcast(self.on_mae_status_update)

        def connect_thread():
            try:
                if self.ws_client.connect():
                    self.on_websocket_connect()
                else:
                    self.add_log("❌ Falha na conexão WebSocket")
            except Exception as e:
                self.add_log(f"❌ Erro na conexão: {e}")
        
        threading.Thread(target=connect_thread, daemon=True).start()

    def on_websocket_connect(self):
        self.is_connected = True
        self.root.after(0, lambda: self.status_label.config(text="Conexão: Conectado ✅", foreground="green"))
        self.add_log("✅ Conectado ao WebSocket!")
        
        if self.ws_client.connected:
            self.ws_client.send_filho_status("online")
            self.add_log("📡 Status online enviado")

    def on_websocket_message(self, data):
        """Processa comandos da mãe"""
        command = data.get('padrao') or data.get('pattern')
        if command:
            self.add_log(f"📨 Comando da mãe: {command}")
            self.root.after(0, lambda c=command: self.last_command_label.config(text=c))
            self.execute_command(command)
        else:
            self.add_log(f"⚠️ Mensagem sem padrão: {data}")

    def on_mae_status_update(self, data):
        """Processa atualizações de status da mãe"""
        mae_status = data.get('mae_status')
        mae_nome = data.get('mae_nome', 'Mãe')
        
        if mae_status:
            if mae_status == "detecting":
                status_text = "ON ✅"
                status_color = "green"
            elif mae_status == "connected":
                status_text = "Conectada"
                status_color = "blue"
            else:
                status_text = "OFF"
                status_color = "red"
            
            # Atualizar label da mãe com nome e status
            mae_display = f"{mae_nome}: {status_text}"
            self.root.after(0, lambda: self.mae_status_label.config(text=mae_display, foreground=status_color))
            self.add_log(f"📊 {mae_nome} - Status: {mae_status}")

    def create_floating_buttons(self):
        """Cria botões pequenos EXATAMENTE como o quadrado da mãe"""
        try:
            self.add_log("🎯 Criando botões flutuantes estilo mãe...")
            
            # Fechar botões existentes
            for button_window in self.floating_buttons.values():
                try:
                    if button_window.winfo_exists():
                        button_window.destroy()
                except:
                    pass
            self.floating_buttons.clear()
            
            # Posições iniciais (lado direito da tela)
            screen_width = self.root.winfo_screenwidth()
            start_x = screen_width - 80
            
            buttons_config = [
                ("f5_button", "F5", "#FFD700", start_x, 100),    # Amarelo
                ("f6_button", "F6", "#32CD32", start_x, 140),    # Verde
                ("f11_button", "F11", "#808080", start_x, 180),  # Cinza
            ]
            
            for button_id, text, color, x, y in buttons_config:
                # Criar janela MUITO PEQUENA - MENOR QUE O QUADRADO DA MÃE
                button_window = tk.Toplevel(self.root)
                button_window.geometry(f"40x25+{x}+{y}")  # Bem pequeno
                button_window.resizable(True, True)  # Permitir redimensionamento
                
                # BOTÃO INVISÍVEL - SÓ PARA MARCAR POSIÇÃO
                button_window.overrideredirect(True)  # SEM decorações
                button_window.attributes('-topmost', True)  # Sempre no topo
                button_window.attributes('-alpha', 0.3)  # MUITO transparente
                button_window.configure(bg='black')  # Fundo preto
                
                # Canvas INVISÍVEL - SÓ MARCADOR DE POSIÇÃO
                canvas = tk.Canvas(button_window, 
                                  width=40, height=25,
                                  bg=color,  # Cor do botão (bem transparente)
                                  highlightthickness=1, 
                                  highlightbackground='red',  # Borda vermelha para ver
                                  bd=0)
                canvas.pack(fill=tk.BOTH, expand=True)
                
                # Texto pequeno para identificar
                canvas.create_text(20, 12, text=text, fill="white", 
                                  font=("Arial", 7, "bold"), tags="button_text")
                
                # Tornar arrastável IGUAL ao quadrado da mãe
                self.make_button_draggable(button_window, canvas)
                self.make_button_resizable(button_window)
                
                # Bind de clique
                canvas.bind("<Button-3>", lambda e, bid=button_id: self.manual_click_button(bid))  # Botão direito
                
                # Armazenar
                self.floating_buttons[button_id] = button_window
                
                self.add_log(f"✅ Botão {text} criado em ({x}, {y})")
            
            self.add_log("🎉 Marcadores invisíveis criados!")
            self.add_log("📍 POSICIONE cada marcador SOBRE o botão real do sistema!")
            self.add_log("🟡 F5 → Sobre botão de COMPRA")
            self.add_log("🟢 F6 → Sobre botão de VENDA") 
            self.add_log("⚫ F11 → Sobre botão de CANCELAR/NEUTRO")
            self.add_log("🎯 Quando a mãe enviar comando, clicará no botão real!")
            
        except Exception as e:
            self.add_log(f"❌ Erro ao criar botões: {e}")
            import traceback
            self.add_log(f"🔍 Detalhes: {traceback.format_exc()}")

    def make_button_draggable(self, window, canvas):
        """Torna o botão arrastável IGUAL ao quadrado da mãe"""
        def start_drag(event):
            window.x = event.x
            window.y = event.y
            window.attributes('-alpha', 0.95)  # Mais visível ao arrastar
            canvas.config(highlightbackground='#E74C3C')  # Vermelho ao arrastar
        
        def drag_window(event):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")
        
        def end_drag(event):
            window.attributes('-alpha', 0.9)  # Volta à transparência normal
            canvas.config(highlightbackground='white')  # Volta ao branco
            print(f"📍 Botão posicionado em: ({window.winfo_x()}, {window.winfo_y()})")
        
        def on_hover_enter(event):
            window.attributes('-alpha', 0.95)
            canvas.config(highlightbackground='#2ECC71', highlightthickness=3)  # Verde hover
        
        def on_hover_leave(event):
            window.attributes('-alpha', 0.9)
            canvas.config(highlightbackground='white', highlightthickness=2)  # Branco normal
        
        # Bind eventos IGUAIS ao quadrado da mãe
        canvas.bind("<Button-1>", start_drag)
        canvas.bind("<B1-Motion>", drag_window)
        canvas.bind("<ButtonRelease-1>", end_drag)
        canvas.bind("<Enter>", on_hover_enter)
        canvas.bind("<Leave>", on_hover_leave)
        
        # Também para a janela
        window.bind("<Button-1>", start_drag)
        window.bind("<B1-Motion>", drag_window)
        window.bind("<ButtonRelease-1>", end_drag)

    def make_button_resizable(self, window):
        """Adiciona funcionalidade de redimensionamento IGUAL ao quadrado da mãe"""
        def start_resize(event):
            window.start_x = event.x_root
            window.start_y = event.y_root
            window.start_width = window.winfo_width()
            window.start_height = window.winfo_height()
        
        def do_resize(event):
            width = max(40, window.start_width + (event.x_root - window.start_x))
            height = max(25, window.start_height + (event.y_root - window.start_y))
            window.geometry(f"{width}x{height}")
        
        # Área de redimensionamento no canto inferior direito
        resize_area = tk.Frame(window, bg='#3498DB', width=8, height=8)
        resize_area.place(relx=1.0, rely=1.0, anchor='se')
        resize_area.bind("<Button-1>", start_resize)
        resize_area.bind("<B1-Motion>", do_resize)

    def manual_click_button(self, button_id):
        """Clique manual no botão"""
        button_names = {
            "f5_button": "F5 (1C)",
            "f6_button": "F6 (-1V)", 
            "f11_button": "F11 (-)"
        }
        
        button_name = button_names.get(button_id, button_id)
        self.add_log(f"🖱️ Clique manual no botão {button_name}")

    def test_pyautogui(self):
        """Testa se o PyAutoGUI está funcionando"""
        try:
            self.add_log("🧪 TESTANDO PYAUTOGUI...")
            
            # Informações básicas
            pos = pyautogui.position()
            size = pyautogui.size()
            
            self.add_log(f"📍 Mouse atual: {pos}")
            self.add_log(f"📺 Tela: {size}")
            
            # Teste de movimento
            original_pos = pyautogui.position()
            test_x, test_y = 100, 100
            
            self.add_log(f"🔄 Movendo mouse para ({test_x}, {test_y})...")
            pyautogui.moveTo(test_x, test_y, duration=0.5)
            
            new_pos = pyautogui.position()
            self.add_log(f"📍 Nova posição: {new_pos}")
            
            # Voltar posição original
            pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.5)
            self.add_log(f"✅ PyAutoGUI funcionando corretamente!")
            
        except Exception as e:
            self.add_log(f"❌ Erro no PyAutoGUI: {e}")

    def show_button_positions(self):
        """Mostra as posições de todos os botões"""
        try:
            self.add_log("📍 POSIÇÕES DOS BOTÕES:")
            
            if not self.floating_buttons:
                self.add_log("⚠️ Nenhum botão criado ainda")
                return
            
            for button_id, button_window in self.floating_buttons.items():
                if button_window.winfo_exists():
                    x = button_window.winfo_x()
                    y = button_window.winfo_y()
                    w = button_window.winfo_width()
                    h = button_window.winfo_height()
                    center_x = x + w // 2
                    center_y = y + h // 2
                    
                    button_names = {
                        "f5_button": "F5 (1C)",
                        "f6_button": "F6 (-1V)", 
                        "f11_button": "F11 (-)"
                    }
                    
                    name = button_names.get(button_id, button_id)
                    self.add_log(f"  {name}: ({x}, {y}) {w}x{h} → Centro: ({center_x}, {center_y})")
                else:
                    self.add_log(f"  {button_id}: FECHADO")
                    
        except Exception as e:
            self.add_log(f"❌ Erro ao mostrar posições: {e}")

    def execute_command(self, command):
        """Executa comando clicando LITERALMENTE no botão correspondente"""
        button_mapping = {
            "1C": "f5_button",
            "-1V": "f6_button",
            "-": "f11_button"
        }
        
        button_id = button_mapping.get(command)
        if button_id and button_id in self.floating_buttons:
            try:
                button_window = self.floating_buttons[button_id]
                if button_window.winfo_exists():
                    # Pegar coordenadas EXATAS do centro do botão
                    btn_x = button_window.winfo_x()
                    btn_y = button_window.winfo_y()
                    btn_width = button_window.winfo_width()
                    btn_height = button_window.winfo_height()
                    
                    # Centro EXATO
                    click_x = btn_x + btn_width // 2
                    click_y = btn_y + btn_height // 2
                    
                    self.add_log(f"🎯 COMANDO DA MÃE: {command}")
                    self.add_log(f"📍 Botão em: ({btn_x}, {btn_y}) - {btn_width}x{btn_height}")
                    self.add_log(f"🖱️ CLICANDO EM: ({click_x}, {click_y})")
                    
                    # ESCONDER o botão temporariamente para não interferir
                    button_window.withdraw()
                    
                    # Pequena pausa
                    import time
                    time.sleep(0.05)
                    
                    # CLICAR NA POSIÇÃO (no botão real por baixo)
                    pyautogui.click(click_x, click_y)
                    
                    # MOSTRAR o botão novamente
                    button_window.deiconify()
                    
                    self.add_log(f"✅ CLIQUE EXECUTADO NA POSIÇÃO! Botão real acionado!")
                    
                    # Feedback visual - piscar a borda
                    try:
                        canvas = button_window.winfo_children()[0]
                        canvas.config(highlightbackground='lime', highlightthickness=3)
                        self.root.after(200, lambda: canvas.config(highlightbackground='red', highlightthickness=1))
                    except:
                        pass
                    
                else:
                    self.add_log(f"❌ Botão {command} não existe ou foi fechado")
            except Exception as e:
                self.add_log(f"❌ ERRO ao clicar botão {command}: {e}")
                import traceback
                self.add_log(f"🔍 Detalhes: {traceback.format_exc()}")
        else:
            if not self.floating_buttons:
                self.add_log(f"⚠️ CRIE OS BOTÕES FLUTUANTES PRIMEIRO!")
                self.add_log(f"💡 Clique em '🎯 CRIAR BOTÕES FLUTUANTES'")
            else:
                self.add_log(f"⚠️ Comando desconhecido: {command}")

    def on_closing(self):
        self.add_log("🔄 Fechando aplicativo...")
        
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
    print("🚀 OctavioSync - App Filho com Botões Flutuantes")
    
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