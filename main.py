import psutil
import subprocess
import time
import logging
import signal
import os
import glob

# Configure logging
logging.basicConfig(filename='../script_runner.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        process = subprocess.Popen(['python3', script_name])
        logging.info(f"Started {script_name} (PID: {process.pid})")
        return process
    except Exception as e:
        logging.error(f"Error running script {script_name}: {e}")
        return None

def check_json_files_exist(directory, timeout=120, interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        json_files = glob.glob(os.path.join(directory, '*.json'))
        if json_files:
            logging.info(f"JSON files found in directory {directory}")
            return True
        time.sleep(interval)
    logging.error(f"No JSON files found in directory {directory} within {timeout} seconds")
    return False

def kill_python_processes():
    for proc in psutil.process_iter():
        if proc.name() == "python" or "python3" in proc.name():
            proc.kill()

def signal_handler(sig, frame):
    logging.info("Received termination signal. Stopping script execution...")
    kill_python_processes()
    exit(0)

if __name__ == "__main__":
    # Register signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)

    # Start the data producer
    logging.info("Starting producer.py")
    producer_process = run_script('producer.py')

    # Start the consumer immediately after producer
    logging.info("Starting consumer_raw.py")
    consumer_raw_process = run_script('consumer_raw.py')

    # Check if both producer and consumer are running
    if check_json_files_exist('data/raw/'):
        logging.info("Both producer and consumer are running. Starting readers...")

        # Wait for a few seconds before starting the other scripts
        time.sleep(5)

        # Start the other readers
        logging.info("Starting reader_references.py")
        references_process = run_script('reader_references.py')

        logging.info("Starting reader_tfidf.py")
        tfidf_process = run_script('reader_tfidf.py')

        # Keep the main process running to prevent Docker container from exiting
        try:
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            signal_handler(signal.SIGINT, None)
    else:
        logging.error("Failed to start either producer.py or consumer_raw.py. Readers will not be started.")









