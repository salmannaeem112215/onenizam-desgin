(() => {
  const script = document.currentScript;
  const screen = Number(script?.dataset.screen || location.pathname.match(/(?:screen\/|\/)(\d+)(?:\.html)?$/)?.[1]);
  const pages = {
    4: ['Sales', '/sales'],
    5: ['Checkout', '/checkout'],
    6: ['New Appointment', '/appointment'],
    7: ['Calendar', '/calendar'],
    9: ['Front Desk', '/front-desk'],
    10: ['Hub', '/hub'],
    11: ['Chats', '/messages'],
    12: ['Services', '/services'],
    13: ['Resources', '/resources'],
    14: ['Services', '/services'],
    15: ['Create Staff', '/staff-create'],
    16: ['Staff', '/staff'],
    17: ['Customers', '/customers'],
    18: ['Add Customer', '/customer-add'],
    19: ['Reviews', '/reviews'],
    20: ['Reports', '/reports'],
    21: ['New Service', '/service-new'],
    22: ['Settings', '/settings'],
    23: ['Billing', '/billing'],
    24: ['Business Setup', '/business-setup'],
    25: ['Business Hours', '/business-hours'],
    26: ['Contact Details', '/contact-details'],
    27: ['Location Setup', '/location-setup'],
    28: ['Media', '/media']
  };
  const primary = [
    ['Front Desk', '/front-desk', 9],
    ['Calendar', '/calendar', 7],
    ['Sales', '/sales', 4],
    ['Chats', '/messages', 11]
  ];

  function hidePreviousNavigation() {
    const candidates = [...document.querySelectorAll('body nav, body header')].filter(element => {
      const text = element.textContent || '';
      return primary.filter(([label]) => text.includes(label)).length >= 2;
    });
    const oldNavigation = candidates.find(element => !candidates.some(other => other !== element && other.contains(element)));
    if (oldNavigation) oldNavigation.classList.add('one-nav-replaced');
  }

  function tab(label, href, active, context = false) {
    const link = document.createElement('a');
    link.className = `one-nav-tab${context ? ' one-nav-context' : ''}`;
    link.href = href;
    link.textContent = label;
    if (active) link.setAttribute('aria-current', 'page');
    return link;
  }

  function render() {
    if (!pages[screen] || document.querySelector('.one-nav-shell')) return;
    document.body.classList.add(`one-nav-screen-${screen}`);
    hidePreviousNavigation();

    const nav = document.createElement('nav');
    nav.className = 'one-nav-shell';
    nav.setAttribute('aria-label', 'Main navigation');
    nav.innerHTML = `
      <div class="one-nav-brand">
        <span class="one-nav-logo" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="6" r="3"/><circle cx="6.3" cy="10" r="3"/><circle cx="17.7" cy="10" r="3"/><circle cx="8.3" cy="16.5" r="3"/><circle cx="15.7" cy="16.5" r="3"/></svg></span>
        <span class="one-nav-brand-copy"><span class="one-nav-brand-name">Salon Azul</span></span>
      </div>
      <div class="one-nav-tabs"></div>
      <div class="one-nav-account">
        <div class="one-nav-actions">
          <button class="one-nav-icon" type="button" aria-label="Apps"><svg viewBox="0 0 24 24" fill="currentColor"><circle cx="6" cy="6" r="1.7"/><circle cx="12" cy="6" r="1.7"/><circle cx="18" cy="6" r="1.7"/><circle cx="6" cy="12" r="1.7"/><circle cx="12" cy="12" r="1.7"/><circle cx="18" cy="12" r="1.7"/><circle cx="6" cy="18" r="1.7"/><circle cx="12" cy="18" r="1.7"/><circle cx="18" cy="18" r="1.7"/></svg></button>
          <button class="one-nav-icon" type="button" aria-label="Notifications"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 7h18s-3 0-3-7"/><path d="M10 19h4"/></svg></button>
        </div>
        <span class="one-nav-user"><strong>Asad Ullah</strong><span>OPERATIONS LEAD</span></span>
        <span class="one-nav-avatar">AU</span>
      </div>`;

    const tabs = nav.querySelector('.one-nav-tabs');
    primary.forEach(([label, href, page]) => tabs.append(tab(label, href, screen === page)));
    if (!primary.some(([, , page]) => page === screen)) {
      const [label, href] = pages[screen];
      tabs.append(tab(label, href, true, true));
    }
    document.body.prepend(nav);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})();
