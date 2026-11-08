const automationForm = document.querySelector("#automation-form");

if (automationForm) {
  const outputPanel = document.querySelector("#automation-output");
  const message = document.querySelector("#automation-message");
  let pendingWorkflow = null;

  function selectedSteps() {
    return [...automationForm.querySelectorAll('input[name="workflow-step"]:checked')].map((input) => input.value);
  }

  async function submitWorkflow(approved) {
    const inputText = document.querySelector("#automation-input").value;
    const steps = selectedSteps();
    const approvalRequired = document.querySelector("#automation-approval").checked;
    const submit = automationForm.querySelector('button[type="submit"]');
    submit.disabled = true;
    message.textContent = approved ? "Running approved workflow…" : "Preparing workflow preview…";

    try {
      const response = await fetch("/api/automation/run", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          input_text: inputText,
          steps,
          approval_required: approvalRequired,
          approved,
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Workflow could not be processed.");
      pendingWorkflow = { input_text: inputText, steps, approval_required: approvalRequired };
      renderWorkflow(payload);
      message.textContent = payload.message;
    } catch (error) {
      message.textContent = error.message || "Workflow failed.";
      outputPanel.hidden = true;
    } finally {
      submit.disabled = false;
    }
  }

  automationForm.addEventListener("submit", (event) => {
    event.preventDefault();
    pendingWorkflow = null;
    submitWorkflow(!document.querySelector("#automation-approval").checked);
  });

  function renderWorkflow(result) {
    const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[char]);
    const log = result.log.map((item) =>
      `<li><strong>${escapeHtml(item.action)}</strong> — ${escapeHtml(item.message)}</li>`
    ).join("");
    const needsApproval = result.status === "awaiting_approval";
    outputPanel.innerHTML = `
      <p class="workflow-status">${needsApproval ? "Approval required" : "Workflow completed"}</p>
      <h4>Step log</h4><ol>${log}</ol>
      <h4>Output preview</h4><pre class="workflow-result"></pre>
      <div class="research-actions">
        ${needsApproval ? '<button class="action-button" id="approve-workflow" type="button">Approve &amp; run</button>' : ""}
        <button class="action-button secondary" id="download-workflow" type="button">Download output</button>
        <button class="text-button" id="export-workflow" type="button">Export workflow JSON</button>
      </div>
    `;
    outputPanel.querySelector(".workflow-result").textContent = result.output;
    if (needsApproval) {
      outputPanel.querySelector("#approve-workflow").addEventListener("click", () => submitWorkflow(true));
    }
    outputPanel.querySelector("#download-workflow").addEventListener("click", () => downloadText("workflow-output.txt", result.output));
    outputPanel.querySelector("#export-workflow").addEventListener("click", () => {
      downloadText("workflow.json", JSON.stringify(pendingWorkflow, null, 2), "application/json");
    });
    outputPanel.hidden = false;
  }

  function downloadText(filename, content, type = "text/plain;charset=utf-8") {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }
}
