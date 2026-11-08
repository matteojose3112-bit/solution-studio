const dataStudioRoot = document.querySelector("#data-studio");
const uploadInput = document.querySelector("#csv-file");
const inspectButton = document.querySelector("#inspect-csv");
const cleanButton = document.querySelector("#clean-csv");
const message = document.querySelector("#data-message");
const results = document.querySelector("#data-results");
const preview = document.querySelector("#data-preview");
const stats = document.querySelector("#data-stats");
const fileName = document.querySelector("#selected-file");

let inspectedFile = null;

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle("error", isError);
}

function selectedFile() {
  return uploadInput.files?.[0] ?? null;
}

function renderInspection(data) {
  stats.replaceChildren();
  [
    ["Rows", data.row_count],
    ["Columns", data.column_count],
    ["Blank rows", data.empty_rows],
    ["Duplicate rows", data.duplicate_rows],
  ].forEach(([label, value]) => {
    const item = document.createElement("div");
    item.className = "stat";
    const number = document.createElement("strong");
    number.textContent = value.toLocaleString();
    const caption = document.createElement("span");
    caption.textContent = label;
    item.append(number, caption);
    stats.append(item);
  });

  preview.replaceChildren();
  const table = document.createElement("table");
  const head = document.createElement("thead");
  const headerRow = document.createElement("tr");
  data.columns.forEach((column) => {
    const cell = document.createElement("th");
    cell.textContent = column.name;
    headerRow.append(cell);
  });
  head.append(headerRow);
  table.append(head);

  const body = document.createElement("tbody");
  data.preview.forEach((row) => {
    const tr = document.createElement("tr");
    row.forEach((value) => {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    });
    body.append(tr);
  });
  body.append;
  table.append(body);
  preview.append(table);
  results.hidden = false;
}

uploadInput.addEventListener("change", () => {
  inspectedFile = null;
  results.hidden = true;
  const file = selectedFile();
  fileName.textContent = file ? file.name : "No file selected";
  cleanButton.disabled = true;
  inspectButton.disabled = !file;
  showMessage(file ? "Ready to inspect. Files stay in this session and are not stored." : "Choose a CSV file to begin.");
});

inspectButton.addEventListener("click", async () => {
  const file = selectedFile();
  if (!file) return;
  inspectButton.disabled = true;
  showMessage("Inspecting CSV…");
  try {
    const form = new FormData();
    form.append("file", file);
    const response = await fetch("/api/data/inspect", { method: "POST", body: form });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Could not inspect this file.");
    inspectedFile = file;
    renderInspection(payload);
    cleanButton.disabled = false;
    showMessage(`Inspection complete · detected delimiter: ${payload.delimiter}`);
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    inspectButton.disabled = false;
  }
});

cleanButton.addEventListener("click", async () => {
  if (!inspectedFile) return;
  cleanButton.disabled = true;
  showMessage("Cleaning and preparing download…");
  const query = new URLSearchParams({
    trim_whitespace: String(document.querySelector("#trim-whitespace").checked),
    remove_empty_rows: String(document.querySelector("#remove-empty-rows").checked),
    remove_duplicate_rows: String(document.querySelector("#remove-duplicate-rows").checked),
  });
  try {
    const form = new FormData();
    form.append("file", inspectedFile);
    const response = await fetch(`/api/data/clean?${query}`, { method: "POST", body: form });
    if (!response.ok) {
      const payload = await response.json();
      throw new Error(payload.detail || "Could not clean this file.");
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${inspectedFile.name.replace(/\\.csv$/i, "")}_cleaned.csv`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    const removed = response.headers.get("x-rows-removed-empty") || "0";
    const duplicates = response.headers.get("x-rows-removed-duplicates") || "0";
    showMessage(`Download ready · removed ${removed} blank rows and ${duplicates} duplicate rows.`);
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    cleanButton.disabled = false;
  }
});
