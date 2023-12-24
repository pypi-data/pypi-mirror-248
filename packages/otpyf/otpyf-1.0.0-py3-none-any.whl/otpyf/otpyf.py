import sys # used by class AudioMessageSynthesizer
import json # used by load_encryption_key(), load_decryption_key(), and save_to_jsonline_file()
import random # used by generate_random_prefix()
import secrets # used by straddle() and generate_csrng_numbers()
import glob # used by load_decryption_key()
import string # used by generate_random_prefix()
import csv # used by csv_checkerboard_to_dict() and print_checkerboard_table
import hashlib # used by generate_deterministic_numbers()
import os.path # used by clear(), load_decryption_key, and save_to_jsonline_file, and class AudioMessageSynthesizer
import wave # used by class AudioMessageSynthesizer

# ---- ENCODE/DECODE FUNCTIONS ---- #

def csv_checkerboard_to_dict(checkerboard_csv):
    # Read a CSV checkerboard file and convert it into a checkerboard dictionary.
    checkerboard = {}
    with open(checkerboard_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header_codes = next(reader, [])  # First row for column codes
        for row in reader:
            row_code = row[0]
            for i, char in enumerate(row[1:], 1):  # Skip the first column
                if char:
                    # This is not used at the moment. But you can change some of the placeholders values with pseudo codes directly while parsing the CSV.
                    if char == 'F/L':
                        char = 'F/L' # 00000
                    if char == 'SPC':
                        char = 'SPC' # 11111
                    if row_code:  # Double digit mapping
                        full_code = row_code + header_codes[i]
                    else:  # Single digit mapping
                        full_code = header_codes[i]
                    checkerboard[char] = full_code
    return checkerboard
    
def straddle(plaintext, checkerboard, number_sequence_code, length):
    #  
    # This function will convert plaintext to plaincode using a checkerboard specified by the user.
    # Additionally, it manages the transition from letters to numbers and vice versa by using a switch code (as per OTP standards).
    # Example. 09123456789 becomes 28012345678928
    # The exact checkerboard code used to switch from numbers to letters and vice versa is specified in the checkerboard.
    #
    plaincode = "" # Initialize an empty string to accumulate the plaincode
    in_number_sequence = False
    #
    # Check if 'SPC' exists in the checkerboard dict.
    # Used to bypass the code mapping process for SPC in cases where it is absent in the checkerboard.
    #
    space_code_exists = 'SPC' in checkerboard

    for char in plaintext.upper():
        # Check if the current character from the plaintext is space and if it is in a checkerboard dict. 
        if char == ' ' and space_code_exists: # `and space_code_exists` 
            if in_number_sequence: # Check if the Number Sequence is already enabled.
                plaincode += number_sequence_code # Add the checkerboard number/letter switch code to finalize the Number Sequence.
                in_number_sequence = False # Disable the Number Sequence check.
            plaincode += checkerboard['SPC'] # Dynamically get the code mapping for the space character from the checkerboard dict.
        elif char.isdigit(): # This will check if the current character is a number or a letter.
            if not in_number_sequence: # Check if the Number Sequence is not enabled.
                plaincode += number_sequence_code # Add the number/letter switch code to start off the Number Sequence.
                in_number_sequence = True # Enable the Number Sequence check.
            plaincode += char # Add any numbers to the plaincode.
        else:
            # Handle any other characters 
            if in_number_sequence: # Check if the Number Sequence check is already enabled
                plaincode += number_sequence_code # Add the number/letter switch code to finalize the Number Sequence.
                in_number_sequence = False # Disable the Number Sequence check.
            plaincode += checkerboard.get(char, '') # Add current checkerboard code to the plaincode

    # If the text ends with an open Number Sequence, close it with the number/letter switch code
    if in_number_sequence:
        plaincode += number_sequence_code
    # This will pad the plaintext with random numbers until it reaches the specfied length
    #
    # WARNING: DO NOT CHANGE THIS UNLESS YOU ABSULETLY KNOW WHAT YOU ARE DOING!
    #
    while len(plaincode) < length:
        plaincode += str(secrets.randbelow(10)) # Changed from 'random.randint(0, 9)' since it is more cryptographically secure

    return plaincode[:length]

def unstraddle(plaincode, checkerboard, number_sequence_code):
    # 
    # This function will convert plaincode to plaintext using a checkerboard specified by the user.
    # Additionally, it manages the transition from letters to numbers and vice versa by using a switch code (as per OTP standards).
    # Example. 28012345678928 becomes 09123456789
    # The exact checkerboard code used to switch from numbers to letters and vice versa is specified in the checkerboard.
    #
    decoded_text = "" # Initialize an empty string to accumulate the decoded text
    i = 0 # Initialize a counter (index) to iterate over the plaincode

    # 
    # Create a reverse mapping from code to letter  
    # The original checkerboard maps letters to codes for encoding, and this reverse mapping 
    # will allow the function to decode the code to letters.
    #
    reverse_checkerboard = {v: k for k, v in checkerboard.items()}
    # Check if 'SPC' exists in the checkerboard dict.
    # Used to bypass the code mapping process for SPC in cases where it is absent in the checkerboard.
    space_code_exists = 'SPC' in checkerboard # Check if 'SPC' exists in the checkerboard
    # Perform code mapping for the space character using the checkerboard dictionary only if the mapping exists, to prevent triggering an error.
    if space_code_exists:
        space_code = checkerboard['SPC'] # Dynamically get the code mapping for the space character from the checkerboard dict

    while i < len(plaincode): # Loop through each character in the plaincode
        #
        # Suppose plaincode is "ABCDEFG", i is 2, and space_code is "CDE" (so len(space_code) is 3).
        # The expression plaincode[i:i + len(space_code)] will extract the substring from plaincode starting at index 2 up to (but not including) index 5.
        # This means the extracted substring would be "CDE" (which is from index 2 to index 4).
        #
        
        #`if plaincode[i:i + len(space_code)] == space_code:`
        if space_code_exists and plaincode[i:i + len(space_code)] == space_code: # When there is a mapping for 'SPC' in the checkerboard dict, check if the current sequence is the checkerboard space code
            decoded_text += ' ' # Add a space character to the decoded text
            #
            # Move the current position in the plaincode string forward by the length of an space code sequence, effectively skipping over that sequence after it has been processed.
            # Let's say i is currently 5, and len(space_code) is 3. 
            # The expression i += len(space_code) will update i to 8. 
            # This means that in the next iteration of the loop, the function will start processing plaincode 
            # from its 8th character (since indexing in Python starts at 0).
            #
            i += len(space_code)
        elif plaincode[i:i + len(number_sequence_code)] == number_sequence_code: # Same as for the space_code but this time for the number_sequence_code
            i += len(number_sequence_code) # Skip the number-letter switch code
            plain_number = "" # Initialize a variable for the numbers
            while i < len(plaincode) and plaincode[i:i + len(number_sequence_code)] != number_sequence_code: # Loop until it reaches the number-letter switch code or until it either reaches the end of plaincode.
                plain_number += plaincode[i] # Add the current number to the variable
                i += 1 # Move to the next character
            i += len(number_sequence_code) # Skip the the number sequence after it has been processed.
            decoded_text += plain_number # Add all of the numbers from the number sequence to the decoded text (i.e plaintext)
        else: # Decoding regular characters
            #
            # Iterate over possible code lengths (from longest to shortest [assuming max length is 5]). You may change from 5 to 2. I'm just being cautious here.
            #
            # NOTE:
            # Suppose the encoded string is "12345". Both "123" and "45" 
            # are valid codes in the checkerboard, but "12345" is also a valid code. 
            # By checking the 5-character code first, the decoder correctly 
            # interprets it as "12345" instead of misinterpreting it as "123" followed by "45".
            #
            for code_length in range(5, 0, -1):
                if i + code_length <= len(plaincode) and plaincode[i:i + code_length] in reverse_checkerboard: # Determine whether a segment of plaincode is a sequence that can be decoded using the reverse_checkerboard, and verify that the segment does not go beyond the end of the plaincode.
                    code = plaincode[i:i + code_length] # Extract the sequence from the plaincode
                    decoded_text += reverse_checkerboard[code] # Decode the checkerboard code and add to the variable
                    i += code_length # Increment index by the length of the checkerboard code (i.e. sequence)
                    break # Break the loop as code has been found and processed
            else:
                i += 1  # Move to the next character in case of unrecognized sequence 

    return decoded_text

# ---- ENCRYPT/DECRYPT FUNCTIONS ---- #

def load_encryption_key(file_path):
# Load a random OTP encryption key from a JSON lines file and return it along with its index.
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError(f"File {file_path} doesn't have any remaining keys.")
            #key_index = random.randint(0, len(lines) - 1) # If you cannot use the secrets module by any chance use this...
            key_index = secrets.randbelow(len(lines))  # Generates a random index
            # Try block to catch some errors
            try:
                key = json.loads(lines[key_index].strip())
                if not isinstance(key, str) or not key.isdigit():
                   raise ValueError(f"Invalid format for the encryption key at line {key_index + 1} on file {file_path}.")
            except json.JSONDecodeError:
                raise ValueError("Failed to read JSON on line {}".format(key_index + 1))
            return key, key_index

    except FileNotFoundError:
        raise FileNotFoundError(f"The specified file was not found: {file_path}")
    except OSError as e:
        raise OSError(f"Error opening file: {e}")
    except IndexError:
        raise IndexError("Index out of range while accessing line in the file.")

def load_decryption_key(directory_path, otp_id):
    #
    # Search for a JSON file that contains an OTP decryption key that starts with the supplied key identifier.
    # Returns the file path, the key, and the key's index in the file if found.
    # Raises an error if no matching key, or file is found, or if any errors occur...
    #
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"The specified directory was not found: {directory_path}")

    for json_file in glob.glob(os.path.join(directory_path, '*pads_recv.json')):
        with open(json_file, 'r') as file:
            lines = file.readlines()
            # Check each line for the otp_id
            for index, line in enumerate(lines):
                try:
                    key = json.loads(line.strip())
                    if isinstance(key, str) and key.startswith(otp_id):
                        if not key.isdigit():
                            raise ValueError(f"Invalid format for the encryption key at line {index + 1} in file {json_file}.")
                        return json_file, key, index
                except json.JSONDecodeError:
                    raise ValueError(f"Failed to read JSON on line {index + 1} in file {json_file}")

    raise ValueError("No matching key or file found for the given One-Time Pad Identifier")

