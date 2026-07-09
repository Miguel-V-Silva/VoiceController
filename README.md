# 🎙️ VoiceController

Controle seu computador usando comandos de voz de forma simples e totalmente offline.

O **VoiceController** utiliza o **Vosk** para reconhecimento de fala e executa ações no Windows, como controlar o volume, pressionar teclas e fechar programas.

## ✨ Funcionalidades

* 🔊 Aumentar e diminuir o volume
* ⏯️ Pressionar **Espaço** (pausar/reproduzir)
* ⌨️ Pressionar **Enter**
* ❌ Fechar a janela atual (`Alt + F4`)
* 🖥️ Desligar o computador
* 🚀 Fácil de adicionar novos comandos

## 📦 Instalação

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd VoiceController
```

Instale as dependências:

```bash
pip install vosk sounddevice pyautogui keyboard
```

Ou instale individualmente:

* `vosk`
* `sounddevice`
* `pyautogui`
* `keyboard`

## 🎤 Modelo do Vosk

Além das bibliotecas, é necessário baixar um modelo de reconhecimento de voz em português.

Você pode encontrar os modelos oficiais em:

https://alphacephei.com/vosk/models

Após baixar, extraia a pasta do modelo para o diretório do projeto e ajuste o caminho no código, caso necessário.

## ▶️ Executando

```bash
python teste.py
```

Quando aparecer a mensagem indicando que o programa está ouvindo, basta falar um dos comandos suportados.

## 🛠️ Tecnologias

* Python
* Vosk
* SoundDevice
* PyAutoGUI
* Keyboard

## 📄 Licença

Este projeto é de código aberto e pode ser utilizado livremente para estudos e projetos pessoais.
