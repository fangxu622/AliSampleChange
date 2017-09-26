##
##项目流程图

https://www.processon.com/view/link/59c63065e4b0ef561373f656

背景：在这个程序里面，只提取两米分辨率的15级瓦片。瓦片大小为256*256

程序输入文件：变化矢量图框，前后期的WMTS服务

程序输出：变化的label 图片，以及对应的前后期瓦片，非变化 前后期瓦片


envelope1.py 根据变化矢量BBOX 生成该范围内的渔网shapefile.

shpTotif.py 将变化矢量栅格化，得到二值图像 ，0 非变化，255变化
其他python 文件均为测试文件

shpcuraster.py 输入变化渔网shapefile 文件，与变化矢量的栅格化图像，,前后期瓦片url，
输出 变化的label 图片，以及对应的前后期瓦片，非变化 前后期瓦片




最后顺便写一下.gitignore 规则

```
# 此为注释 – 将被 Git 忽略

*.a       # 忽略所有 .a 结尾的文件
!lib.a    # 但 lib.a 除外
/TODO     # 仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
build/    # 忽略 build/ 目录下的所有文件
doc/*.txt # 会忽略 doc/notes.txt 但不包括 doc/server/arch.txt

```
