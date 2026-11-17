import json,re
import os
B=os.path.dirname(os.path.abspath(__file__))+'/'
d=json.load(open(B+'slides.json'))

def S(n):
  return [s for s in d if s.get('n')==n]

def walk(x,f):
  if isinstance(x,str): return f(x)
  if isinstance(x,list): return [walk(y,f) for y in x]
  if isinstance(x,dict): return {k:(v if k in('img','imgs','kind','theme') else walk(v,f)) for k,v in x.items()}
  return x

# ---------- specific text edits (before global replaces) ----------
def setb(n,old,new,count=1):
  hit=0
  for s in S(n):
    def f(x):
      nonlocal hit
      if old in x: hit+=1; return x.replace(old,new)
      return x
    for k in list(s.keys()):
      if k in('img','imgs','kind','theme'): continue
      s[k]=walk(s[k],f)
  assert hit>=1,(n,old)

for s in S(3): s.pop('g',None)
setb(3,'30 עסקאות ב־Kobuleti,','30 עסקאות בחודש ב־Kobuleti,')
setb(8,'אתם מוכרים יזם אחד,','אתם המקור,')
setb(8,'עלול לייצר חיכוך מול היזם עצמו','עלול לייצר חיכוך מול המתווכים האחרים')
setb(10,'שני הזולים מבטיחים הכנסה:','שני הסרטונים הזולים מבטיחים הכנסה:')
setb(10,'וטיסה וביקור באתר על חשבון החברה','⟦וטיסה וביקור באתר על חשבון החברה⟧')
setb(13,'לכבות:','המלצה לכבות:')
setb(13,'להוסיף:','המלצה להוסיף:')
setb(22,'ובדרך כלל באותו מחיר יזם. אף אחד מהם לא יכול להציע את המשרד של אחד ממייסדי Archi ושותפיה.',
        'ובדרך כלל באותו מחיר. אבל אף אחד מהם לא יכול להתחרות במקור: מי שממוצב וממותג כאחד ממייסדי Archi ושותפיה העולמיים.')
setb(22,'מי שקונה כאן, קונה מהיזם','מי שקונה כאן, קונה מהמקור')
setb(22,'דרך המייסד שלו','דרך אחד ממייסדי Archi')
for s in S(23): s.pop('g',None)
setb(25,"חלופה א' (מומלצת)","חלופה א'")
setb(25,'עכשיו גם בהרצליה','מחכה לכם לפגישה בהרצליה')
setb(42,'ההחלטה הראשונה היא על איזו תקופה מדובר.','היעד הוא 30 עסקאות בחודש, וכך הוא מתיישב עם התקציב.')
setb(42,'החשבון של 30 עסקאות','החשבון של 30 עסקאות בחודש')
setb(43,'לידים נדרשים ל־30 עסקאות','לידים נדרשים ל־30 עסקאות בחודש')
setb(43,'מגיעים ל־30 עסקאות.','מגיעים ל־30 עסקאות בחודש.')
setb(44,'ו־30 עסקאות לפי התקופה שתוגדר.','ו־30 עסקאות בחודש.')
setb(48,'"משקיע מתאים" לפי הון עצמי, ','')
setb(46,'(שקפים 36 ו־37)','(שקף 36)')
# slide 42: drop the period paragraph and its band
for s in S(42):
  s['b']=[x for x in s['b'] if 'אם 30 הוא יעד לרבעון' not in x[1]]
  if s.get('band'): s['band']=[x for x in s['band'] if x[0]!='רבעון או שנה']
# slide 31: drop format + visual paragraphs
for s in S(31):
  s['b']=[x for x in s['b'] if not (x[1].startswith('פורמט:') or x[1].startswith('ויזואל:'))]
# slide 14 disclaimer (on the table part)
for s in S(14):
  if any(x[0]=='tb' for x in s['b']): s['b'].append(['n','* לא התקבלו נתוני סגירה.'])
# slide 15 asterisk + disclaimer
for s in S(15):
  t=json.dumps(s['b'],ensure_ascii=False)
  if 'כל הסרטונים הם מני מול המצלמה' in t:
    s['b']=json.loads(t.replace('כל הסרטונים הם מני מול המצלמה','כל הסרטונים הם מני מול המצלמה*'))
  s['b'].append(['n','* שינוי הפורמט: פרזנטור במקום מני.'])
