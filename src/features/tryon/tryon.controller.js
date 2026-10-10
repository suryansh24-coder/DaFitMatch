/*
 * DaFitMatch — AI Fit Studio (try-on) controller
 * -------------------------------------------------------------------------
 * Powers ai-fit-studio.html.
 *
 *  - Lets the user pick a catalogue look and add a photo.
 *  - If ENV.TRY_ON_ENDPOINT is configured, the photo + look are POSTed to that
 *    service and the returned image is shown as a real AI result.
 *  - Else if ENV.TRY_ON_PROVIDER === 'huggingface', it calls the free public
 *    IDM-VTON Space on Hugging Face via the official @gradio/client (loaded on
 *    demand from a CDN) and shows the real generated try-on.
 *  - Otherwise (or if the service fails) it produces a clearly-labelled LOCAL
 *    DEMO composite. It never fabricates a "perfect" try-on and never claims
 *    a demo is a real result.
 *
 * Privacy: the chosen photo lives in memory for this tab only. Image data is
 * never written to DaFitMatchStore / localStorage. When a real provider is
 * configured, the photo is sent to that provider only.
 */
(function (global) {
  'use strict';

  var ENV = global.ENV || {};
  var MAX_BYTES = ENV.TRY_ON_MAX_BYTES || 5 * 1024 * 1024;
  var ENDPOINT = typeof ENV.TRY_ON_ENDPOINT === 'string' ? ENV.TRY_ON_ENDPOINT.trim() : '';
  var HAS_ENDPOINT = /^https?:\/\//i.test(ENDPOINT);
  var PROVIDER = (typeof ENV.TRY_ON_PROVIDER === 'string' ? ENV.TRY_ON_PROVIDER : '').trim().toLowerCase();
  var HF_TOKEN = typeof ENV.TRY_ON_HF_TOKEN === 'string' ? ENV.TRY_ON_HF_TOKEN.trim() : '';
  var HF_SPACE = (typeof ENV.TRY_ON_HF_SPACE === 'string' && ENV.TRY_ON_HF_SPACE.trim())
    ? ENV.TRY_ON_HF_SPACE.trim() : 'yisol/IDM-VTON';
  var USE_HF = !HAS_ENDPOINT && PROVIDER === 'huggingface';
  var GRADIO_CLIENT_URL = 'https://cdn.jsdelivr.net/npm/@gradio/client/dist/index.min.js';

  var outfits = [];
  var selected = null;
  var photoFile = null;
  var photoUrl = null;
  var resultUrl = null;
  var resultIsObjectUrl = false;

  function $id(id) { return document.getElementById(id); }

  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function setStatus(text, tone) {
    var el = $id('tryon-status');
    if (!el) return;
    el.textContent = text || '';
    el.className = 'mt-3 text-xs ' +
      (tone === 'error' ? 'text-red-500' : tone === 'ok' ? 'text-emerald-600' : 'text-slate-400');
  }

  /* --- Catalogue --------------------------------------------------------- */
  function loadCatalogue() {
    var select = $id('outfit-select');
    fetch('src/data/catalogue.json')
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) {
        outfits = [];
        (data.catalogues || []).forEach(function (cat) {
          (cat.outfits || []).forEach(function (o) {
            outfits.push(Object.assign({ _category: cat.name || cat.id }, o));
          });
        });
        if (!outfits.length) throw new Error('empty catalogue');
        populateSelect(select);
        preselectFromQuery();
      })
      .catch(function (err) {
        console.warn('[DaFitMatch TryOn] catalogue unavailable', err);
        select.innerHTML = '<option value="">Catalogue unavailable — serve this page over http(s)</option>';
        setStatus('Could not load the outfit catalogue. Run the site from a local server (e.g. python -m http.server) and refresh.', 'error');
      });
  }

  function populateSelect(select) {
    var byCat = {};
    outfits.forEach(function (o) {
      (byCat[o._category] = byCat[o._category] || []).push(o);
    });
    var html = '<option value="">Select an outfit…</option>';
    Object.keys(byCat).forEach(function (cat) {
      html += '<optgroup label="' + esc(cat) + '">';
      byCat[cat].forEach(function (o) {
        html += '<option value="' + esc(o.id) + '">' + esc(o.name) + ' — ' + esc(o.style || '') + '</option>';
      });
      html += '</optgroup>';
    });
    select.innerHTML = html;
  }

  function preselectFromQuery() {
    var id = new URLSearchParams(global.location.search).get('outfit');
    if (!id) return;
    if (!outfits.some(function (o) { return o.id === id; })) return;
    $id('outfit-select').value = id;
    handleOutfitChange();
  }

  function handleOutfitChange() {
    var id = $id('outfit-select').value;
    selected = outfits.filter(function (o) { return o.id === id; })[0] || null;
    var wrap = $id('outfit-preview');
    if (!selected) { wrap.classList.add('hidden'); updateGenerateState(); return; }
    $id('outfit-preview-img').src = selected.image || '';
    $id('outfit-preview-name').textContent = selected.name;
    $id('outfit-preview-items').textContent = (selected.items || []).join(' · ');
    $id('outfit-preview-colors').textContent =
      (selected.colors || []).join(', ') + (selected.platform ? ' · ' + selected.platform : '');
    wrap.classList.remove('hidden');
    updateGenerateState();
  }

  /* --- Photo ------------------------------------------------------------- */
  function revokePhoto() {
    if (photoUrl) { URL.revokeObjectURL(photoUrl); photoUrl = null; }
  }

  function handlePhotoFile(file) {
    if (!file) return;
    if (!/^image\/(png|jpe?g|webp)$/i.test(file.type)) {
      setStatus('Please choose a PNG, JPG or WebP image.', 'error');
      return;
    }
    if (file.size > MAX_BYTES) {
      setStatus('That image is larger than ' + Math.round(MAX_BYTES / 1024 / 1024) + ' MB. Choose a smaller file.', 'error');
      return;
    }
    revokePhoto();
    photoFile = file;
    photoUrl = URL.createObjectURL(file);
    $id('fit-photo-preview').src = photoUrl;
    $id('fit-photo-preview-wrap').classList.remove('hidden');
    $id('fit-photo-clear').classList.remove('hidden');
    setStatus('Photo ready: ' + file.name + ' (stays in this tab).', 'ok');
    updateGenerateState();
  }

  function clearPhoto() {
    revokePhoto();
    photoFile = null;
    $id('fit-photo-preview').removeAttribute('src');
    $id('fit-photo-preview-wrap').classList.add('hidden');
    $id('fit-photo-clear').classList.add('hidden');
    setStatus('No photo selected.', 'muted');
    updateGenerateState();
  }

  function updateGenerateState() {
    var consent = $id('tryon-consent');
    var btn = $id('btn-generate');
    if (!btn) return;
    btn.disabled = !(selected && photoFile && consent && consent.checked);
  }

  /* --- Result ------------------------------------------------------------ */
  function setResult(url, opts) {
    opts = opts || {};
    if (resultIsObjectUrl && resultUrl) URL.revokeObjectURL(resultUrl);
    resultUrl = url;
    resultIsObjectUrl = !!opts.objectUrl;

    var img = $id('result-image');
    var badge = $id('result-badge');
    var notes = $id('result-notes');
    var dl = $id('result-download');

    img.src = url;
    img.classList.remove('hidden');
    $id('result-empty').classList.add('hidden');

    if (opts.ai) {
      badge.textContent = 'AI generated' + (ENV.TRY_ON_PROVIDER ? ' · ' + ENV.TRY_ON_PROVIDER : '');
      badge.className = 'text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full border bg-emerald-50 text-emerald-700 border-emerald-200';
      notes.textContent = 'Generated by an AI try-on model (IDM-VTON) using your photo and the selected outfit. Results come from a public Hugging Face Space.';
    } else {
      badge.textContent = 'Local demo · not AI';
      badge.className = 'text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full border bg-amber-50 text-amber-700 border-amber-200';
      notes.textContent = 'This is a labelled demo composite (your photo + the outfit reference). It is not a real AI try-on. Configure TRY_ON_ENDPOINT in src/config.js to connect a real image-generation service.';
    }
    badge.classList.remove('hidden');

    if (dl) { dl.href = url; dl.classList.remove('hidden'); }
  }

  /* --- Demo composite (canvas) ------------------------------------------ */
  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var image = new Image();
      image.crossOrigin = 'anonymous';
      image.onload = function () { resolve(image); };
      image.onerror = function () { reject(new Error('could not load ' + src)); };
      image.src = src;
    });
  }

  function drawContain(ctx, img, x, y, w, h) {
    var scale = Math.min(w / img.width, h / img.height);
    var dw = img.width * scale, dh = img.height * scale;
    ctx.drawImage(img, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh);
  }

  function buildDemoComposite(userPhotoUrl, outfitImageUrl, outfitName) {
    var outfitPromise = outfitImageUrl
      ? loadImage(outfitImageUrl).catch(function () { return null; })
      : Promise.resolve(null);

    return Promise.all([loadImage(userPhotoUrl), outfitPromise]).then(function (imgs) {
      var W = 900, H = 1100, pad = 18;
      var half = (W - pad * 3) / 2;
      var canvas = document.createElement('canvas');
      canvas.width = W; canvas.height = H;
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, W, H);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 30px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('LOCAL DEMO PREVIEW — NOT AI GENERATED', W / 2, 52);

      ctx.font = '500 20px Inter, sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('Your photo (left) · ' + outfitName + ' (right)', W / 2, 86);

      var top = 120, boxH = 900 - 120;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(18, top, (W - 54) / 2, boxH);
      drawContain(ctx, imgs[0], 18, top, (W - 54) / 2, boxH);

      ctx.fillStyle = '#1e293b';
      ctx.fillRect(36 + (W - 54) / 2, top, (W - 54) / 2, boxH);
      if (imgs[1]) {
        drawContain(ctx, imgs[1], 36 + (W - 54) / 2, top, (W - 54) / 2, boxH);
      } else {
        ctx.fillStyle = '#64748b';
        ctx.fillText('No outfit image', 36 + (W - 54) / 2 + (W - 54) / 4, top + boxH / 2);
      }

      ctx.fillStyle = '#94a3b8';
      ctx.font = '500 19px Inter, sans-serif';
      ctx.fillText('DaFitMatch AI Fit Studio · configure TRY_ON_ENDPOINT for real AI', W / 2, 1060);

      return canvas.toDataURL('image/png');
    });
  }

  /* --- Service call ------------------------------------------------------ */
  function requestService(formData) {
    return fetch(ENDPOINT, { method: 'POST', body: formData })
      .then(function (resp) {
        if (!resp.ok) throw new Error('service responded ' + resp.status);
        var ct = (resp.headers.get('content-type') || '').toLowerCase();
        if (ct.indexOf('application/json') > -1) {
          return resp.json().then(function (data) {
            var url = data.image || data.url || data.output || data.result;
            if (!url) throw new Error('service did not return an image');
            return { url: url, ai: true, objectUrl: /^blob:/i.test(url) };
          });
        }
        if (ct.indexOf('image/') > -1) {
          return resp.blob().then(function (blob) {
            return { url: URL.createObjectURL(blob), ai: true, objectUrl: true };
          });
        }
        throw new Error('unexpected service response');
      });
  }

  function showDemo() {
    return buildDemoComposite(photoUrl, selected.image, selected.name)
      .then(function (url) { setResult(url, { ai: false }); });
  }

  /* --- Hugging Face IDM-VTON provider ----------------------------------- */
  var gradioClientPromise = null;
  function loadGradioClient() {
    if (!gradioClientPromise) {
      gradioClientPromise = import(/* webpackIgnore: true */ GRADIO_CLIENT_URL)
        .catch(function (err) {
          gradioClientPromise = null;
          throw new Error('could not load the AI client library (check your connection)');
        });
    }
    return gradioClientPromise;
  }

  function urlToFile(url, name) {
    return fetch(url)
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.blob(); })
      .then(function (blob) {
        var type = blob.type || 'image/jpeg';
        if (type.indexOf('image/') !== 0) type = 'image/jpeg';
        return new File([blob], name, { type: type });
      });
  }

  function requestHuggingFace() {
    var garmentUrl = selected.tryOnImage || selected.image;
    var garmentName = selected.id + '-garment.jpg';
    return Promise.all([
      loadGradioClient(),
      urlToFile(garmentUrl, garmentName)
    ]).then(function (res) {
      var mod = res[0];
      var garmentFile = res[1];
      var Client = mod.Client;
      var handle_file = mod.handle_file;
      if (!Client || !handle_file) throw new Error('AI client library has an unexpected shape');

      var connectOptions = HF_TOKEN ? { token: HF_TOKEN } : {};
      return Client.connect(HF_SPACE, connectOptions).then(function (app) {
        var description = [selected.name].concat(selected.items || []).join(', ');
        var payload = [
          { background: handle_file(photoFile), layers: [], composite: null },
          handle_file(garmentFile),
          description,
          true,
          false,
          30,
          42
        ];
        return app.predict('/tryon', payload);
      });
    }).then(function (result) {
      var data = result && result.data;
      var out = Array.isArray(data) ? data[0] : data;
      var url = out && (out.url || out.path || (typeof out === 'string' ? out : null));
      if (!url) throw new Error('the AI service did not return an image');
      return { url: url, ai: true, objectUrl: false };
    });
  }

  /* --- Generate ---------------------------------------------------------- */
  function generate() {
    if (!selected) { setStatus('Choose an outfit first.', 'error'); return; }
    if (!photoFile) { setStatus('Add a photo first.', 'error'); return; }
    if (!$id('tryon-consent').checked) { setStatus('Please confirm you consent to using this photo.', 'error'); return; }

    var btn = $id('btn-generate');
    btn.disabled = true;

    if (USE_HF) {
      setStatus('Generating your realistic try-on with AI — this can take 1–2 minutes…', 'muted');
      requestHuggingFace()
        .then(function (res) {
          setResult(res.url, res);
          setStatus('Done — your AI try-on is ready.', 'ok');
        })
        .catch(function (err) {
          console.warn('[DaFitMatch TryOn] Hugging Face error', err);
          var hint = HF_TOKEN ? '' : ' Add a free Hugging Face token (TRY_ON_HF_TOKEN in src/config.js) if this keeps failing.';
          setStatus('AI service unavailable (' + err.message + ').' + hint + ' Showing a labelled demo instead.', 'error');
          return showDemo();
        })
        .then(function () { updateGenerateState(); });
      return;
    }

    if (!HAS_ENDPOINT) {
      setStatus('Building your demo preview…', 'muted');
      showDemo()
        .then(function () {
          setStatus('Demo preview ready. This is not a real AI try-on — see the note.', 'ok');
        })
        .catch(function (err) {
          console.error('[DaFitMatch TryOn] demo failed', err);
          setStatus('Could not build the preview: ' + err.message, 'error');
        })
        .then(function () { updateGenerateState(); });
      return;
    }

    var form = new FormData();
    form.append('image', photoFile, photoFile.name);
    form.append('outfit_id', selected.id);
    form.append('outfit_name', selected.name);
    form.append('items', (selected.items || []).join(', '));
    form.append('colors', (selected.colors || []).join(', '));
    form.append('prompt', 'Photorealistic virtual try-on: keep the person identical and dress them in the selected outfit.');

    setStatus('Sending your photo to the AI service…', 'muted');
    requestService(form)
      .then(function (res) {
        setResult(res.url, res);
        setStatus('Done.', 'ok');
      })
      .catch(function (err) {
        console.warn('[DaFitMatch TryOn] service error', err);
        setStatus('The AI service could not be reached (' + err.message + '). Showing a labelled demo instead.', 'error');
        return showDemo();
      })
      .then(function () { updateGenerateState(); });
  }

  /* --- Init -------------------------------------------------------------- */
  function bind() {
    var select = $id('outfit-select');
    if (select) select.addEventListener('change', handleOutfitChange);

    var input = $id('fit-photo-input');
    if (input) input.addEventListener('change', function () {
      if (this.files && this.files[0]) handlePhotoFile(this.files[0]);
    });

    var clear = $id('fit-photo-clear');
    if (clear) clear.addEventListener('click', clearPhoto);

    var consent = $id('tryon-consent');
    if (consent) consent.addEventListener('change', updateGenerateState);

    var btn = $id('btn-generate');
    if (btn) btn.addEventListener('click', generate);

    global.addEventListener('beforeunload', function () {
      revokePhoto();
      if (resultIsObjectUrl && resultUrl) URL.revokeObjectURL(resultUrl);
    });
  }

  function init() {
    bind();
    loadCatalogue();
    updateGenerateState();
    if (USE_HF) {
      setStatus(HF_TOKEN
        ? 'Real AI try-on enabled (Hugging Face · ' + HF_SPACE + '). Pick a look and add your photo.'
        : 'Real AI try-on is on, but no Hugging Face token is set. Add one in src/config.js, or a demo will be shown.', 'muted');
    } else if (!HAS_ENDPOINT) {
      setStatus('Demo mode: no AI service configured — you will get a clearly-labelled local preview.', 'muted');
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  global.DaFitMatchTryOn = { refresh: updateGenerateState };
})(window);
