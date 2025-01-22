# AgriAid  (software) 🌱

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.18.0-orange)
![Flask](https://img.shields.io/badge/Flask-3.1.0-lightgrey)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10.0-green)

This repository contains the software component of the AgriAid system, which combines machine learning and IoT technologies for agricultural monitoring and disease detection.

## Overview

The software component integrates:

- Disease detection using deep learning
- Sensor data monitoring and analysis
- Web-based user interface
- Real-time video processing

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Dependencies](#dependencies)

---

## Features

- **Plant Disease Detection** 
   - Tomato leaf disease classification using TensorFlow 
   - Real-time image processing with OpenCV 
   - Support for 10 different disease categories 
   
- **Sensor Integration** 
   - Temperature, humidity, and moisture monitoring   
   - CO2 level tracking 
   - Real-time data visualization 
   
- **Web Application** 
   - Flask-based dashboard 
   - Real-time monitoring interface 
   - Disease detection results visualization

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/intropercib/AgriAid.git
   cd AgriAid
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Flask Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

3. Upload an image/video of a tomato leaf and view the prediction results.

---

## Project Structure

```
tomato-leaf-classification/
├── models/
│   ├── classifier.py               # TomatoLeafClassifier class
│   ├── image_classification.ipynb  # Image classification using TensorFlow
│   └── model.h5                    # Trained TensorFlow model
├── static/                         # Static files (CSS, JS, images)
├── templates/                      # HTML templates for the Flask app
├── app.py                          # Flask application
├── requirements.txt                # List of dependencies
├── video_processor.py              # Video processing
├── sensor_data.py                  # Sensor data processing
└── README.md                       # Software documentation
```

---

## Dependencies

The project relies on the following Python packages:

- **TensorFlow**: For deep learning model inference.
- **Flask**: For building the web application.
- **OpenCV**: For image processing.
- **NumPy**: For numerical computations.

For a complete list of dependencies, see the [requirement.txt](/software/requirement.txt) file.

---
<div style="text-align:center; font-size:16px; font-weight:bold;">
🌱 AgriAid - Empowering Agriculture with Technology 🌱
<div>

---