def delete_used_otp_key(file_path, key_index):
    # Function to delete an OTP key once it has been used.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for i, line in enumerate(lines):
            if i != key_index:
                file.write(line)

def mod10_encrypt(plaincode, key, length):
    # 
    # Check if key & plaincode are at the defined length
    #
    if not isinstance(key, str) or not key.isdigit() or len(key) != length:
        raise ValueError(f"The key must be a numeric string of exactly {length} digits.")

    if not isinstance(plaincode, str) or not plaincode.isdigit() or len(plaincode) != length:
        raise ValueError(f"The plaincode must be a numeric string of exactly {length} digits.")
    # Encrypt by performing modulo 10 operation on the provided plaincode and key.
    cipher = ""
    for pc, kc in zip(plaincode, key):
        cipher_digit = (int(pc) - int(kc)) % 10
        cipher += str(cipher_digit)
    return cipher

def encrypt_init(file_path, plaincode, length):
    # Main function to initialize the encryption.

    # Obtain a random One-Time Pad encryption key from a specified json lines file
    key, key_index = load_encryption_key(file_path)
    
    # 
    # Store the identified OTP key without its first group of 5 digits. 
    # That group will be prefixed in the CIPHERTEXT (without actually being encrypted), 
    # and later used during the decryption process as an identifier for the OTP decryption key.
    # WARNING: AS THE KEY IDENTIFIER IS ALREADY PART OF THE CIPHERTEXT, 
    # INCLUDING IT IN THE ENCRYPTION/DECRYPTION PROCESS WOULD ALLOW FOR DECRYPTION OF THE FIRST GROUP OF THE CIPHERTEXT 
    # WHICH WILL ENABLE BRUTE FORCE ATTACK ON THE REST OF THE PLAINCODE. 
    # THIS COULD EASILY LEAD TO DEDUCTION OF THE ENTIRE PLAINTEXT BASED ON THE CONTEXT! 
    #
    # DO NOT CHANGE THIS LOGIC UNLESS YOU ABSULETLY KNOW WHAT YOU ARE DOING!
    #
    otp_key = key[5:]
    # Store the first group (5 digits) of the OTP key as an identifier. Later used during the decryption process
    otp_key_id = key[:5]  # First 5 digits of the key
    # Encrypt the plaincode using the OTP key, but excluding the first group of 5 digits.
    cipher = mod10_encrypt(plaincode, otp_key, length)
    # Append the key identifier to the ciphertext
    encrypted_message = otp_key_id + cipher
    # 
    # Delete the used OTP decryption/encryption key.
    # WARNING: FOR THE ENCRYPTION TO BE UNBREAKABLE, THE KEY MUST NOT BE REUSED AND SHOULD REMAIN A SECRET!    
    #
    delete_used_otp_key(file_path, key_index)

    return encrypted_message, otp_key, otp_key_id

