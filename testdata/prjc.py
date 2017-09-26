# -*- coding: utf-8 -*-

from osgeo import ogr
import os

wgs84prj='''GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'''
# Get a Layer's Extent
inShapefile = r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_1\qingdaoshi_201701.shp"
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()
extent = inLayer.GetExtent()

# Create a Polygon from the extent tuple
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(extent[0],extent[2])
ring.AddPoint(extent[1], extent[2])
ring.AddPoint(extent[1], extent[3])
ring.AddPoint(extent[0], extent[3])
ring.AddPoint(extent[0],extent[2])
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

# Save extent to a new Shapefile
outShapefile = r"C:\Users\Administrator\Downloads\青岛变化图斑\Qingdao_whole_1\qdextent.shp"
outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Remove output shapefile if it already exists
if os.path.exists(outShapefile):
    outDriver.DeleteDataSource(outShapefile)

# Create the output shapefile
outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("states_extent", geom_type=ogr.wkbPolygon)

# Add an ID field
idField = ogr.FieldDefn("id", ogr.OFTInteger)
outLayer.CreateField(idField)

# Create the feature and set values
featureDefn = outLayer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
feature.SetGeometry(poly)
feature.SetField("id", 1)
outLayer.CreateFeature(feature)
feature = None

# Save and close DataSource
inDataSource = None
outDataSource = None

# from osgeo import ogr, osr
#
# spatialRef = osr.SpatialReference()
# spatialRef.ImportFromEPSG(4326)
#
# spatialRef.MorphToESRI()
# file = open('qdextent.prj', 'w')
# file.write(spatialRef.ExportToWkt())
# file.close()
#
# driver = ogr.GetDriverByName('ESRI Shapefile')
# outDataSet = driver.CreateDataSource('1.shp')
# outLayer = outDataSet.CreateLayer("basemap_4326",srs="4326", geom_type=ogr.wkbMultiPolygon)