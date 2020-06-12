# ------------ saves python lists to .txt ---------------------------------------------
#
# Functions:
# -save( <filename.txt> , <array (1D or 2D)>)
#   -> array can be 1 or 2 dimensional
#   -> array type must be int or float
#
# -read( <filename.txt> , <datatype to read> , <number of splits if its 2D, else type 1> )
#   -> datatype can be "int" or "float"
#   
# -------------------------------------------------------------------------------------

def save(filename,array,d):
    f = open(filename,"w")
    if d == 1:
        for i in range(len(array)):
            f.write(str(array[i]) + " ")
    if d == 2:
        for i in range(len(array)):
            for j in range(len(array[0])):
                f.write(str(array[i][j]) + " ")
    f.close()

def read(filename,dtype,d):

    try:
        f = open(filename,"r")
    except:
        print("Saving error: File does not exist")
        return
    
    data = f.read()
    data = data.split()
    f.close()
            
    if dtype == "int":
        n = []
        for i in range(len(data)):
            n.append(int(float(data[i])))

    if dtype == "float":
        n = []
        for i in range(len(data)):
            n.append(float(data[i]))
    data = n

    if d == 1:
        pass
    else:
        counter = 0
        n = []
        for i in range(d):
            m = []
            for j in range(int(len(data)/d)):
                m.append(data[counter])
                counter += 1
            n.append(m)
        data = n
        
    return data
