function showProfile(tab) {
  document.querySelectorAll('#settings .switcher').forEach(section => {
    section.className = 'switcher disappear'
  })

  document.querySelector(tab).className = 'switcher';
}
