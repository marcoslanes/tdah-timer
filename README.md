# 🛡️ TDAH-TIMER

**Shield Timer** é uma ferramenta leve e intuitiva desenvolvida para auxiliar na triagem de tarefas, permitindo o monitoramento preciso do tempo gasto em cada atendimento (**MTTR - Mean Time To Respond**).

## 🚀 Funcionalidades

* **Monitoramento Múltiplo:** Adicione quantas terefas precisar.
* **Controle Individual:** Botões de Play, Pause e Stop independentes por registro.
* **Feedback Visual:** Sistema de cores e "blinking" para chamados pausados e finalizados.
* **Exportação Segura:** Geração de relatórios em CSV com sanitização contra injeção de fórmulas.
* **Segurança de Operação:** Janelas de confirmação para exclusão de registros ou limpeza de tela.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Interface:** CustomTkinter (Modern UI)
* **Build:** PyInstaller (Empacotado em .exe único)

## 📦 Como usar o Executável

1. Vá até a aba [Releases](https://github.com/marcoslanes/tdah-timer/releases).
2. Baixe o arquivo `tdah-timer.exe`.
3. Execute no Windows (não requer instalação).

## 🧑‍💻 Instalação para Desenvolvedores

Se desejar rodar o código fonte:

```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/shield-timer.git](https://github.com/seu-usuario/shield-timer.git)

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install customtkinter