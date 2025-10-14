# 🎯 OctavioSync - Mini App Mãe

Detector visual moderno e eficiente para padrões **1C**, **-1V** e **-** (neutro).

## ✨ Características

- **Detecção Visual Inteligente**: Reconhece padrões por cor RGB
- **Interface Moderna**: Quadrado flutuante arrastável e redimensionável  
- **Performance Otimizada**: Usa NumPy quando disponível para análise rápida
- **Estabilidade**: Sistema anti-ruído com confirmação de padrões
- **Feedback Visual**: Indicadores coloridos em tempo real

## 🚀 Como Usar

### 1. Preparação
```bash
# Instalar dependências obrigatórias
pip install Pillow

# Instalar dependências opcionais (recomendado)
pip install numpy
```

### 2. Execução
```bash
python app_mae.py
```

### 3. Fluxo de Uso
1. **Login**: Faça login com suas credenciais de mãe
2. **Mostrar Quadrado**: Clique para criar o detector visual
3. **Posicionar**: Arraste o quadrado sobre o indicador desejado (1C ou -1V)
4. **Redimensionar**: Ajuste o tamanho conforme necessário
5. **Calibrar**: Clique para definir o ponto de referência
6. **Testar**: Verifique se a detecção está funcionando
7. **Iniciar**: Ative a detecção automática

## 🎨 Padrões Detectados

| Padrão | Cor | Descrição | Threshold |
|--------|-----|-----------|-----------|
| **1C** | 🟡 Amarelo/Dourado | RGB: (180,140,0) - (255,255,100) | 15% |
| **-1V** | 🟢 Verde | RGB: (0,120,0) - (100,255,100) | 15% |
| **-** | ⚫ Escuro/Neutro | RGB: (0,0,0) - (80,80,80) | 50% |

## 🔧 Configurações

As configurações estão em `../shared/config.py`:

```python
DETECTION_CONFIG = {
    "pattern_1c": {
        "name": "1C",
        "color_min_rgb": (180, 140, 0),    # Amarelo escuro
        "color_max_rgb": (255, 255, 100),  # Amarelo claro
        "threshold_pct": 15.0,             # 15% da área
    },
    # ... outros padrões
}
```

## 🎮 Controles do Quadrado

- **Arrastar**: Clique e arraste para mover
- **Redimensionar**: Use a área azul no canto inferior direito
- **Feedback Visual**:
  - 🔵 Azul: Normal
  - 🟢 Verde: Hover
  - 🔴 Vermelho: Arrastando
  - 🟡 Amarelo: Detectando 1C
  - 🟢 Verde: Detectando -1V

## 📊 Indicadores de Status

- **Status**: ON/OFF da detecção
- **Padrão**: Último padrão detectado (com cor)
- **Brilho**: Luminosidade média da região
- **Leituras**: Contador de análises realizadas

## 🔍 Teste e Debug

Execute o teste de configuração:
```bash
python test_detection.py
```

Use a função "Testar Detecção" para análise detalhada:
- Cor média RGB
- Cor dominante
- Distribuição de padrões
- Posição e tamanho da região

## ⚡ Performance

- **Intervalo de Detecção**: 300ms (3.3 FPS)
- **Amostragem Inteligente**: Reduz processamento mantendo precisão
- **NumPy**: Acelera análise em ~5x quando disponível
- **Anti-Ruído**: Requer 2 leituras consecutivas para confirmar mudança

## 🐛 Solução de Problemas

### Detecção não funciona
- Verifique se PIL/Pillow está instalado
- Posicione o quadrado exatamente sobre o indicador
- Ajuste o tamanho do quadrado (maior = mais estável)
- Use "Calibrar" antes de iniciar

### Performance lenta
- Instale NumPy: `pip install numpy`
- Reduza o tamanho do quadrado de detecção
- Feche outros programas pesados

### Padrões incorretos
- Ajuste as configurações RGB em `config.py`
- Modifique os thresholds de porcentagem
- Use "Testar Detecção" para análise

## 📝 Logs

O app exibe logs no console:
- 🚀 Início da detecção
- 📊 Mudanças de padrão
- ✅ Padrões enviados
- 📍 Posicionamento do quadrado
- ❌ Erros e avisos

---

**Desenvolvido para OctavioSync** - Detecção visual moderna e eficiente! 🎯