def mod10_decrypt(ciphertext, key):
    # Decrypt by performing modulo 10 on the provided ciphertext and OTP key.
    decrypted_message = ""
    #
    # The zip function (mod10_decrypt) in Python
    # pairs elements from multiple iterables (like lists or strings) together into tuples. 
    # It stops creating pairs when the shortest iterable is exhausted. 
    # This means you can decrypt a shorter ciphertext with a longer key, 
    # the extra characters in the key are simply ignored, 
    # but you should never do this due to security reasons. 
    #
    for cc, kc in zip(ciphertext, key):
        decrypted_digit = (int(cc) + int(kc)) % 10
        decrypted_message += str(decrypted_digit)
    return decrypted_message

def decrypt_init(directory_path, encrypted_message):
    # Main function to initialize decryption of the ciphertext.
    
    # Get the first group of 5 digits from the ciphertext since they are the OTP decryption key identifier
    otp_key_id = encrypted_message[:5]

    # 
    # Extract the first group of 5 digits from the ciphertext to identify the OTP decryption key.
    # The OTP key identifier won't be used during the actual decryption.
    # WARNING: AS THE KEY IDENTIFIER IS ALREADY PART OF THE CIPHERTEXT, 
    # INCLUDING IT IN THE ENCRYPTION/DECRYPTION PROCESS WOULD ALLOW FOR DECRYPTION OF THE FIRST GROUP OF THE CIPHERTEXT 
    # WHICH WILL ENABLE BRUTE FORCE ATTACK ON THE REST OF THE PLAINCODE. 
    # THIS COULD EASILY LEAD TO DEDUCTION OF THE ENTIRE PLAINTEXT BASED ON THE CONTEXT! 
    #
    # DO NOT CHANGE THIS LOGIC UNLESS YOU ABSULETLY KNOW WHAT YOU ARE DOING!
    #
    ciphertext = encrypted_message[5:]
    
    # Retrive the OTP key using the previously obtained OTP identifier
    json_file, key, key_index = load_decryption_key(directory_path, otp_key_id)
    
    # 
    # Store the OTP KEY without the first group of 5 digits (i.e. the OTP key identifier).
    # This action is taken to ensure that the identifier is not included in the decryption procedure.
    # WARNING: AS THE KEY IDENTIFIER IS ALREADY PART OF THE CIPHERTEXT, 
    # INCLUDING IT IN THE ENCRYPTION/DECRYPTION PROCESS WOULD ALLOW FOR DECRYPTION OF THE FIRST GROUP OF THE CIPHERTEXT 
    # WHICH WILL ENABLE BRUTE FORCE ATTACK ON THE REST OF THE PLAINCODE. 
    # THIS COULD EASILY LEAD TO DEDUCTION OF THE ENTIRE PLAINTEXT BASED ON THE CONTEXT! 
    #
    # DO NOT CHANGE THIS LOGIC UNLESS YOU ABSULETLY KNOW WHAT YOU ARE DOING!
    #
    otp_key = key[5:]
    decrypted_message = mod10_decrypt(ciphertext, otp_key)

    # 
    # Delete the used decryption/encryption OTP key.
    # WARNING: FOR THE ENCRYPTION TO BE UNBREAKABLE, THE KEY MUST NOT BE REUSED AND SHOULD REMAIN A SECRET!   
    #
    delete_used_otp_key(json_file, key_index)

    
    # Return the PLAINCODE, the used OTP decryption key and its identifier
    return decrypted_message, otp_key, otp_key_id

