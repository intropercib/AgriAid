document.addEventListener('DOMContentLoaded', function () {
    const temperatureDataElement = document.getElementById('temperature');
    const humidityDataElement = document.getElementById('humidity');
    const moistureDataElement = document.getElementById('moisture');
    const co2DataElement = document.getElementById('co2');
    const videoFeed = document.getElementById('video-feed');
    const videoPlaceholder = document.getElementById('video-placeholder');
    const connErrorElement = document.getElementById('conn-error');

    // Debugging: Log elements to ensure they are found
    console.log("Temperature element:", temperatureDataElement);
    console.log("Humidity element:", humidityDataElement);
    console.log("Moisture element:", moistureDataElement);
    console.log("CO2 element:", co2DataElement);
    console.log("Connection error element:", connErrorElement);

    // Hide placeholder initially
    if (videoPlaceholder) {
        videoPlaceholder.style.display = 'none';
    }

    // Handle video load error
    if (videoFeed) {
        videoFeed.onerror = function () {
            console.log('Video feed error detected');
            videoFeed.classList.add('hidden');
            if (videoPlaceholder) {
                videoPlaceholder.style.display = 'flex';
            }
        };
    }

    // Handle video load success
    if (videoFeed) {
        videoFeed.onload = function () {
            console.log('Video feed loaded successfully');
            videoFeed.classList.remove('hidden');
            if (videoPlaceholder) {
                videoPlaceholder.style.display = 'none';
            }
        };
    }

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
                    temperatureDataElement.textContent = 'N/A';
                    humidityDataElement.textContent = 'N/A';
                    moistureDataElement.textContent = 'N/A';
                    co2DataElement.textContent = 'N/A';
                } else {

                    connErrorElement.style.display = 'none';
                    temperatureDataElement.textContent = data.Temperature;
                    humidityDataElement.textContent = data.Humidity;
                    moistureDataElement.textContent = data.Moisture;
                    co2DataElement.textContent = data.CO2;

                }
            })
            .catch(error => {
                console.error("Error fetching sensor data:", error);
                if (temperatureDataElement) {
                    temperatureDataElement.textContent = 'Error fetching sensor data: ' + error.message;
                }
            });
    }

    setInterval(fetchSensorData, 5000);
    fetchSensorData();
});