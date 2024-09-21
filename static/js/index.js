import DerivAPIBasic from 'https://cdn.skypack.dev/@deriv/deriv-api/dist/DerivAPIBasic';

const app_id = 63289; // Replace with your app_id
const connection = new WebSocket(`wss://ws.derivws.com/websockets/v3?app_id=${app_id}`);
const api = new DerivAPIBasic({ connection });

const assets = {
    "1HZ10V": { name: "VOLATILITY 10 (1s) INDEX", precision: 2 },
    "R_10": { name: "VOLATILITY 10 INDEX", precision: 3 },
    "1HZ25V": { name: "VOLATILITY 25 (1s) Index", precision: 2 },
    "R_25": { name: "VOLATILITY 25 INDEX", precision: 3 },
    "1HZ50V": { name: "VOLATILITY 50 (1s) Index", precision: 2 },
    "R_50": { name: "VOLATILITY 50 INDEX", precision: 4 },
    "1HZ75V": { name: "VOLATILITY 75 (1s) Index", precision: 2 },
    "R_75": { name: "VOLATILITY 75 INDEX", precision: 4 },
    "1HZ100V": { name: "VOLATILITY 100 (1s) Index", precision: 2 },
    "R_100": { name: "VOLATILITY 100 INDEX", precision: 2 }
};

let selectedAssetSymbol = "R_50"; // Default asset
let precision = 4; // Default precision
let tickList = [];
let previousTick = null;
const maxTicksToTrack = 60;
let ema = null; // Store the current EMA value
const period = 20;

// DOM elements
const assetSelect = document.getElementById('asset-select');
const predictionBox = document.getElementById('prediction');
const ticksDataDiv = document.getElementById('tick-data');
const digitBox = document.getElementById('digit');
const evenProgress = document.getElementById('even-progress');
const oddProgress = document.getElementById('odd-progress');
const evenPercent = document.getElementById('even-percent');
const oddPercent = document.getElementById('odd-percent');
const overProgress = document.getElementById('over-progress');
const underProgress = document.getElementById('under-progress');
const overPercent = document.getElementById('over-percent');
const underPercent = document.getElementById('under-percent');
const scanDigitButton = document.getElementById('scan-digit-btn');

// Format tick value to preserve precision (including trailing zeros)
const formatTick = (tick) => {
    return parseFloat(tick).toFixed(precision); // Use toFixed to preserve trailing zeros
};

// Populate asset dropdown
const populateAssetDropdown = () => {
    for (const [symbol, asset] of Object.entries(assets)) {
        const option = document.createElement('option');
        option.value = symbol;
        option.textContent = asset.name;
        assetSelect.appendChild(option);
    }
};

// Ensure selectedAssetSymbol is valid
const subscribeTicks = async () => {
    selectedAssetSymbol = assetSelect.value || selectedAssetSymbol;
    precision = assets[selectedAssetSymbol].precision;

    const tickRequest = { ticks: selectedAssetSymbol, subscribe: 1 };

    try {
        await api.subscribe(tickRequest);
        connection.addEventListener('message', tickResponse);
        console.log('Subscribed to ticks.');
    } catch (error) {
        console.error('Error subscribing to ticks:', error);
    }
};

const unsubscribeTicks = async () => {
    try {
        await api.send({ forget_all: 'ticks' });
        connection.removeEventListener('message', tickResponse);
        tickList = [];
        previousTick = null;
        ema = null;
        ticksDataDiv.innerHTML = 'No data yet';
        resetProgressBars(); // Reset progress bars when unsubscribing
        console.log('Successfully unsubscribed from ticks.');
    } catch (error) {
        console.error('Error unsubscribing from ticks:', error);
    }
};

