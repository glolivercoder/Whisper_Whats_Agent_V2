# Script to fix the indentation error in main_enhanced.py
with open('main_enhanced.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the problematic section
start_idx = -1
end_idx = -1

# Look for the orphaned code block
for i, line in enumerate(lines):
    # Find the start of the orphaned block
    if 'temp_path = temp_file.name' in line and line.startswith(' ' * 20):
        start_idx = i
        print(f"Found orphaned block starting at line {i+1}")
        break

# If we found the start, look for the end
if start_idx != -1:
    # Look for the proper closing of the synthesize_speech method
    for i in range(start_idx, len(lines)):
        if (lines[i].strip() == 'except Exception as e:' and 
            i+1 < len(lines) and 
            lines[i+1].strip() == 'logger.error(f"TTS error: {e}")' and
            i+2 < len(lines) and
            lines[i+2].strip() == 'return {"success": False, "error": str(e)}'):
            end_idx = i
            print(f"Found end of orphaned block at line {i+1}")
            break

# Remove the orphaned code block if found
if start_idx != -1 and end_idx != -1:
    print(f"Removing lines {start_idx+1} to {end_idx}")
    del lines[start_idx:end_idx]
    
    # Write the fixed file
    with open('main_enhanced.py', 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)
    
    print("File fixed successfully!")
else:
    print("Orphaned code block not found or not properly identified.")