import json
import os
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
O=json.load(open(B+'deck/order.json'))
D=json.load(open(B+'v2/slides5.json'));S={s['n']:s for s in D}
S[2]['b'][2][1]='ההמלצה: למצב אתכם כבית של Archi בישראל.'
def nb(x):
  if isinstance(x,str): return x.replace(' ₪',' ₪')
  if isinstance(x,list): return [nb(y) for y in x]
  if isinstance(x,dict): return {k:nb(v) for k,v in x.items()}
  return x
try: MJ=json.load(open(B+'web/mj.json'))
except Exception: MJ={}
TILES={3:['Rj4','R13','Pool2','Rj1'],8:['Rj5','R16','R12','R21'],21:['P01','Pool1','R11'],25:['R22','R04','R02'],26:['N31','R13','R23']}
DARK_TABLES={7,11,15,23,27,29,38,40,46}
out=[]
for o in O:
  n=o.get('n');L=o['layout'];s=dict(o)
  for k in ('x','y','hb','fy','ih','iw','name'): s.pop(k,None)
  if n: s['b']=S[n]['b'] if 'b' not in s and L not in('cards','creative') else s.get('b')
  img=o.get('hero') or o.get('img')
  if L=='cover': s.update(kind='cover',img='R23')
  elif L=='chapter': s.update(kind='chapter')
  elif L=='location': s.update(kind='location')
  elif L=='closing': s.update(kind='closing',img='R22')
  elif n in TILES:
    s.update(kind='tiles',theme='dark',imgs=MJ.get('tiles',{}).get(str(n),TILES[n]))
  elif n in (4,6,42):
    s.update(kind='hero',img={4:'R04',6:'R23',42:'R21'}[n])
    b=S[n]['b']
    if n==4:
      s['chips']=[['20%','מהשוק בגאורגיה, מאז 2006'],['51','פרויקטים שהושלמו, 32 בביצוע'],['53,000','דיירים']]
      s['band']=[['3,002',b[2][1]],['TRUMP · HILTON',b[3][1]],['$1,600–5,500',b[4][1]]];s['note']=b[5][1]
    if n==6:
      s['chips']=[['300','מיליון דולר השקעה'],['66,400','דולר, מחיר סטודיו התחלתי'],['10/30/60','תשלומים בשלבים'],['2031','מסירה']]
      s['band']=[['ARCHI & NEXT',b[0][1]],['10/30/60',b[1][1]],['50',b[2][1]]];s['more']={'title':'מידע נוסף','b':b[3:]}
    if n==42:
      s['chips']=[['22','עסקאות בחודש ב־100,000 ₪'],['3,300','₪ לעסקה כדי להגיע ל־30'],['135,000','₪ תקציב חודשי ל־30 עסקאות']]
      s['band']=[['100,000 ₪',b[0][1]],['30',b[1][1]],['רבעון או שנה',b[2][1]]]
    s.pop('nums',None)
  elif L=='cards':
    s.update(kind='panels',theme='cream',img=img)
  elif L=='creative':
    s.update(kind='creative',theme='cream',b=S[n]['b'])
  elif L=='quote': s.update(kind='quote',theme='cream',img=img)
  elif L=='chart': s.update(kind='chart',theme='cream',img=img)
  elif L=='table': s.update(kind='table',theme='dark' if n in DARK_TABLES else 'cream',img=img)
  elif L=='stats':  # 9
    s.update(kind='list',theme='dark',img=img,rownums=['21','442,847','86%','',''])
  else:
    s.update(kind='list',theme='dark',img=img)
  if str(n) in MJ and s['kind'] not in ('tiles',): s['img']=MJ[str(n)]
  if n==48: s.update(kind='panels',theme='cream',items=[{'h':x[1].split(': ')[0],'b':x[1].split(': ',1)[1],'n':'%02d'%(i+1)} for i,x in enumerate(S[48]['b'])],cols=3)
  if n==9: s.pop('nums',None)
  s.pop('hero',None);s.pop('layout',None)
  out.append(s)

# split dense slides for breathing room
import copy
SPLIT={10:'mj/s10_2.jpg',14:'mj/s09_0.jpg',15:'mj/window_3.jpg',45:'mj/s45_3.jpg',46:'mj/blocks_0.jpg',11:'mj/s11_0.jpg',36:'mj/suite_0.jpg',38:'mj/s38_3.jpg',39:'mj/s09_1.jpg',43:'mj/phone_1.jpg'}
res=[]
for s in out:
  n=s.get('n')
  if n in SPLIT:
    b=s['b'];a=copy.deepcopy(s);c=copy.deepcopy(s)
    if n in (11,39):
      a['b']=b[:1];c['b']=b[1:];c['kind']='list';c['theme']='cream'
    elif n==43:
      tb=b[0];a['b']=[[tb[0],tb[1],tb[2][:4]]];c['b']=[[tb[0],tb[1],tb[2][4:]]]+b[1:]
    elif n in (15,46,36,38):
      tb=b[0];k=(len(tb[2])+1)//2
      a['b']=[[tb[0],tb[1],tb[2][:k]]];c['b']=[[tb[0],tb[1],tb[2][k:]]]
    elif n==10:
      a['b']=b[:1];c['b']=b[1:];c['kind']='list'
    elif n==14:
      a['b']=b[:2];c['b']=b[2:];c['kind']='list'
    elif n==45:
      a['b']=b[:3];c['b']=b[3:]
    c['img']=SPLIT[n];c['g']='המשך';c['cont']=1
    res+= [a,c]
  else: res.append(s)
out=res
# chapter images
for s in out:
  if s['kind']=='chapter' and str(s.get('num')) in MJ.get('ch',{}): s['img']=MJ['ch'][s['num']]
json.dump(nb(out),open(B+'web/slides.json','w'),ensure_ascii=False)
from collections import Counter
print(len(out),Counter(x['kind'] for x in out))
print([(x.get('n'),x['kind'],x.get('theme'),x.get('img')) for x in out])
