import time
import numpy as np
from multiprocessing import shared_memory

def findNumberParalel(numbers, x:int):

    for i in range(numbers.size):
        if(numbers[i] == x):
            return i

    return None


def main():

    # Creating the vector with 50000 numbers
    vector = np.random.randint(0, high=49999, size=50000)
    x = 12000
    # Testing serial time to find the number within the vector
    start = time.time()
    result = findNumberParalel(vector, x)
    end = time.time()

    ######################### SHARED MEMORY CODE ############################

    # Getting the size of the vector in bytes
    vector_size = vector.nbytes

    # Creating a shared memory block
    shm = shared_memory.SharedMemory(create = True, size = vector_size)
    print(f"Shared memory block name: {shm.name}")

    # Creating a numpy vector using shared memory buffer
    shared_vector = np.ndarray(
        shape=vector.shape, # Gets the original shape (i think this is abount the dimension of array)
        dtype=vector.dtype, # gets the original dtype of the existing array
        buffer=shm.buf # Use shared memory as buffer
    )

    # Copy the numbers from the original vector to shared memory space
    shared_vector[:] = vector[:]

    ######################### SHARED MEMORY CODE ############################


    ######################### Child Process CODE ############################

    

    ######################### Child Process CODE ############################

    # Printing the vector to see if the vector could be created
    print(vector)
    #print(vector.size)

    #Printing the result of the search
    if(result == None):
        print(f"Number not found!")
    else:
        print(f"{x} was found on the {result}st position")
    print(f"Tempo decorrido: {end-start}")

    return 0
if __name__ == "__main__":
    main()