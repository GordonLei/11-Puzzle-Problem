import copy
# an individual state possible in the puzzle 
class state:
    def __init__(self, configuration, goal_locations, outputObj = "", depth = 0, num_nodes = 0, f_value = 0, action_ls = [], f_value_ls = []): 
        # configuration is the representation of the board state as a 2D Array
        self.configuration = configuration
        # goal_locations is the locations of the corressponding index in the goal state
        # for example, index 0 of goal_locations is a tuple representing 
        #       where the (x,y) position of 0 in the goal state 
        #       x meaning the column # /x-coordinate 
        #       y meaning the row # / y-coordinate 
        # the top left corner of the board is (0,0)
        # the bottom right corner of the board is (3,4)
        self.goal_locations = goal_locations
        # how deep the state is in the tree
        self.depth = depth
        # what is the f-value of the state 
        self.f_value = f_value
        # self.depth = depth
        # the number of nodes that were created in the tree so far 
        self.num_nodes = num_nodes
        # the actions needed to get to the current state
        self.action_ls = action_ls
        # the f-values of previous states and the current state 
        self.f_value_ls = f_value_ls 
        # the output file
        self.outputObj = outputObj
    # define the == operation to compare if states are the same 
    def __eq__(self, other):
        for i in range(3):
            for j in range(4):
                if (self.configuration[i][j] != other.configuration[i][j]):
                    return False
        return True 
    # just to return a list representing the number^th row 
    # example get_row(0) gets the first row of the board/state
    # this is just for printing out the board/state
    def get_row(self, number):
        return self.configuration[number]
    # write to the output file the depth, number or nodes created, actions taken, and the f-values
    def print_descriptor(self):
        print ("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")
        self.outputObj.write("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")

        # print(self.action_ls)
        # print(self.f_value_ls)
        print(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
        self.outputObj.write(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
    # this function was not used 
    # if it were to be used it would have printed the state's configuration as well as it's description
    def print_node(self):
        for i in range(3):
            line = " ".join(self.configuration[i])
            print(line + "\n")
            self.outputObj.write(line + "\n")

        print ("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")
        self.outputObj.write("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")

        print(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
        self.outputObj.write(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
    # find the coordinate of the number in the configuration data member of the the state
    # return a tuple representing the coordinates in the form (x,y) or (column number, row number)
    # return (-1,-1) if you cannot find the number 
    def find_pos(self, number):
        for i in range(3):
            for j in range(4):
                if (self.configuration[i][j] == number):
                    return (j,i)
        return(-1,-1)
    # determine the herusitic value of the state (in other words h(x))
    def heuristic(self):
        h_value = 0 
        for i in range(3):
            for j in range(4):
                #print(self.find_pos((self.configuration[0])[2]))
                #print("DONE")
                #print(i,j)
                #print(self.configuration)
                #print(self.configuration[0][2])
                #print(self.find_pos(self.configuration[i][j]))


                goal_location = self.goal_locations[int(self.configuration[i][j])]
                # h_value += self.manhattan_distance(i, j, goal_location[0], goal_location[1])

                # goal location[0] is the column where the current number is located in the goal state (so the x value)
                # goal location[1] is the row where the current number is located in the goal state (so the y value)
                # subtract the row number (j) from goal_location[1] and subtract the column number from goal location[0]
                h_value += self.manhattan_distance(j, i, goal_location[0], goal_location[1])
        
        #print("H_VALUE IS: " + str(h_value))
        return h_value
    # calculate the manhattan distance between two coordinates 
    def manhattan_distance(self, x1,y1, x2, y2):
        return abs(x1 - x2) + abs(y1- y2)
    # calculate the f-value and set it as f_value, then append this value to f_values_ls
    def calculate_f(self):
        # print("f(x) = g(x) + h(x)")
        # print(str(self.depth + self.heuristic()) + " = " + str(self.depth) + " + " + str(self.heuristic()))

        self.f_value = self.depth + self.heuristic()
        self.f_value_ls.append(str(self.f_value))
        
    # expand the the state to find possible moves of swapping the blank space
    # return a list of all these valid possible states, valid meaning it does not go out of bounds from the board
    def expand_node(self):
        # this will continue a list of states that are potential candidates for expansion from A* search 
        children = []          

        # find the position of the blank space in the current state
        blank_pos = self.find_pos(str(0))
        # potential spots that the blank space can swap to/move to
        potential_neighbors = []
        potential_neighbors.extend([
            (blank_pos[0] + 1,blank_pos[1], "R"),
            (blank_pos[0] - 1,blank_pos[1], "L"),
            (blank_pos[0],blank_pos[1] - 1, "U"),
            (blank_pos[0],blank_pos[1] + 1, "D")]   
        )
        # remove the elements in potential_neighers that put the blank space outside of the board
        for elem in potential_neighbors:
            # elem[0] is the column number of the configuration. the max number of columns is 4 therefore it can never be greater than 3
            if (elem[0] < 0 or elem[0] > 3):
                potential_neighbors.remove(elem)
                continue 
            # elem[1] is the column number of the configuration. the max number of rows is 3 therefore it can never be greater than 2
            if (elem[1] < 0 or elem[1] > 2):
                potential_neighbors.remove(elem)
                continue
         
        #print(blank_pos)
        #print(self.configuration)
        '''
        copy_of_config = []
        for i in range(3):
            temp = []
            for j in range(4):
                temp.append(self.configuration[i][j])
            copy_of_config.append(temp)
        '''
        # now create those states and append it to the children class
        for ptn_child in potential_neighbors:
            # create a deep-copy of the current state's configuration so you do not modify the current-state's configuration
            temp_config = copy.deepcopy(self.configuration)
            # print("THIS IS THE ELEM: ", ptn_child)

            col_1 = int(blank_pos[0]) # the current column number of the configuration is the first number in the blank_pos
            row_1 = int(blank_pos[1]) # the current row number of the configuration is the second number in the blank_pos
            col_2 = int(ptn_child[0]) # the current column number of the configuration is the first number in the blank_pos
            row_2 = int(ptn_child[1]) # the current row number of the configuration is the second number in the blank_pos
            
            
            # print("OLD TEMP CONFIG =============")
            # print(temp_config)
            # print("(" + str(x1) + "," + str(y1) + ")" + "(" + str(x2) + "," + str(y2) + ")")

            #print(x2,y2)

            # keep track of the old number of the space that will now be the blank space
            temp_old_number = temp_config[row_2][col_2]
            # put the blank space into the location
            temp_config[row_2][col_2] = '0'
            # in where the blank space used to be, put the old number 
            temp_config[row_1][col_1] = temp_old_number

            # print("NEW TEMP CONFIG =============")
            # print(temp_config)
            
            # increase the depth by 1
            temp_depth = self.depth + 1
            # incremenet the number of nodes by how many states the current node will add
            temp_num_nodes = self.num_nodes + len(potential_neighbors)
            # temporary f_value 
            temp_f_value = self.f_value

            # deep-copy the action_ls and then add what action the current child of the state will do
            temp_action_ls = copy.deepcopy(self.action_ls)
            # print(ptn_child[2])
            temp_action_ls.append(ptn_child[2])
            # print(temp_action_ls)

            # create a deep-copy of the f_value_ls
            temp_f_value_ls = copy.deepcopy(self.f_value_ls)

            # create a temporary variable the represents a potential state to expand upon 
            child = state(temp_config, self.goal_locations, self.outputObj, temp_depth, temp_num_nodes, temp_f_value, temp_action_ls, temp_f_value_ls)
            child.calculate_f() # fix the f_value of this new child then add that f_value into f_value_ls
            # child is completed with necessary information. now add this to the children list 
            children.append(child)
        '''
        print ("EXPECTED CHILDREN =================")
        for child in children:
            print(child.configuration)
        print ("EXPECTED CHILDREN =================")
        '''
        return children
    
# solves the puzzle using the A* algorithmn
class puzzle: 
    def __init__(self, initial_state = [[]], goal_state = [[]], row = 3, col = 4):
        self.row = row
        self.col = col
        self.open = []                  # open queue are the states to be expanded
        self.close = []                 # close queue are the states that have been expanded. used to track repeating states
        self.is_state = initial_state   # the initial state
        self.gl_state = goal_state      # the goal state
        self.output_file = ""
        self.input_file = ""
    # create the puzzle
    def create_puzzle(self, inputObj, outputObj):
        # create 2 3x4 2D array repreresenting the initial state, the current state, and the goal state respectively
        # each of these array show the corresponding states as the board 
        initial_state = [[0 for i in range(4)] for j in range(3)] 
        # curr_state = [[0 for i in range(4)] for j in range(3)] 
        goal_state = [[0 for i in range(4)] for j in range(3)] 
        # a list with tuples representing the coordinates of their goal location of the corressponding index
        # ex. index 0 of goal_location is the goal_state position of the blank space 
        # ex. index 1 of goal_location is the goal_state position of the number 1
        goal_locations = [(0,0) for j in range(12)] 

        # read the input file line by line to create the initial state
        input_lines = inputObj.readlines()                    
        for i in range(3):                                          
            current_numbers = input_lines[i].strip().split() # split each line by spaces to get only the numbers 
            for j in range(4):     
                initial_state[i][j] = current_numbers[j]     # create the configuration/board representation of the numbers as a 2D list 

        # read the input file line by line to create the final state
        for i in range(4,7):                                    
            current_numbers = input_lines[i].split()
            for j in range(4):
                goal_state[i-4][j] = current_numbers[j]  
                goal_locations[ int(current_numbers[j]) ] = (j,i-4)
        #curr_state = initial_state

        # create the first initial state and the goal state into the State class. 
        
        is_state = state(initial_state, goal_locations, outputObj, 0,0,0, [], [])
        is_state.calculate_f() # calculate it's f_value to begin the a*star algorithmn
        gl_state = state(goal_state, goal_locations, outputObj, 0,0,0, [], [])

        self.is_state = is_state
        self.gl_state = gl_state
        self.input_file = inputObj
        self.output_file = outputObj
        self.open = [] 
        self.close = []
    
    # print the initial and goal state and write it to the output file
    def print_states(self):
        # Write the initial state into the output_file
        for i in range(3):
            line = " ".join(self.is_state.get_row(i))
            print(line)
            self.output_file.write(line + "\n")
        # Add a blank line
        self.output_file.write("\n")
        print("\n")
        # Write the goal state into the output_file
        for i in range(3):
            line = " ".join(self.gl_state.get_row(i))
            print(line)
            self.output_file.write(line + "\n")
    # the actual a* search
    def a_star(self):
        # Put the initial state into the open list
        self.open.append(self.is_state)
        # now iterate through this list until it is empty
        while self.open:
            # take the first state in the open list 
            curr_state = self.open[0]

            #print(curr_state.configuration)

            # check if matches the goal state and exit if necessary
            if curr_state == self.gl_state:
                #curr_state.f_value_ls.append('0')
                break
            # expand the node and find the potential states to be expanded 
            pot_for_exp = curr_state.expand_node()
            '''
            print ("RECEIVED CHILDREN =================")
            for child in pot_for_exp:
                print(child.configuration)
            print ("END RECEIVED CHILDREN =================")
            '''
            # for every single possible node to be expanded in the next iteration of the while loop...
            for child_state in pot_for_exp:
                # remove it if it is a repeated state
                if(child_state in self.close):
                    pot_for_exp.remove(child_state)
                    continue
            # now add the not repeated states into the open list 
            for child_state in pot_for_exp:
                self.open.append(child_state)

            '''
            for child_state in pot_for_exp:
                
                print("END ===============")
                print(child_state.configuration)
                print("END ===============")
            '''

            # remove the curr_state from open list and add it to close list
            temp_curr_state = curr_state
            self.open.remove(curr_state)
            #del self.open[0]
            self.close.append(temp_curr_state)
            '''
            print("============================== START OPEN =======================================")
            for elem in self.open:
                print(elem.configuration)
            print("============================== END  OPEN=======================================")
            print("============================== START CLOSE =======================================")
            for elem in self.open:
                print(elem.configuration)
            print("============================== END  CLOSE =======================================")
            '''
            # this part requires you to sort through the open list so the smallest f_value is the first element
            # so sort all of the states in the the open list by the state's f_value
            self.open.sort(key=lambda state:state.f_value)
            
        # print the initial and goal states and add it to the output file 
        # then print the leftover stuff from the final state, like the depth etc.
        self.print_states()
        self.open[0].print_descriptor()



# THESE ARE WHERE TO PUT THE INPUT FILE AND THE OUTPUT FILE NAME
# TO CHANGE THE INPUT FILE, JUST REPLACE "Sample_Input.txt" WITH THE TEXT FILE NAME.
# EXAMPLE, "Sample_Input.txt" --> "Input1.txt" to make the input file Input1.txt
# REMEMBER TO INCLUDE THE QUOTATION MARKS THE .txt EXTENSION

input_file = open("Sample_Input.txt", "r")
output_file = open("Output_Solution.txt", "w+")

input_file_1 = open("Input1.txt", "r")
output_file_1 = open("Output1.txt", "w+")

input_file_2 = open("Input2.txt", "r")
output_file_2 = open("Output2.txt", "w+")

input_file_3 = open("Input3.txt", "r")
output_file_3 = open("Output3.txt", "w+")
 
# create the puzzle solver to run the A* algorithmn 
new_puzzle = puzzle()
new_puzzle.create_puzzle(input_file, output_file)
new_puzzle.a_star()
# reset the puzzle to solve Input1.txt
new_puzzle.create_puzzle(input_file_1, output_file_1)
new_puzzle.a_star()
# reset the puzzle to solve Input2.txt
new_puzzle.create_puzzle(input_file_2, output_file_2)
new_puzzle.a_star()
# reset the puzzle to solve Input3.txt
new_puzzle.create_puzzle(input_file_3, output_file_3)
new_puzzle.a_star()

# close the input file because we do not need to access it anymore
input_file.close()
input_file_1.close()
input_file_2.close()
input_file_3.close()
# close the output file as you should have the solution in the output file
output_file.close()
output_file_1.close()
output_file_2.close()
output_file_3.close()
