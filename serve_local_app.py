import os
import sys
import subprocess
import threading
import time
import queue

def open_port(port):
    output_queue = queue.Queue()

    def _run():
        ENVBIN = sys.exec_prefix
        ENVBIN = os.path.join(ENVBIN, "bin")

        # TODO: assert that a nodeenv exists and has localtunnel installed
        # This can be done with 'pip install nodeenv; nodeenv -p; npm install -g localtunnel'

        commands = f'export PATH="{ENVBIN}:$PATH"; lt --port {port}'
        process = subprocess.Popen(
            commands,
            shell=True,
            text=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # read the output to get the URL
        for line in process.stdout:
            if "https://" in line:  # Check for the URL
                output_queue.put(line.strip()[13:])  # Put the URL into the queue
                break

        process.stdout.close()
        process.wait()

    lt_thread = threading.Thread(target=_run)
    lt_thread.daemon = True
    lt_thread.start()

    # wait for the URL to be available in the queue
    try:
        url = output_queue.get(timeout=10)  # Wait up to 10 seconds for the URL
    except queue.Empty:
        raise TimeoutError("Localtunnel did not provide a URL in time.")
    
    return lt_thread, url


def run_flask_app(app, port):
    def _run():
        app.run(host='0.0.0.0', port=port)

    flask_thread = threading.Thread(target=_run)
    flask_thread.daemon = True
    flask_thread.start()
    return flask_thread

# get the password for the localtunnel URL
def fetch_password_with_retry(retries=10, delay=2):
    url = "https://loca.lt/mytunnelpassword"
    for attempt in range(1, retries + 1):
        try:
            # run the curl command
            result = subprocess.run(
                ["curl", "-s", "-w", "\n%{http_code}", url],
                text=True,
                capture_output=True,
                check=True
            )
            output = result.stdout.rsplit("\n", 1)
            response_data = output[0]
            http_code = output[1]

            if http_code == "502":
                print(f"Password Fetch Attempt {attempt}: Received Bad Gateway error (502). Retrying...")
                time.sleep(delay)
                continue

            elif http_code.startswith("2"):
                return response_data
            
            else:
                raise RuntimeError(f"Unexpected HTTP response code: {http_code}")

        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt}: Curl command failed. Retrying... Error: {e}")
            time.sleep(delay)

    # if all retries fail
    raise RuntimeError("Failed to fetch data after multiple attempts.")
