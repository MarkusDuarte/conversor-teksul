from tkinter import filedialog, messagebox, Tk,ttk
from tkinter.filedialog import askopenfilename
import pandas  as pd
import tkinter as tk
import os
import subprocess
import sqlite3

#Função do botão de carregamento

def loading_screen():
    # Configurar janela de carregamento
    load_window = tk.Tk()
    load_window.title("Carregando...")
    
    # Centralizar janela
    load_window.geometry("300x100+" + 
        str((load_window.winfo_screenwidth() // 2) - 150) + "+" + 
        str((load_window.winfo_screenheight() // 2) - 50))
    
    # Adicionar elementos
    ttk.Label(load_window, text="Por favor aguarde...").pack(pady=10)
    progress = ttk.Progressbar(load_window, mode='indeterminate')
    progress.pack()
    progress.start(10)  # Barra de progresso animada

    # Fechar após 2.5 segundos e abrir programa principal
    load_window.after(2500, lambda: [load_window.destroy(), janela()])
    load_window.mainloop()


# Antes de fechar o programa, certifique-se de encerrá-lo
database_file = ".db"

conn = sqlite3.connect(database_file)

#Listar tabelas no banco de dados (opcional, para identificar o que há no arquivo)

query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)
print("Tabelas no banco de dados:")
print(tables)

# Substitua 'sua_tabela' pelo nome da tabela que você quer carregar
table_name = "sqlite_master"
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

# Exibir as primeiras linhas da tabela
print(df.head())

# Função para selecionar e aplicar o log no arquivo

def fechar_programa():
    janela.destroy()
    os._exit(0)  # Força o encerramento do programa

def criar_e_executar_bat():
    # Ocultar a janela principal do tkinter
    janela = Tk()
    janela.withdraw()
    
    # Abrir o diálogo para selecionar uma pasta
    pasta_selecionada = filedialog.askdirectory(
        title="Selecione a pasta onde o arquivo .bat será criado"
    )
    if not pasta_selecionada:  # Se nenhuma pasta for selecionada
        print("Nenhuma pasta selecionada. Operação cancelada.")
        return

    try:
        # Caminho do arquivo .bat na pasta selecionada
        caminho_do_bat = os.path.join(pasta_selecionada, "executar_contabil.bat")
        
        # Conteúdo do arquivo .bat
        conteudo_bat = """@echo off
@echo off
:inicio
cd /d %~dp0

:: Executa o comando principal
if exist contabil.db (
    dbeng17.exe contabil.db -a contabil.log
) else (
    dbeng17.exe srvcontabil.db -a contabil.log
)

:: Remover o atributo "Somente Leitura" de contabil.log
if exist contabil.log (
    attrib -r contabil.log
)

::fechar o bat

exit
"""
        # Criar o arquivo .bat na pasta selecionada
        with open(caminho_do_bat, "w") as bat_file:
            bat_file.write(conteudo_bat)
        print(f"Arquivo .bat criado em: {caminho_do_bat}")

        # Executar o arquivo .bat em uma nova janela
        subprocess.Popen(f'start cmd /k "{caminho_do_bat}"', shell=True)
        print("Arquivo .bat executado com sucesso.")

        # Remover o atributo "Somente Leitura" de todos os arquivos na pasta
        for arquivo in os.listdir(pasta_selecionada):
            caminho_arquivo = os.path.join(pasta_selecionada, arquivo)
            if os.path.isfile(caminho_arquivo):  # Garantir que seja um arquivo
                os.chmod(caminho_arquivo, 0o666)  # Alterar permissões para leitura e escrita
        
    except Exception as e:
        
        print(f"Erro inesperado: {e}")
    
def substituir_arquivo(origem, destino):
    """
    Substitui o conteúdo do arquivo `destino` pelo conteúdo do arquivo `origem`.

    :param origem: Caminho do arquivo que contém o novo conteúdo.
    :param destino: Caminho do arquivo que será substituído.
    """
    try:
        # Lê o conteúdo do arquivo de origem
        with open(origem, 'rb') as arquivo_origem:
            conteudo = arquivo_origem.read()

        # Escreve o conteúdo no arquivo de destino (sobrescreve o conteúdo existente)
        with open(destino, 'wb') as arquivo_destino:
            arquivo_destino.write(conteudo)

        messagebox.showinfo("Sucesso", f"O arquivo '{destino}' foi substituído com sucesso pelo conteúdo de '{origem}'.")
    except FileNotFoundError as e:
        messagebox.showerror("Erro", f"Erro: {e}")
    except PermissionError:
        messagebox.showerror("Erro", "Permissão negada para acessar os arquivos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

def selecionar_arquivos():
    """
    Função para selecionar o arquivo de origem e definir o arquivo de destino como 'contabil.log'.
    """
    # Abrir janela para selecionar o arquivo de origem
    origem = filedialog.askopenfilename(title="Selecione o arquivo de origem")
    if not origem:
        messagebox.showwarning("Aviso", "Arquivo de origem não selecionado!")
        return

    # Perguntar ao usuário onde salvar o arquivo 'contabil.log'
    diretorio_destino = filedialog.askdirectory(title="Selecione o diretório para salvar 'contabil.log'")
    if not diretorio_destino:
        messagebox.showwarning("Aviso", "Diretório de destino não selecionado!")
        return

    # Construir o caminho do arquivo de destino
    destino = os.path.join(diretorio_destino, "contabil.log")

    # Chamar a função de substituição
    substituir_arquivo(origem, destino)

#Cria tela de carregamento
loading_screen()

# Criar a janela principal
janela = tk.Tk()
janela.title("Aplicador de Banco")
janela.geometry("500x500")

btn_banco = tk.Button(janela, text="Selecionar Pasta do Banco Completo para aplicação", font = ("Arial", 14, "bold"  ) , bg="lightblue", command=lambda: globals().__setitem__('caminho_arquivo', criar_e_executar_bat()))
btn_banco.pack(pady=90)

# Botão para iniciar a substituição
btn_substituir = tk.Button(janela, text="Selecionar arquivos .LOG", font = ("Arial", 14, "bold"  ) , bg="lightblue", command=selecionar_arquivos, width = 20, height=2)
btn_substituir.pack(pady=10)

# Rótulo para exibir o arquivo selecionado
label_arquivo = tk.Label(janela, text="Primeiro arquivo de Modificações, depois o arquivo antigo",font = ("Arial", 10) , wraplength=350)
label_arquivo.pack(pady= 10)

btn_banco = tk.Button(janela, text="Selecionar pasta do Banco Completo para aplicação do Log de Modificações", font = ("Arial", 10, "bold"  ) , bg="lightblue", command=lambda: globals().__setitem__('caminho_arquivo', criar_e_executar_bat()))
btn_banco.pack(pady=10)

# Inicia o loop principal

#processo.terminate()

janela.protocol("WM_DELETE_WINDOW", fechar_programa)

janela.mainloop()