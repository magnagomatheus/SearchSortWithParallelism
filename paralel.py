import time
import numpy as np
import os
from multiprocessing import shared_memory, Process, Pool

# The parameters are: Shared Memory Space, Vector shape, Vector dtype, 
# the indices that define where the process will search.
# and the number to find
def findNumberParalel(shm_name, vector_shape, vector_dtype, start:int, end:int, x:int):

    # Getting the shared memory block created at the main
    shm = shared_memory.SharedMemory(name=shm_name)

    # Reconstructing the Vector from shared memory to here (creating a view)
    shared_vector = np.ndarray(
        shape = vector_shape,
        dtype=vector_dtype,
        buffer = shm.buf
    )

    # this loop will have the indices that was designated when 
    # creating the process itself for each process
    for i in range(start, end):
        if(shared_vector[i] == x):
            print(f"{x} was found on the {i}st position with paralelism.")
            return i

    #print(f"NUMERO NAO ENCONTRADOOOOOOOOOOOOO")
    return None

def findNumberSeq(vector, x:int):

    for i in range(vector.size):
        if(vector[i] == x):
            return i
        
    return None

def main():

    # Creating the vector with 50000 numbers
    vector = np.random.randint(0, high=49999, size=50000)
    x = 10000
    # Testing serial time to find the number within the vector
    start = time.time()
    result = findNumberSeq(vector, x)
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

    # Creating a child process and telling him to use the shared memory space

    ######################## PROCESS 1 #######################################

    tasks = []
    qtdNucleos = os.cpu_count()
    print(f"Quantidade de nucleos: {qtdNucleos}\n")
        
    # Indica a div de trabalho na lista
    divisaoIndices = vector.size // qtdNucleos-1
    
    
    for i in range(qtdNucleos):
        inicio = i * divisaoIndices
        # Indice final do outro processo sera 
        # a soma do indice final do antigo processo + divisao feita (tamanhoVetor/qtdNucleos)
        # Ultimo Processo (qtdNucleos-1) vai ate o (fim vector.size)
        fim = (i + 1) * divisaoIndices if i != qtdNucleos - 1 else vector.size

        # Adicionando os parametros para cada processo
        tasks.append((shm.name, vector.shape, vector.dtype, inicio, fim, x))

    start2 = time.time()
    with Pool(processes=qtdNucleos) as pool:
        results = pool.starmap(findNumberParalel, tasks)

    for result in results:
        if result != None:
            print(result)
    
    end2 = time.time()
    """process1 = Process (
        target=findNumberParalel,
        args=(shm.name, vector.shape, vector.dtype, 0, 12500, x)
    )

    process2 = Process(
        target=findNumberParalel,
        args=(shm.name, vector.shape, vector.dtype, 12501, 25000, x)
    )

    process3 = Process(
        target=findNumberParalel,
        args=(shm.name, vector.shape, vector.dtype, 25001, 37500, x)
    )

    process4 = Process(
        target=findNumberParalel,
        args=(shm.name, vector.shape, vector.dtype, 37501, 50000, x)
    )


    """


    ######################## PROCESS 1 #######################################

    # Free the memory space allocated for shared memory
    shm.close() # Detach the parent from the shared memory
    shm.unlink() # Delete the shared memory block from the memory

    print(f"Search with parallelism time was: {end2 - start2}")

    ######################### Child Process CODE ############################

    # Printing the vector to see if the vector could be created
    #print(vector)
    #print(vector.size)

    print()
    #Printing the result of the search
    if(result == None):
        print(f"Number not found!")
    else:
        print(f"{x} was found on the {result}st position")
    print(f"Tempo decorrido: {end-start}")

    return 0
if __name__ == "__main__":
    main()