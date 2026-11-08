const statusLabel = document.querySelector("#api-status");
const statusDot = document.querySelector(".status-dot");
const versionLabel = document.querySelector("#app-version");

async function connectToApi() {
  try {
    const [healthResponse, versionResponse] = await Promise.all([
      fetch("/api/health", { headers: { Accept: "application/json" } }),
      fetch("/api/version", { headers: { Accept: "application/json" } }),
    ]);

    if (!healthResponse.ok || !versionResponse.ok) {
      throw new Error("API returned an unsuccessful response");
    }

    const health = await healthResponse.json();
    const version = await versionResponse.json();

    if (health.status !== "ok") {
      throw new Error("API health check did not pass");
    }

    statusLabel.textContent = "Local API connected";
    statusDot.classList.add("online");
    versionLabel.textContent = `· v${version.version}`;
  } catch {
    statusLabel.textContent = "API connection unavailable";
    versionLabel.textContent = "· offline";
  }
}

connectToApi();
