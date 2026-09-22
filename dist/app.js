(() => {
  'use strict';

  const meta = window.__COHON_META__ || { stats: {}, topics: [], roles: [] };
  const statusMap = { l: 'live', d: 'dead', m: 'not_listed' };
  const episodes = (window.__COHON_EPISODES__ || []).map((row) => ({
    id: `tj-${row.d}`,
    broadcast_date: row.d,
    year: Number(row.d.slice(0, 4)),
    guest: row.g,
    description: row.x,
    guest_role: meta.roles[row.r],
    topics: row.t.map((index) => meta.topics[index]),
    topic_provenance: meta.topic_provenance,
    official_audio_url: row.a ? meta.official_prefix + row.a : null,
    official_link_status: statusMap[row.s],
    official_link_checked_at: meta.stats.link_checked_at,
    podbean_url: row.p ? meta.podbean_prefix + row.p : null,
    duration: row.u || null,
    review_status: row.c ? 'metadata_crosschecked_two_first_party_sources' : 'metadata_normalized',
    transcript_status: meta.transcript_status,
    evidence_boundary: meta.evidence_boundary
  }));
  const stats = meta.stats || {};
  const PAGE_SIZE = 30;
  const state = { query: '', year: '', topic: '', role: '', status: '', sort: 'newest', page: 1 };

  const $ = (selector) => document.querySelector(selector);
  const list = $('#episode-list');
  const pagination = $('#pagination');
  const template = $('#episode-template');

  const controls = {
    query: $('#search-input'),
    year: $('#year-filter'),
    topic: $('#topic-filter'),
    role: $('#role-filter'),
    status: $('#status-filter'),
    sort: $('#sort-filter')
  };

  const formatNumber = (value) => new Intl.NumberFormat('en-US').format(value || 0);
  const formatDate = (iso) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso}T00:00:00Z`));
  const escapeHTML = (value) => String(value ?? '').replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));

  function optionize(control, values) {
    values.forEach((value) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      control.append(option);
    });
  }

  function initializeControls() {
    optionize(controls.year, [...new Set(episodes.map((episode) => String(episode.year)))].sort((a, b) => b - a));
    optionize(controls.topic, [...new Set(episodes.flatMap((episode) => episode.topics || []))].sort());
    optionize(controls.role, [...new Set(episodes.map((episode) => episode.guest_role))].sort());

    controls.query.addEventListener('input', () => { state.query = controls.query.value.trim(); state.page = 1; render(); });
    ['year', 'topic', 'role', 'status', 'sort'].forEach((key) => {
      controls[key].addEventListener('change', () => { state[key] = controls[key].value; state.page = 1; render(); });
    });
    $('#clear-filters').addEventListener('click', resetFilters);
  }

  function resetFilters() {
    Object.assign(state, { query: '', year: '', topic: '', role: '', status: '', sort: 'newest', page: 1 });
    Object.entries(controls).forEach(([key, control]) => { control.value = state[key]; });
    render();
  }

  function searchableText(episode) {
    return [episode.guest, episode.description, episode.guest_role, ...(episode.topics || [])].join(' ').toLocaleLowerCase();
  }

  function filteredEpisodes() {
    const query = state.query.toLocaleLowerCase();
    const result = episodes.filter((episode) => {
      if (query && !searchableText(episode).includes(query)) return false;
      if (state.year && String(episode.year) !== state.year) return false;
      if (state.topic && !(episode.topics || []).includes(state.topic)) return false;
      if (state.role && episode.guest_role !== state.role) return false;
      if (state.status && episode.official_link_status !== state.status) return false;
      return true;
    });

    result.sort((a, b) => {
      if (state.sort === 'oldest') return a.broadcast_date.localeCompare(b.broadcast_date);
      if (state.sort === 'guest') return a.guest.localeCompare(b.guest) || b.broadcast_date.localeCompare(a.broadcast_date);
      return b.broadcast_date.localeCompare(a.broadcast_date);
    });
    return result;
  }

  function statusLabel(status) {
    return status === 'live' ? 'Audio live' : status === 'dead' ? 'Link unavailable' : 'No link listed';
  }

  function createRecordGrid(episode) {
    const fields = [
      ['Record ID', episode.id],
      ['Review level', episode.review_status.replaceAll('_', ' ')],
      ['Transcript', episode.transcript_status.replaceAll('_', ' ')],
      ['Link check', episode.official_link_checked_at ? episode.official_link_checked_at.slice(0, 10) : 'Not checked'],
      ['Topic provenance', episode.topic_provenance],
      ['Evidence boundary', episode.evidence_boundary]
    ];
    return fields.map(([label, value]) => `<div><dt>${escapeHTML(label)}</dt><dd>${escapeHTML(value)}</dd></div>`).join('');
  }

  function createCard(episode) {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector('.episode-date').textContent = formatDate(episode.broadcast_date);
    node.querySelector('.role-pill').textContent = episode.guest_role;
    const status = node.querySelector('.status-pill');
    status.textContent = statusLabel(episode.official_link_status);
    status.classList.add(episode.official_link_status);
    node.querySelector('h3').textContent = episode.guest || 'Untitled broadcast';
    node.querySelector('.episode-description').textContent = episode.description;
    node.querySelector('.episode-tags').innerHTML = (episode.topics || []).map((tag) => `<span class="tag">${escapeHTML(tag)}</span>`).join('');
    node.querySelector('.record-grid').innerHTML = createRecordGrid(episode);

    const actions = node.querySelector('.episode-actions');
    if (episode.official_link_status === 'live' && episode.official_audio_url) {
      actions.insertAdjacentHTML('beforeend', `<a class="listen-link" href="${escapeHTML(episode.official_audio_url)}" target="_blank" rel="noopener">Listen ↗</a>`);
    } else {
      actions.insertAdjacentHTML('beforeend', '<span class="unavailable">Audio unavailable</span>');
    }
    if (episode.podbean_url) {
      actions.insertAdjacentHTML('beforeend', `<a class="source-link" href="${escapeHTML(episode.podbean_url)}" target="_blank" rel="noopener">Podcast page ↗</a>`);
    }
    return node;
  }

  function renderChips() {
    const chips = [];
    if (state.query) chips.push(['query', `“${state.query}”`]);
    ['year', 'topic', 'role', 'status'].forEach((key) => {
      if (state[key]) chips.push([key, key === 'status' ? statusLabel(state[key]) : state[key]]);
    });
    $('#active-filters').innerHTML = chips.map(([key, label]) => `<button class="filter-chip" data-filter="${key}" type="button">${escapeHTML(label)} ×</button>`).join('');
    $('#active-filters').querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', () => {
        const key = button.dataset.filter;
        state[key] = '';
        controls[key].value = '';
        state.page = 1;
        render();
      });
    });
  }

  function pageButtons(totalPages) {
    if (totalPages <= 1) return '';
    const candidates = new Set([1, totalPages, state.page - 2, state.page - 1, state.page, state.page + 1, state.page + 2]);
    const pages = [...candidates].filter((page) => page >= 1 && page <= totalPages).sort((a, b) => a - b);
    let previous = 0;
    const parts = [`<button type="button" data-page="${state.page - 1}" ${state.page === 1 ? 'disabled' : ''} aria-label="Previous page">←</button>`];
    pages.forEach((page) => {
      if (previous && page - previous > 1) parts.push('<span aria-hidden="true">…</span>');
      parts.push(`<button type="button" data-page="${page}" ${page === state.page ? 'aria-current="page"' : ''} aria-label="Page ${page}">${page}</button>`);
      previous = page;
    });
    parts.push(`<button type="button" data-page="${state.page + 1}" ${state.page === totalPages ? 'disabled' : ''} aria-label="Next page">→</button>`);
    return parts.join('');
  }

  function render() {
    const result = filteredEpisodes();
    const totalPages = Math.max(1, Math.ceil(result.length / PAGE_SIZE));
    if (state.page > totalPages) state.page = totalPages;
    const start = (state.page - 1) * PAGE_SIZE;
    const visible = result.slice(start, start + PAGE_SIZE);
    $('#results-count').textContent = `${formatNumber(result.length)} ${result.length === 1 ? 'record' : 'records'}${result.length ? ` · showing ${formatNumber(start + 1)}–${formatNumber(start + visible.length)}` : ''}`;
    renderChips();
    list.replaceChildren();
    if (!visible.length) {
      list.innerHTML = '<div class="empty-state"><strong>No broadcasts match.</strong><span>Try a broader search or reset the filters.</span></div>';
    } else {
      const fragment = document.createDocumentFragment();
      visible.forEach((episode) => fragment.append(createCard(episode)));
      list.append(fragment);
    }
    pagination.innerHTML = pageButtons(totalPages);
    pagination.querySelectorAll('button[data-page]:not(:disabled)').forEach((button) => {
      button.addEventListener('click', () => {
        state.page = Number(button.dataset.page);
        render();
        $('#archive-title').scrollIntoView({ block: 'start' });
      });
    });
  }

  function renderTimeline() {
    const counts = stats.year_counts || {};
    const years = Object.keys(counts).sort();
    const max = Math.max(...Object.values(counts));
    $('#timeline').innerHTML = years.map((year) => {
      const count = counts[year];
      const height = Math.max(4, Math.round((count / max) * 150));
      return `<button class="year-bar" type="button" data-year="${year}" role="listitem" aria-label="${year}: ${count} broadcasts" style="--h:${height}px"><strong>${count}</strong><i style="height:${height}px"></i><span>${year.slice(2)}</span></button>`;
    }).join('');
    $('#timeline').querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', () => {
        state.year = button.dataset.year;
        controls.year.value = state.year;
        state.page = 1;
        render();
        $('#archive').scrollIntoView();
      });
    });
  }

  function renderTopics() {
    const entries = Object.entries(stats.topic_counts || {}).slice(0, 8);
    const max = Math.max(...entries.map(([, count]) => count));
    $('#topic-bars').innerHTML = entries.map(([topic, count]) => `<button class="topic-row" type="button" data-topic="${escapeHTML(topic)}"><span>${escapeHTML(topic)}</span><strong>${formatNumber(count)}</strong><i style="--w:${(count / max * 100).toFixed(1)}%"></i></button>`).join('');
    $('#topic-bars').querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', () => {
        state.topic = button.dataset.topic;
        controls.topic.value = state.topic;
        state.page = 1;
        render();
        $('#archive').scrollIntoView();
      });
    });
  }

  function applyStats() {
    const links = stats.link_status_counts || {};
    const gaps = (links.dead || 0) + (links.not_listed || 0);
    $('#metric-total').textContent = formatNumber(stats.total_records);
    $('#metric-live').textContent = formatNumber(links.live);
    $('#metric-crosschecked').textContent = formatNumber(stats.two_source_records);
    $('#metric-gaps').textContent = formatNumber(gaps);
    $('#metric-years').textContent = formatNumber(stats.years);
  }

  initializeControls();
  applyStats();
  renderTimeline();
  renderTopics();
  render();
})();
