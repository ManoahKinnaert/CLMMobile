const scripts = [
  {
    containerId: "location-script-container",
    buttonId: "copy-location-btn",
    script: `cat /dev/location > /dev/null &`,
  },
  {
    containerId: "install-script-container",
    buttonId: "copy-install-btn",
    script: `apk add curl && curl -fsSL https://raw.githubusercontent.com/ManoahKinnaert/CLMMobile/main/install_ish.sh | ash`,
  },
  {
    containerId: "launch-script-container",
    buttonId: "copy-launch-btn",
    script: `timer`,
  },
];

async function copyToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {}
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);
  const copied = document.execCommand("copy");
  textarea.remove();
  return copied;
}

scripts.forEach(({ containerId, buttonId, script }) => {
  const container = document.getElementById(containerId);
  const button = document.getElementById(buttonId);

  container.innerHTML = Prism.highlight(script, Prism.languages.bash, "bash");

  const originalButtonHTML = button.innerHTML;
  let resetTimer;
  button.addEventListener("click", async () => {
    const copied = await copyToClipboard(script);
    if (!copied) return;

    button.textContent = button.dataset.copiedText || "Copied!";
    clearTimeout(resetTimer);
    resetTimer = setTimeout(() => {
      button.innerHTML = originalButtonHTML;
    }, 2000);
  });
});
