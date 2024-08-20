# Importa as bibliotecas que a gente vai usar
import cv2  # Para trabalhar com imagens e vídeos
import face_recognition as fr  # Para reconhecer rostos nas imagens
import cvzone  # Ajuda com algumas funções do OpenCV
import os  # Para fazer operações no sistema
import time  # Para lidar com tempo e pausas
import sqlite3  # Para interagir com o banco de dados SQLite
from pyfirmata import Arduino, SERVO  # Para controlar o Arduino e o servo motor
import subprocess  # Para executar novos processos do sistema
import tkinter as tk  # Para criar a interface gráfica
from tkinter import Canvas  # Para desenhar na interface gráfica
from PIL import Image, ImageTk  # Para trabalhar com imagens
import numpy as np  # Para manipular arrays e dados
from datetime import datetime  # Para lidar com datas e horas


# Função para conectar ao banco de dados SQLite
def conectar_banco():
    conn = sqlite3.connect('facial_recognition.db')  # Conecta ao banco de dados
    return conn


# Função para registrar quando alguém faz login
def registrar_entrada(nome, funcao, cpf):
    conn = conectar_banco()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

    # Adiciona a entrada no banco de dados com o horário atual
    cursor.execute('''
        INSERT INTO entradas (nome, funcao, cpf, data_hora)
        VALUES (?, ?, ?, ?)
    ''', (nome, funcao, cpf, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))  # Adiciona a data e hora atual

    conn.commit()  # Salva as mudanças no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

    print(f"Entrada registrada: Nome: {nome}, Função: {funcao}, CPF: {cpf}")  # Confirmação no console


# Configura o Arduino e o servo motor
board = Arduino('COM3')  # Conecta ao Arduino na porta COM3
board.digital[8].mode = SERVO  # Configura o pino 8 para controlar o servo motor

# Função para girar o servo motor
def rotateServo(angle):
    board.digital[8].write(angle)  # Define o ângulo do servo motor
    time.sleep(0.015)  # Espera um pouco para o motor se ajustar


# Configura os LEDs para indicar diferentes estados
ledVM = board.get_pin('d:7:o')  # LED Vermelho (pino digital 7)
ledVD = board.get_pin('d:5:o')  # LED Verde (pino digital 5)
ledAM = board.get_pin('d:6:o')  # LED Amarelo (pino digital 6)

# Configura a captura de vídeo e carrega as imagens de fundo
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Abre a câmera padrão
cap.set(3, 640)  # Define a largura da imagem
cap.set(4, 480)  # Define a altura da imagem

# Carrega as imagens que vamos usar
imgBackgroud = cv2.imread('Resources/screem/menu.png')  # Imagem de fundo do menu
imgLogin = cv2.imread('Resources/screem/6.png')  # Imagem para login bem-sucedido
imgError = cv2.imread('Resources/screem/7.png')  # Imagem para erro
imgMarked = cv2.imread('Resources/screem/4.png')  # Imagem marcada (não usada no código)
imgActive = cv2.imread('Resources/screem/1.png')  # Imagem ativa
imgAnalize = cv2.imread('Resources/screem/5.png')  # Imagem para análise

# Pega as dimensões da imagem de fundo
height, width, _ = imgBackgroud.shape


# Função para carregar os dados dos colaboradores do banco de dados
def carregar_base():
    global nomes, encods, funcoes, cpfs
    nomes = []  # Lista de nomes dos colaboradores
    encods = []  # Lista de encodings das faces
    funcoes = []  # Lista de funções dos colaboradores
    cpfs = []  # Lista de CPFs dos colaboradores

    conn = conectar_banco()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

    cursor.execute("SELECT nome, funcao, cpf, imagem FROM colaboradores")  # Pega os dados dos colaboradores
    colaboradores = cursor.fetchall()  # Recupera todos os colaboradores

    for colaborador in colaboradores:
        nome, funcao, cpf, imagem = colaborador  # Pega os dados do colaborador

        # Converte a imagem BLOB para um formato utilizável
        nparr = np.frombuffer(imagem, np.uint8)  # Converte o BLOB em um array NumPy
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decodifica a imagem

        # Calcula o encoding da face, se houver
        face_encodings = fr.face_encodings(img)  # Calcula o encoding da face
        if face_encodings:  # Se encontrou algum rosto
            encods.append(face_encodings[0])  # Adiciona o encoding à lista
            nomes.append(nome)  # Adiciona o nome à lista
            funcoes.append(funcao)  # Adiciona a função à lista
            cpfs.append(cpf)  # Adiciona o CPF à lista
        else:
            print(f"Nenhum rosto encontrado para o colaborador {nome}. Ignorando...")  # Mensagem de erro se não encontrar rosto

    conn.close()  # Fecha a conexão com o banco de dados
    print('Base de dados carregada!')  # Confirmação de que a base foi carregada com sucesso


