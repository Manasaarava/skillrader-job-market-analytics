"""SkillRadar local demo using only Python standard library and pandas."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import pandas as pd, json, re, os
from collections import Counter
BASE=os.path.dirname(os.path.abspath(__file__)); DATA_PATH=os.path.join(BASE,'data','job_listings.csv')
SKILLS=['python','sql','excel','power bi','tableau','statistics','machine learning','pandas','numpy','data visualization','communication','etl','aws','azure','spark','scikit-learn','nlp','deep learning','matplotlib','problem solving']
ALIASES={'powerbi':'power bi','ms excel':'excel','machine-learning':'machine learning','sklearn':'scikit-learn','data visualisation':'data visualization'}
def load_jobs():
 df=pd.read_csv(DATA_PATH).fillna(''); df['description_norm']=df['description'].astype(str).str.lower()
 for a,b in ALIASES.items(): df['description_norm']=df['description_norm'].str.replace(a,b,regex=False)
 return df
def analyze(df):
 counts=Counter()
 for t in df['description_norm']:
  for s in SKILLS:
   if re.search(r'(?<![a-z0-9])'+re.escape(s)+r'(?![a-z0-9])',t): counts[s.title()]+=1
 return counts
class Handler(BaseHTTPRequestHandler):
 def send_body(self,body,ctype='text/html; charset=utf-8',status=200):
  data=body.encode() if isinstance(body,str) else body; self.send_response(status); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
 def do_GET(self):
  u=urlparse(self.path); df=load_jobs()
  if u.path=='/static/style.css':
   try: self.send_body(open(os.path.join(BASE,'static','style.css'),'rb').read(),'text/css')
   except: self.send_body('Not found',status=404)
  elif u.path=='/api/analysis':
   q=parse_qs(u.query); role=q.get('role',['All roles'])[0]; loc=q.get('location',['All locations'])[0]
   if role!='All roles': df=df[df.role==role]
   if loc!='All locations': df=df[df.location==loc]
   c=analyze(df); skills=[{'skill':k,'count':v,'percent':round(v/max(len(df),1)*100)} for k,v in c.most_common(12)]
   self.send_body(json.dumps({'total':len(df),'roles':sorted(df.role.unique().tolist()),'locations':sorted(df.location.unique().tolist()),'skills':skills,'jobs':df[['company','role','location','experience','salary_lpa']].to_dict(orient='records')}),'application/json')
  elif u.path=='/':
   roles=sorted(df.role.unique()); locs=sorted(df.location.unique()); c=analyze(df); top=c.most_common(8)
   def opts(vals): return ''.join('<option>'+str(v)+'</option>' for v in vals)
   html=open(os.path.join(BASE,'templates','index.html')).read()
   html=html.replace('{% for r in role_options %}<option>{{r}}</option>{% endfor %}',opts(roles)).replace('{% for l in location_options %}<option>{{l}}</option>{% endfor %}',opts(locs))
   # replace initial Jinja values and bars with data; JS refresh then renders current data
   html=html.replace('{{total}}',str(len(df))).replace('{{roles}}',str(df.role.nunique())).replace('{{locations}}',str(df.location.nunique()))
   bars=''.join(f'<div class="barrow"><span>{k}</span><div class="track"><i style="width:{int(v/max(top[0][1],1)*100)}%"></i></div><b>{v}</b></div>' for k,v in top)
   import re as _re
   html=_re.sub(r'\{% for skill,count in top %\}.*?\{% endfor %\}',bars,html,flags=_re.S)
   self.send_body(html)
  else:self.send_body('Not found',status=404)
 def do_POST(self):
  if urlparse(self.path).path!='/api/skill-gap': self.send_body('Not found',status=404); return
  try: payload=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')))); role=payload.get('role','All roles'); existing={x.strip().lower() for x in payload.get('skills','').split(',') if x.strip()}
  except: payload={}; role='All roles'; existing=set()
  df=load_jobs()
  if role!='All roles': df=df[df.role==role]
  c=analyze(df); total=max(len(df),1); demand=[{'skill':k,'count':v,'percent':round(v/total*100)} for k,v in c.most_common()]
  missing=[x for x in demand if x['skill'].lower() not in existing and x['skill'].lower().replace(' ','') not in {s.replace(' ','') for s in existing}]
  self.send_body(json.dumps({'role':role,'existing':sorted(existing),'missing':missing[:8],'note':'Priorities are estimated from the included sample dataset, not a live labor-market feed.'}),'application/json')
 def log_message(self,*args): pass
if __name__=='__main__':
 port=int(os.environ.get('PORT','5000')); print(f'SkillRadar running at http://127.0.0.1:{port}'); HTTPServer(('127.0.0.1',port),Handler).serve_forever()
