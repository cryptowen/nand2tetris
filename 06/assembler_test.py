import pytest
from pathlib import Path
from assembler import Assembler
from assembler import tokenize


asms = list(Path(__file__).cwd().rglob('**/*.asm'))


def test_tokenize():
    res = tokenize(Path(__file__).cwd() / 'add/Add.asm')
    assert list(res) == ['@2', 'D=A', '@3', 'D=D+A', '@0', 'M=D']


@pytest.mark.parametrize("asm", asms)
def test_add(asm):
    res = Assembler(asm).assemble()
    hack = str(asm).replace('asm', 'hack')
    assert res == open(hack).read()
