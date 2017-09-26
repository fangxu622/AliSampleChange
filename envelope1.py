# -*- coding: utf-8 -*-

from osgeo import ogr
import os,sys
import math

resolution=2.1457672119140625E-05
tileSize=resolution*256

wgs84prj='''GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]'''
#Shapefile = r"C:\Users\Administrator\PycharmProjects\untitled\Fisher.shp"

Shapefile=r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_2\qingdaoshi.shp"

#Shapefile1 = r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_1\qingdaoshi_201701.shp"
def cal_tile_row_col(envelope):
    rowMin = int(math.floor((90 - envelope[3]) / tileSize))
    colMin = int(math.floor((180 + envelope[0]) / tileSize))
    rowMax = int(math.ceil((90 - envelope[2]) / tileSize))
    colMax = int(math.ceil((180 + envelope[1]) / tileSize))

    col_number = colMax - colMin
    row_number = rowMax - rowMin

    # 计算shp的四至范围的中心坐标
    center_lat = (envelope[3] + envelope[2]) / 2.0
    center_lon = (envelope[1] + envelope[0]) / 2.0

    return {"colMin":colMin, "rowMin":rowMin, "colMax":colMax, "rowMax":rowMax,
           "col_number":col_number, "row_number":row_number, "center_lat":center_lat,
            " center_lon":center_lon}

driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(Shapefile, 1) # 0 means read-only. 1 means writeable.

#计算变化矢量中每个geometry 的四至将其获得 的瓦片行列号写入txt文本中
# dataSourceChange = driver.Open(Shapefile, 1)
# layerChange = dataSourceChange.GetLayer()
# f=open('colrow.txt','w')
# for featureC in layerChange:
#     geom = featureC.GetGeometryRef()
#     env = geom.GetEnvelope()
#     # print "minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3])
#     colrow=cal_tile_row_col(env)
#     for x in range(0,colrow["col_number"]):
#         for y in range(0, colrow["row_number"]):
#             f.write(str(colrow["colMin"]+x)+","+str(colrow["rowMin"]+y)+"\n")
# f.close()
    #print (env[0], env[2], env[1], env[3])

    #Check to see if shapefile is found.
if dataSource is None:
    print 'Could not open %s' % (Shapefile)
else:
    print 'Opened %s' % (Shapefile)
    layer = dataSource.GetLayer()
    featureCount = layer.GetFeatureCount()
    print "Number of features in %s: %d" % (os.path.basename(Shapefile),featureCount)

layer = dataSource.GetLayer()
extent = layer.GetExtent()
featureCount = layer.GetFeatureCount()
print extent,featureCount
print "*********"


#从shp里面读取的四至范围顺序是left(minX)0 ,right(maxX)1,bottom(minY)2,top(maxY)3

#根据四至范围计算最大最小行列号及行列数量

print "tilesize=",tileSize

rowMin=int(math.floor((90-extent[3]) / tileSize))
colMin=int(math.floor((180+extent[0]) / tileSize))
rowMax=int(math.ceil((90-extent[2]) / tileSize))
colMax=int(math.ceil((180+extent[1]) / tileSize))


col_number=colMax-colMin
row_number=rowMax-rowMin

#计算shp的四至范围的中心坐标
center_lat=(extent[3]+extent[2]) / 2.0
center_lon=(extent[1]+extent[0]) / 2.0

print colMin,rowMin,colMax,rowMax,col_number,row_number,center_lat,center_lon

#根据中心以及 行列数量开始生成渔网 推算左上角坐标
# if (row_number % 2==0): #偶数情况
#     left_top_lat=center_lat+tileSize*(row_number/2);
# else: #奇数情况
#     left_top_lat = center_lat + tileSize * (row_number/2+0.5);
#
# if (col_number % 2 == 0):  # 偶数情况
#     left_top_lon = center_lon - tileSize * (col_number/2);
# else:  # 奇数情况
#     left_top_lon = center_lon - tileSize * (col_number/2+0.5);
left_top_lat=90-rowMin*tileSize
left_top_lon=colMin*tileSize-180
#生成渔网

outShapefile="qingdaofisher.shp"
outDriver=ogr.GetDriverByName("ESRI Shapefile")

if os.path.exists(outShapefile):
    outDriver.DeleteDataSource(outShapefile)

outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("qingdaofisher", geom_type= ogr.wkbPolygon)
featureDefn = outLayer.GetLayerDefn()

outLayer.CreateField(ogr.FieldDefn("left", ogr.OFTReal))
outLayer.CreateField(ogr.FieldDefn("right", ogr.OFTReal))
outLayer.CreateField(ogr.FieldDefn("top", ogr.OFTReal))
outLayer.CreateField(ogr.FieldDefn("bottom", ogr.OFTReal))

outLayer.CreateField(ogr.FieldDefn("col", ogr.OFTInteger))
outLayer.CreateField(ogr.FieldDefn("row", ogr.OFTInteger))


for i in range(0,row_number,1):
    if (i % 50==0):
        print i
    for j in range(0,col_number,1):
        # Create a Polygon from the extent tuple
        poly = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(left_top_lon+j*tileSize, left_top_lat-i*tileSize)
        ring.AddPoint(left_top_lon+(j+1)*tileSize, left_top_lat-i*tileSize)
        ring.AddPoint(left_top_lon+(j+1)*tileSize, left_top_lat-(i+1)*tileSize)
        ring.AddPoint(left_top_lon+j*tileSize, left_top_lat-(i+1)*tileSize)
        ring.AddPoint(left_top_lon+j*tileSize, left_top_lat-i*tileSize)
        poly.AddGeometry(ring)

        # create the feature
        outFeature = ogr.Feature(featureDefn)
        # Set the attributes using the values from the delimited text file
        outFeature.SetField("left",left_top_lon+j*tileSize)
        outFeature.SetField("Right", left_top_lon+(j+1)*tileSize)
        outFeature.SetField("top", left_top_lat-i*tileSize)
        outFeature.SetField("bottom", left_top_lat-(i+1)*tileSize)
        outFeature.SetField("col",colMin+j)
        outFeature.SetField("row",rowMin+i)
        outFeature.SetGeometry(poly)
        outLayer.CreateFeature(outFeature)
        outFeature = None
outDataSource = None

#生成prj文件
file = open('qingdaofisher.prj', 'w')
file.write(wgs84prj)
file.close()



print left_top_lat,left_top_lon



