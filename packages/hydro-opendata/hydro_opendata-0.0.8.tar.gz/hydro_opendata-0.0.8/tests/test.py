import sys
sys.path.append('..')
import numpy as np
# import geopandas as gpd
# aoi = gpd.read_file('test.geojson')
# print(aoi)

print("--------------------catalog------------------")

# from hydro_opendata.catalog.minio import ERA5LCatalog
# catalog = ERA5LCatalog()
# print(catalog.datasets)

print("--------------------reader------------------")

# from hydro_opendata.reader.minio import GPMReader
# gpm = GPMReader()
# start_time=np.datetime64("2023-06-01T00:00:00.000000000")
# end_time=np.datetime64("2023-06-30T23:30:00.000000000")
# bbox=(-123,39,-121,40)
# g1 = gpm.open_dataset(start_time=start_time, end_time=end_time, dataset='camels', bbox=bbox, time_resolution='30m')
# print(g1)

from hydro_opendata.reader.minio import ERA5LReader
reader = ERA5LReader()
start_time=np.datetime64("2018-08-20T00:00:00.000000000")
end_time=np.datetime64("2018-08-20T23:30:00.000000000")
bbox=(115.4,45.1,115.4,45.1)
e1 = reader.open_dataset(
    data_variables=['Total precipitation'],
    start_time=start_time, 
    end_time=end_time, 
    dataset='wis', 
    bbox=bbox)
print(e1.values)