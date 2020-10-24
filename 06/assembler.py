def tokenize(path):
    with open(path) as asm_file:
        for line in asm_file:
            striped_line = line.partition('//')[0].strip()
            if striped_line:
                yield striped_line


def a_cmd2bin(cmd):
    """
    >>> a_cmd2bin('@12')
    '0000000000001100'
    """
    assert cmd[0] == '@'
    return f'0{int(cmd[1:]):015b}'


COMP_DICT = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101',
}

DEST_DICT = {
    '': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}

JUMP_DICT = {
    '': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


SYMBOLS = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 0x4000,
    'KBD': 0x6000,
}


def c_cmd2bin(cmd):
    """
    >>> c_cmd2bin('D=A')
    '1110110000010000'
    """
    if '=' in cmd:
        dest, _, tail = cmd.partition('=')
        comp, _, jump = tail.partition(';')
    else:
        dest = ''
        comp, _, jump = cmd.partition(';')
    # print({
    #     'cmd': cmd,
    #     'dest': dest,
    #     'comp': comp,
    #     'jump': jump,
    # })
    return f'111{COMP_DICT[comp]}{DEST_DICT[dest]}{JUMP_DICT[jump]}'


def cmd2bin(cmd):
    if cmd.startswith('@'):
        return a_cmd2bin(cmd)
    else:
        return c_cmd2bin(cmd)


def command_type(cmd):
    if cmd.startswith('@'):
        return 'A_COMMAND'
    if cmd.startswith('(') and cmd.endswith(')'):
        return 'L_COMMAND'
    return 'C_COMMAND'


class Assembler:
    def __init__(self, path):
        self.cmds = [(cmd, command_type(cmd)) for cmd in tokenize(path)]
        self.current_rom_addr = 0
        self.current_var_addr = 16
        self.bin_codes = []
        self.symbols = dict(SYMBOLS)

    def symbol(self, cmd):
        if cmd.startswith('@'):
            return cmd[1:]
        if cmd.startswith('(') and cmd.endswith(')'):
            return cmd[1:-1]

    def assemble(self):
        for cmd, cmd_type in self.cmds:
            if cmd_type == 'A_COMMAND' or cmd_type == 'C_COMMAND':
                self.current_rom_addr += 1
            else:
                self.symbols[self.symbol(cmd)] = self.current_rom_addr
        for cmd, cmd_type in self.cmds:
            if cmd_type == 'A_COMMAND':
                current_symbol = self.symbol(cmd)
                if current_symbol.isdigit():
                    self.bin_codes.append(a_cmd2bin(cmd))
                elif current_symbol in self.symbols:
                    self.bin_codes.append(a_cmd2bin(f'@{self.symbols[current_symbol]}'))
                else:
                    self.symbols[current_symbol] = self.current_var_addr
                    self.current_var_addr += 1
                    self.bin_codes.append(a_cmd2bin(f'@{self.symbols[current_symbol]}'))
            elif cmd_type == 'C_COMMAND':
                self.bin_codes.append(c_cmd2bin(cmd))
        return '\n'.join(self.bin_codes) + '\n'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
