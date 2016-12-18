__author__ = 'tpaul'
from termcolor import cprint
from colorama import init
import sys
def decorate(text, basic, edge, center):
    init()
    sys.stdout.write('\n')
    background = 'on_green'
    foreground = 'cyan'

    if len(text) % 2 == 0:
        top = edge + basic*(len(text)/2) + center*2 + basic*(len(text)/2) + edge
        core = edge + ' ' + text + ' ' + edge
        bottom = edge+basic*(len(text)/2)+center*2+basic*(len(text)/2)+edge
        sys.stdout.write('\t\t\t')
        cprint(top, foreground, background, attrs=['bold'])
        sys.stdout.write('\t\t\t')
        cprint(core, foreground, background, attrs=['bold'])
        sys.stdout.write('\t\t\t')
        cprint(bottom, foreground, background, attrs=['bold'])
        sys.stdout.write('\n')
    else:
        top = edge + basic*(len(text)/2) + center*3 + basic*(len(text)/2) + edge
        core = edge + ' ' + text + ' ' + edge
        bottom = edge+basic*(len(text)/2)+center*3+basic*(len(text)/2)+edge
        sys.stdout.write('\t\t\t')
        cprint(top, foreground, background, attrs=['bold'])
        sys.stdout.write('\t\t\t')
        cprint(core, foreground, background, attrs=['bold'])
        sys.stdout.write('\t\t\t')
        cprint(bottom, foreground, background, attrs=['bold'])
        sys.stdout.write('\n')
