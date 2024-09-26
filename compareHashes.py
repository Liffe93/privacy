import hashlib

# Function to calculate the SHA-256 hash of a file
def calculate_file_hash(file_path, hash_function='sha256'):
    hash_func = hashlib.new(hash_function)
    
    # Open file in binary mode and read in chunks
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):  # Read the file in chunks of 8192 bytes
            hash_func.update(chunk)
    
    # Return the hexadecimal digest of the hash
    return hash_func.hexdigest()

# Example usage:
file_path_downloaded = 'downloaded_image.jpg'  # Replace with the path to your downloaded image
file_path_emailed = 'emailed_image.jpg'        # Replace with the path to the image you received via email

# Calculate the SHA-256 hash of both files
hash_downloaded = calculate_file_hash(file_path_downloaded, 'sha256')
hash_emailed = calculate_file_hash(file_path_emailed, 'sha256')

# Compare the two hashes
if hash_downloaded == hash_emailed:
    print("The files are identical.")
else:
    print("The files are different.")
