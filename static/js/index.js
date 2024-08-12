import DerivAPIBasic from 'https://cdn.skypack.dev/@deriv/deriv-api/dist/DerivAPIBasic';

const app_id = 63289; // Replace with your app_id or leave as 1089 for testing
const connection = new WebSocket(`wss://ws.derivws.com/websockets/v3?app_id=${app_id}`);
const api = new DerivAPIBasic({ connection });

const assets = {
    "VOLATILITY 10 (1s) INDEX": ["1HZ10V", 2],
    "VOLATILITY 10 INDEX": ["R_10", 3],
    "VOLATILITY 25 (1s) INDEX": ["1HZ25V", 2],
    "VOLATILITY 25 INDEX": ["R_25", 3],
    "VOLATILITY 50 (1s) INDEX": ["1HZ50V", 2],
    "VOLATILITY 50 INDEX": ["R_50", 4],
    "VOLATILITY 75 (1s) INDEX": ["1HZ75V", 2],
    "VOLATILITY 75 INDEX": ["R_75", 4],
    "VOLATILITY 100 (1s) INDEX": ["1HZ100V", 2],
    "VOLATILITY 100 INDEX": ["R_100", 2]
};

let selectedAssetSymbol = "R_50";
let tickList = [];
let previousTick = null;
let overUnderThreshold = 5; // Default threshold value
const maxTicksToTrack = 60; // Number of ticks to track
let ema = null; // Store the current EMA value
const period = 20; // Number of ticks to calculate EMA

const assetSelect = document.getElementById('asset-select');
const thresholdButtons = document.querySelectorAll('.threshold-button');
const predictionBox = document.getElementById('prediction-box');
const predictionButton = document.getElementById('prediction-button');
const overButton = document.getElementById('over-button');
const underButton = document.getElementById('under-button');
const evenButton = document.getElementById('even-button');
const oddButton = document.getElementById('odd-button');
const ticksDataDiv = document.getElementById('tick-data');
const scanDigitButton = document.getElementById('scan-digit-button');
const digitBox = document.getElementById('digit-box');
let subscriptionActive = false;
let intervalId = null;

// Populate asset dropdown
const populateAssetDropdown = () => {
    for (const [name, [symbol]] of Object.entries(assets)) {
        const option = document.createElement('option');
        option.value = symbol;
        option.textContent = name;
        assetSelect.appendChild(option);
    }
};

// Subscribe to ticks
const subscribeTicks = async () => {
    if (subscriptionActive) {
        console.log('Already subscribed to ticks.');
        return;
    }

    selectedAssetSymbol = assetSelect.value;
    const tickRequest = { ticks: selectedAssetSymbol };

    try {
        await api.subscribe(tickRequest);
        connection.addEventListener('message', tickResponse);
        subscriptionActive = true;
        console.log('Subscribed to ticks.');
    } catch (error) {
        console.error('Error subscribing to ticks:', error);
    }
};

const unsubscribeTicks = async () => {
    if (!subscriptionActive) {
        console.log('No active subscription to unsubscribe from.');
        return;
    }

    try {
        await api.send({ forget_all: 'ticks' });
        connection.removeEventListener('message', tickResponse);

        subscriptionActive = false;
        tickList = [];
        previousTick = null;
        ema = null;
        ticksDataDiv.innerHTML = 'No data yet';
        resetProgressBars();

        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
        digitBox.textContent = '0';
        console.log('Successfully unsubscribed from ticks and reset state.');

    } catch (error) {
        console.error('Error unsubscribing from ticks:', error);
    }
};


// Update the progress bars for Over and Under
const updateOverUnderProgressBars = (currentDigit) => {
    const underCount = tickList.filter(tick => parseInt(tick.slice(-1), 10) <= overUnderThreshold).length;
    const overCount = tickList.length - underCount;

    const underPercentage = (underCount / tickList.length) * 100;
    const overPercentage = 100 - underPercentage;

    document.querySelector('.under-progress').style.width = `${underPercentage}%`;
    document.querySelector('.under-percent').textContent = `${Math.round(underPercentage)}%`;

    document.querySelector('.over-progress').style.width = `${overPercentage}%`;
    document.querySelector('.over-percent').textContent = `${Math.round(overPercentage)}%`;
};