# ---- MISC FUNCTIONS ---- #
def clear():
    #
    # Clears the terminal screen and scroll back to present
    # the user with a nice clean, new screen. Useful for managing
    # menu screens in terminal applications.
    #
    os.system('cls||echo -e \\\\033c')
    
def split_into_groups_of_five(number):
    #
    # Splits the given number into groups of five digits for readability
    #
    # Args:
    # number (int or str): The number to be split into groups.
    #
    # Returns:
    # str: The number split into groups of five digits, separated by spaces.
    #
    
    # Convert the number to a string (if it isn't already)
    num_str = str(number)
    
    # Split the string into groups of 5, starting from the end 
    grouped = [num_str[max(i-5, 0):i] for i in range(len(num_str), 0, -5)]

    # Reverse the groups to maintain the original order and join with spaces
    return ' '.join(reversed(grouped))

def print_checkerboard_table(csv_filepath):
    #
    # This function will print the checkerboard obtained from the CSV into a nice table.
    #
    with open(csv_filepath, 'r') as file:
        # Read the CSV using csv.reader
        reader = csv.reader(file)
        lines = list(reader)

        # Determine the maximum width of each column
        widths = [max(len(entry) for entry in column) for column in zip(*lines)]

        # Print the header with column names underlined
        header = lines[0]
        print(' | '.join(entry.ljust(widths[i]) for i, entry in enumerate(header)))
        print('-' * (sum(widths) + 3 * (len(widths) - 1)))

        # Print the rows
        for line in lines[1:]:
            print(' | '.join(entry.ljust(widths[i]) for i, entry in enumerate(line)))

