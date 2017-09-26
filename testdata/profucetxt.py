# -*- coding: utf-8 -*-

from osgeo import ogr
import os,sys
from osgeo import osr
import math

resolution=2.1457672119140625E-05
tileSize=resolution*256

wgs84prj='''GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]'''
#Shapefile = r"C:\Users\Administrator\PycharmProjects\untitled\Fisher.shp"



Shapefile = r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_1\qingdaoshi_201701.shp"
def cal_tile_row_col(envelope):
    rowMin = int(math.floor((90 - envelope[3]) / tileSize))
    colMin = int(math.floor((180 + envelope[0]) / tileSize))
    rowMax = int(math.ceil((90 - envelope[2]) / tileSize))
    colMax = int(math.ceil((180 + envelope[1]) / tileSize))

    col_number = colMax - colMin+1
    row_number = rowMax - rowMin+1

    # 计算shp的四至范围的中心坐标
    center_lat = (envelope[3] + envelope[2]) / 2.0
    center_lon = (envelope[1] + envelope[0]) / 2.0

    return {"colMin":colMin, "rowMin":rowMin, "colMax":colMax, "rowMax":rowMax,
           "col_number":col_number, "row_number":row_number, "center_lat":center_lat,
            " center_lon":center_lon}

driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(Shapefile, 1) # 0 means read-only. 1 means writeable.

#计算变化矢量中每个geometry 的四至将其获得 的瓦片行列号写入txt文本中
dataSourceChange = driver.Open(Shapefile, 1)
layerChange = dataSourceChange.GetLayer()
f=open('colrowchange.txt','w')
for featureC in layerChange:
    geom = featureC.GetGeometryRef()
    env = geom.GetEnvelope()
    # print "minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3])
    colrow=cal_tile_row_col(env)
    for x in range(0,colrow["col_number"]):
        for y in range(0, colrow["row_number"]):
            f.write(str(colrow["colMin"]+x)+","+str(colrow["rowMin"]+y)+"\n")
f.close()

for featureC in layerChange:
    geom = featureC.GetGeometryRef()
    env = geom.GetEnvelope()
    # print "minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3])
    colrow=cal_tile_row_col(env)
    for x in range(0,colrow["col_number"]):
        for y in range(0, colrow["row_number"]):
            f.write(str(colrow["colMin"]+x)+","+str(colrow["rowMin"]+y)+"\n")
f.close()