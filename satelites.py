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
from astropy.wcs import WCS
from astropy.visualization import astropy_mpl_style
from photutils.detection import DAOStarFinder 
from astropy.stats import mad_std
from mpl_toolkits.axes_grid1 import make_axes_locatable

import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia

# Declarando a imagem .fits
image = '/home/tiago/Documents/GitHub/satelites/Capture_1.fits'

# Coordenadas do fundo de ceu 
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
header = Image_data[0].header

# Extracting WCS information
wcs = WCS(header)

# Calculando o RA ae o DEc do centro da imagem
ra_center, dec_center = wcs.all_pix2world(x, y, 1)

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
Star_Finder = DAOStarFinder(threshold=5.*dpm, fwhm=3., sky = med_ceu)

# Encontrando as posicoes e os fluxos das estrelas 
sources = Star_Finder(data)

# Criando um filtro conforme a porcentagem do pico inserida pelo usuario
peak_values = sources['peak']
lower_peak_value = np.percentile(peak_values, Lower_peak)
upper_peak_value = np.percentile(peak_values, Upper_peak)

# Filtro para um pico minimo e maximo das estrelas
selected_star = sources[(sources['peak'] > lower_peak_value) & (sources['peak'] < upper_peak_value)]

# Calculando o RA e o DEc das estrelas
x_centroids = selected_star['xcentroid']
y_centroids = selected_star['ycentroid']
ra_dec_positions = wcs.all_pix2world(x_centroids, y_centroids, 1)
ra_dec_positions = np.array(ra_dec_positions)
ra_positions = ra_dec_positions[:, 0]
dec_positions = ra_dec_positions[:, 1]

# Salvando a imagem em .png com as estrelas detectadas em vermelho
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(data, cmap='gray', origin='lower', vmin=np.percentile(data, 5), vmax=np.percentile(data, 95))
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.5)  
plt.colorbar(im, cax=cax, orientation='horizontal', label='Contagem')
ax.scatter(selected_star['xcentroid'], selected_star['ycentroid'], s=1., color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.savefig(image.replace('.fits', '') + '_stars.png')

# Salvando as posicoes das estrelas encontradas
selected_star.write(image.replace('.fits', '') + '_stars.csv', format='csv', overwrite=True)

# Teste com a blibioteca Gaia
# Calculando a distancia das estrelas do centro da imagem
#x_selected = selected_star['xcentroid']
#y_selected = selected_star['ycentroid']
#d_selected = np.sqrt(x_selected**2 + y_selected**2)

# Leando RA e o DEC
#RA = 204.6559022244836
#DEC = -45.70318228689955

#coord = SkyCoord(ra=RA, dec=DEC, unit=(u.degree, u.degree), frame='icrs')
#width = u.Quantity(0.1, u.deg)
#height = u.Quantity(0.1, u.deg)
#gaia_results = Gaia.query_object_async(coordinate=coord, width=width, height=height)

#matched_stars = []
#for gaia_star in gaia_results:
#    if abs(gaia_star.dist - d_star) <= 0.2: 
#        matched_stars.append((gaia_star.ra.deg, gaia_star.dec.deg))

# Salvando os pontos acima do fundo de ceu
x_indices, y_indices = np.where(data > med_ceu)

print(x_indices)





