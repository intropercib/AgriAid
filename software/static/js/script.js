document.addEventListener('DOMContentLoaded', function () {
    const sensorDataElement = document.getElementById('sensor-data');
    const videoFeed = document.getElementById('video-feed');
    const videoPlaceholder = document.getElementById('video-placeholder');

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
                    sensorDataElement.textContent = `Error: ${data.error}`;
                } else {
                    sensorDataElement.textContent = `
                        Key: ${data.key}
                        Value: ${data.value}
                    `;
                }
            })
            .catch(error => {
                console.error("Error fetching sensor data:", error);
                sensorDataElement.textContent = 'Error fetching sensor data: ' + error.message;
            });
    }

    setInterval(fetchSensorData, 5000);
    fetchSensorData();
});