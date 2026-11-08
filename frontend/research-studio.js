const researchForm = document.querySelector("#research-form");

if (researchForm) {
  const sourceList = document.querySelector("#research-sources");
  const addSourceButton = document.querySelector("#add-research-source");
  const reportOutput = document.querySelector("#research-report");
  const message = document.querySelector("#research-message");
  let sourceCount = 1;

  function addSource() {
    if (sourceCount >= 8) {
      message.textContent = "Research Studio supports up to 8 sources per report.";
      return;
    }
    sourceCount += 1;
    const card = document.createElement("fieldset");
    card.className = "research-source";
    card.innerHTML = `
      <legend>Source ${sourceCount}</legend>
      <label>Source title<input name="title" maxlength="200" required placeholder="Article or report title"></label>
      <label>Source URL<input name="url" type="url" maxlength="2000" required placeholder="https://example.com/source"></label>
      <label>Relevant notes or excerpt<textarea name="notes" maxlength="4000" rows="4" required placeholder="Paste the relevant findings or excerpt from this source."></textarea></label>
      <button class="text-button remove-source" type="button">Remove source</button>
    `;
    sourceList.append(card);
    card.querySelector(".remove-source").addEventListener("click", () => {
      card.remove();
      sourceCount -= 1;
      [...sourceList.querySelectorAll(".research-source")].forEach((item, index) => {
        item.querySelector("legend").textContent = `Source ${index + 1}`;
      });
    });
  }

  addSourceButton.addEventListener("click", addSource);

  researchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = researchForm.querySelector('button[type="submit"]');
    submit.disabled = true;
    message.textContent = "Building your source-linked brief…";
    reportOutput.hidden = true;

    const sources = [...sourceList.querySelectorAll(".research-source")].map((card) => ({
      title: card.querySelector('[name="title"]').value,
      url: card.querySelector('[name="url"]').value,
      notes: card.querySelector('[name="notes"]').value,
    }));

    try {
      const response = await fetch("/api/research/report", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ question: document.querySelector("#research-question").value, sources }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not build the research report.");
      renderReport(payload);
      reportOutput.hidden = false;
      message.textContent = "Working brief generated. Verify the sources before relying on the findings.";
    } catch (error) {
      message.textContent = error.message || "Research report failed.";
    } finally {
      submit.disabled = false;
    }
  });

  function renderReport(report) {
    const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[char]);
    const points = report.key_points.length
      ? report.key_points.map((point) => `<li>${escapeHtml(point)}</li>`).join("")
      : "<li>No extractable findings were found in the supplied notes.</li>";
    const sources = report.sources.map((source) =>
      `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">[${source.id}] ${escapeHtml(source.title)}</a></li>`
    ).join("");
    const limitations = report.limitations.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
    reportOutput.innerHTML = `
      <div class="research-report-heading"><p class="eyebrow">GENERATED WORKING BRIEF</p><h3>${escapeHtml(report.question)}</h3></div>
      <h4>Executive summary</h4><p>${escapeHtml(report.executive_summary)}</p>
      <h4>Key points from supplied notes</h4><ol>${points}</ol>
      <h4>Sources</h4><ol>${sources}</ol>
      <h4>Limitations and review</h4><ul>${limitations}</ul>
      <button class="action-button secondary" id="download-research-report" type="button">Download Markdown report</button>
    `;
    document.querySelector("#download-research-report").addEventListener("click", () => {
      const markdown = [
        `# Research brief: ${report.question}`, "",
        "## Executive summary", report.executive_summary, "",
        "## Key points from supplied notes",
        ...report.key_points.map((point) => `- ${point}`), "",
        "## Sources", ...report.sources.map((source) => `- [${source.id}] [${source.title}](${source.url})`), "",
        "## Limitations and review", ...report.limitations.map((item) => `- ${item}`), "",
      ].join("\n");
      const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "research-brief.md";
      link.click();
      URL.revokeObjectURL(url);
    });
  }
}
