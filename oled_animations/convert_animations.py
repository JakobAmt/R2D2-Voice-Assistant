# This script extracts the frame data from the Arduino .ino files
# and saves them as binary files for Python to use

import re
import os

def extract_frames(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    frames = []
    # Find all frame arrays
    pattern = r'const uint8_t PROGMEM frame\d+\[1024\] = \{([^}]+)\}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        # Extract hex bytes
        bytes_list = re.findall(r'0x[0-9a-fA-F]+', match)
        frame_bytes = bytes([int(b, 16) for b in bytes_list])
        frames.append(frame_bytes)
    
    return frames

# Save frames as binary
def save_frames(frames, output_file):
    with open(output_file, 'wb') as f:
        for frame in frames:
            f.write(frame)
    print(f"Saved {len(frames)} frames to {output_file}")

# Run conversion - update paths to match where you saved the .ino files
frames1 = extract_frames('animation1.ino')
frames2 = extract_frames('animation2.ino')
frames3 = extract_frames('animation3.ino')
frames4 = extract_frames('animation4.ino')

save_frames(frames1, 'anim1.bin')
save_frames(frames2, 'anim2.bin')
save_frames(frames3, 'anim3.bin')
save_frames(frames4, 'anim4.bin')
