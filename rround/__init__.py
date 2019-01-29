from termcolor import colored


def cp(*x, color='yellow'):
    x = ' '.join([str(i) for i in x])
    print(colored(x, color, 'on_cyan', attrs=['bold']))