# slide 5 sources
for s in S(5):
  s['b']=[x for x in s['b'] if 'העסקה הממוצעת' not in x[1]]
  for x in s['b']:
    if x[1].startswith('בטביליסי:'): x[1]='בטביליסי: 10% מהמכירות ב־2024, 11% בארבעת החודשים הראשונים של 2025, ו־12% בשבעת החודשים הראשונים של 2025.'
  s['bars']=[{'v':10,'l':'2024'},{'v':11,'l':'ינואר עד אפריל 2025'},{'v':12,'l':'ינואר עד יולי 2025','hi':1}]
  s['b'].append(['n','מקורות: Galt & Taggart, דוחות שוק הדיור בטביליסי (יוני וספטמבר 2025) ובבטומי (אפריל 2026). נתון 2,000 הרוכשים: מני בניש, מעריב, אוקטובר 2026.'])
# location tags off
for s in d:
  if s['kind']=='location': s['tags']=[]

# ---------- creatives: title + creative only ----------
ADS={32:[('מודעה A: היזם הגדול בגאורגיה','cr/32a.jpg'),('מודעה B: 53,000 דיירים','cr/32b.jpg')],
     33:[('מודעה A: Swissôtel על הים השחור','cr/33a_v2.jpg'),('מודעה B: מלון חמישה כוכבים','cr/33b.jpg')],
     34:[('מודעה A: עדיין חושבים על גאורגיה?','cr/34a.jpg'),('מודעה B: צעד אחד מדירה','cr/34b.jpg')],
     35:[('מודעה A: ההזמנה לאירוע ההשקה','cr/35a.jpg'),('מודעה B: חבר מביא חבר','cr/35b.jpg'),('מודעה C: כבר השקעתם בגאורגיה','cr/35c.jpg')]}
for n,ads in ADS.items():
  for s in S(n):
    s['ads']=[{'h':h,'img':i} for h,i in ads]
    s['b']=[x for x in s['b'] if x[0]=='p']
for s in S(35):
  for x in s['b']:
    if 'היא תיכנס למודעה B.' in x[1]: x[1]=x[1].replace('היא תיכנס למודעה B.','היא תיכנס למודעה B. ומודעה C בודקת אם פנייה חגיגית ללקוחות שכבר קנו מביאה יותר נרשמים לאירוע מאשר ההזמנה במודעה A.')
setb(34,'אם מי שכבר נחשף מתקדם בזכות מענה להתנגדויות, או בזכות דחיפות.','אם מי שכבר נחשף נענה יותר לפנייה האישית של מני, או להדמיית הפרויקט והמכירה המוקדמת.')

# ---------- images ----------
IMG={2:'mj/s02_1.jpg'}
for s in S(2): s['logo']=1; s['img']='R22'
for s in S(22): s['img']='archi/archi_office_meet.jpg'
for s in S(29): s['img']='mj/sales_gallery.jpg'
for s in S(30): s['img']='mj/sales_phone.jpg'
for s in S(41): s['img']='mj/crm.jpg'
for s in S(3): s['imgs'][1]='mj/office_logo.jpg'
for s in S(21): s['imgs'][2]='mj/ages.jpg'

# ---------- remove slides 18 and 37, renumber ----------
d=[s for s in d if s.get('n') not in (18,37)]
def newn(n):
  if n is None: return None
  if n<18: return n
  if n<37: return n-1
  return n-2
TOTAL=46
def refs(x):
  x=re.sub(r'(שקפים )(\d+)( (?:עד|ו־) ?)(\d+)',lambda m:m.group(1)+str(newn(int(m.group(2))))+m.group(3)+str(newn(int(m.group(4)))),x)
  x=re.sub(r'(שקף )(\d+)',lambda m:m.group(1)+str(newn(int(m.group(2)))),x)
  return x
for s in d:
  if s.get('n'): s['n']=newn(s['n'])
  for k in list(s.keys()):
    if k in('img','imgs','kind','theme','n','num'): continue
    s[k]=walk(s[k],refs)
  if s['kind']!='chapter' and s.get('num'): s['num']=None

