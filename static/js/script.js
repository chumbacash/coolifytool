const forms = document.querySelector(".forms"),
      pwShowHide = document.querySelectorAll(".eye-icon"),
      links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
        
        pwFields.forEach(password => {
            if(password.type === "password"){
                password.type = "text";
                eyeIcon.classList.replace("bx-hide", "bx-show");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("bx-show", "bx-hide");
        });
    });
});

links.forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault(); //preventing form submit
        forms.classList.toggle("show-signup");
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-analysis');
    const stopButton = document.getElementById('stop-analysis');
    const tickDisplay = document.getElementById('tick-display');

    startButton.addEventListener('click', () => {
        const selectedAsset = document.getElementById('assets').value;
        fetch('/start_analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ asset: selectedAsset })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    });

    stopButton.addEventListener('click', () => {
        fetch('/stop_analysis', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    });

    // WebSocket setup
    const socket = io(); // Ensure Socket.IO client library is included

    socket.on('tick_update', (data) => {
        tickDisplay.textContent = `Current Tick: ${data.tick}`;
    });
});
