import sys

if len(sys.argv != 2):
    raise Exception

if sys.argv[1] == 'client':
    print('Running in client mode')
elif sys.argv[1] == 'server':
    print('Running in server mode')
else:
    raise Exception
