#===================== Bibliotecas para manipulação de dados e visualização =====================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import earthpy.plot as ep
from matplotlib.colors import ListedColormap, Colormap

#===================== Bibliotecas para manipulação de dados geoespaciais =====================
import geopandas as gpd
import rasterio as rio
from rasterio import mask
from rasterio.merge import merge
from rasterio.transform import from_bounds
from rasterio.io import MemoryFile
from rasterio.features import geometry_mask
from shapely.geometry import Polygon, box
from pyproj import Transformer
import xarray as xr

#===================== Bibliotecas para criação de widgets interativos =====================
from ipywidgets import Accordion, HTML, VBox, IntSlider, interact
from IPython.display import display

#===================== Bibliotecas para processamento de dados e computação paralela =====================
from dask import delayed, compute
from dask.diagnostics import ProgressBar
import numba as nb

#===================== Bibliotecas para machine learning e análise =====================
from sklearn.cluster import AgglomerativeClustering
from xpysom import XPySom
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform, pdist

#===================== Bibliotecas para manipulação de sistemas e processos =====================
import subprocess
import sys
import os
import warnings
from rasterio.errors import NotGeoreferencedWarning
import time

# Configurando filtros de warnings
warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)

#===================== Bibliotecas para progress tracking =====================
from tqdm import tqdm
#===================== Bibliotecas para manipulação de tipagem =====================
from typing import List, Dict, Optional, Tuple, Union
#===================== Bibliotecas para acesso a catálogos de dados =====================
import pystac_client

@nb.njit
def nan_helper_numba(y, cloud):
    return (cloud > 7) | (cloud <= 3), lambda z: z.nonzero()[0]

@nb.njit
def interpolate_vec_numba(x, cloud):
    nans, idx = nan_helper_numba(x, cloud)
    try:
        x[nans] = np.interp(idx(nans), idx(~nans), x[~nans])
        return x
    except:
        return x

@nb.njit(parallel=True)
def interpolate_mtx_numba(mtx, cloud):
    nrows, ncols = mtx.shape
    mtx_interpolated = np.empty_like(mtx)

    for i in nb.prange(nrows):
        mtx_interpolated[i, :] = interpolate_vec_numba(mtx[i, :], cloud[i, :])

    return mtx_interpolated


def connect_to_stac(url: str, parameters: Optional[Dict] = None) -> pystac_client.Client:
    """
    Conectar ao cliente STAC com parâmetros opcionais.

    Parâmetros:
        url (str): URL do endpoint STAC.
        parameters (Optional[Dict]): Dicionário de parâmetros opcionais para a conexão.

    Retorna:
        pystac_client.Client: Cliente STAC conectado.
    """
    return pystac_client.Client.open(url, parameters=parameters)

def search_stac(client: pystac_client.Client, start_date: str, end_date: str, collections: List[str], bbox: Optional[List[float]] = None, tiles: Optional[List[str]] = None, limit: int = 100) -> List[Dict]:
    """
    Pesquisar itens no STAC usando bbox ou tiles.

    Parâmetros:
        client (pystac_client.Client): Cliente STAC.
        start_date (str): Data de início no formato 'YYYY-MM-DD'.
        end_date (str): Data de fim no formato 'YYYY-MM-DD'.
        collections (List[str]): Lista de coleções a serem pesquisadas.
        bbox (Optional[List[float]]): Bounding box para a pesquisa.
        tiles (Optional[List[str]]): Lista de tiles para a pesquisa.
        limit (int): Limite de itens a serem retornados.

    Retorna:
        List[Dict]: Lista de itens retornados pela pesquisa.
    """
    if bbox:
        # Busca usando bbox
        item_search = client.search(
            collections=collections,
            bbox=bbox,
            datetime=f'{start_date}/{end_date}',
            limit=limit
        )
    elif tiles:
        # Busca usando query para tiles
        item_search = client.search(
            query={"bdc:tile": {"in": tiles}},
            datetime=f'{start_date}/{end_date}',
            collections=collections,
            limit=limit
        )
    else:
        raise ValueError("Either 'bbox' or 'tiles' must be specified for searching.")
    
    try:
        items = list(item_search.items())
    except:
        items = list(item_search.get_items())
    
    return items[::-1]

def get_timetamps(items):
    return list(dict.fromkeys([item.datetime.strftime("%Y_%m_%d") for item in items]))

