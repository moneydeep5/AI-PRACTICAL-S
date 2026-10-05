const input = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const errorBox = document.getElementById('errorBox');

const predictionEl = document.getElementById('prediction');
const confidenceEl = document.getElementById('confidence');
const messageEl = document.getElementById('message');
const scoreRing = document.getElementById('scoreRing');
const evidenceList = document.getElementById('evidenceList');

const bars = {
    positive: [document.getElementById('positiveBar'), document.getElementById('positiveValue')],
    neutral: [document.getElementById('neutralBar'), document.getElementById('neutralValue')],
    negative: [document.getElementById('negativeBar'), document.getElementById('negativeValue')]
};

input.addEventListener('input', () => {
    charCount.textContent = `${input.value.length} / 1000`;
});

document.querySelectorAll('.prompt').forEach(button => {
    button.addEventListener('click', () => {
        input.value = button.dataset.text;
        input.dispatchEvent(new Event('input'));
    });
});

function showError(message) {
    errorBox.textContent = message;
    errorBox.style.display = 'block';
}

function clearError() {
    errorBox.textContent = '';
    errorBox.style.display = 'none';
}

function setPredictionTheme(label) {
    const css = getComputedStyle(document.documentElement);
    const angle = label === 'positive' ? 130 : label === 'negative' ? 280 : 200;
    const color = label === 'positive' ? css.getPropertyValue('--positive') : label === 'negative' ? css.getPropertyValue('--negative') : css.getPropertyValue('--neutral');
    scoreRing.style.background = `conic-gradient(${color} ${angle}deg, rgba(255,255,255,.07) ${angle}deg)`;
    predictionEl.className = `prediction-label support-${label}`;
}

function renderEvidence(items) {
    if (!items || items.length === 0) {
        evidenceList.innerHTML = '<div class="empty-state">No strong known-word evidence was found. The model is less certain.</div>';
        return;
    }
    evidenceList.innerHTML = items.map(item => `
        <div class="evidence-item">
            <div>
                <div class="evidence-word">“${item.word}”</div>
                <div class="evidence-supports support-${item.supports}">supports ${item.supports}</div>
            </div>
            <div class="evidence-strength">strength ${item.strength}</div>
        </div>
    `).join('');
}

async function analyze() {
    clearError();
    const text = input.value.trim();
    if (!text) {
        showError('Please enter some text first.');
        input.focus();
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('span').textContent = 'Analyzing...';

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Analysis failed.');

        predictionEl.textContent = data.prediction;
        confidenceEl.textContent = `${data.confidence}%`;
        messageEl.textContent = data.message;
        setPredictionTheme(data.prediction);

        Object.keys(bars).forEach(label => {
            const value = data.probabilities[label] || 0;
            bars[label][0].style.width = `${value}%`;
            bars[label][1].textContent = `${value}%`;
        });

        renderEvidence(data.evidence);
    } catch (error) {
        showError(error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('span').textContent = 'Analyze with AI';
    }
}

analyzeBtn.addEventListener('click', analyze);

input.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') analyze();
});

document.querySelectorAll('.nav-item').forEach(button => {
    button.addEventListener('click', () => {
        const target = button.dataset.section;
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        document.querySelectorAll('.section').forEach(section => section.classList.remove('active-section'));
        button.classList.add('active');
        document.getElementById(target).classList.add('active-section');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
