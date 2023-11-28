from flask import Flask, render_template, redirect, request, url_for
import requests
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form.get('username')
        userid = request.form.get('userid')
        message = request.form.get('message')

        try:
            # Get the URL from the query parameter
            message = request.form.get('message')
            if not message:
                return 'No message provided', 400

            username = request.form.get('username')
            userid = request.form.get('userid')

            url = f"https://vercel-og-pritter.vercel.app/api/pritter?message={message}"
            if username:
                url += f"&username={username}"
            if userid:
                url += f"&userid={userid}"

            # Fetch the image
            response = requests.get(url)
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
                # データの処理（保存等）が完了したらホームにリダイレクト
                return redirect(url_for('form'))
            else:
                return 'Error in printing', 500

        except Exception as e:
            # Handle any exceptions
            return str(e), 500

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