def organize_items_by_time(items: List[Dict]) -> List[List[Dict]]:
    """Organizar itens por tile."""
    items_ = [[item for item in items if item.datetime.strftime("%Y_%m_%d") == date] 
          for date in dict.fromkeys(item.datetime.strftime("%Y_%m_%d") for item in items)]
    return items_

def recortar_raster(geometrias, raster_path):
    with rio.open(raster_path) as src:
        if isinstance(geometrias, (gpd.GeoSeries, gpd.GeoDataFrame, Polygon)):
            geometrias = gpd.GeoSeries([geometrias], crs='EPSG:4326').to_crs(src.crs) if isinstance(geometrias, Polygon) else geometrias.to_crs(src.crs)
            imagem_cortada, transformacao = mask.mask(src, geometrias.geometry, crop=True)
    return imagem_cortada[0]

#======================================================================================================

def recortar_raster_multi(
    geometrias: Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon],
    raster_path: str
) -> Tuple[np.ndarray, rio.Affine, rio.crs.CRS]:
    """
    Recorta um raster com base em geometrias fornecidas e retorna a imagem cortada, 
    a transformação e o CRS (Sistema de Referência de Coordenadas).

    Args:
        geometrias (Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon]): Geometria(s) usada(s) para recortar o raster. 
            Pode ser uma GeoSeries, GeoDataFrame ou um objeto Polygon.
        raster_path (str): Caminho do arquivo raster a ser recortado.

    Returns:
        Tuple[np.ndarray, rio.Affine, rio.crs.CRS]: 
            - imagem_cortada[0] (np.ndarray): O raster recortado como array numpy.
            - transformacao (rio.Affine): A transformação aplicada ao raster recortado.
            - crs (rio.crs.CRS): O sistema de referência de coordenadas do raster original.
    """
    with rio.open(raster_path) as src:
        crs = src.crs
        if isinstance(geometrias, (gpd.GeoSeries, gpd.GeoDataFrame, Polygon)):
            geometrias = gpd.GeoSeries([geometrias], crs='EPSG:4326').to_crs(src.crs) if isinstance(geometrias, Polygon) else geometrias.to_crs(src.crs)
            imagem_cortada, transformacao = mask.mask(src, geometrias.geometry, crop=True)
    return imagem_cortada[0], transformacao, crs


def merge_cropped_rasters(
    cropped_rasters: List[Tuple[np.ndarray, rio.Affine, rio.crs.CRS]]
) -> np.ndarray:
    """
    Combina múltiplos rasters recortados em um único raster mosaico.

    Args:
        cropped_rasters (List[Tuple[np.ndarray, rio.Affine, rio.crs.CRS]]): Lista de rasters recortados, 
            cada item é uma tupla contendo o raster (np.ndarray), a transformação (rio.Affine) e o CRS (rio.crs.CRS).

    Returns:
        np.ndarray: O mosaico resultante da combinação dos rasters recortados.
    """
    memfiles = []
    for mosaic, transform, crs in cropped_rasters:
        meta = {
            "driver": "GTiff",
            "height": mosaic.shape[0],
            "width": mosaic.shape[1],
            "count": 1,
            "dtype": mosaic.dtype,
            "crs": crs,
            "transform": transform,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "DEFLATE",
            "nodata": 0
        }
        memfile = MemoryFile()
        with memfile.open(**meta) as dataset:
            dataset.write(mosaic, 1)
        memfiles.append(memfile)
    
    datasets = [memfile.open() for memfile in memfiles]
    mosaic, out_trans = merge(datasets)
    out_meta = datasets[0].meta.copy()
    out_meta.update({
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })
    
    return mosaic[0]


def meta_output(
    cropped_rasters: List[Tuple[np.ndarray, rio.Affine, rio.crs.CRS]]
) -> Tuple[rio.Affine, dict]:
    """
    Gera metadados para os rasters recortados, combinando-os em um mosaico e retornando 
    a transformação e os metadados resultantes.

    Args:
        cropped_rasters (List[Tuple[np.ndarray, rio.Affine, rio.crs.CRS]]): Lista de rasters recortados, 
            onde cada item é uma tupla contendo o raster (np.ndarray), a transformação (rio.Affine) e o CRS (rio.crs.CRS).

    Returns:
        Tuple[rio.Affine, dict]: 
            - out_trans (rio.Affine): A transformação resultante do mosaico combinado.
            - out_meta (dict): Os metadados atualizados do mosaico, incluindo altura, 
              largura e transformação.
    """
    memfiles = []
    for mosaic, transform, crs in cropped_rasters:
        meta = {
            "driver": "GTiff",
            "height": mosaic.shape[0],
            "width": mosaic.shape[1],
            "count": 1,
            "dtype": mosaic.dtype,
            "crs": crs,
            "transform": transform,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "DEFLATE",
            "nodata": 0
        }
        memfile = MemoryFile()
        with memfile.open(**meta) as dataset:
            dataset.write(mosaic, 1)
        memfiles.append(memfile)
    
    datasets = [memfile.open() for memfile in memfiles]
    mosaic, out_trans = merge(datasets)
    out_meta = datasets[0].meta.copy()
    out_meta.update({
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })
    
    return out_trans, out_meta

