# Programa Satelites
Programa para identificação de posição x,y de satélites ("imagem traço") e determinação de RA,DEC equivalentes nos pixeis da imagem.


# Objetivos:
1) Identificar fontes (estrelas) no CCD
  - Detecção e ajuste de Gaussiana (depois usar também moffat, outra?) 
  - Determinar tamanho de anel ou janela de detecção (como vamos fazer: fixo, variável, individual para cada fonte?)
  - determinação de altura da Gaussiana e FWHM

 2) Determinar RA/DEC das estrelas
  - Determinar tamanho do FOV
  - Fazer Query no GAIA para identificação das estrelas a partir da coordenada central
  - Determinar x,y <-> RA,DEC das estrelas 

3) Detecção da imagem traço
  - Identificar na imagem FITS o traço do satélite
  - Ajustar gaussiana 2D (possível com 1 px?)
  - Determinar a posição x,y dos extremos do traço
  - Determinar a posição x,y central
  - Fornecer as posições relatvas x,y <-> RA,DEC

# Tarefas:
29/01- Criação GIT, Verificar ferramentas do python (astropy, numpy, etc) para realizar as tarefas  (1) e (2)

05/02- Discussão e implementação da tarefa (1) com as ferramentas encontradas
12/03- Testes e verificação
19/02- Discussão e implementação da tarefa (2) com as ferramentas encontradas
26/02- Testes e verificação

04/03- Discussão de ferramentas e procedimentos para as tarefas (3.1) e (3.2)
11/03- Implementação das tarefas (3.1) e (3.2)
18/03- Testes e verificação
25/03- Implementação da tarefa (3) completa

01/04- Testes e verificação
08/04- Discussão e determinação de erros e incertezas
15/04- Validação
22/04- Entrega do programa
