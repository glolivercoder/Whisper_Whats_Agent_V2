with open('main_enhanced.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the method
start_line = -1
for i, line in enumerate(lines):
    if 'async def synthesize_speech' in line:
        start_line = i
        print(f'synthesize_speech method starts at line {i+1}')
        break

if start_line != -1:
    # Look for the end of the method (next method or class)
    end_line = -1
    for i in range(start_line + 1, len(lines)):
        # Check if this line starts a new method or class
        stripped = lines[i].strip()
        if (stripped.startswith('def ') or 
            stripped.startswith('async def ') or 
            stripped.startswith('class ') or
            (stripped == '' and i + 1 < len(lines) and 
             (lines[i + 1].strip().startswith('def ') or 
              lines[i + 1].strip().startswith('async def ') or 
              lines[i + 1].strip().startswith('class ')))):
            end_line = i
            print(f'synthesize_speech method ends at line {i}')
            break
    
    if end_line == -1:
        # If we didn't find the end, go to the end of the file
        end_line = len(lines)
        print(f'synthesize_speech method ends at end of file (line {end_line})')
        
    print(f'Method spans from line {start_line+1} to {end_line}')
else:
    print('Method start not found')