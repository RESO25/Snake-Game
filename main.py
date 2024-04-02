from tkinter import *
import random

LARGURA_JOGO = 700
ALTURA_JOGO = 700
VELOCIDADE = 100
ESPACO = 50
SEGMENTOS = 3
COR_COBRA = "#00FF00"
COR_COMIDA = "#FF0000"
COR_FUNDO = "#000000"

class Cobra:
    def __init__(self):
        self.tamano = SEGMENTOS
        self.coordenadas = []
        self.quadrados = []

        for i in range(0, SEGMENTOS):
            self.coordenadas.append([0, 0])

        for x, y in self.coordenadas:
            quadrado = canvas.create_rectangle(x, y, x+ESPACO, y+ESPACO, fill=COR_COBRA, tag='cobra')
            self.quadrados.append(quadrado)

class Comida:
    def __init__(self):

        x = random.randint(0, int((LARGURA_JOGO/ESPACO)-1)) * ESPACO
        y = random.randint(0, int((ALTURA_JOGO/ESPACO)-1)) * ESPACO

        self.coordenadas = [x, y]
        canvas.create_oval(x, y, x + ESPACO, y + ESPACO, fill=COR_COMIDA, tag='comida')

def proximo_turno(cobra, comida):
    x, y = cobra.coordenadas[0]

    if direcao == "cima":
        y -= ESPACO
    elif direcao == "direita":
        x += ESPACO
    elif direcao == "baixo": 
        y += ESPACO
    elif direcao == "esquerda":
        x -= ESPACO

    cobra.coordenadas.insert(0, (x, y))
    quadrado = canvas.create_rectangle(x, y, x+ESPACO, y+ESPACO, fill=COR_COBRA)
    cobra.quadrados.insert(0, quadrado)

    if x == comida.coordenadas[0] and y == comida.coordenadas[1]:
        global pontuacao
        pontuacao += 1
        texto.config(text="Pontos: {}".format(pontuacao))

        canvas.delete("comida")
        comida = Comida()

    else:

        del cobra.coordenadas[-1]
        canvas.delete(cobra.quadrados[-1])
        del cobra.quadrados[-1]

    if checar_colisoes(cobra):
        game_over()
    else:
        janela.after(VELOCIDADE, proximo_turno, cobra, comida)

def mudar_direcao(nova_direcao):
    global direcao

    if nova_direcao == 'esquerda':
        if direcao != 'direita':
            direcao = nova_direcao

    if nova_direcao == 'direita':
        if direcao != 'esquerda':
            direcao = nova_direcao

    if nova_direcao == 'cima':
        if direcao != 'baixo':
            direcao = nova_direcao

    if nova_direcao == 'baixo':
        if direcao != 'cima':
            direcao = nova_direcao
              
def checar_colisoes(cobra):
    x, y = cobra.coordenadas[0]

    if x < 0 or x > LARGURA_JOGO:
        print("GAME OVER")
        return True
    
    if y < 0 or y > ALTURA_JOGO:
        print("GAME OVER")
        return True

    for segmento in cobra.coordenadas[1:]:
        if x == segmento[0] and y == segmento[1]:
            print("GAME OVER")
            return True

def game_over():
    canvas.delete(ALL)
    canvas.create_text((canvas.winfo_width()/2), (canvas.winfo_height()/2), font=("consolas", 40), text="GAME OVER", fill="red", tag="gameover")

def reiniciar_jogo():
    global cobra, comida, pontuacao, direcao

    # Reinicia todas as variáveis pro seu valor inicial
    canvas.delete(ALL)
    cobra = Cobra()
    comida = Comida()
    pontuacao = 0
    direcao = 'baixo'
    texto.config(text="Pontos:{}".format(pontuacao))
    proximo_turno(cobra, comida)

janela = Tk()

janela.title("snek game")
janela.resizable(False, False)

pontuacao = 0;
direcao = 'baixo'

texto = Label(janela, text="Pontos: {}".format(pontuacao), font=('consolas', 30))
texto.pack()

canvas = Canvas(janela, bg=COR_FUNDO, height=ALTURA_JOGO, width=LARGURA_JOGO)
canvas.pack()

janela.update()

largura_janela = janela.winfo_width()
altura_janela = janela.winfo_height()

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

x = int((largura_tela/2) - (largura_janela/2))
y = int((altura_tela/2) - (altura_janela/2))

janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

janela.bind('<Up>', lambda event: mudar_direcao('cima'))
janela.bind('<w>', lambda event: mudar_direcao('cima'))

janela.bind('<Right>', lambda event: mudar_direcao('direita'))
janela.bind('<d>', lambda event: mudar_direcao('direita'))

janela.bind('<Down>', lambda event: mudar_direcao('baixo'))
janela.bind('<s>', lambda event: mudar_direcao('baixo'))

janela.bind('<Left>', lambda event: mudar_direcao('esquerda'))
janela.bind('<a>', lambda event: mudar_direcao('esquerda'))

janela.bind('<r>', lambda event: reiniciar_jogo())

cobra = Cobra()
comida = Comida()

proximo_turno(cobra, comida)

janela.mainloop()