from flask import Flask, request
import requests
import subprocess

app = Flask(__name__)


@app.route('/')
def hello_world():
    paragraph = "<p>Hello, World!</p>"
    return paragraph


@app.route('/print_online_picture')
def print_online_picture():
    try:
        # Get the URL from the query parameter
        message = request.args.get(
            'message')
        if not message:
            return 'No message provided', 400

        # Fetch the image
        response = requests.get(
            f"https://vercel-og-pritter.vercel.app/api/static?message={message}")
        if response.status_code != 200:
            return 'Failed to fetch image', 500

        # Save the image temporarily
        temp_image_path = 'temp_image.png'
        with open(temp_image_path, 'wb') as file:
            file.write(response.content)

        # Define the command and arguments for subprocess
        command = 'tools/phomemo-filter.py'
        args = [temp_image_path]

        # Execute the command and redirect output to /dev/rfcomm0
        with open('/dev/rfcomm0', 'wb') as device:
            result = subprocess.run([command] + args, stdout=device)

        # Check if the command was successful
        if result.returncode == 0:
            return 'Printed successfully'
        else:
            return 'Error in printing', 500

    except Exception as e:
        # Handle any exceptions
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