# ---------- merge 36 (channel roles) + 37 (budget) ----------
roles=[x for s in d if s.get('n')==36 for x in s['b'] if x[0]=='tb']
R={r[0]:r for t in roles for r in t[2]}
bud=[s for s in d if s.get('n')==37 and not s.get('cont')][0]
bcont=[s for s in d if s.get('n')==37 and s.get('cont')][0]
brows=bud['b'][0][2]
rows=[
 ['מטא: קמפיין השקעה','חשיפה וסיפור: הסרט על מני, סרטוני וידאו, מפגשי ריכוז','35%','35,000 ₪'],
 ['מטא: קמפיין פרויקט (Kobuleti)','מכירה מוקדמת: בדיקה של טופס מיידי מול דף נחיתה','20%','20,000 ₪'],
 ['מטא: רימרקטינג','החזרה: צופים ב־50% מסרטון ומבקרי הדף ב־30 יום','10%','10,000 ₪'],
 ['גוגל חיפוש','לכידת מי שכבר מחפש: חיפושים על נדל"ן בגאורגיה, על Kobuleti ועל Archi, בעברית ובאנגלית','20%','20,000 ₪'],
 ['יוטיוב','עומק: הסרט המלא על מני, סרטוני פרויקט ובניית קהלים','10%','10,000 ₪'],
 ['ניסויים','בדיקה: קהלים חדשים, למשל צעירים או חיילים, עם סינון','5%','5,000 ₪'],
]
merged={'n':36,'t':'ערוצים ותקציב פתיחה','g':'100,000 ₪ בחודש. לכל ערוץ תפקיד אחד, והתקציב זז לפי עלות לפגישה ולא לפי עלות לליד.','eyb':bud['eyb'],
 'b':[['tb',['ערוץ','תפקיד','חלק','סכום חודשי'],rows],
      ['n','ובנוסף, בלי תקציב מדיה: דף נחיתה לכל מסלול (המרה וסינון), אירוע ההשקה ומפגשי ריכוז (אמון וסגירה), ושיתוף פעולה עם איסתא או מועדון עסקים.']],
 'num':None,'kind':'table','theme':'dark','img':'mj/media_desk.jpg'}
bcont['n']=36; bcont['t']='ערוצים ותקציב פתיחה'
nd=[]
for s in d:
  if s.get('n')==36 and s is not bcont:
    if merged not in nd: nd.append(merged)
    continue
  if s.get('n')==37 and not s.get('cont'): continue
  nd.append(s)
d=nd
def newn2(n): return n-1 if n and n>37 else n
def refs2(x):
  x=re.sub(r'(שקפים )(\d+)( (?:עד|ו־) ?)(\d+)',lambda m:m.group(1)+str(newn2(int(m.group(2))))+m.group(3)+str(newn2(int(m.group(4)))),x)
  x=re.sub(r'(שקף )(\d+)',lambda m:m.group(1)+str(newn2(int(m.group(2)))),x)
  return x
for s in d:
  if s.get('n'): s['n']=newn2(s['n'])
  for k in list(s.keys()):
    if k in('img','imgs','kind','theme','n','num'): continue
    s[k]=walk(s[k],refs2)
# ---------- new slide 33: Georgia travellers ----------
geo={'n':33,'t':'מודעות לקהל גאורגיה','g':'מי שכבר היה בגאורגיה, או מתכנן לטוס אליה, מכיר את הים. נשאר להראות לו את הדירה.','eyb':'הקמפיין והקריאייטיב',
 'b':[['p','קהל: ישראלים שחזרו מגאורגיה או מתכננים לטוס אליה, לפי עניין בתיירות בגאורגיה ובטיסות לבטומי ולטביליסי, וקהל שיתוף הפעולה עם איסתא. הם כבר ראו את החוף במו עיניהם, ולכן המודעה לא צריכה לשכנע שגאורגיה שווה, רק שיש להם דירה משלהם על הים.'],
      ['p','מה בודקים: אם הקהל הזה נענה יותר לחוויה ולמותג Swissôtel (מודעה A), או למחיר החודשי ולפריסת התשלומים (מודעה B).']],
 'num':None,'kind':'creative','theme':'dark','img':None,
 'ads':[{'h':'מודעה A: הים של גאורגיה','img':'cr/geo_a.jpg'},{'h':'מודעה B: דירה על הים בגאורגיה','img':'cr/geo_b.jpg'}]}
