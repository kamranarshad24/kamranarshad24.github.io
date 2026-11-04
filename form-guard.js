/* Lead form guard.
 * The spam check (Cloudflare Turnstile) can take 5+ seconds to get ready after
 * the form opens. A visitor using autofill can press Send before that, and the
 * backend then files the lead as spam with no email to the owner, while the
 * visitor still sees the thank-you page. This holds the submit until the check
 * is ready (max 10 s, then sends anyway) and adds a small "_js" field
 * (fill time ms, page age ms) so the backend can tell a real browser from a bot.
 * Used by every form that posts to /api/lead.
 */
(function () {
  if (window.__kaFormGuard) return;
  window.__kaFormGuard = 1;

  var MSG = {
    en: 'Securing your request…', de: 'Anfrage wird gesichert…', fr: 'Sécurisation de votre demande…',
    es: 'Protegiendo tu solicitud…', it: 'Messa in sicurezza della richiesta…',
    nl: 'Je aanvraag wordt beveiligd…', pt: 'A proteger o seu pedido…'
  };
  var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  var msg = MSG[lang] || MSG.en;
  var loaded = Date.now();
  var MAX_WAIT = 10000;

  function isLead(f) { return f && f.tagName === 'FORM' && /\/api\/lead$/.test(f.action || ''); }
  function token(f) { var i = f.querySelector('[name="cf-turnstile-response"]'); return i ? i.value : ''; }
  function push(o) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(o); }

  function stamp(f) {
    var h = f.querySelector('input[name="_js"]');
    if (!h) { h = document.createElement('input'); h.type = 'hidden'; h.name = '_js'; f.appendChild(h); }
    var now = Date.now();
    h.value = (now - (f._kaT || loaded)) + ',' + (now - loaded);
  }

  // Start the fill clock when the visitor first touches the form.
  document.addEventListener('focusin', function (e) {
    var f = e.target && e.target.form;
    if (isLead(f) && !f._kaT && !(e.target.type === 'submit')) f._kaT = Date.now();
  }, true);

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!isLead(f)) return;
    if (f._kaGo || token(f)) { f._kaGo = 0; stamp(f); return; }

    // Check not ready: hold this submit and resend once it is.
    e.preventDefault();
    e.stopPropagation();
    if (f._kaWait) return;
    f._kaWait = 1;
    var b = f.querySelector('[type="submit"]');
    var label = b ? b.innerHTML : '';
    if (b) { b.disabled = true; b.textContent = msg; b.setAttribute('aria-busy', 'true'); }
    var t0 = Date.now();

    (function poll() {
      var ready = !!token(f);
      if (!ready && Date.now() - t0 < MAX_WAIT) { setTimeout(poll, 150); return; }
      f._kaWait = 0;
      f._kaGo = 1;
      if (b) { b.disabled = false; b.innerHTML = label; b.removeAttribute('aria-busy'); }
      push({ event: 'audit_form_held', hold_ms: Date.now() - t0, check_ready: ready });
      if (f.requestSubmit) f.requestSubmit(b || undefined); else { stamp(f); f.submit(); }
    })();
  }, true);
})();
