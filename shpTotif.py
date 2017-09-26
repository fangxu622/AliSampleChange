# -*- coding: utf-8 -*-

from osgeo import gdal, ogr

# Define pixel_size and NoData value of new raster
pixel_size = 2.1457672119140625E-05
#y_res = 2.1457672119140625E-05

NoData_value = 0

# Filename of input OGR file
#vector_fn = r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_1\qingdaoshi_201701.shp"
vector_fn=r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_2\qingdaoshi.shp"
# Filename of the raster Tiff that will be created
raster_fn = r'D:\QD\qingdaoChange.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

ss=source_layer.GetSpatialRef()
# Create the destination data source
raster_width= int((x_max - x_min) /pixel_size)
raster_height = int((y_max - y_min) / pixel_size)

target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, raster_width, raster_height, 1, gdal.GDT_Byte)

target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

target_ds.SetProjection(str(ss))

band = target_ds.GetRasterBand(1)
#band.SetNoDataValue(NoData_value)

# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[255])