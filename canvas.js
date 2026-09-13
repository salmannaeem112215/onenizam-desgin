(() => {
  const screens = [
    [1,'Sign in','login'],[29,'Forgot password','forgot-password'],[30,'Create account','create-account'],[31,'Verify code','verify-code'],[2,'Create password','create-password'],[3,'Password updated','password-updated'],
    [10,'Salon hub','hub'],[9,'Front desk','front-desk'],[7,'Calendar','calendar'],[6,'New appointment','appointment'],[4,'Sales','sales'],[5,'Checkout','checkout'],
    [11,'Messages','messages'],[12,'Services','services'],[13,'Resources','resources'],[14,'Service details','14'],[21,'New service','service-new'],[16,'Staff','staff'],
    [15,'Create staff','staff-create'],[17,'Customers','customers'],[18,'Add customer','customer-add'],[19,'Reviews','reviews'],[20,'Reports','reports'],[22,'Settings','settings'],
    [23,'Billing','billing'],[24,'Business setup','business-setup'],[25,'Business hours','business-hours'],[26,'Contact details','contact-details'],[27,'Location setup','location-setup'],[28,'Media','media'],
    ['B1','Landing page','B1'],['B2','App selection','B2'],['B3','Email verification','B3'],['B4','Bookable services','B4'],['B5','Business basics','B5'],['B6','Setup review','B6'],['B7','Business photos','B7'],['B8','Create account','B8'],['B9','Staff setup','B9'],['B10','Plan selection','B10']
  ];
  const viewport = document.getElementById('viewport'), world = document.getElementById('world');
  const key = 'onenizam-canvas-v1';
  let saved;
  try { saved = JSON.parse(localStorage.getItem(key)); } catch (_) {}
  let x = 40, y = 40, scale = .6, selected, gesture, space = false, lastTap;
  const pointers = new Map();
  const cards = screens.map(([id, name, route], index) => {
    const position = saved?.positions?.[id];
    const card = {id, x: Number.isFinite(position?.x) ? position.x : index % 6 * 410, y: Number.isFinite(position?.y) ? position.y : Math.floor(index / 6) * 330};
    card.url = '/' + route + (id === 31 ? '?email=preview%40example.com&flow=reset' : '');
    const el = document.createElement('article');
    el.className = 'screen'; el.tabIndex = 0; el.dataset.id = id;
    el.setAttribute('aria-label', name + '. Drag to reposition. Press Enter to open.');
    el.innerHTML = `<div class="screen-label"><span><b>${String(id).padStart(2,'0')}</b> ${name}</span><a href="${card.url}" aria-label="Open ${name}">Open ↗</a></div><div class="preview"><iframe title="${name} preview" tabindex="-1" loading="lazy" sandbox="allow-scripts allow-same-origin"></iframe></div>`;
    const frame = el.querySelector('iframe');
    frame.dataset.src = card.url;
    frame.addEventListener('load', () => {
      // Keep prototype controls inside the preview; canvas gestures live on the card.
      try {
        const style = frame.contentDocument.createElement('style');
        style.textContent = '.screen-nav-wrap{display:none!important}';
        frame.contentDocument.head.append(style);
      } catch (_) {}
    });
    el.addEventListener('keydown', event => { if (event.key === 'Enter' && event.target === el) location.assign(card.url); });
    card.el = el; world.append(el); return card;
  });
  document.getElementById('count').textContent = `${cards.length} screens`;
  function persist() {
    try { localStorage.setItem(key, JSON.stringify({x,y,scale,positions:Object.fromEntries(cards.map(c => [c.id,{x:c.x,y:c.y}]))})); } catch (_) {}
  }
  function render() {
    world.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
    viewport.style.backgroundPosition = `${x}px ${y}px`;
    viewport.style.backgroundSize = `${24 * scale}px ${24 * scale}px`;
    document.getElementById('zoom').value = `${Math.round(scale * 100)}%`;
    cards.forEach(c => { c.el.style.left = c.x + 'px'; c.el.style.top = c.y + 'px'; });
  }
  function zoom(next, px = viewport.clientWidth / 2, py = viewport.clientHeight / 2) {
    next = Math.max(.12, Math.min(2.5, next));
    x = px - (px - x) * next / scale; y = py - (py - y) * next / scale; scale = next; render();
  }
  function fit() {
    const left = Math.min(...cards.map(c => c.x)), top = Math.min(...cards.map(c => c.y));
    const width = Math.max(...cards.map(c => c.x + 360)) - left, height = Math.max(...cards.map(c => c.y + 270)) - top;
    scale = Math.max(.12, Math.min(1, (viewport.clientWidth - 64) / width, (viewport.clientHeight - 100) / height));
    x = (viewport.clientWidth - width * scale) / 2 - left * scale;
    y = (viewport.clientHeight - height * scale) / 2 - top * scale; render(); persist();
  }
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const frame = entry.target.querySelector('iframe');
    frame.src = frame.dataset.src; observer.unobserve(entry.target);
  }), {root:viewport, rootMargin:'150px'});
  cards.forEach(c => observer.observe(c.el));
  viewport.addEventListener('wheel', event => {
    event.preventDefault(); const rect = viewport.getBoundingClientRect();
    zoom(scale * Math.exp(-event.deltaY * (event.deltaMode === 1 ? .035 : .002)), event.clientX - rect.left, event.clientY - rect.top); persist();
  }, {passive:false});
  viewport.addEventListener('pointerdown', event => {
    if (event.target.closest('a') || (event.button !== 0 && event.button !== 1)) return;
    event.preventDefault(); viewport.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, {x:event.clientX,y:event.clientY});
    if (pointers.size === 2) {
      const [a,b] = [...pointers.values()];
      gesture = {type:'pinch', distance:Math.hypot(a.x-b.x,a.y-b.y), mx:(a.x+b.x)/2, my:(a.y+b.y)/2}; lastTap = null; return;
    }
    const card = !space && event.button !== 1 && cards.find(c => c.el === event.target.closest('.screen'));
    selected?.el.classList.remove('selected'); selected = card;
    card?.el.classList.add('selected');
    gesture = {type:card ? 'card' : 'pan',card,sx:event.clientX,sy:event.clientY,x:card ? card.x : x,y:card ? card.y : y,moved:false};
    viewport.classList.add('dragging');
  });
  viewport.addEventListener('pointermove', event => {
    if (!pointers.has(event.pointerId) || !gesture) return;
    pointers.set(event.pointerId,{x:event.clientX,y:event.clientY});
    if (gesture.type === 'pinch') {
      if (pointers.size !== 2) return;
      const [a,b] = [...pointers.values()], distance = Math.hypot(a.x-b.x,a.y-b.y), mx = (a.x+b.x)/2, my = (a.y+b.y)/2;
      const rect = viewport.getBoundingClientRect();
      zoom(scale * distance / Math.max(1,gesture.distance), gesture.mx - rect.left, gesture.my - rect.top);
      x += mx - gesture.mx; y += my - gesture.my;
      Object.assign(gesture,{distance,mx,my}); render(); return;
    }
    const dx = event.clientX - gesture.sx, dy = event.clientY - gesture.sy;
    if (Math.hypot(dx,dy) > 5) gesture.moved = true;
    if (!gesture.moved) return;
    if (gesture.card) { gesture.card.x = gesture.x + dx / scale; gesture.card.y = gesture.y + dy / scale; }
    else { x = gesture.x + dx; y = gesture.y + dy; }
    render();
  });
  function end(event) {
    if (!pointers.has(event.pointerId)) return;
    if (event.type === 'pointerup' && gesture?.card && !gesture.moved) {
      const now = Date.now();
      if (lastTap?.id === gesture.card.id && now - lastTap.time < 450) location.assign(gesture.card.url);
      lastTap = {id:gesture.card.id,time:now};
    } else lastTap = null;
    pointers.delete(event.pointerId); gesture = null; viewport.classList.remove('dragging'); persist();
  }
  viewport.addEventListener('pointerup', end); viewport.addEventListener('pointercancel', end);
  document.getElementById('plus').onclick = () => { zoom(scale * 1.2); persist(); };
  document.getElementById('minus').onclick = () => { zoom(scale / 1.2); persist(); };
  document.getElementById('fit').onclick = fit;
  document.getElementById('reset').onclick = () => { cards.forEach((c,i) => { c.x = i % 6 * 410; c.y = Math.floor(i / 6) * 330; }); fit(); document.getElementById('status').textContent = 'Screen layout reset.'; };
  window.addEventListener('keydown', event => {
    if (event.target.closest('button,a') || event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.code === 'Space') { event.preventDefault(); space = true; }
    if (event.key.toLowerCase() === 'f') fit();
    if (event.key === '+' || event.key === '=') { zoom(scale * 1.2); persist(); }
    if (event.key === '-') { zoom(scale / 1.2); persist(); }
  });
  window.addEventListener('keyup', event => { if (event.code === 'Space') space = false; });
  window.addEventListener('blur', () => { space = false; pointers.clear(); gesture = null; viewport.classList.remove('dragging'); });
  if ([saved?.x,saved?.y,saved?.scale].every(Number.isFinite) && saved.scale >= .12 && saved.scale <= 2.5) { ({x,y,scale} = saved); render(); }
  else fit();
})();
