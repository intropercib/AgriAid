document.addEventListener('DOMContentLoaded', function () {
    const temperatureDataElement = document.getElementById('temperature');
    const videoFeed = document.getElementById('video-feed');
    const videoPlaceholder = document.getElementById('video-placeholder');
    const connErrorElement = document.getElementById('conn-error');

    // Hide placeholder initially
    videoPlaceholder.style.display = 'none';

    // Handle video load error
    videoFeed.onerror = function () {
        console.log('Video feed error detected');
        videoFeed.classList.add('hidden');
        videoPlaceholder.style.display = 'flex';
    };

    // Handle video load success
    videoFeed.onload = function () {
        console.log('Video feed loaded successfully');
        videoFeed.classList.remove('hidden');
        videoPlaceholder.style.display = 'none';
    };

    // Fetch sensor data every 5 seconds
    function fetchSensorData() {
        fetch('/sensor_data')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Received data from backend:", data);
                if (data.error) {
                    connErrorElement.textContent = data.error;
                    temperatureDataElement.textContent = `N/A`;
                } else {
                    connErrorElement.style.display = 'none';
                    temperatureDataElement.textContent = data.value;
                }
            })
            .catch(error => {
                console.error("Error fetching sensor data:", error);
                temperatureDataElement.textContent = 'Error fetching sensor data: ' + error.message;
            });
    }

    setInterval(fetchSensorData, 5000);
    fetchSensorData();
});