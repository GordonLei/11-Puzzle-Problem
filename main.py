# Open up an input file with read access
# Next open/create a file to represent the output file 
input_file = open("Sample_Input.txt", "r")
output_file = open("Output_Solution.txt", "w+")

# create 3 3x4 2D array repreresenting the initial state, the current state, and the goal state respectively
# each of these array show the corresponding states as the board 
initial_state = [[0 for i in range(4)] for j in range(3)] 
curr_state = [[0 for i in range(4)] for j in range(3)] 
goal_state = [[0 for i in range(4)] for j in range(3)] 


input_lines = input_file.readlines()                    # read each line in the input text and put it into a list 
for i in range(3):                                      # for each row...
    current_numbers = input_lines[i].strip().split()    # split every line by the spaces to get the individual numbers in another list
    for j in range(4):                                  # for each column...
        initial_state[i][j] = current_numbers[j]        # put the number into the corressponding spot in the 2D array to simulate the board

for i in range(4,7):                                    # create a representation of the goal_state as a 2D array to simulate the board
    current_numbers = input_lines[i].split()
    for j in range(4):
        goal_state[i-4][j] = current_numbers[j]

for i in range(3): 
    for j in range(4):
        #print(str(i) + " " + str(j))
        print(goal_state[i][j] + " ")  


input_file.close()
output_file.close()