#==================================================================================================================


def get_meta(
    geometrias: Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon],
    raster_path: str
) -> Dict[str, Union[str, int, rio.crs.CRS, np.dtype, rio.Affine]]:
    """
    Gera e retorna metadados de um raster com base nas geometrias fornecidas e o caminho do arquivo raster.

    Args:
        geometrias (Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon]): Geometria(s) usada(s) para recortar o raster. 
            Pode ser uma GeoSeries, GeoDataFrame ou um objeto Polygon.
        raster_path (str): Caminho do arquivo raster a ser processado.

    Returns:
        Dict[str, Union[str, int, rio.crs.CRS, np.dtype, rio.Affine]]: Dicionário contendo os metadados do raster, como driver, altura, largura, CRS, tipo de dado e transformações.
    """
    with rio.open(raster_path) as src:
        crs = src.crs
        if isinstance(geometrias, (gpd.GeoSeries, gpd.GeoDataFrame, Polygon)):
            geometrias = gpd.GeoSeries([geometrias], crs='EPSG:4326').to_crs(src.crs) if isinstance(geometrias, Polygon) else geometrias.to_crs(src.crs)
            image, transform = mask.mask(src, geometrias.geometry, crop=True)
            
    meta = {
        "driver": "GTiff",
        "height": image[0].shape[0],
        "width": image[0].shape[1],
        "count": 1,
        "dtype": image.dtype,
        "crs": crs,
        "predictor": 1,
        "transform": transform,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
        "compress": "DEFLATE",
        "nodata": -9999
    }
    return meta


def find_href(
    item: object,  
    name: str
) -> Optional[str]:
    """
    Encontra o href de uma banda ou nome comum especificado em um item STAC.

    Args:
        item (object): Item STAC que contém as assets e metadados.
        name (str): Nome da banda ou nome comum a ser procurado.

    Returns:
        Optional[str]: O href da banda correspondente ou None se não for encontrado.
    """
    for band, asset in item.assets.items():
        if band == name:
            return asset.href
        if 'eo:bands' in asset.extra_fields and asset.extra_fields['eo:bands']:
            band_info = asset.extra_fields['eo:bands'][0]
            if 'common_name' in band_info and band_info['common_name'] == name:
                return asset.href
    return None


def cube_to_time_series(
    data_array: xr.DataArray, 
    bands: List[str], 
    time_coords: List[str]
) -> xr.DataArray:
    """
    Transforma um data cube em uma série temporal.

    Args:
        data_array (xr.DataArray): O array de dados contendo o data cube.
        bands (List[str]): Lista de bandas presentes no data cube.
        time_coords (List[str]): Lista de coordenadas de tempo para a série temporal.

    Returns:
        xr.DataArray: Um novo DataArray com os dados organizados como uma série temporal por banda e tempo.
    """
    band_ts_list = []
    aux_meta = data_array.attrs

    for i, band in enumerate(bands):
        band_data = data_array[i].values
        flattened_data = band_data.reshape(len(time_coords), -1).transpose(1, 0)
        
        ts_data = xr.DataArray(
            flattened_data,
            coords={"pixel": range(flattened_data.shape[0]), "time": time_coords, "band": band},
            dims=["pixel", "time"],
            name="TimeSeries"
        )
        band_ts_list.append(ts_data)
    
    combined_ts_data = xr.concat(band_ts_list, dim="band")
    combined_ts_data.attrs = aux_meta

    return combined_ts_data


