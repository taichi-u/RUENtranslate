import sys
if __name__ == '__main__':
    for x in sys.stdin:
        x = x.strip()  # start/end should be no " "
        x = x.replace('▁', ' ')  # '▁' -> " "
        x = ' '.join(x.split())  # "  "-> " "
        print(x)