def generate_deterministic_numbers(length, lines, pass_phrase):
    #
    # Generates a list of deterministic numbers, each of a given length, based on a passphrase.
    # Uses SHA-256 to generate a hash of the passphrase concatenated with a counter.
    # Each character of the hash is converted to an integer and taken modulo 10 to get a single digit.
    #
    # NOTE: Dont use this lol, its not secure!
    #
    numbers = []
    for i in range(lines):
        # Create a hash of the passphrase concatenated with the line number 
        hash_input = (pass_phrase + str(i)).encode()
        hash_output = hashlib.sha256(hash_input).hexdigest()

        # Convert the hash to a number string of the specified length
        number = ''.join([str(int(char, 16) % 10) for char in hash_output])[:length]
        numbers.append(number)

    return numbers

def generate_csrng_numbers(length, lines):
    #
    # Generates a list of cryptographically secure random numbers from the system noise, each of a given length. Used for generation of OTP encryption/decryption keys.
    # os.urandom() generates a string of 'length' random bytes
    # We convert each byte to an integer and take its modulo 10 to get a single digit
    #
    # return [''.join([str(int.from_bytes(os.urandom(1), 'big') % 10) for _ in range(length)]) for _ in range(lines)]
    #
    return [''.join([str(secrets.randbelow(10)) for _ in range(length)]) for _ in range(lines)]

def save_to_jsonline_file(filename, numbers):
    #
    # Saves a list of numbers to a jsonline file without overwriting existing files.
    # Raises:
    #     FileExistsError: If the file already exists.
    #

    # Check if the file already exists. 
    if os.path.exists(filename):
        raise FileExistsError(f"File '{filename}' already exists. Operation cancelled to prevent overwriting.")

    # Write the numbers to the file.
    with open(filename, 'w') as file:
        for number in numbers:
            json.dump(number, file)
            file.write('\n')

