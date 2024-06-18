import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

import json

import Physics

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/pool.html':
            try:
                # Open the pool-table.html file
                with open('pool.html', 'rb') as file:
                    content = file.read()
                # Send HTTP response for HTML content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                # If file not found, send 404 response
                self.send_error(404, 'File not found')
        else:
            # For other paths, send 404 response
            self.send_error(404, 'File not found')

    def do_POST(self):
        if self.path == '/shot':
            # Get the content length from the request headers
            content_length = int(self.headers['Content-Length'])
            # Read the POST data
            post_data = self.rfile.read(content_length)
            # Parse the JSON data
            data = json.loads(post_data.decode('utf-8'))
            # Extract cue ball position and release position
            cue_ball_position = data['cueBallPosition']
            release_position = data['releasePosition']

            # Calculate the difference between x and y components
            dx = release_position['x'] - cue_ball_position['x']
            dy = release_position['y'] - cue_ball_position['y']

            # Compute initial velocity components (assuming constant acceleration)
            #initial_velocity_x = dx * acceleration_constant
            #initial_velocity_y = dy * acceleration_constant

            #Game time
            newGame = Physics.Game(gameName="Test Game", player1Name="Pinky", player2Name="Browny")

            #Shot time
            newGame.shoot("Test Game", "Pinky", table, dx, dy)

            response_data = {
                'message': "Got shot positions",
                'positions sent': data
            }


            # Insert code to add the resulting shot to the database
            # Respond with a success message or appropriate status code
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Shot successfully added to the database".encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')



# Main block for running the server
if __name__ == '__main__':
    try:
        # Create an instance of the HTTPServer
        httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
        print('Server listening on port:', int(sys.argv[1]))
        # Start the server
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to stop the server
        print('Server stopped')
        httpd.server_close()