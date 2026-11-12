(() => {
  const search = document.querySelector('#search');
  if (!search) return;
  let category = '全部工具';
  const cards = [...document.querySelectorAll('.tool-card')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const card of cards) {
      const visible = (category === '全部工具' || card.dataset.category === category) && card.dataset.search.toLocaleLowerCase().includes(query);
      card.hidden = !visible;
      if (visible) count++;
    }
    document.querySelector('.empty').hidden = count !== 0;
    document.querySelector('#result-count').textContent = `找到 ${count} 个工具`;
    for (const button of buttons) {
      const active = button.dataset.filter === category;
      button.classList.toggle('selected', active);
      button.setAttribute('aria-pressed', String(active));
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filter(); }));
  search.addEventListener('input', filter);
  document.querySelector('#reset').addEventListener('click', () => { category = '全部工具'; search.value = ''; filter(); search.focus(); });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName) && !document.activeElement.isContentEditable && !event.ctrlKey && !event.metaKey && !event.altKey) { event.preventDefault(); search.focus(); }
    if (event.key === 'Escape' && document.activeElement === search) { search.value = ''; filter(); }
  });
})();
