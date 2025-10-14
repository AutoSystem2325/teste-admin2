import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import threading
from datetime import datetime

# Adicionar o diretório shared ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from config import SERVER_URL, WEBSOCKET_URL, DETECTION_CONFIG, UI_CONFIG
from api_client import OctavioSyncAPIClient
from websocket_client import OctavioSyncWebSocketClient

# Tentar importar dependências para captura de tela
try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
    print("✅ PIL/Pillow disponível")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL/Pillow não instalado. Instale com: pip install Pillow")

# Tentar importar numpy para processamento otimizado
try:
    import numpy as np
    NUMPY_AVAILABLE = True
    print("✅ NumPy disponível - Detecção otimizada ativada")
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ NumPy não instalado. Instale com: pip install numpy (opcional, mas recomendado)")

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OctavioSync - Mãe Login")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        
        # Centralizar janela
        self.center_window()
        
        # Cliente API
        self.api_client = OctavioSyncAPIClient(SERVER_URL)
        
        # Setup UI
        self.setup_ui()
        
        # Resultado do login
        self.login_success = False
        self.user_token = None
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.root.winfo_screenheight() // 2) - (250 // 2)
        self.root.geometry(f"300x250+{x}+{y}")
    
    def setup_ui(self):
        """Configura a interface de login"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="OctavioSync - Mãe", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=25)
        self.email_entry.pack(pady=(0, 10))
        
        # Senha
        ttk.Label(main_frame, text="Senha:").pack(anchor=tk.W)
        self.senha_entry = ttk.Entry(main_frame, width=25, show="*")
        self.senha_entry.pack(pady=(0, 20))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack()
        
        ttk.Button(buttons_frame, text="Login", 
                  command=self.login).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Cadastrar", 
                  command=self.show_cadastro).pack(side=tk.LEFT)
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focar no email
        self.email_entry.focus()
    
    def login(self):
        """Realiza login"""
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha email e senha")
            return
        
        # Desabilitar botões durante login
        for widget in self.root.winfo_children():
            self.disable_widgets(widget)
        
        def login_thread():
            if self.api_client.login_mae(email, senha):
                self.user_token = self.api_client.get_token()
                self.login_success = True
                self.root.after(0, self.close_window)
            else:
                self.root.after(0, self.on_login_error)
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def disable_widgets(self, widget):
        """Desabilita widgets recursivamente"""
        try:
            widget.configure(state='disabled')
        except:
            pass
        for child in widget.winfo_children():
            self.disable_widgets(child)
    
    def enable_widgets(self, widget):
        """Habilita widgets recursivamente"""
        try:
            widget.configure(state='normal')
        except:
            pass
        for child in widget.winfo_children():
            self.enable_widgets(child)
    
    def on_login_error(self):
        """Callback para erro no login"""
        messagebox.showerror("Erro", "Email ou senha incorretos")
        # Reabilitar widgets
        for widget in self.root.winfo_children():
            self.enable_widgets(widget)
    
    def show_cadastro(self):
        """Mostra janela de cadastro"""
        CadastroWindow(self.root, self.api_client)
    
    def close_window(self):
        """Fecha a janela"""
        self.root.destroy()
    
    def run(self):
        """Executa a janela de login"""
        self.root.mainloop()
        return self.login_success, self.user_token

class CadastroWindow:
    def __init__(self, parent, api_client):
        self.api_client = api_client
        
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastrar Mãe")
        self.window.geometry("300x280")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.window.winfo_screenheight() // 2) - (280 // 2)
        self.window.geometry(f"300x280+{x}+{y}")
    
    def setup_ui(self):
        """Configura interface de cadastro"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Cadastrar Mãe", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Nome
        ttk.Label(main_frame, text="Nome:").pack(anchor=tk.W)
        self.nome_entry = ttk.Entry(main_frame, width=25)
        self.nome_entry.pack(pady=(0, 10))
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=25)
        self.email_entry.pack(pady=(0, 10))
        
        # Senha
        ttk.Label(main_frame, text="Senha:").pack(anchor=tk.W)
        self.senha_entry = ttk.Entry(main_frame, width=25, show="*")
        self.senha_entry.pack(pady=(0, 20))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack()
        
        ttk.Button(buttons_frame, text="Cadastrar", 
                  command=self.cadastrar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.window.destroy).pack(side=tk.LEFT)
        
        self.nome_entry.focus()
    
    def cadastrar(self):
        """Realiza cadastro"""
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not all([nome, email, senha]):
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        if len(senha) < 6:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres")
            return
        
        def cadastro_thread():
            if self.api_client.cadastrar_mae(nome, email, senha):
                self.window.after(0, self.on_success)
            else:
                self.window.after(0, self.on_error)
        
        threading.Thread(target=cadastro_thread, daemon=True).start()
    
    def on_success(self):
        """Callback sucesso"""
        messagebox.showinfo("Sucesso", "Mãe cadastrada com sucesso!")
        self.window.destroy()
    
    def on_error(self):
        """Callback erro"""
        messagebox.showerror("Erro", "Erro ao cadastrar. Verifique os dados.")

