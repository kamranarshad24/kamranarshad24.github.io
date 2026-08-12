/*!
 * Custom consent manager — Google Consent Mode v2
 * No third-party CMP, no account, no external requests.
 *
 * IMPORTANT: the consent *defaults* must run before the GTM snippet.
 * That inline block lives in each page's <head>; this file only renders
 * the UI and pushes consent updates.
 */
(function () {
  'use strict';

  var KEY = 'ka_consent_v1';
  var CATS = [
    {
      id: 'analytics',
      name: 'Analytics',
      desc: 'Google Analytics 4 and Microsoft Clarity. Tells me which pages get read and where people get stuck. Clarity also records anonymised session replays.',
      signals: ['analytics_storage']
    },
    {
      id: 'ads',
      name: 'Advertising',
      desc: 'Google Ads and Meta. Measures whether an ad actually led to an enquiry, and allows remarketing.',
      signals: ['ad_storage', 'ad_user_data', 'ad_personalization']
    }
  ];

  function gtag() { window.dataLayer = window.dataLayer || []; window.dataLayer.push(arguments); }

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  }

  function save(choice) {
    var payload = {
      analytics: !!choice.analytics,
      ads: !!choice.ads,
      ts: new Date().toISOString(),
      v: 1
    };
    try { localStorage.setItem(KEY, JSON.stringify(payload)); } catch (e) {}
    apply(payload);
    return payload;
  }

  function apply(c) {
    var state = {
      analytics_storage:  c.analytics ? 'granted' : 'denied',
      ad_storage:         c.ads ? 'granted' : 'denied',
      ad_user_data:       c.ads ? 'granted' : 'denied',
      ad_personalization: c.ads ? 'granted' : 'denied'
    };
    gtag('consent', 'update', state);
    // Custom tags (Clarity, Meta) are NOT governed by Consent Mode automatically.
    // Gate them in GTM on this event / these variables.
    window.dataLayer.push({
      event: 'consent_update',
      consent_analytics: c.analytics ? 'granted' : 'denied',
      consent_ads: c.ads ? 'granted' : 'denied'
    });
  }

  var CSS = ''
    + '.kac-scrim{position:fixed;inset:0;background:rgba(8,26,54,.55);z-index:2147483000;'
    + 'opacity:0;transition:opacity .25s ease}'
    + '.kac-scrim.on{opacity:1}'
    + '.kac{position:fixed;left:0;right:0;bottom:0;z-index:2147483001;'
    + 'font-family:"Instrument Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;'
    + 'background:#fff;color:#0B2143;border-top:1px solid #DDE5F0;'
    + 'box-shadow:0 -8px 40px -12px rgba(8,26,54,.28);'
    + 'transform:translateY(102%);transition:transform .34s cubic-bezier(.22,.61,.36,1)}'
    + '.kac.on{transform:translateY(0)}'
    + '.kac-in{max-width:1140px;margin:0 auto;padding:20px 24px;display:flex;gap:22px;'
    + 'align-items:center;flex-wrap:wrap}'
    + '.kac-txt{flex:1 1 340px;min-width:0}'
    + '.kac-txt h2{font-family:"Bricolage Grotesque",Georgia,serif;font-size:17px;font-weight:700;'
    + 'margin:0 0 5px;letter-spacing:-.01em;color:#0B2143}'
    + '.kac-txt p{margin:0;font-size:14px;line-height:1.55;color:#5C6E8C;max-width:70ch}'
    + '.kac-txt a{color:#166FDB}'
    + '.kac-btns{display:flex;gap:10px;flex-wrap:wrap;flex-shrink:0}'
    + '.kac-b{font:inherit;font-size:14px;font-weight:600;padding:11px 20px;border-radius:999px;'
    + 'cursor:pointer;border:1px solid transparent;min-height:44px;white-space:nowrap;'
    + 'transition:background .2s ease,border-color .2s ease}'
    + '.kac-b1{background:#166FDB;color:#fff}.kac-b1:hover{background:#0F5FC4}'
    + '.kac-b2{background:#fff;color:#0B2143;border-color:#C6D2E4}.kac-b2:hover{border-color:#8B9AB4}'
    + '.kac-b3{background:transparent;color:#5C6E8C;text-decoration:underline;padding:11px 8px}'
    + '.kac-b3:hover{color:#0B2143}'
    + '.kac-panel{max-width:1140px;margin:0 auto;padding:0 24px 22px;display:none}'
    + '.kac-panel.on{display:block}'
    + '.kac-row{display:flex;gap:16px;align-items:flex-start;padding:15px 0;border-top:1px solid #DDE5F0}'
    + '.kac-row h3{font-size:14.5px;font-weight:700;margin:0 0 3px;color:#0B2143}'
    + '.kac-row p{margin:0;font-size:13.2px;line-height:1.5;color:#5C6E8C;max-width:74ch}'
    + '.kac-row .lock{font-size:12.5px;color:#8B9AB4;white-space:nowrap;padding-top:2px}'
    + '.kac-sw{position:relative;flex-shrink:0;width:46px;height:26px;margin-top:2px}'
    + '.kac-sw input{position:absolute;opacity:0;width:100%;height:100%;margin:0;cursor:pointer;z-index:2}'
    + '.kac-sw span{position:absolute;inset:0;background:#C6D2E4;border-radius:999px;'
    + 'transition:background .2s ease;pointer-events:none}'
    + '.kac-sw span::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;'
    + 'background:#fff;border-radius:50%;transition:transform .2s ease}'
    + '.kac-sw input:checked+span{background:#166FDB}'
    + '.kac-sw input:checked+span::after{transform:translateX(20px)}'
    + '.kac-sw input:focus-visible+span{outline:2px solid #166FDB;outline-offset:3px}'
    + '.kac-b:focus-visible{outline:2px solid #166FDB;outline-offset:3px}'
    + '@media(max-width:700px){.kac-in{padding:18px;gap:16px}'
    + '.kac-btns{width:100%}.kac-b{flex:1 1 auto;text-align:center}'
    + '.kac-panel{padding:0 18px 18px}}'
    + '@media(prefers-reduced-motion:reduce){.kac,.kac-scrim,.kac-sw span,.kac-sw span::after'
    + '{transition:none!important}}';

  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (html != null) n.innerHTML = html;
    return n;
  }

  function build(existing) {
    var style = el('style'); style.textContent = CSS;
    document.head.appendChild(style);

    var scrim = el('div', { class: 'kac-scrim', hidden: 'hidden' });

    var bar = el('div', {
      class: 'kac', role: 'dialog', 'aria-modal': 'false',
      'aria-labelledby': 'kac-h', 'aria-describedby': 'kac-p'
    });

    var rows = CATS.map(function (c) {
      var on = existing ? !!existing[c.id] : false;
      return ''
        + '<div class="kac-row">'
        + '<label class="kac-sw"><input type="checkbox" data-cat="' + c.id + '"'
        + (on ? ' checked' : '') + ' aria-label="' + c.name + '"><span></span></label>'
        + '<div><h3>' + c.name + '</h3><p>' + c.desc + '</p></div>'
        + '</div>';
    }).join('');

    bar.innerHTML = ''
      + '<div class="kac-in">'
      +   '<div class="kac-txt">'
      +     '<h2 id="kac-h">Cookies on this site</h2>'
      +     '<p id="kac-p">I use analytics and advertising cookies to see what people read and '
      +       'whether my own ads work. Nothing loads until you choose. '
      +       '<a href="/privacy-policy.html">Privacy policy</a>.</p>'
      +   '</div>'
      +   '<div class="kac-btns">'
      +     '<button class="kac-b kac-b3" data-act="manage" aria-expanded="false">Manage</button>'
      +     '<button class="kac-b kac-b2" data-act="reject">Reject all</button>'
      +     '<button class="kac-b kac-b1" data-act="accept">Accept all</button>'
      +   '</div>'
      + '</div>'
      + '<div class="kac-panel" id="kac-panel">'
      +   rows
      +   '<div class="kac-row"><div class="lock">Always on</div>'
      +     '<div><h3>Strictly necessary</h3><p>Remembers this choice so you are not asked again. '
      +     'Cannot be turned off.</p></div></div>'
      +   '<div style="padding-top:14px"><button class="kac-b kac-b2" data-act="save">Save my choices</button></div>'
      + '</div>';

    document.body.appendChild(scrim);
    document.body.appendChild(bar);
    requestAnimationFrame(function () { bar.classList.add('on'); });

    function close() {
      bar.classList.remove('on');
      scrim.classList.remove('on');
      scrim.hidden = true;
      setTimeout(function () { bar.remove(); scrim.remove(); }, 340);
      document.removeEventListener('keydown', onKey);
    }

    function onKey(e) { if (e.key === 'Escape') { save({ analytics: false, ads: false }); close(); } }
    document.addEventListener('keydown', onKey);

    bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-act]'); if (!b) return;
      var act = b.getAttribute('data-act');

      if (act === 'manage') {
        var p = bar.querySelector('#kac-panel');
        var open = p.classList.toggle('on');
        b.setAttribute('aria-expanded', String(open));
        b.textContent = open ? 'Hide options' : 'Manage';
        scrim.hidden = !open;
        if (open) requestAnimationFrame(function () { scrim.classList.add('on'); });
        else scrim.classList.remove('on');
        return;
      }
      if (act === 'accept') { save({ analytics: true, ads: true }); close(); return; }
      if (act === 'reject') { save({ analytics: false, ads: false }); close(); return; }
      if (act === 'save') {
        var choice = {};
        bar.querySelectorAll('[data-cat]').forEach(function (i) {
          choice[i.getAttribute('data-cat')] = i.checked;
        });
        save(choice); close(); return;
      }
    });
  }

  // Re-open from anywhere: <a href="#" data-consent-open>Cookie settings</a>
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-consent-open]');
    if (!t) return;
    e.preventDefault();
    if (!document.querySelector('.kac')) build(read());
  });

  function init() {
    var stored = read();
    if (stored) { apply(stored); return; }   // choice already made
    build(null);                              // first visit
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
