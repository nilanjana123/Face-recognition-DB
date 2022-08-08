print('Welocome to the FACE RECOGNITION SYSTEM\n')
while(1):
    c = input('Enter your choice : \n1 : REGESTRATION\n2 : TRAINING\n3 : RECOGNITION\n4 : RECOGNITION WITH IMAGE\n5 : EXIT WINDOW\n')
    if(c == '1'):
        import Capture
    elif(c == '2'):
        import Trainer
    elif (c == '3'):
        import Recogniser
    elif (c == '4'):
        import ImgRecog
    elif (c == '5'):
        exit(1)
    else:
        print('WRONG INPUT')