class CriarFilhoWindow:
    def __init__(self, parent, api_client):
        self.api_client = api_client
        
        self.window = tk.Toplevel(parent)
        self.window.title("Criar Filho")
        self.window.geometry("350x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"350x400+{x}+{y}")
    
    def setup_ui(self):
        """Configura interface de criar filho"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Criar Novo Filho", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Nome
        ttk.Label(main_frame, text="Nome:").pack(anchor=tk.W)
        self.nome_entry = ttk.Entry(main_frame, width=30)
        self.nome_entry.pack(pady=(0, 10))
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.pack(pady=(0, 10))
        
        # Senha
        ttk.Label(main_frame, text="Senha:").pack(anchor=tk.W)
        self.senha_entry = ttk.Entry(main_frame, width=30, show="*")
        self.senha_entry.pack(pady=(0, 10))
        
        # Validade
        ttk.Label(main_frame, text="Validade (YYYY-MM-DD):").pack(anchor=tk.W)
        self.validade_entry = ttk.Entry(main_frame, width=30)
        self.validade_entry.pack(pady=(0, 5))
        
        # Exemplo de validade
        from datetime import datetime, timedelta
        exemplo_data = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        ttk.Label(main_frame, text=f"Exemplo: {exemplo_data}", 
                 font=("Arial", 8), foreground="gray").pack(anchor=tk.W, pady=(0, 15))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack()
        
        ttk.Button(buttons_frame, text="Criar Filho", 
                  command=self.criar_filho).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.window.destroy).pack(side=tk.LEFT)
        
        self.nome_entry.focus()
    
    def criar_filho(self):
        """Cria o filho"""
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        validade = self.validade_entry.get().strip()
        
        if not all([nome, email, senha, validade]):
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        if len(senha) < 6:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres")
            return
        
        # Validar formato da data
        try:
            datetime.strptime(validade, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato YYYY-MM-DD")
            return
        
        def criar_thread():
            # Pegar ID da mãe logada
            mae_id = self.api_client.get_user_id()
            if not mae_id:
                self.window.after(0, lambda: messagebox.showerror("Erro", "Erro ao obter ID da mãe"))
                return
            
            # Criar filho
            if self.api_client.criar_filho(nome, email, senha, mae_id, validade):
                self.window.after(0, self.on_success)
            else:
                self.window.after(0, self.on_error)
        
        threading.Thread(target=criar_thread, daemon=True).start()
    
    def on_success(self):
        """Callback sucesso"""
        messagebox.showinfo("Sucesso", "Filho criado com sucesso!")
        self.window.destroy()
    
    def on_error(self):
        """Callback erro"""
        messagebox.showerror("Erro", "Erro ao criar filho. Verifique os dados.")

class ControlWindow:
    def __init__(self, token, api_client=None):
        self.token = token
        self.api_client = api_client
        self.ws_client = None
        self.is_on = False
        self.detection_thread = None
        self.detection_window = None
        self.base_brightness = None
        
        # Histórico para detecção de mudanças
        self.last_pattern = None
        self.pattern_stability_count = 0  # Contador de estabilidade
        self.stability_threshold = 2  # Precisa de 2 leituras iguais para enviar
        
        self.root = tk.Tk()
        self.root.title("OctavioSync - Controle")
        self.root.geometry("350x320")
        self.root.resizable(False, False)
        
        # Centralizar inicialmente
        self.center_window()
        
        self.setup_ui()
        
        # Conectar WebSocket
        self.connect_websocket()
        
        # Configurar fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centraliza a janela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.root.winfo_screenheight() // 2) - (320 // 2)
        self.root.geometry(f"350x320+{x}+{y}")
    
    def create_detection_square(self):
        """Cria o quadrado flutuante de detecção moderno"""
        if self.detection_window:
            self.detection_window.destroy()
        
        # Posicionar próximo à janela principal
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        
        # Posição inicial: ao lado direito da janela principal
        square_x = main_x + main_width + 20
        square_y = main_y + 50
        
        # Criar janela PEQUENA e PRECISA para detecção
        self.detection_window = tk.Toplevel(self.root)
        self.detection_window.geometry(f"30x20+{square_x}+{square_y}")  # Bem pequeno
        self.detection_window.resizable(True, True)  # Permitir redimensionamento
        
        # Remover decorações mas manter funcionalidade
        self.detection_window.overrideredirect(True)
        
        # Configurações visuais - TRANSPARENTE
        self.detection_window.attributes('-topmost', True)
        self.detection_window.attributes('-alpha', 0.3)  # Bem transparente
        self.detection_window.configure(bg='black')  # Fundo preto transparente
        
        # Canvas simples - vai desaparecer durante captura
        canvas = tk.Canvas(self.detection_window, 
                          width=30, height=20,
                          bg='red',  # Vermelho visível
                          highlightthickness=2, 
                          highlightbackground='white',
                          bd=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Texto indicador
        canvas.create_text(15, 10, text="◯", fill="white", 
                          font=("Arial", 10, "bold"), tags="indicator")
        
        # Tornar arrastável e redimensionável
        self.make_square_draggable(self.detection_window, canvas)
        self.make_square_resizable(self.detection_window)
        
        print("🎯 Quadrado de detecção criado - Posicione sobre o indicador desejado")
        return self.detection_window
    
    def make_square_resizable(self, window):
        """Adiciona funcionalidade de redimensionamento"""
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
        resize_area = tk.Frame(window, bg='#3498DB', width=10, height=10)
        resize_area.place(relx=1.0, rely=1.0, anchor='se')
        resize_area.bind("<Button-1>", start_resize)
        resize_area.bind("<B1-Motion>", do_resize)
    
    def test_detection(self):
        """TESTE COM SALVAMENTO - Vamos ver o que está sendo capturado"""
        if not self.detection_window:
            messagebox.showwarning("Aviso", "Primeiro clique em 'Mostrar Quadrado'")
            return
        
        try:
            x = self.detection_window.winfo_x()
            y = self.detection_window.winfo_y()
            width = self.detection_window.winfo_width()
            height = self.detection_window.winfo_height()
            
            print(f"🧪 CAPTURANDO: ({x}, {y}) - {width}x{height}")
            
            screenshot = self.capture_screen_region(x, y, width, height)
            
            if screenshot:
                # SALVAR A IMAGEM para você ver o que foi capturado
                screenshot.save("captura_teste.png")
                print("💾 Imagem salva como 'captura_teste.png'")
                
                # Analisar
                pattern, brightness, debug_info = self.analyze_screenshot(screenshot)
                
                # Pegar TODAS as cores únicas da imagem
                colors = []
                for x_px in range(width):
                    for y_px in range(height):
                        r, g, b = screenshot.getpixel((x_px, y_px))
                        colors.append((r, g, b))
                
                # Cores únicas (primeiras 10)
                unique_colors = list(set(colors))[:10]
                color_strings = [f"({r},{g},{b})" for r, g, b in unique_colors]
                
                result_msg = (
                    f"🎯 TESTE COM IMAGEM SALVA\n\n"
                    f"DETECTADO: {pattern}\n\n"
                    f"ANÁLISE: {debug_info}\n\n"
                    f"CORES ENCONTRADAS:\n" + 
                    "\n".join(color_strings) + "\n\n"
                    f"📁 Verifique o arquivo 'captura_teste.png'\n"
                    f"para ver exatamente o que foi capturado!"
                )
                
                messagebox.showinfo("Teste com Imagem", result_msg)
                
                print(f"✅ RESULTADO: {pattern}")
                print(f"📊 {debug_info}")
                print(f"🎨 Cores únicas: {len(unique_colors)}")
                print(f"🎨 Primeiras cores: {' | '.join(color_strings[:5])}")
                
            else:
                messagebox.showerror("Erro", "Falha na captura")
                
        except Exception as e:
            print(f"❌ ERRO: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
    
    def _get_color_samples(self, screenshot):
        """Pega amostras de cores específicas da imagem"""
        try:
            width, height = screenshot.size
            samples = []
            
            # Pegar amostras de diferentes pontos
            points = [
                (width//4, height//4),      # Canto superior esquerdo
                (3*width//4, height//4),    # Canto superior direito  
                (width//2, height//2),      # Centro
                (width//4, 3*height//4),    # Canto inferior esquerdo
                (3*width//4, 3*height//4),  # Canto inferior direito
            ]
            
            for i, (x, y) in enumerate(points):
                if x < width and y < height:
                    r, g, b = screenshot.getpixel((x, y))
                    samples.append(f"P{i+1}: ({r},{g},{b})")
            
            return " | ".join(samples)
        except:
            return "N/A"
    

    
    def _get_average_color(self, screenshot):
        """Calcula cor média da imagem"""
        try:
            if NUMPY_AVAILABLE:
                import numpy as np
                img_array = np.array(screenshot)
                avg_color = np.mean(img_array, axis=(0, 1))
                return f"({avg_color[0]:.0f}, {avg_color[1]:.0f}, {avg_color[2]:.0f})"
            else:
                # Fallback sem numpy
                width, height = screenshot.size
                r_sum = g_sum = b_sum = 0
                pixel_count = 0
                
                for x in range(0, width, max(1, width//10)):
                    for y in range(0, height, max(1, height//10)):
                        r, g, b = screenshot.getpixel((x, y))
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        pixel_count += 1
                
                if pixel_count > 0:
                    return f"({r_sum//pixel_count}, {g_sum//pixel_count}, {b_sum//pixel_count})"
                return "(0, 0, 0)"
        except:
            return "N/A"
    
    def _get_dominant_color(self, screenshot):
        """Identifica cor dominante"""
        try:
            # Análise simples baseada nos padrões configurados
            pattern, _, _ = self.analyze_screenshot(screenshot)
            
            color_map = {
                "1C": "Amarelo/Dourado",
                "-1V": "Verde", 
                "-": "Escuro/Neutro"
            }
            
            return color_map.get(pattern, "Indefinida")
        except:
            return "N/A"
    
    def calibrate_detection(self):
        """Calibra a detecção"""
        if not self.detection_window:
            messagebox.showwarning("Aviso", "Primeiro crie o quadrado de detecção")
            return
        
        try:
            x = self.detection_window.winfo_x()
            y = self.detection_window.winfo_y()
            width = self.detection_window.winfo_width()
            height = self.detection_window.winfo_height()
            
            screenshot = self.capture_screen_region(x, y, width, height)
            
            if screenshot:
                pattern, brightness, color_info = self.analyze_screenshot(screenshot)
                self.base_brightness = brightness
                
                messagebox.showinfo("Calibração", 
                    f"Calibração concluída!\n"
                    f"Brilho base: {brightness:.1f}\n"
                    f"Padrão: {pattern}\n"
                    f"Cor: {color_info}")
                
                print(f"CALIB: Base brightness={brightness:.1f}, Pattern={pattern}")
            else:
                messagebox.showerror("Erro", "Não foi possível capturar")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na calibração: {e}")
    
    def setup_ui(self):
        """Configura interface de controle"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Detector Visual", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Status Frame - Mais organizado
        status_frame = ttk.LabelFrame(main_frame, text="Status da Detecção", padding="8")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status principal
        main_status_frame = ttk.Frame(status_frame)
        main_status_frame.pack(fill=tk.X, pady=2)
        ttk.Label(main_status_frame, text="Status:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.status_label = ttk.Label(main_status_frame, text="OFF", 
                                     font=("Arial", 9), foreground="red")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Padrão detectado
        pattern_frame = ttk.Frame(status_frame)
        pattern_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pattern_frame, text="Padrão:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.pattern_label = ttk.Label(pattern_frame, text="-", font=("Arial", 9))
        self.pattern_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Debug info
        debug_frame = ttk.Frame(status_frame)
        debug_frame.pack(fill=tk.X, pady=2)
        self.debug_label = ttk.Label(debug_frame, text="Brilho: - | Leituras: 0", 
                                    font=("Arial", 8), foreground="gray")
        self.debug_label.pack()
        
        # Controles Frame - Simplificado
        controls_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botão mostrar quadrado
        ttk.Button(controls_frame, text="📍 Mostrar Quadrado", 
                  command=self.create_detection_square).pack(pady=(0, 8))
        
        # Botão criar filho
        ttk.Button(controls_frame, text="👶 Criar Filho", 
                  command=self.show_criar_filho).pack(pady=(0, 8))
        
        # Botão principal - maior e destacado
        self.toggle_button = ttk.Button(controls_frame, text="🚀 INICIAR DETECÇÃO", 
                                       command=self.toggle_status)
        self.toggle_button.pack()
        
        # Instruções simplificadas
        ttk.Label(main_frame, text="1. Mostrar Quadrado → 2. Posicionar → 3. INICIAR", 
                 font=("Arial", 8), foreground="gray").pack(pady=(5, 0))
        
        # Status de tempo real
        self.realtime_label = ttk.Label(main_frame, text="⚡ DETECÇÃO EM TEMPO REAL", 
                                       font=("Arial", 8, "bold"), foreground="orange")
        self.realtime_label.pack()
    
    def make_square_draggable(self, window, canvas):
        """Torna o quadrado arrastável com feedback visual"""
        def start_drag(event):
            window.x = event.x
            window.y = event.y
            window.attributes('-alpha', 0.9)
            canvas.config(highlightbackground='#E74C3C')  # Vermelho ao arrastar
        
        def drag_window(event):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")
        
        def end_drag(event):
            window.attributes('-alpha', 0.8)
            canvas.config(highlightbackground='#3498DB')  # Volta ao azul
            print(f"📍 Quadrado posicionado em: ({window.winfo_x()}, {window.winfo_y()})")
        
        def on_hover_enter(event):
            if not hasattr(window, 'dragging'):
                window.attributes('-alpha', 0.95)
                canvas.config(highlightbackground='#2ECC71', highlightthickness=3)  # Verde hover
        
        def on_hover_leave(event):
            if not hasattr(window, 'dragging'):
                window.attributes('-alpha', 0.8)
                canvas.config(highlightbackground='#3498DB', highlightthickness=2)  # Azul normal
        
        # Bind eventos
        canvas.bind("<Button-1>", start_drag)
        canvas.bind("<B1-Motion>", drag_window)
        canvas.bind("<ButtonRelease-1>", end_drag)
        canvas.bind("<Enter>", on_hover_enter)
        canvas.bind("<Leave>", on_hover_leave)
        
        # Também para a janela
        window.bind("<Button-1>", start_drag)
        window.bind("<B1-Motion>", drag_window)
        window.bind("<ButtonRelease-1>", end_drag)
    
    def connect_websocket(self):
        """Conecta ao WebSocket"""
        self.ws_client = OctavioSyncWebSocketClient(WEBSOCKET_URL, self.token)
        
        def connect_thread():
            if self.ws_client.connect():
                # Enviar informações da mãe quando conectar
                self.broadcast_mae_status("connected")
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def toggle_status(self):
        """Alterna status ON/OFF e notifica filhos"""
        self.is_on = not self.is_on
        
        if self.is_on:
            self.status_label.config(text="ON ✅", foreground="green")
            self.toggle_button.config(text="⏹️ PARAR DETECÇÃO")
            self.start_detection()
            # Notificar filhos que a mãe está ON
            self.broadcast_mae_status("detecting")
        else:
            self.status_label.config(text="OFF", foreground="red")
            self.toggle_button.config(text="🚀 INICIAR DETECÇÃO")
            self.pattern_label.config(text="-")
            self.debug_label.config(text="Brilho: - | Leituras: 0")
            self.stop_detection()
            # Notificar filhos que a mãe está OFF
            self.broadcast_mae_status("stopped")

    def broadcast_mae_status(self, status):
        """Envia status da mãe para todos os filhos"""
        try:
            if self.ws_client and hasattr(self.ws_client, 'sio'):
                # Pegar nome da mãe do API client
                mae_nome = "Mãe"  # Default
                if hasattr(self, 'api_client') and self.api_client.user_info:
                    mae_nome = self.api_client.user_info.get('nome', 'Mãe')
                
                broadcast_data = {
                    'mae_status': status,
                    'mae_nome': mae_nome
                }
                
                self.ws_client.sio.emit('mae_status_broadcast', broadcast_data)
                print(f"📡 Status da mãe enviado: {status} ({mae_nome})")
        except Exception as e:
            print(f"❌ Erro ao enviar status da mãe: {e}")
    
    def capture_screen_region(self, x, y, width, height):
        """Captura região SEM interferência do quadrado"""
        if not PIL_AVAILABLE:
            print("Erro: PIL/Pillow não disponível")
            return None
        
        try:
            # ESCONDER o quadrado temporariamente
            if self.detection_window:
                self.detection_window.withdraw()  # Esconde a janela
            
            # Pequena pausa para garantir que sumiu
            import time
            time.sleep(0.05)  # 50ms
            
            # CAPTURAR a região sem o quadrado
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            # MOSTRAR o quadrado novamente
            if self.detection_window:
                self.detection_window.deiconify()  # Mostra a janela
            
            return screenshot
            
        except Exception as e:
            print(f"Erro ao capturar tela: {e}")
            # Garantir que o quadrado volta mesmo se der erro
            if self.detection_window:
                try:
                    self.detection_window.deiconify()
                except:
                    pass
            return None
    
    def analyze_screenshot(self, screenshot):
        """
        ABORDAGEM EXTREMAMENTE SIMPLES
        Apenas verifica se é claro, escuro, ou colorido
        """
        try:
            width, height = screenshot.size
            
            if width == 0 or height == 0:
                return "-", 0, "EMPTY"
            
            # Contar pixels por faixa de brilho
            muito_escuro = 0    # < 50
            escuro = 0          # 50-100  
            medio = 0           # 100-150
            claro = 0           # 150-200
            muito_claro = 0     # > 200
            
            total_r = total_g = total_b = 0
            total_pixels = width * height
            
            for x in range(width):
                for y in range(height):
                    r, g, b = screenshot.getpixel((x, y))
                    
                    total_r += r
                    total_g += g  
                    total_b += b
                    
                    brilho = (r + g + b) / 3
                    
                    if brilho < 50:
                        muito_escuro += 1
                    elif brilho < 100:
                        escuro += 1
                    elif brilho < 150:
                        medio += 1
                    elif brilho < 200:
                        claro += 1
                    else:
                        muito_claro += 1
            
            # Médias RGB
            avg_r = total_r / total_pixels
            avg_g = total_g / total_pixels
            avg_b = total_b / total_pixels
            avg_brilho = (avg_r + avg_g + avg_b) / 3
            
            # DETECÇÃO MELHORADA - Procurar pixels específicos
            detected = "-"
            
            # Contar pixels amarelos e verdes com critérios REAIS
            pixels_amarelos = 0
            pixels_verdes = 0
            
            # Reprocessar com critérios baseados nas cores capturadas
            for x in range(width):
                for y in range(height):
                    r, g, b = screenshot.getpixel((x, y))
                    
                    # VERDE - Critério MUITO específico baseado na cor real (189,255,255)
                    if (g >= 240 and b >= 240 and g > r and b > r and r < 200):  # Verde cyan brilhante específico
                        pixels_verdes += 1
                    # AMARELO - Critério original que funcionava
                    elif r >= 150 and g >= 150 and b < 200 and (r + g) > (b * 2):
                        pixels_amarelos += 1
            
            # Detecção com PRIORIDADE para verde (mais específico)
            if pixels_verdes > 0:
                detected = "-1V"  # PRIORIDADE: Verde primeiro
            elif pixels_amarelos > 0:
                detected = "1C"  # Depois amarelo
            elif (muito_escuro + escuro) > (total_pixels * 0.6):  # 60% escuro
                detected = "-"
            
            # Debug info
            pct_claro = ((claro + muito_claro) / total_pixels) * 100
            pct_escuro = ((muito_escuro + escuro) / total_pixels) * 100
            
            # Info sobre pixels coloridos encontrados
            pct_amarelo = (pixels_amarelos / total_pixels) * 100
            pct_verde = (pixels_verdes / total_pixels) * 100
            
            debug_info = f"Claro:{pct_claro:.1f}% RGB:({avg_r:.0f},{avg_g:.0f},{avg_b:.0f}) Amarelo:{pixels_amarelos}px({pct_amarelo:.2f}%) Verde:{pixels_verdes}px({pct_verde:.2f}%)"
            
            return detected, avg_brilho, debug_info
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            return "-", 0, "ERROR"
                    
        except Exception as e:
            print(f"ERRO na análise: {e}")
            return "-", 0, "ERROR"
    

    
    def _analyze_screenshot_fallback(self, screenshot):
        """Análise fallback sem numpy"""
        try:
            width, height = screenshot.size
            total_pixels = width * height
            
            if total_pixels == 0:
                return "-", 0, "EMPTY"
            
            # Amostragem para performance
            step = max(1, min(width, height) // 15)
            pattern_counts = {config["name"]: 0 for config in DETECTION_CONFIG.values()}
            sampled_pixels = 0
            brightness_sum = 0
            
            for x in range(0, width, step):
                for y in range(0, height, step):
                    if x < width and y < height:
                        r, g, b = screenshot.getpixel((x, y))
                        brightness_sum += (r + g + b) / 3
                        sampled_pixels += 1
                        
                        # Verificar cada padrão
                        for config in DETECTION_CONFIG.values():
                            min_r, min_g, min_b = config["color_min_rgb"]
                            max_r, max_g, max_b = config["color_max_rgb"]
                            
                            if (min_r <= r <= max_r and 
                                min_g <= g <= max_g and 
                                min_b <= b <= max_b):
                                pattern_counts[config["name"]] += 1
                                break
            
            # Calcular percentuais
            pattern_percentages = {}
            for name, count in pattern_counts.items():
                pattern_percentages[name] = (count / sampled_pixels) * 100 if sampled_pixels > 0 else 0
            
            # Detectar padrão com prioridade
            detected_pattern = "-"
            max_confidence = 0
            
            for pattern_name in ["1C", "-1V", "-"]:
                if pattern_name in pattern_percentages:
                    percentage = pattern_percentages[pattern_name]
                    threshold = next((config["threshold_pct"] for config in DETECTION_CONFIG.values() 
                                    if config["name"] == pattern_name), 10.0)
                    
                    if percentage >= threshold and percentage > max_confidence:
                        detected_pattern = pattern_name
                        max_confidence = percentage
                        break
            
            brightness = brightness_sum / sampled_pixels if sampled_pixels > 0 else 0
            color_info = " | ".join([f"{name}:{pct:.1f}%" for name, pct in pattern_percentages.items()])
            
            return detected_pattern, brightness, color_info
            
        except Exception as e:
            print(f"Erro no fallback: {e}")
            return "-", 0, "ERROR"
    
    def start_detection(self):
        """DETECÇÃO FUNCIONAL EM TEMPO REAL"""
        if not self.detection_window:
            messagebox.showwarning("Aviso", "Crie o quadrado primeiro")
            return
        
        if not PIL_AVAILABLE:
            messagebox.showerror("Erro", "PIL/Pillow não instalado")
            self.is_on = False
            return
        
        print("🚀 INICIANDO DETECÇÃO FUNCIONAL")
        
        def detection_loop():
            import time
            
            reading_count = 0
            last_sent_pattern = None
            
            try:
                while self.is_on and self.detection_window:
                    try:
                        # Capturar região do quadrado
                        x = self.detection_window.winfo_x()
                        y = self.detection_window.winfo_y()
                        width = self.detection_window.winfo_width()
                        height = self.detection_window.winfo_height()
                        
                        # Capturar e analisar
                        screenshot = self.capture_screen_region(x, y, width, height)
                        
                        if screenshot:
                            current_pattern, brightness, debug_info = self.analyze_screenshot(screenshot)
                            reading_count += 1
                            
                            # Atualizar display a cada 2 leituras
                            if reading_count % 2 == 0:
                                self.root.after(0, lambda p=current_pattern, b=brightness, c=reading_count: 
                                               self.update_display_simple(p, b, c))
                            
                            # ENVIAR QUANDO MUDAR
                            if current_pattern != last_sent_pattern:
                                self.send_pattern(current_pattern)
                                last_sent_pattern = current_pattern
                                print(f"📤 ENVIADO: {current_pattern} | Leitura #{reading_count}")
                                print(f"📊 Debug: {debug_info}")
                        
                        # Intervalo de 200ms (5 FPS)
                        time.sleep(0.2)
                        
                    except Exception as e:
                        print(f"❌ Erro na leitura: {e}")
                        time.sleep(0.5)
                        
            except Exception as e:
                print(f"💥 Erro crítico na detecção: {e}")
        
        # Iniciar thread de detecção
        self.detection_thread = threading.Thread(target=detection_loop, daemon=True)
        self.detection_thread.start()
    
    def update_display_simple(self, pattern, brightness, reading_count):
        """Atualização simples do display"""
        try:
            # Cores para os padrões
            colors = {"1C": "#FFD700", "-1V": "#32CD32", "-": "#808080"}
            color = colors.get(pattern, "#FFFFFF")
            
            self.pattern_label.config(text=f"Padrão: {pattern}", foreground=color)
            self.debug_label.config(text=f"Brilho: {brightness:.1f} | Leituras: {reading_count}")
            
            # Atualizar indicador no quadrado
            if self.detection_window:
                try:
                    canvas = self.detection_window.winfo_children()[0]
                    canvas.delete("indicator")
                    canvas.create_text(15, 10, text=pattern, fill="white", 
                                     font=("Arial", 6, "bold"), tags="indicator")
                except:
                    pass
        except Exception as e:
            print(f"Erro no display: {e}")
    
    def send_pattern(self, pattern: str):
        """Envia padrão detectado"""
        if not self.is_on:
            return
        
        if self.ws_client and self.ws_client.is_connected():
            self.ws_client.send_mae_update(pattern)
            print(f"Padrão enviado: {pattern}")
        else:
            print("WebSocket não conectado")
    
    def update_display(self, pattern, brightness, reading_count):
        """Atualiza display"""
        self.pattern_label.config(text=f"Padrão: {pattern}")
        self.debug_label.config(text=f"Brilho: {brightness:.1f} | Leituras: {reading_count}")
    
    def update_display_enhanced(self, pattern, brightness, reading_count, color_info):
        """Atualiza display com informações detalhadas"""
        # Cor do padrão
        color_map = {"1C": "#FFD700", "-1V": "#32CD32", "-": "#808080"}
        pattern_color = color_map.get(pattern, "#FFFFFF")
        
        self.pattern_label.config(text=f"Padrão: {pattern}", foreground=pattern_color)
        self.debug_label.config(text=f"Brilho: {brightness:.1f} | Leituras: {reading_count}")
        
        # Atualizar indicador visual no quadrado
        if self.detection_window:
            try:
                canvas = self.detection_window.winfo_children()[0]
                canvas.delete("indicator")
                
                # Indicador baseado no padrão
                if pattern == "1C":
                    canvas.create_text(20, 12, text="1C", fill="#FFD700", 
                                     font=("Arial", 8, "bold"), tags="indicator")
                elif pattern == "-1V":
                    canvas.create_text(20, 12, text="-1V", fill="#32CD32", 
                                     font=("Arial", 7, "bold"), tags="indicator")
                else:
                    canvas.create_text(20, 12, text="-", fill="#808080", 
                                     font=("Arial", 10, "bold"), tags="indicator")
            except:
                pass
    
    def stop_detection(self):
        """Para detecção"""
        print("Detecção parada")
        self.last_pattern = None
        self.pattern_stability_count = 0
    
    def show_criar_filho(self):
        """Mostra janela para criar filho"""
        CriarFilhoWindow(self.root, self.api_client)
    
    def on_closing(self):
        """Callback fechamento"""
        self.is_on = False
        if self.detection_window:
            self.detection_window.destroy()
        if self.ws_client:
            self.ws_client.disconnect()
        self.root.destroy()
    
    def run(self):
        """Executa janela de controle"""
        self.root.mainloop()

class AppMae:
    def __init__(self):
        pass
    
    def run(self):
        """Executa o fluxo completo"""
        login_window = LoginWindow()
        success, token = login_window.run()
        
        if not success:
            return
        
        # Passar o api_client para ter acesso às informações da mãe
        control_window = ControlWindow(token, login_window.api_client)
        control_window.run()

def main():
    """Função principal"""
    app = AppMae()
    app.run()

if __name__ == "__main__":
    main() 

