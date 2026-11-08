const siteForm = document.querySelector("#site-generator-form");

if (siteForm) {
  const message = document.querySelector("#site-generator-message");
  const serviceList = document.querySelector("#site-services");
  const addServiceButton = document.querySelector("#add-site-service");
  let serviceCount = 1;

  addServiceButton.addEventListener("click", () => {
    if (serviceCount >= 6) {
      message.textContent = "Add up to six services.";
      return;
    }
    serviceCount += 1;
    const label = document.createElement("label");
    label.className = "site-service-field";
    label.innerHTML = `Service ${serviceCount}<input name="services" maxlength="100" required placeholder="Service name"><button class="text-button remove-service" type="button">Remove</button>`;
    serviceList.append(label);
    label.querySelector(".remove-service").addEventListener("click", () => {
      label.remove();
      serviceCount -= 1;
      [...serviceList.querySelectorAll(".site-service-field")].forEach((item, index) => {
        item.firstChild.textContent = `Service ${index + 1}`;
      });
    });
  });

  siteForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = siteForm.querySelector('button[type="submit"]');
    submit.disabled = true;
    message.textContent = "Generating your website starter…";
    const payload = {
      business_name: document.querySelector("#site-business-name").value,
      tagline: document.querySelector("#site-tagline").value,
      description: document.querySelector("#site-description").value,
      services: [...serviceList.querySelectorAll('input[name="services"]')].map((input) => input.value),
      contact_email: document.querySelector("#site-email").value,
      accent_color: document.querySelector("#site-color").value,
    };
    try {
      const response = await fetch("/api/development/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Website generation failed.");
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${payload.business_name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "business"}-website.zip`;
      link.click();
      URL.revokeObjectURL(url);
      message.textContent = "Website starter generated. Unzip it and open index.html to preview.";
    } catch (error) {
      message.textContent = error.message || "Website generation failed.";
    } finally {
      submit.disabled = false;
    }
  });
}
