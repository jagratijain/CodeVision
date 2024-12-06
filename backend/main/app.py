import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import threading
import queue

app = Flask(__name__)
CORS(app)

# Global queue to pass data between Flask route and OpenCV display thread
frame_queue = queue.Queue()
stop_event = threading.Event()

def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))

def display_video():
    while not stop_event.is_set():
        try:
            # Try to get a frame from the queue with a timeout
            frame_data = frame_queue.get(timeout=1)
            
            # Unpack frame data
            frame = frame_data['frame']
            spots = frame_data['spots']
            spots_status = frame_data['spots_status']

            # Draw rectangles and status for each parking spot
            for spot_indx, spot in enumerate(spots):
                spot_status = spots_status[spot_indx]
                x1, y1, w, h = spots[spot_indx]

                if spot_status:
                    frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
                else:
                    frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

            # Add available spots text
            cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
            cv2.putText(frame, 'Available spots: {} / {}'.format(
                str(sum(spots_status)), 
                str(len(spots_status))
            ), (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display the frame
            cv2.namedWindow('Parking Spot Detection', cv2.WINDOW_NORMAL)
            cv2.imshow('Parking Spot Detection', frame)
            
            # Wait for 25ms and check for 'q' key to quit
            key = cv2.waitKey(25)
            if key & 0xFF == ord('q'):
                stop_event.set()
        
        except queue.Empty:
            # If queue is empty, continue waiting
            continue
        except Exception as e:
            print(f"Error in display thread: {e}")
            stop_event.set()

@app.route('/process_media', methods=['POST'])
def process_video():
    # Reset global state
    global frame_queue
    frame_queue = queue.Queue()
    stop_event.clear()

    # Retrieve the uploaded video and mask files
    video_file = request.files.get('video')
    mask_file = request.files.get('mask')

    if not video_file or not mask_file:
        return jsonify({'error': 'Both video and mask files are required'}), 400

    # Save uploaded video and mask to temporary files
    video_path = './temp_video.mp4'
    mask_path = './temp_mask.png'
    video_file.save(video_path)
    mask_file.save(mask_path)

    # Load the mask image
    mask = cv2.imread(mask_path, 0)
    if mask is None:
        return jsonify({'error': 'Invalid mask file'}), 500

    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({'error': 'Video cannot be opened'}), 500

    # Get connected components for the parking spots
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    spots = util.get_parking_spots_bboxes(connected_components)

    # Start the display thread
    display_thread = threading.Thread(target=display_video)
    display_thread.start()

    # Video processing
    spots_status = [None for _ in spots]
    diffs = [None for _ in spots]
    previous_frame = None
    frame_nmr = 0
    step = 30

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_nmr % step == 0 and previous_frame is not None:
            for spot_indx, spot in enumerate(spots):
                x1, y1, w, h = spot
                spot_crop = frame[y1:y1 + h, x1:x1 + w]
                
                if spot_crop.size > 0 and previous_frame[y1:y1 + h, x1:x1 + w].size > 0:
                    diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w])

        if frame_nmr % step == 0:
            # Determine spots status
            if previous_frame is None:
                arr_ = range(len(spots))
            else:
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
            
            for spot_indx in arr_:
                spot = spots[spot_indx]
                x1, y1, w, h = spot
                spot_crop = frame[y1:y1 + h, x1:x1 + w]

                if spot_crop.size > 0:
                    spot_status = util.empty_or_not(spot_crop)
                    spots_status[spot_indx] = spot_status

            # Put frame data in queue for display thread
            frame_queue.put({
                'frame': frame,
                'spots': spots,
                'spots_status': spots_status
            })

        if frame_nmr % step == 0:
            previous_frame = frame.copy()

        frame_nmr += 1

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    stop_event.set()
    display_thread.join()

    return jsonify({
        'message': 'Video processing completed',
        'total_spots': len(spots)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)