/*!
 * In-page audit form for service, case study and blog pages.
 * Before: every "Free audit" button sent the visitor to the homepage and
 * opened the form there. Now the form opens on the page they are reading.
 * The links still point to /#contact, so without JS they work as before.
 * Posts to /api/lead like the homepage form; the backend records this page.
 */
(function () {
  'use strict';
  if (document.getElementById('audit-modal')) return; // homepage has its own form

  var LANGS = ['de', 'fr', 'es', 'it', 'nl', 'pt'];
  var seg = location.pathname.split('/')[1];
  var lang = LANGS.indexOf(seg) > -1 ? seg : 'en';

  // Wording is copied from each language's homepage form.
  var T = {
    en: { close: 'Close', kicker: 'Free, no obligation', title: 'Book Your Free Audit',
      sub: "Leave your details and I'll come back within 24 hours to book your free 15-minute audit.",
      name: 'Your Name *', namePh: 'e.g. Sarah Mitchell', email: 'Email Address *', emailPh: 'you@company.com',
      opt: 'optional', msg: 'What do you need help with?',
      msgPh: "e.g. I need help ranking locally / my Google Ads aren't producing leads / I need a new site...",
      send: 'Send Request →', foot: 'Reply within 24 hours · No spam, ever' },
    de: { close: 'Schließen', kicker: 'Kostenlos und unverbindlich', title: 'Kostenlosen Audit buchen',
      sub: 'Ich prüfe Ihre Anzeigen, Ihre Website oder Ihre Sichtbarkeit in der Suche 15 Minuten lang live und nenne Ihnen eine Sache, die Sie diese Woche verbessern können.',
      name: 'Ihr Name *', namePh: 'z. B. Anna Schmidt', email: 'E-Mail-Adresse *', emailPh: 'sie@firma.de',
      opt: 'optional', msg: 'Wobei brauchen Sie Unterstützung?', msgPh: '',
      send: 'Anfrage senden →', foot: 'Antwort innerhalb von 24 Stunden · Kein Spam, niemals' },
    fr: { close: 'Fermer', kicker: 'Gratuit, sans engagement', title: 'Réservez votre audit gratuit',
      sub: "J'examine vos publicités, votre site ou votre visibilité dans la recherche en direct pendant 15 minutes, et je vous indique une chose à corriger cette semaine.",
      name: 'Votre nom *', namePh: 'ex. : Claire Martin', email: 'Adresse e-mail *', emailPh: 'vous@entreprise.fr',
      opt: 'facultatif', msg: "Sur quoi avez-vous besoin d'aide ?", msgPh: '',
      send: 'Envoyer la demande →', foot: 'Réponse sous 24 heures · Jamais de spam' },
    es: { close: 'Cerrar', kicker: 'Gratis, sin compromiso', title: 'Reserva tu auditoría gratuita',
      sub: 'Reviso tus anuncios, tu web o tu presencia en buscadores en directo durante 15 minutos y te digo una cosa que puedes corregir esta semana.',
      name: 'Tu nombre *', namePh: 'p. ej., Laura García', email: 'Correo electrónico *', emailPh: 'tu@empresa.com',
      opt: 'opcional', msg: '¿En qué necesitas ayuda?', msgPh: '',
      send: 'Enviar solicitud →', foot: 'Respuesta en 24 horas · Nunca spam' },
    it: { close: 'Chiudi', kicker: 'Gratuito, senza impegno', title: 'Prenoti il Suo audit gratuito',
      sub: 'Analizzo dal vivo per 15 minuti i Suoi annunci, il Suo sito o la Sua visibilità nella ricerca e Le indico una cosa da sistemare questa settimana.',
      name: 'Il Suo nome *', namePh: 'es. Giulia Rossi', email: 'Indirizzo email *', emailPh: 'lei@azienda.it',
      opt: 'facoltativo', msg: 'In cosa Le serve aiuto?', msgPh: '',
      send: 'Invia la richiesta →', foot: 'Risposta entro 24 ore · Mai spam' },
    nl: { close: 'Sluiten', kicker: 'Gratis en vrijblijvend', title: 'Plan uw gratis audit',
      sub: 'Ik bekijk in 15 minuten live uw advertenties, uw website of uw vindbaarheid, en vertel u één ding dat u deze week kunt verbeteren.',
      name: 'Uw naam *', namePh: 'bijv. Sanne de Vries', email: 'E-mailadres *', emailPh: 'u@bedrijf.nl',
      opt: 'optioneel', msg: 'Waarmee kan ik u helpen?', msgPh: '',
      send: 'Aanvraag versturen →', foot: 'Reactie binnen 24 uur · Nooit spam' },
    pt: { close: 'Fechar', kicker: 'Gratuito e sem compromisso', title: 'Agende sua auditoria gratuita',
      sub: 'Vou analisar seus anúncios, seu site ou sua presença nas buscas ao vivo, em 15 minutos, e te dizer uma coisa que você pode corrigir esta semana.',
      name: 'Seu nome *', namePh: 'ex.: Ana Souza', email: 'E-mail *', emailPh: 'voce@empresa.com.br',
      opt: 'opcional', msg: 'Com o que você precisa de ajuda?', msgPh: '',
      send: 'Enviar solicitação →', foot: 'Resposta em até 24 horas · Nunca envio spam' }
  }[lang];

  var CSS =
    '.lf-ov{display:none;position:fixed;inset:0;z-index:2147483002;background:rgba(8,26,54,.66);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);align-items:center;justify-content:center;padding:20px;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}' +
    '.lf-ov.on{display:flex}' +
    '.lf-card{background:#fff;border-radius:20px;padding:38px;max-width:470px;width:100%;margin:auto;position:relative;box-shadow:0 40px 90px rgba(8,26,54,.35);animation:lf-in .25s ease;color:#0B2143;text-align:left;box-sizing:border-box}' +
    '.lf-card *{box-sizing:border-box}' +
    '@keyframes lf-in{from{opacity:0;transform:translateY(16px) scale(.97)}to{opacity:1;transform:none}}' +
    '.lf-x{position:absolute;top:16px;right:16px;background:#F4F7FB;border:0;width:34px;height:34px;border-radius:50%;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#5C6E8C;line-height:1}' +
    '.lf-x:hover{background:#0B2143;color:#fff}' +
    '.lf-k{font-family:var(--mono,ui-monospace,monospace);font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:#166FDB;display:block;margin:0 0 10px}' +
    '.lf-t{font-family:var(--display,inherit);font-size:26px;font-weight:700;letter-spacing:-.015em;margin:0 0 8px;color:#0B2143;line-height:1.2;padding-right:30px}' +
    '.lf-s{font-size:14px;color:#5C6E8C;margin:0 0 22px;line-height:1.6}' +
    '.lf-f{margin:0 0 16px}' +
    '.lf-f label{font-size:12.5px;font-weight:600;color:#2E4368;display:block;margin:0 0 6px}' +
    '.lf-f label span{color:#8B9AB4;font-weight:400}' +
    '.lf-f input,.lf-f textarea{width:100%;padding:12px 14px;border:1.5px solid #DDE5F0;border-radius:10px;font-size:16px;font-family:inherit;color:#0B2143;outline:none;background:#fff;margin:0}' +
    '.lf-f input:focus,.lf-f textarea:focus{border-color:#166FDB;box-shadow:0 0 0 3px rgba(28,121,233,.14)}' +
    '.lf-f textarea{resize:vertical}' +
    '.lf-go{width:100%;padding:15px;background:#166FDB;color:#fff;border:0;border-radius:12px;font-size:15.5px;font-weight:700;cursor:pointer;font-family:inherit;margin-top:8px}' +
    '.lf-go:hover{background:#0F5FC4}.lf-go:disabled{opacity:.7;cursor:wait}' +
    '.lf-foot{font-family:var(--mono,ui-monospace,monospace);font-size:11px;letter-spacing:.04em;color:#8B9AB4;text-align:center;margin:14px 0 0}' +
    '.lf-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}' +
    '@media(max-width:480px){.lf-ov{padding:12px}.lf-card{padding:28px 20px 22px}.lf-t{font-size:23px}}';

  var ov, lastFocus, tsLoaded = false;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function build() {
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
    var next = 'https://marketingkamran.com/' + (lang === 'en' ? '' : lang + '/') + 'thankyou.html';
    ov = document.createElement('div');
    ov.className = 'lf-ov';
    ov.innerHTML =
      '<div class="lf-card" role="dialog" aria-modal="true" aria-labelledby="lf-title">' +
      '<button type="button" class="lf-x" aria-label="' + esc(T.close) + '">×</button>' +
      '<span class="lf-k">' + esc(T.kicker) + '</span>' +
      '<p class="lf-t" id="lf-title">' + esc(T.title) + '</p>' +
      '<p class="lf-s">' + esc(T.sub) + '</p>' +
      '<form action="/api/lead" method="POST" id="lf-form">' +
      '<input type="hidden" name="_next" value="' + next + '">' +
      '<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" class="lf-hp">' +
      '<div class="lf-f"><label for="lf-name">' + esc(T.name) + '</label><input id="lf-name" type="text" name="name" required autocomplete="name" autocapitalize="words" placeholder="' + esc(T.namePh) + '"></div>' +
      '<div class="lf-f"><label for="lf-mail">' + esc(T.email) + '</label><input id="lf-mail" type="email" name="contact" required inputmode="email" autocomplete="email" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="' + esc(T.emailPh) + '"></div>' +
      '<div class="lf-f"><label for="lf-wa">WhatsApp <span>(' + esc(T.opt) + ')</span></label><input id="lf-wa" type="tel" name="whatsapp" inputmode="tel" autocomplete="tel" placeholder="+44 7700 900000"></div>' +
      '<div class="lf-f"><label for="lf-msg">' + esc(T.msg) + '</label><textarea id="lf-msg" name="message" rows="3" placeholder="' + esc(T.msgPh) + '"></textarea></div>' +
      '<div class="cf-turnstile" data-sitekey="0x4AAAAAAFrmwIHjyjDHaleJ" data-action="free_audit"></div>' +
      '<button type="submit" class="lf-go">' + esc(T.send) + '</button>' +
      '</form>' +
      '<p class="lf-foot">' + esc(T.foot) + '</p>' +
      '</div>';
    document.body.appendChild(ov);
    ov.addEventListener('click', function (e) { if (e.target === ov || e.target.closest('.lf-x')) close(); });
    ov.querySelector('form').addEventListener('submit', function (e) {
      var b = this.querySelector('.lf-go');
      if (b.disabled) { e.preventDefault(); return; }
      b.disabled = true; // stop double submits; the page navigates to the thank-you page
      setTimeout(function () { b.disabled = false; }, 8000);
      push({ event: 'audit_form_submit', audit_form: 'inpage' });
    });
  }

  function push(o) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(o); }

  function open(source) {
    if (!ov) build();
    if (!tsLoaded) {
      tsLoaded = true;
      var s = document.createElement('script');
      s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
      s.async = true;
      document.head.appendChild(s);
    }
    lastFocus = document.activeElement;
    ov.classList.add('on');
    document.documentElement.style.overflow = 'hidden';
    push({ event: 'audit_modal_open', audit_form: 'inpage', audit_cta: source || '' });
    setTimeout(function () { var f = document.getElementById('lf-name'); if (f) f.focus(); }, 60);
  }

  function close() {
    if (!ov) return;
    ov.classList.remove('on');
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // A link counts as an audit CTA when it points at a homepage (/, /xx/, /index.html) with #contact.
  function isAuditLink(a) {
    if (!a.hash || a.hash !== '#contact' || a.origin !== location.origin) return false;
    return /^\/([a-z]{2}\/)?(index\.html)?$/.test(a.pathname);
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || !isAuditLink(a)) return;
    e.preventDefault();
    var cls = a.className || '';
    open(/float-cta/.test(cls) ? 'float' : (a.closest('header,nav') ? 'nav' : 'body'));
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ov && ov.classList.contains('on')) close();
  });
  window.openAuditForm = open;
})();
