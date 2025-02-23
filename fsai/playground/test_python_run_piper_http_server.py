import pytest
import requests
from flask import Flask
from threading import Thread

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    # Set up the Flask app in a separate thread
    app = Flask(__name__)
    server_thread = Thread(target=run_server)
    server_thread.start()
    yield
    server_thread.join()

def run_server():
    from src.python_run.piper.http_server import main
    main()

def test_long_sentence_synthesize(setup_server):
    # Define a long sentence
    long_sentence = (
        "Hello world, this is a test of the http server. It should be able to handle a long sentence without any issues."
    )

    # Send a POST request to the server with the long sentence
    response = requests.post("http://localhost:5000/", data=long_sentence)

    # Check if the response is successful and contains audio data
    assert response.status_code == 200
    assert response.content  # Ensure that some audio data is returned

    # Use aplay to play the audio data
    import subprocess
    subprocess.run(["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1", "-t", "raw", "-"], input=response.content)


    def test_stream_synthesize(setup_server):
            
        long_sentence = (
            "This is a streaming test of the HTTP server. "
            "The server should stream audio data as it processes the text."
        )

        # Send a POST request to the server with the long sentence
        response = requests.post("http://localhost:5000/stream", data=long_sentence, stream=True)

        # Check if the response is successful
        assert response.status_code == 200

        import subprocess

        # Initialize a buffer and define a threshold (in bytes)
        buffer = b""
        buffer_threshold = 4096*16  # Adjust this value as needed

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # Filter out keep-alive chunks
                buffer += chunk
                if len(buffer) >= buffer_threshold:
                    subprocess.run(
                        ["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1", "-t", "raw", "-"],
                        input=buffer,
                    )
                    buffer = b""

        # Play any remaining buffered data
        if buffer:
            subprocess.run(
                ["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1", "-t", "raw", "-"],
                input=buffer,
            )
