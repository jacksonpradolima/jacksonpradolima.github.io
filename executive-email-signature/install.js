'use strict';
function selectSignature(key) {
  const range = document.createRange();
  range.selectNodeContents(document.getElementById(key));
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
  document.getElementById(key + '-status').textContent = 'Signature selected. Press Ctrl+C (Command+C on Mac), then paste into Gmail with Ctrl+V.';
}
document.querySelectorAll('[data-select]').forEach(button => button.addEventListener('click', () => selectSignature(button.dataset.select)));
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const key = button.dataset.copy;
  const node = document.getElementById(key);
  try {
    if (!window.isSecureContext || !navigator.clipboard?.write || !window.ClipboardItem) throw new Error('Rich clipboard unavailable');
    await navigator.clipboard.write([new ClipboardItem({
      'text/html': new Blob([node.innerHTML], {type: 'text/html'}),
      'text/plain': new Blob([node.innerText], {type: 'text/plain'})
    })]);
    document.getElementById(key + '-status').textContent = 'Signature copied. Paste into Gmail with Ctrl+V.';
  } catch (error) {
    selectSignature(key);
    document.getElementById(key + '-status').textContent = 'Automatic copy failed. Signature selected: press Ctrl+C (Command+C on Mac), then paste into Gmail.';
  }
}));
const urls = [...new Set([...document.querySelectorAll('.signature img')].map(img => img.src))];
Promise.all(urls.map(url => new Promise(resolve => {
  const li = document.createElement('li');
  const link = document.createElement('a'); link.href = url; link.textContent = url.split('/').pop();
  li.append(link, ' — checking…'); document.getElementById('assets').append(li);
  const img = new Image();
  const timer = setTimeout(() => finish(false), 15000);
  let done = false;
  function finish(ok) {
    if (done) return; done = true; clearTimeout(timer);
    li.lastChild.textContent = ok ? ' — public image loaded' : ' — unavailable; do not install yet';
    resolve(ok);
  }
  img.onload = () => finish(img.naturalWidth > 0); img.onerror = () => finish(false); img.src = url;
}))).then(results => {
  document.getElementById('hosting').textContent = results.every(Boolean) ? 'All five public images loaded successfully in this browser.' : 'Hosting is not ready: one or more images failed. Do not install until all five load.';
});