carregar_base()  # Chama a função para carregar os dados dos colaboradores


# Função para comparar o encoding de uma imagem com os encodings armazenados
def compararEnc(encImg):
    for id, enc in enumerate(encods):
        comp = fr.compare_faces([encImg], enc)  # Compara o encoding da imagem com o armazenado
        if comp[0]:  # Se encontrou uma correspondência
            return True, nomes[id], funcoes[id], cpfs[id]  # Retorna o resultado da comparação
    return False, None, None, None  # Retorna que não encontrou correspondência


# Função para voltar ao menu principal
def voltar():
    print("Voltando ao menu principal...")  # Mensagem de retorno
    cap.release()  # Libera a câmera
    cv2.destroyAllWindows()  # Fecha todas as janelas do OpenCV
    root.quit()  # Fecha a janela Tkinter
    subprocess.Popen(["python", "menu_principal.py"])  # Executa o script do menu principal


# Configura a interface gráfica com Tkinter
root = tk.Tk()  # Cria a janela principal
root.title("Reconhecimento Facial")  # Define o título da janela

# Cria um Canvas para exibir a imagem
canvas = Canvas(root, width=width, height=height)  # Cria um Canvas com as dimensões da imagem
canvas.pack()  # Adiciona o Canvas à janela

# Cria o botão "Voltar"
btn_voltar = tk.Button(root, text="Voltar", command=voltar, font=('Arial', 16), width=25, bg='#6f50f8', fg='white')  # Configura o botão
canvas.create_window(1010, 550, window=btn_voltar)  # Adiciona o botão ao Canvas


# Função para atualizar a imagem no Canvas
def update_canvas(img):
    # Converte a imagem OpenCV para uma imagem Tkinter
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte para RGB
    img_pil = Image.fromarray(img_rgb)  # Converte para PIL
    img_tk = ImageTk.PhotoImage(image=img_pil)  # Converte para Tkinter

    # Atualiza o Canvas com a nova imagem
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)  # Adiciona a imagem ao Canvas
    canvas.image = img_tk  # Mantém uma referência à imagem


# Função para adicionar texto com fundo colorido
def put_text_with_background(img, text, position, font, font_scale, font_color, font_thickness, bg_color, padding=10):
    # Pega o tamanho do texto
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)  # Calcula o tamanho

    # Calcula a posição do retângulo de fundo
    x, y = position  # Posição do texto
    bg_x1 = x - padding  # Coordenada x do canto superior esquerdo
    bg_y1 = y - text_height - padding  # Coordenada y do canto superior esquerdo
    bg_x2 = x + text_width + padding  # Coordenada x do canto inferior direito
    bg_y2 = y + baseline + padding  # Coordenada y do canto inferior direito

    # Desenha o retângulo de fundo
    cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1)  # Desenha o retângulo preto

    # Desenha o texto sobre o retângulo de fundo
    cv2.putText(img, text, position, font, font_scale, font_color, font_thickness)  # Adiciona o texto


# Variáveis de controle para exibir mensagens
message_displayed = False  # Para saber se a mensagem está exibida
display_start_time = 0  # Quando a mensagem foi exibida
display_duration = 3000  # Quanto tempo a mensagem deve aparecer (em milissegundos)

# Tempo que a imagem de login fica visível após o login (em segundos)
login_display_time = 7  # Tempo em segundos

# Controle da exibição da imagem de login
login_start_time = None  # Quando a imagem de login foi exibida
show_login_image = False  # Se a imagem de login deve ser mostrada
detecting_face = True  # Se estamos detectando rostos


