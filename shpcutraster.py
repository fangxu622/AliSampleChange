# -*- coding: utf-8 -*-

import os,sys
from osgeo import osr,gdal,gdalnumeric,ogr
import math
import urllib2
import cv2

shpath=r"C:\Users\Administrator\PycharmProjects\untitled\qingdaofisher.shp"
tileurl1="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201701_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=tile&TILECOL=tile&FORMAT=image%2Fjpeg"
tileurl2="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201702_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=tile&TILECOL=tile&FORMAT=image%2Fjpeg"
resolution=2.1457672119140625E-05
tileSize=resolution*256
driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(shpath, 1)

fisher_layer = dataSource.GetLayer()
#从shp里面读取的四至范围顺序是left(minX)0 ,right(maxX)1,bottom(minY)2,top(maxY)3
fisher_extent = fisher_layer.GetExtent()

fisher_width= int((fisher_extent[1]-fisher_extent[0])/tileSize)
fisher_height= int((fisher_extent[3]-fisher_extent[2])/tileSize)

print fisher_width,fisher_height
ds = gdal.Open(r'D:\QD\qingdaoChange.tif')

para_transform=ds.GetGeoTransform()#SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

#
dif_width=int(round((para_transform[0]-fisher_extent[0])/resolution))
dif_height=int(round((fisher_extent[3]-para_transform[3])/resolution))

#从第二行第二列起算
pixel_start_col=256-dif_width
pixel_start_row=256-dif_height

print para_transform,dif_width,dif_height
label_path=r"D:\QD\change\label"

srcArray = gdalnumeric.LoadFile(r'D:\QD\qingdaoChange.tif')
from skimage import io
print "开始生成图片与label"
image_time1_path_change = r"D:\QD\change\time1"
image_time2_path_change = r"D:\QD\change\time2"
image_time1_path_NO_change = r"D:\QD\NoChange\time1"
image_time2_path_NO_change = r"D:\QD\NoChange\time2"
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
for row_i in range(1,fisher_height):
    for col_j in range(1,fisher_width):
        #计算渔网feature ID
        FID=fisher_width*row_i+col_j
        #读取该ID 的瓦片行列号
        feature=fisher_layer.GetFeature(FID)
        tile_col=feature.GetField("col")
        tile_row=feature.GetField("row")
        label_numpy=srcArray[pixel_start_row+(row_i-1)*256:pixel_start_row+row_i*256,pixel_start_col+(col_j-1)*256:pixel_start_col+col_j*256]
        send_tile_url1 = tileurl1.replace("TILEROW=tile&TILECOL=tile",
                                    "TILEROW=" + str(tile_row) +"&"+ "TILECOL=" + str(tile_col))
        send_tile_url2 = tileurl2.replace("TILEROW=tile&TILECOL=tile",
                                     "TILEROW=" + str(tile_row) +"&"+ "TILECOL=" + str(tile_col))
        if(255 in label_numpy):
            cv2.imwrite(label_path+"\\"+str(tile_col)+"_"+str(tile_row)+"label.png",label_numpy)
            res1 = urllib2.urlopen(send_tile_url1)
            res2 = urllib2.urlopen(send_tile_url2)
            f1 = open(image_time1_path_change+"\\"+str(tile_col)+"_"+str(tile_row)+'_t1.jpg', "wb")
            f2 = open(image_time2_path_change + "\\"+str(tile_col) + "_" + str(tile_row) + '_t2.jpg', "wb")
            f1.write(res1.read())
            f2.write(res2.read())
            f1.close()
            f2.close()
        else:
            request3 = urllib2.Request(send_tile_url1, headers=headers)
            res3 = urllib2.urlopen(request3)
            img3=res3.read()
            # try:
            #     res3 = urllib2.urlopen(send_tile_url1)
            # except urllib2.HTTPError, e:
            #     print res3.code
            #     print res3.reason
            #     print res3.geturl()
            request4 = urllib2.Request(send_tile_url2, headers=headers)
            res4 = urllib2.urlopen(request4)
            img4 = res4.read()
            #nochange_count=nochange_count+1
            #if (nochange_count % 500 == 0): print "nochange_count=", nochange_count
            if(len(img3)>=500):
                f3 = open(image_time1_path_NO_change + "\\" + str(tile_col) + "_" + str(tile_row) + '_t1_n.jpg', "wb")
                f3.write(img3)
                f3.close()
            if(len(img4)>=500):
                f4 = open(image_time2_path_NO_change + "\\" + str(tile_col) + "_" + str(tile_row) + '_t2_n.jpg', "wb")
                f4.write(img4)
                f4.close()
        if (FID %500==0):
            print "FID = ",FID


# srcArray = gdalnumeric.LoadFile('qingdaoChange.tif')
#
# ds = gdal.Open('qingdaoChange.tif')
#
# #获得图像四至范围
# #SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
#
# print ds.GetGeoTransform(),type(srcArray)
# #help(ds.RasterIo)