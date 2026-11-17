import json
import os
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
s=open(B+'web/deck3_src.html').read()
d=open(B+'web/slides.json').read()
s=s.replace('const DATA=/*DATA*/[];','const DATA='+d+';').replace('/*MATADOR*/',open(B+'fonts/matador.css').read())
open(B+'web/deck3.html','w').write(s);print(len(s))
# publish: wrap and copy to the repo root (served by GitHub Pages)
root=os.path.dirname(B.rstrip('/'))
h=s.replace('<title>Kobuleti · תוכנית אסטרטגית</title>','<title>Archi Presentation · Kobuleti</title>',1)
h='<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+h+'\n</html>\n'
open(os.path.join(root,'index.html'),'w').write(h);print('wrote',os.path.join(root,'index.html'))