# Função para processar cada frame da câmera
def process_frame():
    global faceLoc, sleepRegister, sleepError, message_displayed, display_start_time, nome, funcao, cpf, login_start_time, show_login_image, detecting_face

    success, img = cap.read()  # Captura um frame da câmera
    if not success:
        print("Falha ao capturar imagem da câmera.")  # Mensagem de erro se falhar
        return

    imgP = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte a imagem para RGB
    imgActual = imgActive.copy()  # Copia a imagem ativa
    sleepRegister = False  # Controla se o registro está em andamento
    sleepError = False  # Controla se houve um erro

    if detecting_face:
        try:
            faceLoc.append(fr.face_locations(imgP)[0])  # Tenta detectar um rosto
        except:
            faceLoc = []  # Limpa a lista se não encontrar rosto

    if faceLoc:
        y1, x2, y2, x1 = faceLoc[-1]  # Pega as coordenadas do rosto detectado
        w, h = x2 - x1, y2 - y1  # Calcula a largura e altura do retângulo
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 0))  # Desenha um retângulo ao redor da face
        imgActual = imgAnalize.copy()  # Usa a imagem para análise
        ledAM.write(1)  # Acende o LED amarelo para indicar análise

    if len(faceLoc) > 20:
        encodeImg = fr.face_encodings(imgP)[0]  # Obtém o encoding da face
        comp, nome, funcao, cpf = compararEnc(encodeImg)  # Compara o encoding com os armazenados

        if comp:
            imgActual = imgLogin.copy()  # Mostra a imagem de login
            faceLoc = []  # Limpa a lista de localizações de face
            sleepRegister = True  # Indica que o registro está em andamento
            ledAM.write(0)  # Desliga o LED amarelo
            ledVD.write(1)  # Acende o LED verde
            rotateServo(130)  # Gira o servo motor
            time.sleep(7)  # Espera 7 segundos
            rotateServo(0)  # Retorna o servo motor à posição inicial
            ledVD.write(0)  # Desliga o LED verde

            # Adiciona o texto com fundo colorido
            put_text_with_background(imgActual, f'{nome} - {funcao}', (910, 510), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                     (255, 255, 255), 2, (0, 0, 0))  # Fundo preto

            # Registra a entrada no banco de dados
            registrar_entrada(nome, funcao, cpf)

            # Inicia o temporizador para mostrar a imagem de login
            login_start_time = time.time()  # Captura o tempo atual
            show_login_image = True  # Indica que a imagem de login deve ser exibida
            detecting_face = False  # Desativa a detecção de rosto

        else:
            imgActual = imgError.copy()  # Mostra a imagem de erro
            faceLoc = []  # Limpa a lista de localizações de face
            sleepError = True  # Indica que ocorreu um erro
            ledVM.write(1)  # Acende o LED vermelho
            ledAM.write(0)  # Desliga o LED amarelo
            time.sleep(5)  # Espera 5 segundos
            ledVM.write(0)  # Desliga o LED vermelho

    # Atualiza a imagem de fundo com a imagem capturada e a atual
    imgBackgroud[162:162 + 480, 55:55 + 640] = img  # Adiciona a imagem capturada
    imgBackgroud[44:44 + 633, 808:808 + 414] = imgActual  # Adiciona a imagem atual

    # Verifica o tempo de exibição da imagem de login
    if show_login_image:
        if time.time() - login_start_time < login_display_time:  # Se ainda estiver dentro do tempo
            imgBackgroud[44:44 + 633, 808:808 + 414] = imgLogin  # Mostra a imagem de login
            # Adiciona o texto com fundo colorido
            put_text_with_background(imgBackgroud, f'{nome} - {funcao}', (830, 510), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                     (255, 255, 255), 2, (248, 80, 111))  # Fundo colorido
        else:
            show_login_image = False  # Indica que a imagem de login não deve mais ser exibida
            login_start_time = None  # Limpa o tempo de início
            detecting_face = True  # Reativa a detecção de rosto

    # Atualiza o Canvas com a imagem atual
    update_canvas(imgBackgroud)

    # Controla a exibição das mensagens
    if message_displayed:
        if (time.time() - display_start_time) * 1000 >= display_duration:  # Se o tempo de exibição tiver passado
            message_displayed = False  # Indica que a mensagem não está mais exibida
            display_start_time = 0  # Limpa o tempo de início

    root.after(1, process_frame)  # Reexecuta a função process_frame a cada 1 ms


process_frame()  # Inicia o processamento dos frames
root.mainloop()  # Inicia o loop principal do Tkinter
