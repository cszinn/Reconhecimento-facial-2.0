import os # Para fazer operações no sistema
import tkinter as tk # Para criar a interface gráfica
from tkinter import Canvas # Para desenhar na interface gráfica
from PIL import ImageTk, ImageDraw, Image  # Para trabalhar com imagens
import cv2 # Para trabalhar com imagens e vídeos


def abrir_reconhecimento():
    """Esconde o menu principal e abre o script de reconhecimento facial."""
    root.withdraw()  # Esconde a janela principal
    os.system('python reconhecimento.py')  # Executa o script de reconhecimento facial
    root.deiconify()  # Mostra a janela principal novamente após o script terminar


def abrir_cadastro():
    """Esconde o menu principal e abre o script de cadastro de usuários."""
    root.withdraw()  # Esconde a janela principal
    os.system('python cadastro.py')  # Executa o script de cadastro
    root.deiconify()  # Mostra a janela principal novamente após o script terminar

def fechar_menu():
    """Fecha a janela principal e encerra o aplicativo."""
    root.destroy()  # Fecha a janela principal e encerra o programa

def criar_retangulo_arredondado(imagem, largura, altura, raio):
    """Cria uma imagem com um retângulo de cantos arredondados."""
    # Criar uma máscara para o retângulo com cantos arredondados
    mask = Image.new('L', (largura, altura), 0)  # Cria uma máscara preta
    draw = ImageDraw.Draw(mask)  # Prepara para desenhar na máscara
    draw.rounded_rectangle([(0, 0), (largura, altura)], raio, fill=255)  # Desenha o retângulo arredondado

    # Aplicar a máscara à imagem
    imagem = imagem.convert('RGBA')  # Converte a imagem para o modo RGBA
    imagem_com_mascara = Image.new('RGBA', (largura, altura))  # Cria uma nova imagem com a mesma dimensão
    imagem_com_mascara.paste(imagem, (0, 0), mask)  # Aplica a máscara à imagem

    return imagem_com_mascara  # Retorna a imagem com cantos arredondados


# Configuração da interface gráfica principal
root = tk.Tk()  # Cria a janela principal
root.title('Sistema de Reconhecimento Facial')  # Define o título da janela

# Carregar e exibir a imagem de fundo
bg_image_path = 'Resources/screem/menu.png'
bg_image = Image.open(bg_image_path)  # Abre a imagem de fundo
bg_image_tk = ImageTk.PhotoImage(bg_image)  # Converte a imagem para um formato compatível com Tkinter

# Cria um Canvas para exibir a imagem de fundo
canvas = Canvas(root, width=bg_image_tk.width(), height=bg_image_tk.height())
canvas.pack(fill="both", expand=True)  # Adiciona o Canvas à janela e expande para preencher
canvas.create_image(0, 0, anchor='nw', image=bg_image_tk)  # Adiciona a imagem de fundo ao Canvas

# Carregar a imagem de sobreposição
overlay_image_path = 'Resources/screem/exemplo.png'
overlay_image = Image.open(overlay_image_path)  # Abre a imagem de sobreposição

# Redimensiona a imagem (se necessário)
novo_tamanho = (635, 479)  # Novo tamanho para a imagem
overlay_image = overlay_image.resize(novo_tamanho, Image.LANCZOS)  # Redimensiona a imagem usando filtro LANCZOS

# Cria a imagem com cantos arredondados
overlay_image_arredondada = criar_retangulo_arredondado(overlay_image, novo_tamanho[0], novo_tamanho[1], 10)

# Converte a imagem para um formato compatível com Tkinter e adiciona ao Canvas
overlay_image_tk = ImageTk.PhotoImage(overlay_image_arredondada)
canvas.create_image(59, 163, anchor='nw', image=overlay_image_tk)  # Adiciona a imagem de sobreposição ao Canvas


# Adiciona título e botões à interface
label1 = tk.Label(root, text="Bem Vindo!", font=('Arial', 19, 'bold'), bg='white', fg='#6f50f8')  # Título
label2 = tk.Label(root, text="Escolha uma opção", font=('Arial', 19, 'bold'), bg='white', fg='#6f50f8')  # Subtítulo

# Cria os botões com comandos específicos
btn_reconhecimento = tk.Button(root, text="Reconhecimento", command=abrir_reconhecimento,
                               font=('Arial', 16), width=25, bg='#6f50f8', fg='white')  # Botão para reconhecimento facial
btn_cadastro = tk.Button(root, text="Cadastro", command=abrir_cadastro, font=('Arial', 16),
                         width=25, bg='#6f50f8', fg='white')  # Botão para cadastro de usuários
btn_fechar = tk.Button(root, text="Sair", command=fechar_menu, font=('Arial', 16),
                         width=25, bg='#6f50f8', fg='white')  # Botão para fechar o aplicativo

# Posiciona os widgets no Canvas usando o método create_window()
canvas.create_window(1010, 100, window=label1)  # Adiciona o título
canvas.create_window(1010, 150, window=label2)  # Adiciona o subtítulo
canvas.create_window(1010, 350, window=btn_reconhecimento)  # Adiciona o botão de reconhecimento
canvas.create_window(1010, 450, window=btn_cadastro)  # Adiciona o botão de cadastro
canvas.create_window(1010, 550, window=btn_fechar)  # Adiciona o botão de fechar

root.mainloop()  # Inicia o loop principal da interface gráfica
