import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import AzureError, ResourceExistsError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simplestream.db'
db = SQLAlchemy(app)

# Azure Blob Storage configuration
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=librewaves;AccountKey=BskP51KKJyrHTubyE3Dlmk1sz1BHfQkH5EpiGoxZDC3Ce57/va6dsxzDLHtv+WRCjTsVFvUHqpKF+AStdsLHtQ==;EndpointSuffix=core.windows.net'

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# User Model
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	playlists = db.relationship('Playlist', backref='user', lazy=True)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

# Playlist Model
class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	songs = db.relationship('Song', backref='playlist', lazy=True)

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id

# Song Model
class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	artist = db.Column(db.String(100), nullable=False)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

	def __init__(self, title, artist, playlist_id):
		self.title = title
		self.artist = artist
		self.playlist_id = playlist_id

# Create the database if it doesn't exist
with app.app_context():
	db.create_all()
		
# Create a new playlist endpoint
@app.route('/playlist', methods=['POST'])
def create_playlist():
	data = request.get_json()
	name = data['name']
	user_id = data['user_id']
	playlist = Playlist(name=name, user_id=user_id)
	db.session.add(playlist)
	db.session.commit()
	return jsonify({'message': 'Playlist created successfully'})

# Delete a playlist endpoint
@app.route('/playlist/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
	playlist = Playlist.query.get(playlist_id)
	if playlist:
		db.session.delete(playlist)
		db.session.commit()
		return jsonify({'message': 'Playlist deleted successfully'})
	return jsonify({'message': 'Playlist not found'})

# Add a new song to a playlist endpoint
@app.route('/playlist/<int:playlist_id>/song', methods=['POST'])
def add_song_to_playlist(playlist_id):
	data = request.get_json()
	title = data['title']
	artist = data['artist']
	song = Song(title=title, artist=artist, playlist_id=playlist_id)
	db.session.add(song)
	db.session.commit()
	return jsonify({'message': 'Song added to playlist successfully'})

# Remove a song from a playlist endpoint
@app.route('/playlist/<int:playlist_id>/song/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
	song = Song.query.get(song_id)
	if song and song.playlist_id == playlist_id:
		db.session.delete(song)
		db.session.commit()
		return jsonify({'message': 'Song removed from playlist successfully'})
	return jsonify({'message': 'Song not found or does not belong to the playlist'})

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
	# data = request.get_json()
	# username = data['username']
	# email = data['email']
	# password = data['password']
	# user = User(username=username, email=email, password=password)
	# db.session.add(user)
	# db.session.commit()

	username = request.form['username']

	print(username)

	try:
		# Create a unique container name based on the username
		container_name = username.lower()  # You can modify this if needed

		# Create a ContainerClient instance and attempt to create the container
		container_client = blob_service_client.get_container_client(container_name)
		container_client.create_container()

		return jsonify({'message': 'User registered successfully'})
	except ResourceExistsError:
		return jsonify({'error': 'Username already exists. Please choose a different username.'}), 409
	except Exception as e:
		return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


# User login endpoint
@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	username = data['username']
	password = data['password']
	user = User.query.filter_by(username=username).first()
	if user and user.password == password:
		return jsonify({'message': 'Login successful'})
	return jsonify({'message': 'Invalid credentials'})

# User logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
	# Perform any necessary logout operations
	return jsonify({'message': 'Logged out successfully'})

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
	# Retrieve the files and username from the request
	files = request.files.getlist('file')
	username = request.form['username']

	try:
		container_name = username  # Set the container name based on the username

		container_client = blob_service_client.get_container_client(container_name)

		# Upload each file to Azure Blob Storage
		for file in files:
			# Generate a unique filename
			blob_client = container_client.get_blob_client(file.filename)

			# Upload the file to Azure Blob Storage
			blob_client.upload_blob(file.stream.read())

		return jsonify({'message': 'Files uploaded successfully'})
	except AzureError as e:
		return jsonify({'error': 'An error occurred while uploading the files to Azure Blob Storage', 'details': str(e)}), 500
	except Exception as e:
		return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Get files endpoint
@app.route('/files', methods=['GET'])
def get_files():
	try:
		username = request.args.get('username')
		if not username:
			return jsonify({'error': 'Username not provided'}), 400

		container_name = username.lower()

		container_client = blob_service_client.get_container_client(container_name)

		blobs = container_client.list_blobs()
		files = [blob.name for blob in blobs]
		return jsonify(files), 200
	except Exception as e:
		print(e)
		return str(e), 500

# Rename file endpoint
@app.route('/rename', methods=['PUT'])
def rename_file():
	old_filename = request.args.get('old_filename')
	new_filename = request.args.get('new_filename')
	username = request.args.get("username")

	container_client = blob_service_client.get_container_client(username)

	try:
		# Get the blob client for the old filename
		old_blob_client = container_client.get_blob_client(old_filename)

		# Create a new blob client with the new filename
		new_blob_client = container_client.get_blob_client(new_filename)

		# Start the copy operation
		new_blob_client.start_copy_from_url(old_blob_client.url)

		# Delete the old blob
		old_blob_client.delete_blob()

		return jsonify({'message': 'File renamed successfully'})
	except AzureError as e:
		return jsonify({'error': 'An error occurred while renaming the file in Azure Blob Storage', 'details': str(e)}), 500
	except Exception as e:
		return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


# Delete file endpoint
@app.route('/delete', methods=['DELETE'])
def delete_file():
	filename = request.args.get('filename')
	username = request.args.get('username')

	username = request.args.get('username')
	if not username:
		return jsonify({'error': 'Username not provided'}), 400

	try:
		container_client = blob_service_client.get_container_client(username)
		# Delete the file from Azure Blob Storage
		blob_client = container_client.get_blob_client(filename)
		blob_client.delete_blob()

		return jsonify({'message': 'File deleted successfully'})
	except AzureError as e:
		return jsonify({'error': 'An error occurred while deleting the file from Azure Blob Storage', 'details': str(e)}), 500
	except Exception as e:
		return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
	app.run()
