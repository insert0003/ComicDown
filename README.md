## 说明
原本这些代码是自己使用的，没有做过任何整理。
当有人说想用的时候，发现太乱了，所以做一些说明。
其实个人比较懒，如果大家有想法可以修改合并。

## 使用之前
使用“getComic.py”之前，需要安装以下的库。
<pre>
pip install BeautifulSoup4
pip install lxml
</pre>

使用“kcc”进行漫画转换之前，需要安装以下的库。
<pre>
pip install psutil
pip install python-slugify
pip install Pillow
</pre>

下载kcc
<pre>
git clone https://github.com/ciromattia/kcc.git
</pre>
### Windows
设置本目录和Python的目录到Path环境变量
C:\Users\tte\AppData\Local\Programs\Python\Python36-32\;
C:\Users\tte\AppData\Local\Programs\Python\Python36-32\Scripts\;

### Linux
拷贝kindlegen到/usr/bin目录


## 下载漫画
通过下面命令可以从"comic.txt"里面，获取漫画地址,开始话,结束话
然后下载到本地文件夹中。
写法(忽略加号)： 漫画网址+空格+开始话+空格+结束话

<pre>
python getComic.py
</pre>

## 转换漫画
### Ｗindows
<pre>
python kcc/kcc-c2e.py -n 2 download/漫画名字
</pre>

### Linux
<pre>
python3 kcc/kcc-c2e.py -n 2 download/漫画名字
</pre>
