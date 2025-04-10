#! /usr/bin/env python3

import sys
import os
import argparse

# Reference https://usb.org/sites/default/files/hut1_21.pdf Page 83

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


HID_KEYS = [
    0x0, 0x0, 0x0, 0x0,
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    '\n', 0x0, 0x0, # DEL
    0x0, # TAB
    ' ', # SPACE
    '-', '=', '[', ']', '\\', 0x0, ';', '\'', '`', ',', '.', '/',
    0x0, # CAPS LOCK
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4f, # R_ARROW
    0x0, # L_ARROW
    0x0, # D_ARROW
    0x0, # U_ARROW
    0x0, # NUM LOCK
]

HID_SHIFT_KEYS = [
    0x0, 0x0, 0x0, 0x0,
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '\n', 0x0, 0x0, # DEL
    0x0, # TAB
    ' ', # SPACE
    '_', '+', '{', '}', '|', 0x0, ':', '"', '~', '<', '>', '?',
    0x0, # CAPS LOCK
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4f, # R_ARROW
    0x0, # L_ARROW
    0x0, # D_ARROW
    0x0, # U_ARROW
    0x0, # NUM LOCK
]


TAB_SPACES = 2
NAME = os.path.basename(os.path.realpath(__file__))

DESCRIPTION = "\n" \
              "\n" \
              "usage: %s [options]\n" % NAME

EPILOG = "\n" \
         "\n" \
         "Examples:\n" \
         "\tSomething\n" \
         "\n"

def convert_hid_to_text(input_file_path, output_file_path, debug = False):
    
    data_buffer = [[]]
    with open(input_file_path, 'rb') as input_file:
        if debug: print ("Opened file: %s" % input_file_path)
        data = input_file.read(4)
        flag_capslock = False
        cursor = [0, 0]
        while data:
            data = input_file.read(4)
            if len(data) < 4:
                if debug: print ("Finished reading in the data")
                break
            flag_shift = True if (flag_capslock) else False
            flag_control = False
            if data[1] & 0x02:
                flag_shift = not flag_shift

            # Check if we need to move the cursor
            if data[0] == 0x2B: # Tab
                if debug: print ("tab")
                flag_control = True
                cursor[1] += TAB_SPACES
                
            elif data[0] == 0x2A: # Backspace
                if debug: print ("<BACKSPACE>")
                flag_control = True
                if cursor[1] == 0:
                    if cursor[0] > 0:
                        cursor[0] = cursor[0] - 1
                        if cursor[0] > 0:
                            cursor[1] = cursor[0] - 1
                        else:
                            cursor[1] = 0
            #elif data[0] == 0x4C: # Delete
            #    flag_control = True
            #    # TODO
            #    pass 

            #elif data[0] == 0x75: # Insert
            #    flag_control = True
            #    # TODO
            #    pass

            #elif data[0] == 0x80: # Home
            #    flag_control = True
            #    # TODO
            #    pass

            #elif data[0] == 0x81: # End
            #    flag_control = True
            #    # TODO
            #    pass

            #elif data[0] == 0x86: # Page Down
            #    flag_control = True
            #    # TODO
            #    pass

            #elif data[0] == 0x85: # Page Up
            #    flag_control = True
            #    # TODO
            #    pass

            # Arrows
            else:
                if data[0] != 0:
                    value = HID_SHIFT_KEYS[data[0]] if flag_shift else HID_KEYS[data[0]]
                    if debug: print (value, end = '')

                    while len(data_buffer) <= cursor[0]:
                        data_buffer.append([])
                    while len(data_buffer[cursor[0]]) <= cursor[1]:
                        data_buffer[cursor[0]].append(' ')
                    data_buffer[cursor[0]][cursor[1]]


                    data_buffer[cursor[0]].insert(cursor[1], value)
                    if data[0] == 0x28:
                        cursor[0] += 1
                        cursor[1] = 0
                    else:
                        cursor[1] = cursor[1] + 1



    #if debug:
    #    print ("Buffer: %s" % str(data_buffer))
            
            
    with open(output_file_path, 'w') as output_file:
        # Read in 4 bytes from the input
        for b in data_buffer:
            s = ""
            for d in b:
                s += d
            output_file.write(s)
        #cursor = [0, 0]

        #while cursor[0] < len(buffer[0]) and cursor[1] < len(buffer[cursor[0]][cursor[1]]):
        #    val = buffer[cursor[0]][cursor[1]]
        #    output_file.write(val)
        #    if cursor[1] >= len(buffer[cursor[0]]) and val != '\n':
        #        val = '\n'

        #    if val == '\n':
        #        cursor[0] += 1
        #        cursor[1] = 0
        #        output_file.write('\n')
        #    else:
        #        cursor[1] = cursor[1] + 1



def main(argv):
    #Parse out the commandline arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    parser.add_argument("filename",
                        default=["something"])

    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Enable Debug Messages")

    args = parser.parse_args()
    print ("Running Script: %s" % NAME)


    if args.debug:
        print ("test: %s" % str(args.filename))

    input_file_path = args.filename
    output_file_path = os.path.splitext(args.filename)[0] + ".txt"
    convert_hid_to_text(input_file_path, output_file_path, args.debug)

if __name__ == "__main__":
    main(sys.argv)


