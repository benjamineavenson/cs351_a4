#Benjamin Eavenson
#CS351 Assignment 4

def create_index(input_file, output_path, sorted):
    myIn = open(input_file, "r")
    output_file = output_path + input_file
    if sorted:
        output_file += "_sorted"
    myOut = open(output_file, "w")
    entry = myIn.readline()
    inList = [] #Our list of entries
    while entry != "":
        inList.append(entry)
        entry = myIn.readline()

    if sorted:  #Sort our list of entries if specified
        inList.sort()

    for entry in inList:

        entry = entry.split(",")

        #First four bits are based on animal type
        if entry[0] == "cat":
            outLine = "1000"
        elif entry[0] == "dog":
            outLine = "0100"
        elif entry[0] == "turtle":
            outLine = "0010"
        elif entry[0] == "bird":
            outLine = "0001"

        entry[1] = int(entry[1])
        #Next 10 bits are based on animal age
        if entry[1] < 11:
            outLine += "1000000000"
        elif entry[1] < 21:
            outLine += "0100000000"
        elif entry[1] < 31:
            outLine += "0010000000"
        elif entry[1] < 41:
            outLine += "0001000000"
        elif entry[1] < 51:
            outLine += "0000100000"
        elif entry[1] < 61:
            outLine += "0000010000"
        elif entry[1] < 71:
            outLine += "0000001000"
        elif entry[1] < 81:
            outLine += "0000000100"
        elif entry[1] < 91:
            outLine += "0000000010"
        else:
            outLine += "0000000001"
        
        #Last 2 bits are based on adoption status
        if entry[2] == "True\n":
            outLine += "10"
        elif entry[2] == "False\n":
            outLine += "01"
        
        outLine += "\n"
        myOut.write(outLine)

    myIn.close()
    myOut.close()





