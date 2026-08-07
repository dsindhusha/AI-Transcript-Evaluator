const evaluateBtn = document.getElementById("evaluateBtn");

evaluateBtn.addEventListener("click", async () => {

    const audioFile = document.getElementById("audioFile").files[0];
    const groundTruth = document.getElementById("groundTruth").value.trim();

    if (!audioFile) {
        alert("Please select an audio file.");
        return;
    }

    if (!groundTruth) {
        alert("Please enter the ground truth transcript.");
        return;
    }

    evaluateBtn.disabled = true;
    evaluateBtn.innerText = "⏳ Evaluating...";

    const formData = new FormData();

    formData.append("file", audioFile);
    formData.append("ground_truth", groundTruth);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/evaluate-audio",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.detail || "Unable to evaluate audio."
            );

        }

        const data = await response.json();

        document.getElementById("results").style.display = "block";

        showTranscript(data);

        showScore(data);

        showScoreBreakdown(data);

        showIncorrect(data.incorrect_information);

        showSimpleList(
            "missingList",
            data.missing_information,
            "No Missing Information"
        );

        showSimpleList(
            "extraList",
            data.extra_information,
            "No Extra Information"
        );

        showSimpleList(
            "conflictingList",
            data.conflicting_information,
            "No Conflicting Information"
        );

    }
    catch (error) {

        console.error(error);

        alert(error.message);

    }
    finally {

        evaluateBtn.disabled = false;

        evaluateBtn.innerText = "Evaluate Audio";

    }

});


function showTranscript(data) {

    document.getElementById("generatedTranscript").innerText =
        data.generated_transcript;

}


function showScore(data) {

    const score = data.score;

    const scoreElement = document.getElementById("score");

    const progressBar = document.getElementById("progressBar");

    const message = document.getElementById("scoreMessage");

    scoreElement.innerText = `${score}/100`;

    progressBar.style.width = `${score}%`;

    if (score >= 90) {

        progressBar.style.background = "#16a34a";
        scoreElement.style.color = "#16a34a";
        message.innerText = "Excellent";

    }

    else if (score >= 70) {

        progressBar.style.background = "#f59e0b";
        scoreElement.style.color = "#f59e0b";
        message.innerText = "Good";

    }

    else {

        progressBar.style.background = "#dc2626";
        scoreElement.style.color = "#dc2626";
        message.innerText = "Needs Improvement";

    }

}


function showScoreBreakdown(data) {

    const breakdown = data.score_breakdown;

    let html = "";

    html += `
        <div class="breakdown-row">
            <span>Starting Score</span>
            <span>${breakdown.starting_score}</span>
        </div>
    `;

    if (breakdown.incorrect.deduction > 0) {

        html += `
            <div class="breakdown-row">
                <span>Incorrect (${breakdown.incorrect.count})</span>
                <span>-${breakdown.incorrect.deduction}</span>
            </div>
        `;

    }

    if (breakdown.missing.deduction > 0) {

        html += `
            <div class="breakdown-row">
                <span>Missing (${breakdown.missing.count})</span>
                <span>-${breakdown.missing.deduction}</span>
            </div>
        `;

    }

    if (breakdown.extra.deduction > 0) {

        html += `
            <div class="breakdown-row">
                <span>Extra (${breakdown.extra.count})</span>
                <span>-${breakdown.extra.deduction}</span>
            </div>
        `;

    }

    if (breakdown.conflicting.deduction > 0) {

        html += `
            <div class="breakdown-row">
                <span>Conflicting (${breakdown.conflicting.count})</span>
                <span>-${breakdown.conflicting.deduction}</span>
            </div>
        `;

    }

    html += `
        <div class="breakdown-row breakdown-final">
            <span>Final Score</span>
            <span>${breakdown.final_score}</span>
        </div>
    `;

    document.getElementById("scoreBreakdown").innerHTML = html;

}


function showIncorrect(items) {

    const container = document.getElementById("incorrectList");

    container.innerHTML = "";

    if (items.length === 0) {

        container.innerHTML = `
            <div class="no-error">
                ✅ No Incorrect Information
            </div>
        `;

        return;

    }

    items.forEach(item => {

        container.innerHTML += `

            <div class="error-item">

                <div class="error-label">
                    Expected
                </div>

                <div>
                    ${item.expected}
                </div>

                <br>

                <div class="error-label">
                    Found
                </div>

                <div>
                    ${item.found}
                </div>

            </div>

        `;

    });

}


function showSimpleList(id, items, emptyMessage) {

    const container = document.getElementById(id);

    container.innerHTML = "";

    if (items.length === 0) {

        container.innerHTML = `
            <div class="no-error">
                ✅ ${emptyMessage}
            </div>
        `;

        return;

    }

    items.forEach(item => {

        container.innerHTML += `
            <div class="error-item">
                ${
                    typeof item === "string"
                        ? item
                        : JSON.stringify(item, null, 2)
                }
            </div>
        `;

    });

}