// Update the progress bars for Even and Odd
const updateEvenOddProgressBars = () => {
    const evenCount = tickList.filter(tick => parseInt(tick.slice(-1), 10) % 2 === 0).length;
    const oddCount = tickList.length - evenCount;

    const evenPercentage = (evenCount / tickList.length) * 100;
    const oddPercentage = 100 - evenPercentage;

    document.querySelector('.even-progress').style.width = `${evenPercentage}%`;
    document.querySelector('.even-percent').textContent = `${Math.round(evenPercentage)}%`;

    document.querySelector('.odd-progress').style.width = `${oddPercentage}%`;
    document.querySelector('.odd-percent').textContent = `${Math.round(oddPercentage)}%`;
};

// Perform a simple prediction based on historical data
const simplePrediction = () => {
    if (tickList.length < maxTicksToTrack) return 'NAN';

    const recentTicks = tickList.slice(-maxTicksToTrack);
    const avg = recentTicks.reduce((sum, tick) => sum + parseInt(tick.slice(-1), 10), 0) / recentTicks.length;

    return avg > overUnderThreshold ? 'Rise' : 'Fall';
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

// Handle incoming tick data
const tickResponse = (event) => {
    const data = JSON.parse(event.data);
    if (data.tick) {
        analyzeTick(data.tick);
    }
};

// Analyze and display tick data
const analyzeTick = (currentTick) => {
    const currentQuote = String(currentTick.quote); // Convert currentQuote to a string
    tickList.push(currentQuote);
    if (tickList.length > maxTicksToTrack) tickList.shift();

    const currentDigit = parseInt(currentQuote.slice(-1), 10);
    const evenOdd = currentDigit % 2 === 0 ? "even" : "odd";

    if (ema === null && tickList.length >= period) {
        ema = calculateInitialEMA(tickList.slice(-period).map(q => parseFloat(q)));
    } else if (ema !== null) {
        ema = calculateEMA(parseFloat(currentQuote), ema);
    }

    let prediction = tickList.length >= 10 ? simplePrediction() : 'NAN';
    if (tickList.length >= period) {
        prediction = parseFloat(currentQuote) > ema ? 'Rise' : 'Fall';
    }

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

    updateEvenOddProgressBars();
    updateOverUnderProgressBars();

    predictionBox.textContent = `Prediction: ${prediction}`;
    predictionBox.style.backgroundColor = prediction === 'Rise' ? 'green' : 'red';
    predictionBox.style.color = 'white';

    previousTick = currentTick;
};

// Reset progress bars
const resetProgressBars = () => {
    document.querySelector('.even-progress').style.width = `0%`;
    document.querySelector('.even-percent').textContent = `0%`;

    document.querySelector('.odd-progress').style.width = `0%`;
    document.querySelector('.odd-percent').textContent = `0%`;

    document.querySelector('.over-progress').style.width = `0%`;
    document.querySelector('.over-percent').textContent = `0%`;

    document.querySelector('.under-progress').style.width = `0%`;
    document.querySelector('.under-percent').textContent = `0%`;
};

// Start updating digit every 20 seconds
const startUpdatingDigit = () => {
    if (intervalId) {
        clearInterval(intervalId);
    }

    digitBox.textContent = getRandomNumber();

    intervalId = setInterval(() => {
        digitBox.textContent = getRandomNumber();
    }, 20000);
};

// Generate a random number between 0 and 9
const getRandomNumber = () => Math.floor(Math.random() * 10);

// Event listeners
document.getElementById('ticks').addEventListener('click', subscribeTicks);
document.getElementById('ticks-unsubscribe').addEventListener('click', unsubscribeTicks);
predictionButton.addEventListener('click', () => {
    const prediction = simplePrediction();
    predictionBox.textContent = `Prediction: ${prediction}`;
    predictionBox.style.backgroundColor = prediction === 'Rise' ? 'green' : 'red';
    predictionBox.style.color = 'white';
});
scanDigitButton.addEventListener('click', () => {
    startUpdatingDigit();
});

thresholdButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        overUnderThreshold = parseInt(event.target.getAttribute('data-value'), 10);
        console.log(`Threshold set to: ${overUnderThreshold}`);
    });
});

// Initialize dropdown
populateAssetDropdown();