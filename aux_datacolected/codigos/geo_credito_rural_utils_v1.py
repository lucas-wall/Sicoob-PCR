# Importações de bibliotecas para manipulação de dados e visualização
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import earthpy.plot as ep

# Importações de bibliotecas para manipulação de dados geoespaciais
from rasterio import mask
import shapely.geometry
import rasterio as rio
import geopandas as gpd

# Importações para criação de widgets interativos
from ipywidgets import Accordion, HTML
from IPython.display import display


def recortar_raster_map(geometrias: gpd.GeoSeries, raster_path: str) -> (np.ndarray, tuple):
    """
    Recortar um raster com base em geometrias fornecidas.

    Parâmetros:
        geometrias (gpd.GeoSeries, gpd.GeoDataFrame, shapely.geometry.Polygon): Geometrias para recorte.
        raster_path (str): Caminho para o arquivo raster a ser recortado.

    Retorna:
        np.ndarray: Imagem recortada.
        tuple: Bounding box da imagem recortada no formato (xmin, xmax, ymin, ymax).
    """
    with rio.open(raster_path) as src:
        # Verificar e reprojetar geometrias se necessário
        if isinstance(geometrias, (gpd.GeoSeries, gpd.GeoDataFrame)):
            if geometrias.crs != src.crs:
                geometrias = geometrias.to_crs(src.crs)
        elif isinstance(geometrias, shapely.geometry.Polygon):
            geometrias = gpd.GeoSeries([geometrias], crs='EPSG:4326')
            if geometrias.crs != src.crs:
                geometrias = geometrias.to_crs(src.crs)
        else:
            raise ValueError("Geometrias deve ser um GeoSeries, GeoDataFrame ou shapely.geometry.Polygon")

        # Aplicar máscara para recortar o raster
        imagem_cortada, transformacao = mask.mask(src, geometrias.geometry, crop=True)
        
        # Calcular bounding box da imagem recortada
        ymax = transformacao[5]
        xmin = transformacao[2]
        ymin = ymax + (transformacao[4] * imagem_cortada.shape[1])
        xmax = xmin + (transformacao[0] * imagem_cortada.shape[2])
        
        # Transformar coordenadas para EPSG:4326
        xmin_lon, ymin_lat = rio.warp.transform(src.crs, 'EPSG:4326', [xmin], [ymin])
        xmax_lon, ymax_lat = rio.warp.transform(src.crs, 'EPSG:4326', [xmax], [ymax])
        
    # Retornar a imagem recortada e o bounding box
    return imagem_cortada[0], (xmin_lon[0], xmax_lon[0], ymin_lat[0], ymax_lat[0])

def plot(imagem_cortada: np.ndarray, bbox: tuple, classes: gpd.GeoDataFrame):
    """
    Plotar imagem com uma legenda.

    Parâmetros:
        imagem_cortada (np.ndarray): Imagem .
        bbox (tuple): Bounding box da imagem no formato (xmin, xmax, ymin, ymax).
        classes (pd.DataFrame): DataFrame contendo informações de classe com colunas 'Value', 'Color', 'Category', 'Label'.
    """
    # Extrair valores únicos da imagem e contar suas ocorrências
    values, num_occurrences = np.unique(imagem_cortada, return_counts=True)
    cmap_colors, height_class_labels, bounds = [], [], []
    
    for value in values:
        # Configurar cores e rótulos para valores específicos
        if value == 0:
            cmap_colors.append('#EBEBEB')
            height_class_labels.append("No Data")
        else:
            class_info = classes[classes['Class_ID'] == value]
            if not class_info.empty:
                cmap_colors.append(class_info['Color'].values[0])
                height_class_labels.append(class_info['Descricao'].values[0])
            else:
                cmap_colors.append('#000000')
                height_class_labels.append(f"Value {value}")
        bounds.append(value)
    bounds.append(bounds[-1] + 1)

    # Criar colormap e normalização
    cmap = mcolors.ListedColormap(cmap_colors)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    # Calcular áreas e porcentagens das classes presentes na imagem
    total_pixels = np.sum(num_occurrences[values != 0])
    areas = (num_occurrences[values != 0] * 30 * 30) / 10000
    percentages = (num_occurrences[values != 0] / total_pixels) * 100

    # Organizar informações de classe em um DataFrame
    class_info = classes.set_index('Class_ID').loc[values[values != 0]]
    class_info['Area (ha)'] = areas
    class_info['Percentage (%)'] = percentages
    class_info = class_info[[ 'Descricao', 'Area (ha)', 'Percentage (%)']]
    class_info['Percentage (%)'] = class_info['Percentage (%)'].map('{:.2f}'.format)
    total_area = np.sum(areas)

    # Plotar a imagem com legenda
    fig, ax = plt.subplots(figsize=(6, 8))
    im = ax.imshow(imagem_cortada, cmap=cmap, norm=norm, extent=bbox, interpolation='none')
    ep.draw_legend(im, titles=height_class_labels)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(f'Área Total: {total_area:.2f} ha')
    plt.show()

    # Exibir informações de classe em uma tabela interativa
    table_html = class_info.to_html(index=True)
    accordion = Accordion(children=[HTML(f"<div style='background-color:white; padding:10px; border:2px solid black; width:60%;'>{table_html}</div>")])
    accordion.set_title(0, 'Tabela de Informações')
    display(accordion)