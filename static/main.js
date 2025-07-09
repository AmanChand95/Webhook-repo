async function loadEvents() {
  try {
    const res  = await fetch('/events');
    if (!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    const ul   = document.getElementById('events');
    ul.innerHTML = '';

    data.forEach(e => {
      // determine badge color & label
      const badge = document.createElement('span');
      badge.className = `badge ${e.type}`;
      badge.textContent = e.type.replace('_', ' ');

      // build message
      let mainMsg = '';
      if (e.type === 'push') {
        mainMsg = `${e.author} pushed to <span class="branch">${e.to_branch}</span>`;
      } else if (e.type === 'pull_request') {
        const action = e.action === 'merged' ? 'merged' : 'submitted a pull request from';
        mainMsg = `${e.author} ${action} <span class="branch">${e.from_branch}</span> → <span class="branch">${e.to_branch}</span>`;
      }

      // wrap into li
      const li = document.createElement('li');
      li.appendChild(badge);

      const msg = document.createElement('div');
      msg.className = 'event-msg';
      msg.innerHTML = mainMsg;
      // timestamp below
      const ts = document.createElement('span');
      ts.className = 'timestamp';
      ts.textContent = new Date(e.timestamp).toUTCString();
      msg.appendChild(ts);

      li.appendChild(msg);
      ul.appendChild(li);
    });

  } catch (err) {
    console.error('Failed to load events:', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadEvents();
  setInterval(loadEvents, 15000);
});
