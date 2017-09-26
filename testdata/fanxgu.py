
import urllib2

tileurl="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201701_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=1216&TILECOL=6847&FORMAT=image%2Fjpeg"

turl="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201702_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=9623&TILECOL=54530&FORMAT=image%2Fjpeg"

turl1="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201702_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=14&TILEROW=4908&TILECOL=27339&FORMAT=image%2Fjpeg"

turl2="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201702_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=54662&TILECOL=9622&FORMAT=image%2Fjpeg"
#54662_9622

turl3="http://123.56.192.226:7090/onemap/rest/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=201701_all&STYLE=default&TILEMATRIXSET=matrix_id&TILEMATRIX=15&TILEROW=9622&TILECOL=54662&FORMAT=image%2Fjpeg"
res = urllib2.urlopen(turl3)
#help(res)
#res = urllib2.urlopen('')
f = open('f8.jpg',"wb")

print res.info
#req = urllib2.Request(turl1)
img=res.read()

print len(img)
print len(res.read()),res.getcode()
#print type(len(res.read()))
#l=len(res.read())
#print l
# if(16730>=100):
#     print "x"
# else:
#     print "y"
f.write(img)
# print res.read()==None
f.close()



#help(res.read)