def compress_index(bitmap_index, output_path, compression_method, word_size):
    myIn = open(bitmap_index, "r")
    myOut = None

    #First we put our data into columns instead of rows

    columns = []
    for i in range(16):
        columns.append("")

    entry = myIn.readline()
    while entry != "":
        for i in range(16):
            columns[i] += entry[i]
        entry = myIn.readline()


    total_fills = 0
    total_literals = 0
    total_dirty = 0

    if compression_method == "WAH":
        output_file = output_path + bitmap_index + "_WAH_" + str(word_size) #setup output file
        myOut = open(output_file, "w")
        for column in columns:  #a row for each column
            head = 0    #this is where we are in the column
            output = ""
            while head+word_size-1 < len(column)+1: #while we have at least a whole word left
                curr = column[head:head+word_size-1]    #grab a word
                if ((curr == ("0" * (word_size-1))) or (curr == ("1" * (word_size-1)))): #if the word is all ones or all zeros
                    runType = curr #store it
                    runs = 1    # we have a run
                    total_fills += 1
                    head += (word_size-1)   #move the head up
                    curr = column[head:head+word_size-1]    #grab the next word
                    while ((runType == curr) and (runs != (2**(word_size-2)-1))): #if this new word is the same as the last word
                        runs += 1   #and we have enough room to store another run, do so
                        total_fills += 1
                        head += (word_size-1)   #move the head up
                        if head+word_size-1 >= len(column)+1:   #if there isnt another word to grab we break
                            break  
                        curr = column[head:head+word_size-1]    #grab the next word
                    bitType = runType[0]    #specify if its a run of ones or zeros
                    fill = format(runs, "b")    #convert to a binary string
                    while len(fill) < (word_size-2):    #pad with zeros
                        fill = "0" + fill
                    output += "1" + bitType + fill  #add to the output string
                else:   #a literal
                    total_literals += 1
                    output += "0" + curr
                    head += word_size-1
            if column[head] != "\n":
                last = "0" + column[head:]
                total_literals += 1
                while len(last) < word_size:
                    last += "0"
                output += last
            output += "\n"
            myOut.write(output)


    elif compression_method =="BBC":
        output_file = output_path + bitmap_index + "_BBC_8"   #setup output file
        myOut = open(output_file, "w")
        for column in columns:  #each column is a line
            head = 0    #this is where we are looking at in the column
            output = ""
            done = False    #we will set this if we want to leave our main loop at some point
            while head+8 < len(column)+1:   #while there is another byte to read
                runs = 0
                literals = ""
                header = ""
                while runs < 32767:    #count runs up to 32767
                    curr = column[head:head+8]
                    if curr == "0" * 8: #we've just read in a run
                        total_fills += 1
                        runs += 1
                        head += 8
                    else:   #we've just read in a dirty byte/literal
                        break
                    if head + 8 > len(column)+1:    #no more to read, set done to true
                        done = True
                        break
                if not done:
                    curr = column[head:head+8]  #make sure we are looking at the next byte before continuing
                if runs <= 6:         #first three bits of header byte is number of runs
                    header += format(runs, "b")
                    while len(header) < 3:
                        header = "0" + header
                    if done:
                        header += "00000"   #if we are done make sure to add the rest of the header byte
                else:
                    header = "111"  #more than 6 runs
                    if done:
                        header += "00000"
                if not done:    #if we are done, this will skip down to the extra header bytes section
                    dirty = -1              #do we have a dirty byte? and do we have runs following it?
                    if curr == "00000001" and column[head+8:head+16] == "0"*8:
                        dirty = 7
                    elif curr == "00000010" and column[head+8:head+16] == "0"*8:
                        dirty = 6
                    elif curr == "00000100" and column[head+8:head+16] == "0"*8:
                        dirty = 5
                    elif curr == "00001000" and column[head+8:head+16] == "0"*8:
                        dirty = 4
                    elif curr == "00010000" and column[head+8:head+16] == "0"*8:
                        dirty = 3
                    elif curr == "00100000" and column[head+8:head+16] == "0"*8:
                        dirty = 2
                    elif curr == "01000000" and column[head+8:head+16] == "0"*8:
                        dirty = 1
                    elif curr == "10000000" and column[head+8:head+16] == "0"*8:
                        dirty = 0
                    if dirty != -1:
                        header += "1"   #next 5 bits of header for dirty byte
                        dirty = format(dirty, "b")
                        while len(dirty) < 4:   #pad out to correct length
                            dirty = "0" + dirty
                        header += dirty #append to the header
                        total_dirty += 1
                        head += 8   #dont forget to move our head
                    else: #next 5 bits for literals
                        num_literals = 0
                        while num_literals < 15:  #count up to 15 literals
                            curr = column[head:head+8]
                            if curr != "0" * 8:
                                literals += curr
                                num_literals += 1
                                total_literals += 1
                                head += 8
                            else:   #no more literals
                                break
                            if head+8 > len(column)+1:  #nothing more to read
                                break
                        header += "0"   #append to header
                        num_literals = format(num_literals, "b")
                        while len(num_literals) < 4:
                            num_literals = "0" + num_literals   #padding out with zeros
                        header += num_literals
                #extra header bytes if needed
                if (runs > 6) and (runs < 128): #next byte for runs (7-127)
                    header += "0" #a zero to indicate that there is only one extra byte
                    runs = format(runs, "b")
                    while len(runs) < 7:
                        runs = "0" + runs
                    header += runs
                elif (runs > 127):  #next 2 bytes for runs (8-32767)
                    header += "1" #a one to indicate we are using two extra bytes
                    runs = format(runs, "b")
                    while len(runs) < 15:
                        runs = "0" + runs
                    header += runs
                output += header + literals     #add the header followed by literals to our output
            output += "\n"  #we have finished a column, time for a new line
            myOut.write(output)


    else:
        print("Specified compression method not supported")
    

    myIn.close()    #dont forget to close our files
    if myOut != None:
        myOut.close()

    print("Total fills compressed: " + str(total_fills))
    print("Total literals compressed: " + str(total_literals))
    print("Total dirty bytes compressed: " + str(total_dirty))