def create_geometry_mask(
    filtered_shape: Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon], 
    transposed_cubo: xr.DataArray
) -> np.ndarray:
    """
    Cria uma máscara de geometria com base em uma forma filtrada e em um data cube transposto.

    Args:
        filtered_shape (Union[gpd.GeoSeries, gpd.GeoDataFrame, Polygon]): A geometria filtrada.
        transposed_cubo (xr.DataArray): O data cube contendo os atributos de transformação e dimensões.

    Returns:
        np.ndarray: A máscara criada a partir da geometria e do data cube.
    """
    mask_fora = geometry_mask(
        [filtered_shape], 
        transform=transposed_cubo.attrs['transform'], 
        invert=True, 
        out_shape=(transposed_cubo.attrs['height'], transposed_cubo.attrs['width'])
    ).flatten()
    
    return mask_fora


def process_cube(
    shapefile: gpd.GeoDataFrame,
    query_bands: List[str],
    start_date: str,
    end_date: str,
    collections: List[str],
    stac_url: str = 'https://data.inpe.br/bdc/stac/v1/',
    interpolate: bool = True
) -> xr.DataArray:
    """
    Processa um cubo de dados a partir de itens STAC e retorna o cubo transposto.

    Parâmetros:
    -----------
    shapefile_path : str
        O caminho para o shapefile contendo as geometrias.
    query_bands : List[str]
        Lista de nomes de bandas para consulta.
    start_date : str
        Data de início para consultar itens (formato 'YYYY-MM-DD').
    end_date : str
        Data de término para consultar itens (formato 'YYYY-MM-DD').
    collections : List[str]
        Lista de nomes de coleções para consultar no STAC.
    stac_url : str, opcional
        A URL da API STAC para conectar. Padrão é 'https://data.inpe.br/bdc/stac/v1/'.
    interpolate : bool, opcional
        Se deve realizar interpolação no cubo de dados. Padrão é True.

    Retorna:
    --------
    xr.DataArray
        O cubo de dados processado e transposto.
    """

    # ===========================
    # Lendo o shapefile e selecionando a geometria
    # ===========================
    start_time = time.time()
    geometria = shapefile.iloc[0].geometry
    xmin, ymin, xmax, ymax = geometria.bounds
    bbox = [xmin, ymin, xmax, ymax]

    # ===========================
    # Reprojetando a geometria para projeção Albers
    # ===========================
   
    albers_projection = (
        'PROJCS["unknown",GEOGCS["unknown",DATUM["Unknown based on GRS80 ellipsoid",'
        'SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]]],'
        'PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,'
        'AUTHORITY["EPSG","9122"]]],PROJECTION["Albers_Conic_Equal_Area"],'
        'PARAMETER["latitude_of_center",-12],PARAMETER["longitude_of_center",-54],'
        'PARAMETER["standard_parallel_1",-2],PARAMETER["standard_parallel_2",-22],'
        'PARAMETER["false_easting",5000000],PARAMETER["false_northing",10000000],'
        'UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    )
    geometria_albers = gpd.GeoSeries([geometria], crs="EPSG:4326").to_crs(albers_projection)

    # ===========================
    # Conectando ao STAC e pesquisando itens
    # ===========================
   
    client = connect_to_stac(stac_url)
    items = search_stac(client, start_date, end_date, collections, bbox=bbox)
    timestamp = get_timetamps(items)
    items_ = np.array(organize_items_by_time(items))

    # ===========================
    # Preparando os dados para processamento
    # ===========================
    x_data = {}

    for image_group in items_:
        date = image_group[0].datetime.strftime("%Y-%m-%d")
        x_data[date] = []
        # Se a geoemtria intersecta com mais de um tile
        for band in query_bands:
            if (len(image_group) > 1):
                cropped_rasters = [delayed(recortar_raster_multi)(geometria_albers, find_href(image, band)) for image in image_group]
                mosaic_task = delayed(merge_cropped_rasters)(cropped_rasters)
                x_data[date].append({str(band): mosaic_task})
            else:
                cropped_rasters = [delayed(recortar_raster)(geometria_albers, find_href(image, band)) for image in image_group]
                x_data[date].append({str(band): cropped_rasters})
   
    # ===========================
    # Construindo a série temporal
    # ===========================
    time_series = np.squeeze([[x_data[date][i][str(band)] for date in sorted(x_data.keys())] for i, band in enumerate(query_bands)])
    data_array = xr.DataArray(
        np.array(time_series, dtype=object),  # dtype=object para suportar objetos Dask
        coords={"band": query_bands, "time": sorted(x_data.keys())},
        dims=["band", "time"],
        name="DataCube"
    )
    
    # ===========================
    # Computando o cubo de dados
    # ===========================
    print(" Fazendo download do cubo de dados")
    tasks = [data_array.loc[band, data_array.time[0].values:data_array.time[-1].values].values for band in query_bands]
    tasks_flat = [item for sublist in tasks for item in sublist]

    with ProgressBar():
        computed_data = compute(*tasks_flat)

    # ===========================
    # Reconstruindo o cubo de dados
    # ===========================
    timeline_length = len(data_array.coords["time"])
    _data = np.array([computed_data[i:i + timeline_length] for i in range(0, len(computed_data), timeline_length)])

    datacube = xr.DataArray(
        _data,
        coords={
            "band": query_bands,
            "time": data_array.coords["time"],
            "y": range(_data.shape[2]),
            "x": range(_data.shape[3])
        },
        dims=["band", "time", "y", "x"],
        name="DataCube"
    )

    # ===========================
    # Obtendo metadados e configurando atributos
    # ===========================
    if (len(image_group) > 1):
        meta = meta_output(compute(*cropped_rasters))
        for key in meta[1].keys():
            datacube.attrs[key] = meta[1][key]
    
    else:
        meta = get_meta(geometria_albers, find_href(items_[0][0], query_bands[0]))
        for key in meta.keys():
            datacube.attrs[key] = meta[key]
        
    datacube.attrs['bbox'] = bbox
   

    # ===========================
    # Convertendo cubo para série temporal
    # ===========================
    ts = cube_to_time_series(datacube, datacube.coords['band'].values, datacube.coords['time'].values)
    cloud = ts.sel(band='SCL')
    ts = ts.drop_sel(band='SCL')
   

    # ===========================
    # Criando máscara da geometria
    # ===========================
  
    mask_fora = create_geometry_mask(geometria_albers[0], ts)


    # ===========================
    # Interpolando o cubo
    # ===========================
    print(" Iniciando a interpolação do cubo")
    start_time_2 = time.time()
    if interpolate:
        for i in range(ts.shape[0]):
            ts[i][mask_fora] = interpolate_mtx_numba(ts[i][mask_fora].values, cloud[mask_fora].values)
        tempo_execucao = time.time() - start_time_2
        print(f"Interpolação concluída em {tempo_execucao:.2f} segundos.")

    # ===========================
    # Transpondo o cubo de dados
    # ===========================
    
    transposed_cubo = ts.stack(band_time=("band", "time")).transpose("pixel", "band_time")
    tempo_execucao = time.time() - start_time
    print(f"Tempo final de conclusão: {tempo_execucao:.2f} segundos.")

    return transposed_cubo, mask_fora




def som_time_series_clustering(
    transposed_cubo: xr.DataArray, 
    mask_fora: Optional[np.ndarray] = None, 
    n: int = 3, 
    random_seed: int = 123, 
    n_parallel: int = 0, 
    training_steps: int = 50,
    result: bool = True
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """
    Realiza a clusterização SOM nas séries temporais do cubo de dados transposto.

    Parâmetros:
    -----------
    transposed_cubo : xr.DataArray
        Cubo de dados transposto contendo as séries temporais.
    mask_fora : Optional[np.ndarray], opcional
        Máscara booleana indicando os pixels a serem incluídos na clusterização.
        Se None, utiliza todos os dados.
    n : int, opcional
        Dimensão da grade SOM (n x n). Padrão é 3.
    random_seed : int, opcional
        Semente aleatória para reprodução dos resultados. Padrão é 123.
    n_parallel : int, opcional
        Número de threads paralelas a serem usadas. Padrão é 0 (sem paralelismo).
    training_steps : int, opcional
        Número de passos de treinamento. Padrão é 50.
    result : bool, opcional
        Se False, retorna apenas os neurônios e as previsões. Se True, retorna também a imagem resultante da clusterização.

    Retorna:
    --------
    Se result for True:
        result_image : np.ndarray
            Imagem com o resultado da clusterização SOM.
    neuron_weights : np.ndarray
        Pesos dos neurônios SOM após o treinamento.
    predictions : np.ndarray
        Previsões (clusters) para cada ponto da série temporal.
    """

  
    if mask_fora is None:
        time_series = transposed_cubo
    else:
        time_series = transposed_cubo[mask_fora]

  
    som = XPySom(n, n, time_series.shape[1], random_seed=random_seed, n_parallel=n_parallel)
    som.train(time_series, training_steps)

  
    neuron_weights = np.array([som.get_weights()[i][j] for i in range(n) for j in range(n)])


    predictions = som.winner(time_series)

   
    

  
    position = {(i, j): idx for idx, (i, j) in enumerate([(i, j) for i in range(n) for j in range(n)])}
    predictions = np.array([position[tuple(coord)] for coord in predictions]).astype("int")
    
    if not result:
        return neuron_weights, predictions

    
    result_image = np.full(transposed_cubo.attrs['height'] * transposed_cubo.attrs['width'], -9999)

    
    if mask_fora is not None:
        result_image[mask_fora] = predictions
    else:
        result_image = predictions

  
    return result_image.reshape(transposed_cubo.attrs['height'], transposed_cubo.attrs['width']), neuron_weights, predictions




def get_band_slice(
    train: np.ndarray, 
    band: str, 
    bands: List[str]
) -> np.ndarray:
    """
    Retorna uma fatia da matriz de dados de entrada correspondente à banda fornecida.

    Parameters:
    -----------
    train : np.ndarray
        A matriz de dados de entrada de forma (n_samples, n_features).
    band : str
        O nome da banda a ser extraída.
    bands : List[str]
        A lista de todos os nomes de bandas na matriz de dados de entrada.

    Returns:
    --------
    np.ndarray
        A fatia da matriz de dados de entrada correspondente à banda fornecida.
    """
    n_bands = len(bands)
    step = len(train[0]) // n_bands
    band_indices = dict(zip(bands, range(n_bands)))
    start, end = band_indices[band] * step, (band_indices[band] + 1) * step
    return train[:, start:end]

def plot_codebooks(
    cubo: xr.DataArray,
    neurons: np.ndarray,
    predictions: np.ndarray,
    band: str,
    n: int,
    mask: Optional[np.ndarray] = None
) -> None:
    """
    Analisar e plotar a banda específica dos dados de cubo e os pesos dos neurônios.

    Parameters:
    -----------
    cubo : xarray.DataArray
        O cubo de dados contendo dimensões 'band', 'time', e 'pixel'.
    neurons : np.ndarray
        A matriz de pesos dos neurônios de forma (n_samples, n_features).
    predictions : np.ndarray
        Array contendo as predições ou índices dos clusters para cada amostra.
    band : str
        A banda específica a ser analisada.
    n : int
        Número de clusters ou neurônios a serem plotados.
    mask : Optional[np.ndarray], opcional
        Um array booleano para filtrar os pixels correspondentes, por padrão None.

    Returns:
    --------
    None
        A função não retorna nada, apenas exibe os gráficos.
    """
    
    array = get_band_slice(neurons.astype("int16"), band, np.unique(cubo.band.values)) / 10000

    unique_predictions, counts = np.unique(predictions, return_counts=True)

    formatted_timestamps = [str(ts)[:10] for ts in np.unique(cubo.time.values)]

    fig, axs = plt.subplots(n, n, figsize=(16, 8), sharex=True, sharey=True)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(wspace=0.5)

    total_series = len(predictions)  

    for idx, ax in enumerate(axs.flat):
        if idx >= len(unique_predictions):
            ax.axis('off')  
            continue
        
        indices = np.where(predictions == unique_predictions[idx])[0]

        if mask is not None and np.any(mask):
            cluster_series = cubo.sel(band=band).values[mask][indices] / 10000
        else:
            cluster_series = cubo.sel(band=band).values[indices] / 10000
        
        ts_mean = np.mean(cluster_series, axis=0)
        std_devs = np.std(cluster_series, axis=0)
        upper_limit = ts_mean + std_devs
        lower_limit = ts_mean - std_devs

        ax.plot(ts_mean, color='red', linewidth=0.8, label="mean")
        ax.plot(array[idx], color='white', linewidth=2, label="codebook")

        ax.set_facecolor(cm.viridis(idx / (n*n-1)))
        ax.set_xticks(np.arange(0, len(array[idx]), 2))
        ax.set_xticklabels(formatted_timestamps[::2], rotation=45, ha='right', weight='light')
        ax.set_yticks(np.arange(-1, 1.2, 0.2))
        ax.grid(True, linestyle='--', color='white', linewidth=0.3)
        ax.axhline(0, color='white', linestyle='--', linewidth=0.3)

        percent_series = (counts[idx] / total_series) * 100


        ax.set_title(f"N° de séries temporais: {counts[idx]} ({percent_series:.2f}%)", color='black', fontsize=12, fontweight='bold')

        ax.fill_between(range(len(array[idx])), lower_limit, upper_limit, color='gray', alpha=0.9, linewidth=0, label="std")

        ax.legend()


    plt.tight_layout()
    plt.show()

    
def plot_cluster_image(cubo: xr.DataArray, predictions: List[int], result: np.ndarray, cmap: str = 'viridis') -> None:
    """
    Plota a imagem resultante da clusterização e adiciona uma legenda para os clusters.

    Parâmetros:
    -----------
    cubo : xr.DataArray
        O cubo de dados do tipo xarray contendo as dimensões e atributos (como bbox).
    predictions : List[int]
        Lista com as previsões (clusters) para cada pixel.
    result : np.ndarray
        O resultado da clusterização a ser plotado.
    cmap : str, opcional
        O colormap a ser utilizado no gráfico. Padrão é 'viridis'.

    Retorna:
    --------
    None
    """
 
    if not all(attr in cubo.attrs for attr in ['height', 'width', 'bbox']):
        raise ValueError("O cubo de dados precisa ter os atributos 'height', 'width' e 'bbox'.")
   
    height = cubo.attrs['height']
    width = cubo.attrs['width']
    bbox = cubo.attrs['bbox']

    fig, ax = plt.subplots(figsize=(20, 10))
    
    # Gerando os labels dos clusters
    height_class_labels = [("Cluster: " + str(neuron_index)) for neuron_index in list(np.unique(predictions))]
    
    
    image = ax.imshow(
        np.ma.masked_equal(result.reshape(height, width), -9999),
        extent=[bbox[0], bbox[2], bbox[1], bbox[3]], 
        cmap=cmap
    )
    

    for spine in ax.spines.values():
        spine.set_visible(False)
    
  
    ep.draw_legend(image, titles=height_class_labels)
  
    plt.show()


# ===========================================
# Definição de Funções
# ===========================================

def perform_clustering_dtw(
    dist_matrix: np.ndarray, 
    threshold: Optional[float] = None, 
    nclust: Optional[int] = None
) -> Optional[np.ndarray]:
    """
    Realiza o agrupamento aglomerativo utilizando uma matriz de distância DTW e 
    salva o dendrograma.

    Parâmetros:
    -----------
    dist_matrix : np.ndarray
        Matriz de distância (2D) entre as séries temporais.
    threshold : Optional[float], opcional
        Limite de distância para o dendrograma, por padrão None.
    nclust : Optional[int], opcional
        Número de clusters desejados, por padrão None. Se fornecido, `threshold` será ignorado.

    Retorna:
    --------
    Optional[np.ndarray]
        Array de rótulos dos clusters, ou None se a matriz de distância for inválida.
    """
    

    if dist_matrix.shape[0] > 0 and dist_matrix.shape[1] > 0 and not np.isnan(dist_matrix).all():
        
        dist_array = squareform(dist_matrix, checks=False)

  
        plt.figure(figsize=(18, 8))
        dendrogram = sch.dendrogram(sch.linkage(dist_array, method='average'), color_threshold=threshold, leaf_font_size=7)
        
  
        model = AgglomerativeClustering(n_clusters=nclust, metric='precomputed', linkage='average', distance_threshold=threshold)
        

        model.fit(dist_matrix)
        labels = model.labels_
        
        labels = np.append(labels, 255)
        
        
        plt.title(f"Número de grupos finais: {len(np.unique(labels[:-1]))} - Distância: {threshold}")
        if threshold:
            plt.axhline(y=threshold, color='r', linestyle='--')
        
        plt.show()
        
        return labels
    
    else:
       
        print("A matriz de distância DTW está vazia ou contém NaNs.")
        return None

@nb.njit(parallel=True)
def apply_labels_vector(predictions: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Aplica os rótulos aos predictions de forma paralela.

    Parâmetros:
    -----------
    predictions : np.ndarray
        Array de predições.
    labels : np.ndarray
        Array de rótulos.
    
    Retorna:
    --------
    output : np.ndarray
        Array com os rótulos aplicados.
    """
    n = predictions.shape[0]
    output = np.empty_like(predictions)
    for i in nb.prange(n):
        output[i] = labels[predictions[i]]
    return output

def plot_cluster_map(labels: np.ndarray, n: int, th: Optional[float] = None) -> None:
    """
    Plota um mapa de clusters com coloração viridis e rótulos sobrepostos.

    Parâmetros:
    -----------
    labels : np.ndarray
        Array 1D de rótulos que será remodelado para formar a matriz n x n.
    n : int
        O tamanho da matriz (n x n).
    th : Optional[float], opcional
        Threshold para exibir no título, se fornecido.
    """
    mlabels = labels.reshape(n, n)
    fig, ax = plt.subplots(figsize=(9, 9), sharey=True)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, str(mlabels[i][j]), va='center', ha='center', color='red')
    ax.imshow(mlabels, cmap='viridis', interpolation='none')
    ax.grid(True, which='both', color='grey', linestyle='-', linewidth=0.5)
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_xticks(np.arange(0, n, 1))
    ax.set_yticks(np.arange(0, n, 1))
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1.5)
    ax.grid(which='major', color='none')
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)
    ax.spines['left'].set_lw(1.5)
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['right'].set_lw(1.5)
    ax.spines['top'].set_lw(1.5)
    title = f"Número de grupos finais {len(np.unique(labels))}"
    if th is not None:
        title += f" - Distância: {th}"
    plt.title(title)
    plt.show()

def combine_colormaps(cmap_list: List[str], n_colors: int) -> ListedColormap:
    """
    Combina uma lista de colormaps (passados como nomes) para criar uma paleta com o número desejado de cores.

    Parâmetros:
    -----------
    cmap_list : List[str]
        Lista de nomes de colormaps a serem combinados.
    n_colors : int
        Número total de cores desejadas.

    Retorna:
    --------
    ListedColormap
        O colormap combinado.
    """
    colormaps = [plt.get_cmap(cmap_name) for cmap_name in cmap_list]
    colors_per_cmap = n_colors // len(colormaps)
    remaining_colors = n_colors % len(colormaps)
    combined_colors = np.vstack([
        cmap(np.linspace(0, 1, colors_per_cmap + (1 if i < remaining_colors else 0))) 
        for i, cmap in enumerate(colormaps)
    ])
    return ListedColormap(combined_colors)

def calculate_distance_matrix(weights: np.ndarray, series_length: int, num_series: int) -> np.ndarray:
    """
    Calcula a matriz de distância usando DTW ou outro método apropriado.

    Parâmetros:
    -----------
    weights : np.ndarray
        Pesos dos neurônios.
    series_length : int
        Comprimento das séries.
    num_series : int
        Número de séries.

    Retorna:
    --------
    np.ndarray
        Matriz de distância calculada.
    """
    dist_matrix = squareform(pdist(weights, metric='euclidean'))
    return dist_matrix



def plot_time_series_with_colormap(
    n: int, 
    labels: np.ndarray, 
    neuron_weights: np.ndarray, 
    band_name: str, 
    formulas: np.ndarray, 
    cmap_list: List[Colormap] = [plt.cm.viridis]  
) -> None:
    """
    Função para plotar séries temporais com colormap.

    Parâmetros:
    -----------
    n : int
        O número de neurônios na grade SOM (n x n).
    labels : np.ndarray
        Matriz de rótulos dos clusters (neurônios) que será usada para a plotagem.
    neuron_weights : np.ndarray
        Pesos dos neurônios SOM após o treinamento, contendo as séries temporais.
    band_name : str
        O nome da banda que será extraída dos pesos dos neurônios.
    formulas : np.ndarray
        Fórmulas ou bandas associadas ao cubo de dados, necessárias para `get_band_slice`.
    cmap_list : List[Colormap], opcional
        Lista de objetos de colormap a serem combinados para a visualização. Padrão é 'viridis'.
    
    Retorna:
    --------
    None
    """

   
    n_cores = len(np.unique(labels[:-1]))

  
    cmap = combine_colormaps(cmap_list, n_cores)


    time_series_aux = get_band_slice(neuron_weights, band_name, formulas) / 10000
    mlabels = labels[:-1].reshape(n, n)

 
    fig, axs = plt.subplots(n, n, figsize=(20, 12), sharey=True)

    for neuron_index, neuron in enumerate(time_series_aux):
        col1 = neuron_index % n
        row1 = neuron_index // n
        ax = axs[row1, col1]


        ax.plot(neuron, linewidth=2, color='white')

   
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
            spine.set_visible(False)

 
        ax.text(
            0.5, 0.5, str(mlabels[row1][col1]),
            color='red', fontsize=14, fontweight='bold',
            ha='center', va='center'
        )

     
        ax.set_facecolor(cmap.colors[mlabels[row1][col1]])


    plt.show()