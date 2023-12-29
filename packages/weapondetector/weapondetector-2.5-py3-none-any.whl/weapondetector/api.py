
from waitress import serve
from flask import Flask, request, jsonify
import json
import threading
from queue import Queue
import logging
from weapondetector.utils import upload_media

app = Flask(__name__)

# Create a queue to store requests
request_queue = Queue()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def processing_thread():
    while True:
        try:
            # Get a request from the queue
            data_str = request_queue.get()
            data = json.loads(data_str)
            print(type(data), data)

            # Process the request
            video_file_path = data.get("video_file_path")
            img_file_path = data.get("img_file_path")
            camera_name = data.get("camera_name")
            acc = data.get("acc")

            if not all([video_file_path, img_file_path, camera_name, acc]):
                logger.warning(f'Invalid request: {data}')
            else:
                # Perform the upload operation
                logger.info(f'Uploading video for camera {camera_name}')
                upload_media(video_file_path, img_file_path, camera_name, acc)

            # Mark the task as done in the queue
            request_queue.task_done()
            print("Done")

        except Exception as e:
            logger.error(f"Error in processing thread: {str(e)}")


@app.route('/uploadvideo', methods=['POST'])
def uploadvideo():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Add the request to the queue
            request_queue.put(str(data))

            return jsonify({'message': 'Video upload request added to the queue'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == "__main__":

    process_thread = threading.Thread(target=processing_thread)
    process_thread.daemon = True
    process_thread.start()

    try:

        serve(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:

        print("Stopping the processing thread...")
        process_thread.join()
        print("Application stopped.")