// Handle incoming tick data
const analyzeTick = (currentTick) => {
    if (!assets[selectedAssetSymbol]) {
        console.error(`Selected asset symbol "${selectedAssetSymbol}" is not valid.`);
        unsubscribeTicks();
        return;
    }

    const currentQuote = formatTick(currentTick.quote); // Use formatted tick value
    tickList.push(currentQuote);
    if (tickList.length > maxTicksToTrack) tickList.shift();

    const currentDigit = parseInt(currentQuote.replace('.', '').slice(-1), 10); // Extract digit
    const evenOdd = currentDigit % 2 === 0 ? "even" : "odd";

    if (ema === null && tickList.length >= period) {
        ema = calculateInitialEMA(tickList.slice(-period).map(q => parseFloat(q)));
    } else if (ema !== null) {
        ema = calculateEMA(parseFloat(currentQuote), ema);
    }

    let prediction = tickList.length >= 10 ? simplePrediction() : 'N/A';
    if (tickList.length >= period) {
        prediction = parseFloat(currentQuote) > ema ? 'rise' : 'fall';
    }

    updateProgressBars(currentDigit); // Update progress bars for even/odd and over/under

    ticksDataDiv.innerHTML = `
        <pre>
--------------------------------------------
Current Tick: ${currentQuote}
Even/Odd: ${evenOdd}
Digit: ${currentDigit}
Prediction: ${prediction}
--------------------------------------------
        </pre>
    `;

    predictionBox.textContent = `Prediction: ${prediction}`;
    predictionBox.style.backgroundColor = prediction === 'rise' ? 'green' : 'red';
    previousTick = currentTick;
};

// Function to calculate the initial EMA (simple moving average)
const calculateInitialEMA = (ticks) => {
    const sum = ticks.reduce((acc, tick) => acc + tick, 0);
    return sum / ticks.length;
};

// Function to calculate EMA for the current tick
const calculateEMA = (currentTick, previousEMA) => {
    const multiplier = 2 / (period + 1);
    return (currentTick - previousEMA) * multiplier + previousEMA;
};

// Update the progress bars for Even/Odd and Over/Under
const updateProgressBars = (currentDigit) => {
    // Even/Odd Progress Bar Calculation
    const evenCount = tickList.filter(tick => parseInt(tick.replace('.', '').slice(-1), 10) % 2 === 0).length;
    const oddCount = tickList.length - evenCount;
    const evenPercentage = (evenCount / tickList.length) * 100;
    const oddPercentage = 100 - evenPercentage;

    evenProgress.style.width = `${evenPercentage}%`;
    evenPercent.textContent = `${Math.round(evenPercentage)}%`;

    oddProgress.style.width = `${oddPercentage}%`;
    oddPercent.textContent = `${Math.round(oddPercentage)}%`;

    // Over/Under Progress Bar Calculation (based on last digit, not the full tick value)
    const underCount = tickList.filter(tick => parseInt(tick.replace('.', '').slice(-1), 10) < 5).length;
    const overCount = tickList.length - underCount;
    const underPercentage = (underCount / tickList.length) * 100;
    const overPercentage = 100 - underPercentage;

    underProgress.style.width = `${underPercentage}%`;
    underPercent.textContent = `${Math.round(underPercentage)}%`;

    overProgress.style.width = `${overPercentage}%`;
    overPercent.textContent = `${Math.round(overPercentage)}%`;
};

// Perform a simple prediction based on historical data
const simplePrediction = () => {
    if (tickList.length < maxTicksToTrack) return 'N/A';

    const recentTicks = tickList.slice(-maxTicksToTrack).map(tick => parseFloat(tick));
    const avg = recentTicks.reduce((sum, tick) => sum + tick, 0) / recentTicks.length;

    return avg > 5 ? 'Rise' : 'Fall';
};

// Reset progress bars
const resetProgressBars = () => {
    evenProgress.style.width = `0%`;
    oddProgress.style.width = `0%`;
    evenPercent.textContent = `0%`;
    oddPercent.textContent = `0%`;

    overProgress.style.width = `0%`;
    underProgress.style.width = `0%`;
    overPercent.textContent = `0%`;
    underPercent.textContent = `0%`;
};

// Handle incoming tick data via WebSocket
const tickResponse = (event) => {
    const data = JSON.parse(event.data);
    if (data.tick) {
        analyzeTick(data.tick);
    }
};

// Generate a random number between 0 and 9 for scan digit
const getRandomNumber = () => Math.floor(Math.random() * 10);

// Scan Digit functionality
const startUpdatingDigit = () => {
    digitBox.textContent = getRandomNumber(); // Update the digit display with random value
};

scanDigitButton.addEventListener('click', () => {
    startUpdatingDigit(); // Trigger the scan digit functionality when button is clicked
});

// Event listeners
document.getElementById('subscribe-btn').addEventListener('click', subscribeTicks);
document.getElementById('unsubscribe-btn').addEventListener('click', unsubscribeTicks);

// Initialize dropdown
populateAssetDropdown();
