import numpy as np
import rasterio as rio
from shapely.geometry import Point
import random

# definição de funções importantes para normalização e contraste de imagens
delta = 0.0000000001

# Função para gerar pontos aleatórios dentro de um polígono
def generate_random_points(polygon, num_points=1):
    min_x, min_y, max_x, max_y = polygon.bounds
    points = []
    while len(points) < num_points:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(random_point):
            points.append(random_point)
    return points

# calcula os mínimos e máximos, e aplicar uma normalização min/max
# retornando a matriz normalizada entre 0 e L
def normalizar(matriz_original, L):
    if np.isnan(matriz_original).all():
        return matriz_original
    (min_pixel, max_pixel) = (np.nanmin(matriz_original), np.nanmax(matriz_original))
    matriz_float = np.where(np.isnan(matriz_original), 0, matriz_original.copy().astype(float))
    matriz_normalizada = (L - 1) * (matriz_float - min_pixel) / (max_pixel - min_pixel + delta)
    matriz_normalizada = np.where(np.isnan(matriz_original), 0, matriz_normalizada)
    return matriz_normalizada
    
# calcula os mínimos e máximos, e aplicar uma normalização min/max
# retornando a matriz normalizada entre 0 e L
def normalizar_2p(matriz_original, L):
    min_2p = np.percentile(matriz_original, 2)
    max_2p = np.percentile(matriz_original, 98)
    matriz_float = np.where(np.isnan(matriz_original), 0, matriz_original.copy().astype(float))
    matriz_normalizada = (L - 1) * (matriz_float - min_2p) / (max_2p - min_2p + delta)
    matriz_normalizada[matriz_normalizada > L] = L
    matriz_normalizada[matriz_normalizada < 0] = 0
    matriz_normalizada = np.where(np.isnan(matriz_original), 0, matriz_normalizada)
    return matriz_normalizada
    
def aplicar_contraste_ganho_offset(matriz_original, L, ganho, offset):
    matriz_resultante = matriz_original.copy() * ganho + offset
    matriz_resultante[matriz_resultante > L] = L
    return matriz_resultante

def aplicar_contraste_log(matriz_original, L, normalizar_resultado = True):
    matriz_resultante = L * np.log(1 + matriz_original.copy()) / np.log(L)
    if normalizar_resultado:
        matriz_resultante = normalizar(matriz_resultante, L)
    else:
        matriz_resultante[matriz_resultante > L] = L
    return matriz_resultante

def aplicar_contraste_raiz(matriz_original, L, N, normalizar_resultado = True):
    matriz_resultante = np.power(L, 1 / N) * np.power(matriz_original.copy(), 1 / N)
    if normalizar_resultado:
        matriz_resultante = normalizar(matriz_resultante, L)
    else:
        matriz_resultante[matriz_resultante > L] = L
    return matriz_resultante

def aplicar_contraste_quadrado(matriz_original, L, N, normalizar_resultado = True):
    matriz_resultante = np.power(matriz_original.copy(), N) / L
    if normalizar_resultado:
        matriz_resultante = normalizar(matriz_resultante, L)
    else:
        matriz_resultante[matriz_resultante > L] = L
    return matriz_resultante

def normalizar_array(arr):
    norm_arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    return norm_arr

def carregar_banda_sentinel2_bdc(item, banda, gleba):
    with rio.open(item.assets[banda].href) as raster:
        # matriz = raster.read(1, window=gleba)
        matriz, _ = rio.mask.mask(raster, gleba.geometry.to_crs(raster.crs), crop=True)
        return matriz[0]

def carregar_banda_sentinel2_bdc_scl(item, banda, gleba, scl):
    with rio.open(item.assets[banda].href) as raster:
        # matriz = raster.read(1, window=gleba)
        matriz, _ = rio.mask.mask(raster, gleba.geometry.to_crs(raster.crs), crop=True)
        matriz = np.where(scl != 0, np.where(scl < 8, matriz[0], np.nan), np.nan) 
        return matriz