# Robert Panerio
# Python 3
# CS 427
# ROBE; 18 15 2 5; 67 53 5 13

import sys

#SubkeyN = lowerbyte( ActualKey rol (N * 4)) xor lowerbyte( NamePrimesN )

def rol(ActualKey, rol):
    # bit shifting the upper byte to the right by 16-rol and shifting the lower byte to the right by rol
    return  (ActualKey >> (16 - (rol))) | (ActualKey << (rol)) 

def feistel(message, key, nonce, chunk_N):

    # prime of names
    namePrime_arr = [ 67, 53, 5, 13 ]

    # divide 'm' for left and right
    m = (nonce + chunk_N)
    right_n = m & 0xFF
    left_n = (m & 0xFF00) >> 8

    F = None

    # loop through each round
    for n in range(0,4):

        # calculate the subkey
        subkey_N = (rol(key,n*4) & 0xFF) ^ (namePrime_arr[n] & 0xFF)
        F = subkey_N ^ right_n

        #swap left and right
        temp = right_n
        right_n = F ^ left_n
        left_n = temp

    # swapping left and right at end
    temp = right_n
    right_n = left_n
    left_n = temp

    # bit shifting left side by 8 and adding the right side
    enc = (left_n << 8) + right_n
    res = enc ^ int(message, 16)
    return res

def main():

    # read input from standard in
    for line in sys.stdin:
        stdin_input = line.split()

        # saving the input
        nonce = int(stdin_input[0], 16)
        key = int(stdin_input[1], 16)
        message = stdin_input[2]
    
        # checks if message is even
        if len(message) % 2 != 0:
            print("ERROR: wrong input \'message\'; must be even in length")
            exit(-1)

        # append zero if the message does not have enough length
        if len(message) % 4 != 0:
            message = message + "00"

        # parse the message by 4 chunks (4 characters per array element)
        message = [message[x:x+4] for x in range(0, len(message), 4)]

        encrypt = None
        for n, m in enumerate(message):
            temp = feistel(m, key, nonce, n)
            encrypt = temp if encrypt is None else ((encrypt << 16) + temp)

        print(hex(encrypt)[2:])

if __name__ == '__main__':
    main()