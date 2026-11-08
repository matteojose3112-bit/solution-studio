const documentForm = document.querySelector("#document-form");

if (documentForm) {
  const fileInput = document.querySelector("#document-file");
  const fileLabel = document.querySelector("#document-file-name");
  const message = document.querySelector("#document-message");
  const output = document.querySelector("#document-output");
  const extractButton = document.querySelector("#extract-document");

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    fileLabel.textContent = file ? `${file.name} · ${(file.size / 1024).toFixed(1)} KB` : "No file selected";
    extractButton.disabled = !file;
    output.hidden = true;
  });

  documentForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const file = fileInput.files[0];
    if (!file) return;
    extractButton.disabled = true;
    message.textContent = "Extracting document text…";
    output.hidden = true;

    try {
      const form = new FormData();
      form.append("file", file);
      const response = await fetch("/api/documents/extract", { method: "POST", body: form });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not extract this document.");
      const metadata = Object.entries(payload.metadata || {});
      output.innerHTML = `
        <div class="document-stats">
          <span><strong>${payload.word_count.toLocaleString()}</strong> words</span>
          <span><strong>${payload.character_count.toLocaleString()}</strong> characters</span>
          <span><strong>${payload.page_count ?? "—"}</strong> pages</span>
        </div>
        <h4>Document metadata</h4>
        <dl>${metadata.length ? metadata.map(([key, value]) => `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`).join("") : "<p>No embedded metadata found.</p>"}</dl>
        <h4>Extracted text</h4>
        <pre class="document-text"></pre>
        ${payload.truncated ? "<p class='research-message'>Text was limited to the first 100,000 characters.</p>" : ""}
        <button class="action-button secondary" id="download-document-text" type="button">Download extracted text</button>
      `;
      output.querySelector(".document-text").textContent = payload.text;
      output.querySelector("#download-document-text").addEventListener("click", () => {
        const blob = new Blob([payload.text], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = file.name.replace(/\.[^.]+$/, "") + "_extracted.txt";
        link.click();
        URL.revokeObjectURL(url);
      });
      output.hidden = false;
      message.textContent = "Extraction complete. Your file was processed in memory and was not saved.";
    } catch (error) {
      message.textContent = error.message || "Document extraction failed.";
    } finally {
      extractButton.disabled = false;
    }
  });

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[char]);
  }
}
