const {chromium}=require('playwright');const W=__dirname;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
 await p.route('**/*',async r=>{const u=r.request().url();if(u.includes('cdnjs'))return r.fulfill({path:W+'/node_modules/gsap/dist/gsap.min.js',contentType:'application/javascript'});if(u.includes('fonts.g'))return r.abort();return r.continue();});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+require('path').resolve(W,'../../index.html'));await p.waitForTimeout(2500);
 let last=-1,stuck=0;for(let k=0;k<400;k++){await p.keyboard.press('ArrowLeft');await p.waitForTimeout(60);}
 await p.waitForTimeout(800);
 const st=await p.evaluate(()=>({h:location.hash,vis:[...document.querySelectorAll('.s')].filter(s=>getComputedStyle(s).visibility!=='hidden'&&+getComputedStyle(s).opacity>0.05).length,imgs:document.querySelectorAll('img').length,mem:performance.memory&&performance.memory.usedJSHeapSize}));
 console.log(JSON.stringify(st),errs.slice(0,5));await b.close();})();
