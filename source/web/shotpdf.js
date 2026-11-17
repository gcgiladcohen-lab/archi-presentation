const {chromium}=require('playwright');const fs=require('fs');const W=__dirname;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1.5});
 await p.route('**/*',async r=>{const u=r.request().url();
  if(u.includes('cdnjs')) return r.fulfill({path:W+'/node_modules/gsap/dist/gsap.min.js',contentType:'application/javascript'});
  if(u.includes('fonts.googleapis')){let css='';for(const [fam,dir,w] of [['Heebo','heebo',[400,500,700]],['Syncopate','syncopate',[400,700]]]){for(const x of w){for(const sub of ['hebrew','latin','latin-ext']){const f=`${W}/node_modules/@fontsource/${dir}/files/${dir}-${sub}-${x}-normal.woff2`;if(fs.existsSync(f))css+=`@font-face{font-family:'${fam}';font-weight:${x};src:url(file://${f}) format('woff2');}\n`;}}}return r.fulfill({body:css,contentType:'text/css'});}
  if(u.includes('fonts.gstatic'))return r.abort();return r.continue();});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+require('path').resolve(W,'../../index.html'));await p.waitForTimeout(2000);
 const ks=await p.evaluate(()=>[...document.querySelectorAll('.s')].map(s=>s.style.getPropertyValue('--k')));
 const ids=process.argv[2]==='all'?ks.map((_,i)=>i):process.argv[2].split(',').map(Number);
 for(const i of ids){await p.evaluate(i=>window.__go(i,true),i);await p.waitForTimeout(1900);await p.evaluate(i=>{const s=document.querySelectorAll(".s")[i];s.querySelectorAll("[data-step]").forEach(e=>e.classList.add("in"));s.querySelectorAll("mark.mk").forEach(m=>m.style.backgroundSize="100% 100%");document.querySelectorAll(".dots,.stepdots,.sd").forEach(e=>e.style.display="none")},i);await p.waitForTimeout(700);await p.screenshot({path:`${W}/pdf/${String(i).padStart(2,'0')}.png`});}
 console.log(JSON.stringify(ks));console.log(errs.join('\n')||'ok');await b.close();})();
