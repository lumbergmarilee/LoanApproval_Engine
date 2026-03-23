function syncAmount(val) {
  document.getElementById("amountInput").value = val;
  clearResult();
}

function syncAmountFromInput(val) {
  document.getElementById("amountSlider").value = val;
  clearResult();
}

function syncPeriod(val) {
  document.getElementById("periodInput").value = val;
  clearResult();
}

function syncPeriodFromInput(val) {
  document.getElementById("periodSlider").value = val;
  clearResult();
}

function clearResult() {
  document.getElementById("result").innerHTML = "";
  document.getElementById("error").style.display = "none";
}

async function submitLoan() {
  clearResult();
  const code = document.getElementById("customCode").value.trim();
  if (!code) { showError("Please enter a personal code."); return; }

  const btn = document.getElementById("submitBtn");
  btn.disabled = true;
  btn.textContent = "Checking…";

  try {
    const res = await fetch("/api/loan-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        personalCode: code,
        loanAmount: Number(document.getElementById("amountInput").value),
        loanPeriod: Number(document.getElementById("periodInput").value)
      })
    });
    const data = await res.json();
    if (!res.ok) { showError(data.error); return; }

    const ok = data.decision === "positive";
    let html = '<div class="card result ' + (ok ? "result-ok" : "result-no") + '">';
    html += '<span class="badge ' + (ok ? "badge-ok" : "badge-no") + '">' + (ok ? "Approved" : "Declined") + "</span>";
    if (ok) {
      html += "<p><strong>€" + Number(data.approvedAmount).toLocaleString("en") + "</strong> over <strong>" + data.approvedPeriod + " months</strong></p>";
    } else {
      html += "<p>" + (data.reason || "Not eligible") + "</p>";
    }
    if (data.note) html += '<p class="note">' + data.note + "</p>";
    html += "</div>";
    document.getElementById("result").innerHTML = html;
  } catch (e) {
    showError("Could not reach the server. Is Flask running?");
  } finally {
    btn.disabled = false;
    btn.textContent = "Check Eligibility";
  }
}

function showError(msg) {
  const el = document.getElementById("error");
  el.textContent = msg;
  el.style.display = "block";
}