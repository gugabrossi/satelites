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
image = '/home/tiago/Documents/GitHub/satelites/Teste/Pasiphae.fits'

#Coordenadas do fundo de ceu 
x = 1497
y = 1025.25
raio = 4.

# Star filter
Lower_peak = 30.
Upper_peak = 70.

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

# Configurando a função DAOStarFinder para encontrar estrelas
Star_Finder = DAOStarFinder(threshold=5.*dpm, fwhm=3.)

# Encontrando as posicoes e os fluxos das estrelas 
sources = Star_Finder(data)

# Criando um filtro conforme a porcentagem do pico inserida pelo usuario
peak_values = sources['peak']
lower_peak_value = np.percentile(peak_values, Lower_peak)
upper_peak_value = np.percentile(peak_values, Upper_peak)

# Filtro para um pico minimo e maximo das estrelas
selected_star = sources[(sources['peak'] > lower_peak_value) & (sources['peak'] < upper_peak_value)]

# Salvando a imagem em .png com as estrelas detectadas em vermelho
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(data, cmap='gray', origin='lower', vmin=np.percentile(data, 5), vmax=np.percentile(data, 95))
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.5)  
plt.colorbar(im, cax=cax, orientation='horizontal', label='Contagem')
ax.scatter(selected_star['xcentroid'], selected_star['ycentroid'], s=1., color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.savefig(str(image) + '.png')

# Salvando as posições das estrelas encontradas
selected_star.write(str(image) + '.csv', format='csv', overwrite=True)
