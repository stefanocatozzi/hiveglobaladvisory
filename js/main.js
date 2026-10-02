document.addEventListener('DOMContentLoaded', function () {
  var year = document.getElementById('year');
  if (year) { year.textContent = new Date().getFullYear(); }

  // close the mobile nav after a link is clicked
  var navToggle = document.getElementById('nav-toggle');
  if (navToggle) {
    document.querySelectorAll('nav.primary a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (link.closest('details.lang-switch')) { return; }
        navToggle.checked = false;
      });
    });
  }

  // close the language switcher when clicking outside it
  document.addEventListener('click', function (e) {
    document.querySelectorAll('details.lang-switch[open]').forEach(function (d) {
      if (!d.contains(e.target)) { d.removeAttribute('open'); }
    });
  });
});
