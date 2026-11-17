const {chromium}=require('playwright');const fs=require('fs');const W=__dirname;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.route('**/*',async r=>{const u=r.request().url();
  if(u.includes('cdnjs')) return r.fulfill({path:W+'/node_modules/gsap/dist/gsap.min.js',contentType:'application/javascript'});
  if(u.includes('fonts.googleapis')){let css='';for(const [fam,dir,w] of [['Heebo','heebo',[200,300,400,500,600,700,800,900]],['Frank Ruhl Libre','frank-ruhl-libre',[300,400,500]],['Syncopate','syncopate',[400,700]]]){for(const x of w){for(const sub of ['hebrew','latin']){const f=`${W}/node_modules/@fontsource/${dir}/files/${dir}-${sub}-${x}-normal.woff2`;if(fs.existsSync(f))css+=`@font-face{font-family:'${fam}';font-weight:${x};src:url(file://${f}) format('woff2');}\n`;}}}return r.fulfill({body:css,contentType:'text/css'});}
  if(u.includes('fonts.gstatic'))return r.abort();return r.continue();});
 await p.goto('file://'+require('path').resolve(W,'../../index.html'));await p.waitForTimeout(1000);
 const n=await p.evaluate(()=>document.querySelectorAll('.s').length);const all=[];
 for(let i=0;i<n;i++){await p.evaluate(i=>window.__go(i,true),i);await p.waitForTimeout(2600);
  const r=await p.evaluate(i=>{const s=document.querySelectorAll('.s')[i];const out=[];
   // text leaf boxes: use Range rects per text node
   const boxes=[];const tw=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);let t;
   while(t=tw.nextNode()){if(!t.textContent.trim())continue;const el=t.parentElement;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
     let hid=false;for(let e=el;e&&e!==s;e=e.parentElement){const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden'||+c.opacity===0){hid=true;break}}if(hid)continue;
     const rg=document.createRange();rg.selectNodeContents(t);for(const rc of rg.getClientRects()){if(rc.width<2)continue;boxes.push({x:rc.left,y:rc.top,w:rc.width,h:rc.height,t:t.textContent.trim().slice(0,30),el})}}
   // overlaps between boxes of different elements
   for(let a=0;a<boxes.length;a++)for(let c=a+1;c<boxes.length;c++){const A=boxes[a],B=boxes[c];if(A.el===B.el)continue;
     const ox=Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x),oy=Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y);
     if(ox>3&&oy>Math.min(A.h,B.h)*0.6)out.push('OVERLAP: '+A.t+' | '+B.t);}
   // out of slide or clipped
   for(const B of boxes){if(B.x<0||B.y<0||B.x+B.w>1920||B.y+B.h>1080)out.push('OUTSIDE: '+B.t+' '+[B.x,B.y,B.w,B.h].map(Math.round));
     for(let e=B.el;e&&e!==s;e=e.parentElement){const c=getComputedStyle(e);if(c.overflow==='hidden'||c.overflowY==='hidden'){const R=e.getBoundingClientRect();if(B.y+B.h>R.bottom+12||B.y<R.top-14||B.x<R.left-2||B.x+B.w>R.right+2){out.push('CLIPPED: '+B.t+' in .'+e.className);break}}}}
   return [...new Set(out)].slice(0,12);},i);
  if(r.length)all.push(i+': '+r.join('\n   '));}
 console.log(all.join('\n')||'CLEAN');await b.close();})();
