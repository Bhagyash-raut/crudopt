document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  const status = document.getElementById("statusMessage");

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(form);

      const res = await fetch("/contact", {
        method: "POST",
        body: formData,
      });

      if (res.redirected) {
        window.location.href = res.url;
      } else {
        status.textContent = "Submitted successfully!";
        form.reset();
      }
    });
  }
});
