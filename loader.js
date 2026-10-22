/* Accredited Interchange — page loader (Webflow or GHL)
   Each page on the site holds only one custom-code embed:
     <div id="ai-root" data-page="home"></div>
     <script src="https://mylaunchpartner.github.io/accredited-interchange/loader.js"></script>
   This script fetches pages/<page>.html from the repo, drops it into the
   mount, then runs that page's scripts (nav, calculator, FAQ, GHL form/calendar).
   Edit the page files in GitHub — the live site picks up changes within ~10 min. */
(function () {
  var mount = document.getElementById('ai-root');
  if (!mount || mount.getAttribute('data-ai-loaded')) return;
  mount.setAttribute('data-ai-loaded', '1');

  var self = document.currentScript;
  var BASE = self.src.replace(/[?#].*$/, '').replace(/[^\/]*$/, '');
  var BUST = 'v=' + Math.floor(Date.now() / 300000); // new cache key every 5 min
  var page = (mount.getAttribute('data-page') || 'home').replace(/[^a-z0-9-]/gi, '');

  mount.style.minHeight = '100vh';

  function runScripts(root) {
    var list = Array.prototype.slice.call(root.querySelectorAll('script'));
    // Page scripts were written for a fresh page load. Here the page has
    // already loaded, so run any 'load' / 'DOMContentLoaded' callbacks now.
    var orig = window.addEventListener;
    var origDoc = document.addEventListener;
    window.addEventListener = function (t, f, o) {
      if ((t === 'load' || t === 'DOMContentLoaded') && document.readyState === 'complete') { setTimeout(f, 0); return; }
      return orig.call(this, t, f, o);
    };
    document.addEventListener = function (t, f, o) {
      if (t === 'DOMContentLoaded' && document.readyState !== 'loading') { setTimeout(f, 0); return; }
      return origDoc.call(this, t, f, o);
    };
    function restore() { window.addEventListener = orig; document.addEventListener = origDoc; }

    return list.reduce(function (chain, old) {
      return chain.then(function () {
        return new Promise(function (done) {
          var s = document.createElement('script');
          for (var i = 0; i < old.attributes.length; i++) s.setAttribute(old.attributes[i].name, old.attributes[i].value);
          if (old.src) { s.onload = s.onerror = done; }
          else { s.textContent = old.textContent; }
          old.parentNode.replaceChild(s, old);
          if (!old.src) done();
        });
      });
    }, Promise.resolve()).then(function () { setTimeout(restore, 50); }, restore);
  }

  fetch(BASE + 'pages/' + page + '.html?' + BUST)
    .then(function (r) {
      if (!r.ok) throw new Error('pages/' + page + '.html → ' + r.status);
      return r.text();
    })
    .then(function (html) {
      mount.innerHTML = html;
      mount.style.minHeight = '';
      return runScripts(mount);
    })
    .then(function () {
      // Honour links like /#payroll arriving from another page
      if (location.hash) {
        var t = document.getElementById(location.hash.slice(1));
        if (t) setTimeout(function () { t.scrollIntoView(); }, 120);
      }
    })
    .catch(function (err) {
      if (window.console) console.error('[AI loader]', err);
      mount.style.minHeight = '';
      mount.innerHTML = '<p style="padding:80px 24px;text-align:center;font:16px/1.6 -apple-system,sans-serif;color:#0F1222">' +
        'Sorry, this page didn’t load. Please refresh, or <a href="/contact-us">contact us</a>.</p>';
    });
})();
