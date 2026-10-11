// Gedeelde compositielaag: bouwt op de computer een inhoudstafel naast de reel.
(function(){
  const stage=document.getElementById('stage'); if(!stage) return;
  const ctrl=document.querySelector('.ctrl'), hint=document.querySelector('.hint');
  const scenes=[...stage.querySelectorAll('.scene')];
  const col=document.createElement('div'); col.className='reelcol';
  stage.parentNode.insertBefore(col,stage);
  [stage,ctrl,hint].forEach(el=>{ if(el) col.appendChild(el); });

  const first=scenes[0];
  const latin=(first.querySelector('h2')||{}).textContent||document.title;
  const common=(first.querySelector('.note')||{}).textContent||'';
  const toc=document.createElement('nav'); toc.className='toc'; toc.setAttribute('aria-label','Hoofdstukken van deze fiche');
  const items=scenes.map((s,i)=>{
    const t=(s.querySelector('.tag')||{}).textContent||('Scène '+(i+1));
    let label=t.charAt(0).toUpperCase()+t.slice(1).toLowerCase();
    if(i===0&&/plantenfiche/i.test(t)) label='Intro';
    return `<li><button type="button" data-i="${i}">${label}</button></li>`;
  }).join('');
  toc.innerHTML=`<span class="eyebrow">Plantenfiche</span><h1>${latin}</h1>`+
    (common?`<p class="common">${common}</p>`:'')+`<ol>${items}</ol>`;
  col.after(toc);
  const btns=[...toc.querySelectorAll('button')];
  btns.forEach(b=>b.addEventListener('click',()=>{ if(window.__reel) window.__reel.go(+b.dataset.i); }));
  function mark(i){ btns.forEach((b,k)=>{ if(k===i) b.setAttribute('aria-current','step'); else b.removeAttribute('aria-current'); }); }
  document.addEventListener('reel:scene',e=>mark(e.detail));
  const on=scenes.findIndex(s=>s.classList.contains('on')); mark(on<0?0:on);
})();
