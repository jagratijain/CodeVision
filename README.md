# Smart Car Spot Detector

## Introduction
Managing spots efficiently in crowded or large parking lots is a challenging task. Traditional methods of monitoring parking lot occupancy are often manual, time-consuming, and prone to errors. With increasing urbanization, there is a growing demand for automated, real-time parking management systems.
The objective of this project is to develop an Smart Car Spot Detector that uses machine learning and computer vision to analyse video feeds and determine parking spot occupancy in real-time.
The system should enable:
1.	Seamless user interaction via a React-based frontend for uploading parking lot video and mask images.
2.	Real-time detection and tracking of parking spots occupancy status using Flask as a backend.
3.	Effective communication between the frontend and backend, ensuring accurate and timely updates on parking space availability

## Features
1. Seamless user interaction via a React-based frontend for uploading parking lot video and mask images.
2. Real-time detection and tracking of parking spaces' occupancy status using Flask as a backend.
3. Effective communication between the frontend and backend, ensuring accurate and timely updates on parking space availability.


## Setup and Installation

### Backend Setup
1. Navigate to the backend directory: `cd backend/main`
2. Install the required dependencies: `pip install -r requirements.txt`
2. Run the Flask application: `python app.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install the required dependencies: `npm install`
3. Start the development server: `npm run dev`

This will launch the frontend application, which can be accessed at `http://localhost:3000`.

## How it Works

The Smart Car Spot Detector consists of two main components: the backend and the frontend.

### Frontend
The frontend, or React application, is a user interface where users can upload mask and video files. The mask is a picture that highlights the parking spaces, and the film is a representation of a parking lot.  Users can initiate the processing of these files by submitting them via a form.

### Backend
Video and mask files uploaded from the frontend are accepted by the Flask server. It analyzes the data to find related elements (parking places) in the mask and tracks whether a parking spot is occupied or vacant in the video frames.  To identify any changes in parking place occupancy, the system examines the video frame by frame and compares subsequent frames. 
After that, it replies to the frontend with the data it has processed, including each parking spot's state. 


## Conclusion
In order to track parking spots occupancy in real-time, Smart Car Spot Detector is made to process video feeds and mask images. The technology uses machine learning and computer vision techniques to determine whether parking spaces are occupied and available in a particular video. By identifying related components that serve as regions of interest in the video, the mask picture is utilized to locate parking spots.
