########################################
#  Codigo para estrelas em um campo    #
########################################
# Gustavo Rossi, Victor Lattari e Tiago Francisco
# Data: 06/02/2024
# Python3

#####################################
# Bibliotecas  e arquivo de entrada #
#####################################
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from photutils.detection import DAOStarFinder 
from astropy.stats import mad_std
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Declarando a imagem .fits
image = '/home/tiago/Documents/GitHub/satelites/Capture_1.fits'

#Coordenadas do fundo de ceu 
x = 1497
y = 1025.25
raio = 4.

#####################################
#           Codigo                  #
#####################################
# Lendo a imagem .fits e salvando a contagem em data
Image_data = fits.open(image)
data = Image_data[0].data

# 1. Opcao
# Calculando o desvio padrao mediano (dpm) da imagem
# Como calcular o desvio padrao mediano:
# 1 passo. Calcule a mediana dos dados.
# 2 passo. Para cada ponto de dado, calcule a distancia absoluta entre esse ponto e a mediana.
# 3 passo. Calcule a mediana dessas distancias absolutas.
dpm = mad_std(data)

# 2. Opcao
# Quantidade de linhas e colunas 
i,j = np.indices(data.shape)

# Criando um circulo que ira representar o fundo de ceu
circ = np.where(np.sqrt((i-x)*(i-x)+(j-y)*(j-y)) < raio)

# Mediana do ceu
med_ceu = np.median(data[circ])

# Configurando a funcao DAOStarFinder para encontrar estrelas
Star_Finder = DAOStarFinder(threshold=1.*med_ceu, fwhm=12.)

# Encontrando as posicoes e os fluxos das estrelas 
sources = Star_Finder(data)

# Salvando a imagem em .png com as estrelas detectadas em amarelo
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(data, cmap='gray', origin='lower', vmin=np.percentile(data, 5), vmax=np.percentile(data, 95))
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.5)
plt.colorbar(im, cax=cax, orientation='horizontal', label='Contagem')
ax.scatter(sources['xcentroid'], sources['ycentroid'], s=0.5, color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.savefig(str(image) + '.png')

# Salvar as posições das estrelas encontradas
sources.write('estrelas.csv', format='csv', overwrite=True)
