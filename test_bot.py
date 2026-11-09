import sys
sys.path.insert(0, '.')
from bot import parse_command

def test_parse():
    cmd, args = parse_command('/add 100 Продукты молоко')
    assert cmd == 'add' and args[0] == '100'

if __name__ == '__main__':
    test_parse()
    print('ok')