def generate_random_prefix(length=4):
    # Generate a random string of uppercase letters and digits.
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# --- Convert message to audio section --- # 
class AudioMessageSynthesizer:
    # Class-level attributes for sounds and alpha...
    # Define the file names for digit and alphabet sounds.
    # These files should be WAV files representing spoken digits and phonetic alphabet.
    # The WAV files should be mono, resampled to 22050Hz, exported as .WAV - 16-bit PCM
    #sounds = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]
    #alpha = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "x-ray", "yankee", "zulu"]

    # Define the default pause durations in seconds. # 1 = 1sec, 0.25 = 200ms, 0.02 = 20ms, and 0.001 = 1ms.
    char_pause_duration = 0.05  # Time gap between spoken characters. "0.2" makes for very good distinct pauses
    special_pause_duration = 0.4  # Longer time gap for special characters like commas and spaces. "1" makes for very good distinct pauses

    def __init__(self, message, prepend_audio, append_audio, sounds, alpha):
        # Constructor: Initializes the synthesizer with a message and optional audio files to add before and after the message.
        self.message = message  # The message to be synthesized.
        self.prepend_audio = prepend_audio  # Audio files to play before the message.
        self.append_audio = append_audio  # Audio files to play after the message.
        self.sounds = sounds # The audio files to play for digits
        self.alpha = alpha # The audio files to play for alphabet

    def get_vo_file(self, character):
        # Determine the file path for the given character's audio representation.
        # This method maps characters to their respective audio files.
        if character.isdigit():
            # For digits, return the corresponding number sound file.
            return os.path.join("vo", self.sounds[int(character)])
        elif character in [',', ' ']:
            # For commas and spaces, indicate a pause is needed.
            return "pause"
        elif character == '.':
            # For periods, use a specific sound file.
            return os.path.join("vo", "_blank.wav")
        elif character == '\n':
            # For periods, use a specific sound file.
            return os.path.join("vo", "_blank.wav")
        elif character.isalpha():
            # For alphabetic characters, use the corresponding phonetic alphabet sound file.
            return os.path.join("vo", "phonetic", f"{self.alpha[ord(character.lower()) - ord('a')]}.wav")
        return None  # Return None for any other characters.

    def construct_wav(self):
        # Create a single WAV file from the provided text message
        print("Synthesizing...")
        infiles = []

        # Add audio files that are set to play before the main message.
        infiles.extend(self.resolve_paths(self.prepend_audio))

        # Process each character in the message and add corresponding audio files to the list.
        for character in self.message:
            vo_file = self.get_vo_file(character)
            if vo_file != "pause":
                # For regular characters, add their voice file and a short pause.
                infiles.append(os.path.join(sys.path[0], vo_file))
                infiles.append(self.generate_pause(AudioMessageSynthesizer.char_pause_duration))
            else:
                # For commas and spaces (i.e for one-time pad groups), add a longer pause.
                infiles.append(self.generate_pause(AudioMessageSynthesizer.special_pause_duration))

        # Add audio files that are set to play after the main message.
        infiles.extend(self.resolve_paths(self.append_audio))

        # Combine all audio files into a single WAV file.
        self.combine_audio_files(infiles, os.path.join(sys.path[0], "cipher.wav"))
        print("Audio synthesis completed")

    def resolve_paths(self, files):
        # Resolve the paths of audio files, ensuring they exist. If not, they are skipped.
        resolved_files = []
        for file in files.split(","):
            # Handle relative file paths by prefixing them with the system path.
            if not file.startswith(("/", ".")):
                file = os.path.join(sys.path[0], file)
            # Add the file to the list if it exists.
            if os.path.exists(file):
                resolved_files.append(file)
            else:
                print(f"File {file} does not exist... skipped!")
        return resolved_files

    def combine_audio_files(self, infiles, outfile):
        # Combine multiple audio files (including pauses) into a single WAV file.
        output_params = None
        data = []

        # Process each input file.
        for infile in infiles:
            if isinstance(infile, list):
                # Handle pause data (represented as a list) by adding it directly to the data array.
                chunk_params, chunk_data = infile
                if not output_params:
                    # Set the output parameters based on the first file's parameters.
                    output_params = chunk_params
                data.append(chunk_data)
            else:
                # Open and read each audio file, appending its frames to the data array.
                with wave.open(infile, 'rb') as w:
                    if not output_params:
                        output_params = w.getparams()
                    data.append(w.readframes(w.getnframes()))

        # Write the combined audio data to the output file.
        with wave.open(outfile, 'wb') as output:
            output.setparams(output_params)
            for frames in data:
                output.writeframes(frames)

    def generate_pause(self, duration):
        # Generate a pause of a specified duration.
        framerate = 44100  # Standard audio sampling rate
        silence = bytearray(int(duration * framerate * 2))  # Calculate silence length in bytes
        params = (1, 2, framerate, len(silence)//2, 'NONE', 'not compressed')  # Audio parameters for the silence
        return [params, silence]

# AudioMessageSynthesizer usage:
# message = "123456789 abcdefghijklmnopqrstuvwxyz"
# prepend_audio = "./vo/misc/buzzer.wav,vo/misc/buzzer.wav,vo/misc/buzzer.wav,vo/misc/buzzer.wav"
# append_audio = "./vo/_end.wav"
# synthesizer = AudioMessageSynthesizer(message, prepend_audio, append_audio)
# synthesizer.construct_wav()

# If necessary, you can use manual checkerboard mapping like so
# checkerboard_manual = {
#     'A': '0', 'T': '1', 'O': '3', 'N': '4', 'E': '5', 'S': '7', 
#     'I': '8', 'R': '9', 'B': '20', 'C': '21', 'D': '22', 'F': '23', 
#     'G': '24', 'H': '25', 'J': '26', 'K': '27', 'L': '28', 'M': '29',
#     'P': '60', 'Q': '61', 'U': '62', 'V': '63', 'W': '64', 'X': '65', 
#     'Y': '66', 'Z': '67', 'F/L': '68', 'SPC': '69'
# }
#
