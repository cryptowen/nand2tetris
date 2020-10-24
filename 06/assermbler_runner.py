import os
from pathlib import Path

file_path = Path(__file__).cwd()
asm_files = file_path.rglob('**/*.asm')
assembler_path = file_path.parent.parent / Path('tools/Assembler.sh')
for f in asm_files:
    os.system(f'{assembler_path} {f}')
