

# def fun1(f):
#     if (f < 2000): return 1
#     if (2000<= f and f < 4000 ): return 5
#     if (4000<= f  ): return 10


import numpy as np

# n=[2.1457672119140625E-05*256.0,2.1457672119140625E-05*256.0]
#
# #n=[0.0054931640625, 0.0054931640625]
#
# x=(115.75623600509833, 115.77466800509833, 28.983383999947527, 29.001815999947528)
# y=(x[1]-x[0])/n[0]
# colMin,rowMin,colMax,rowMax,col_number,row_number,center_lat,center_lon
#  54528 9621 54784 9906 257 286 36.367548022 120.235020016
#37.1530704829 119.529148434

#print n

from osgeo import ogr
import os

shapefile = r"C:\Users\Administrator\PycharmProjects\untitled\Fisher.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()

layer.SetAttributeFilter("Label = 10")

# for feature in layer:
#     print feature.GetField("left")
feature=layer.GetFeature(10)
print feature.GetField("left")
# help(layer.GetFeature)