print('Valid inputs: start, end, halt, exit')
while True:
    command = input('Input: ')
    
    if (command == 'start'):
        print('Going to start')
    elif (command == 'end'):
        print('Going to end')
    elif (command == 'halt'):
        print('Ending')
    elif (command == 'exit'):
        print('Exiting program')
        break