def newn3(n): return n+1 if n and n>=33 else n
def refs3(x):
  x=re.sub(r'(שקפים )(\d+)( (?:עד|ו־) ?)(\d+)',lambda m:m.group(1)+str(m.group(2) if int(m.group(2))<33 else int(m.group(2))+1)+m.group(3)+str(newn3(int(m.group(4)))),x)
  x=re.sub(r'(שקף )(\d+)',lambda m:m.group(1)+str(newn3(int(m.group(2)))),x)
  return x
for s in d:
  if s.get('n'): s['n']=newn3(s['n'])
  for k in list(s.keys()):
    if k in('img','imgs','kind','theme','n','num','ads'): continue
    s[k]=walk(s[k],refs3)
idx=max(i for i,s in enumerate(d) if s.get('n')==32)
d.insert(idx+1,geo)
# ---------- global replaces ----------
G=[('ישר מהבית','ישירות מהיזם'),('מני בייניש','מני בניש'),('מני ביניש','מני בניש'),('בייניש','בניש'),
   ('הגדול במדינה','הגדול בגאורגיה'),('ליווי של Archi Rent','ליווי אקסקלוסיבי'),('Archi Rent','ליווי אקסקלוסיבי'),('66,400','64,000')]
def money(x):
  for a,b in G: x=x.replace(a,b)
  x=re.sub(r'(\d[\d,\.]*) עד (\d[\d,\.]*) דולר',r'$\1 עד $\2',x)
  x=re.sub(r'(\d[\d,\.]*) (מיליון|אלף) דולר',r'$\1 \2',x)
  x=re.sub(r'(\d[\d,\.]*) דולר',r'$\1',x)
  x=re.sub(r'(\d[\d,\.]*) (?:ש"ח|ש״ח|שקלים|שקל)\b',r'\1 ₪',x)
  return x
d=[walk(s,money) for s in d]
# chips: currency into the number
for s in d:
  for c in s.get('chips',[]) or []:
    if c[1].startswith('מיליון דולר'): c[0]='$'+c[0]; c[1]=c[1].replace('מיליון דולר','מיליון')
    if c[1].startswith('דולר, '): c[0]='$'+c[0]; c[1]=c[1].replace('דולר, ','')
  if s.get('chips'):
    s['chips']=[[('$64,000' if c[0] in('$66,400','66,400') else c[0]),c[1]] for c in s['chips']]
# proofreading: closing period on tile/panel body text
for s in d:
  for it in s.get('items') or []:
    if isinstance(it,dict) and isinstance(it.get('b'),str):
      t=it['b'].rstrip()
      if t and not re.search(r'[\.\?!:"”)]$',t): it['b']=t+'.'
# ---------- geo audience in tracks + budget ----------
for s in d:
  if s.get('t')=='ארבעה מסלולי קמפיין':
    s['t']='חמישה מסלולי קמפיין'; s['g']='שני מסלולים מרכזיים ושלושה שתומכים בהם, וכולם מובילים ל־Kobuleti.'
    rows=s['b'][0][2]; i=[r[0] for r in rows].index('פרויקט')
    rows.insert(i+1,['קהל גאורגיה','הים של גאורגיה, מותג Swissôtel והמחיר החודשי של Kobuleti','ישראלים שחזרו מגאורגיה או מתכננים לטוס אליה, וקהל שיתוף הפעולה עם איסתא','השארת פרטים לבדיקת דירות פנויות','שיחה על הנכס והתנאים, שנשענת על החוויה שכבר יש להם מגאורגיה'])
  if s.get('t')=='ערוצים ותקציב פתיחה' and not s.get('cont'):
    rows=s['b'][0][2]
    for r in rows:
      if r[0].startswith('מטא: קמפיין פרויקט'): r[2]='15%'; r[3]='15,000 ₪'
    i=[r[0] for r in rows].index('מטא: רימרקטינג')
    rows.insert(i,['מטא: קהל גאורגיה','קהל חם: מי שחזר מגאורגיה או מתכנן לטוס אליה','5%','5,000 ₪'])
json.dump(d,open(B+'slides.json','w'),ensure_ascii=False)
left=[(s.get('n'),m) for s in d for m in re.findall(r'[^"]{0,20}(?:דולר|ש"ח|ש״ח|ישר מהבית|בייניש|ביניש|66,400|הגדול במדינה)[^"]{0,20}',json.dumps(s,ensure_ascii=False))]
print(len(d),'slides; leftovers:',left)
