with open('main_enhanced.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = False
for i, line in enumerate(lines):
    if 'async def synthesize_speech' in line:
        print(f'synthesize_speech method starts at line {i+1}: {line.strip()}')
        found = True
        break

if not found:
    print('Method not found')