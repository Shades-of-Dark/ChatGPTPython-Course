# Import socket module
import socket

import requests
from PIL import Image




def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer

    s.connect((host, port))

    # message you send to server
    message = "getting images..."
    while True:

        # message sent to server
        s.send(message.encode('ascii'))

        # message received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue?(y/n) :')
        if ans == 'y':
            pass
        else:
            break
        query = input('\nGive us an image link: ')
        try:
            # This statement requests the resource at
            # the given link, extracts its contents
            # and saves it in a variable
            data = requests.get(query).content

            # Opening a new file named img with extension .jpg
            # This file would store the data of the image file
            filename = input("\nName the file: ")
            f = open(filename + '.jpg', 'wb')

            # Storing the image data inside the data variable to the file
            f.write(data)
            f.close()

            # Opening the saved image and displaying it
            img = Image.open(filename + '.jpg')
            img.show()
        except:
            print("error check your url to make sure it's correct.")
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
