// Sofra Notes — lightweight enhancements
(() => {
  const form = document.querySelector("[data-newsletter]");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]').value.trim();
      if (!email) return;
      form.innerHTML = `<p style="margin:0;color:var(--cream)">Teşekkürler — check your inbox for a confirmation note.</p>`;
    });
  }

  // Mark external links
  document.querySelectorAll('a[href^="http"]').forEach((a) => {
    if (!a.hostname.endsWith("sofranotes.com")) {
      a.setAttribute("rel", "noopener external");
      a.setAttribute("target", "_blank");
    }
  });
})();
