import copy

class state:
    def __init__(self, configuration, goal_locations, depth = 0, num_nodes = 0, f_value = 0, action_ls = [], f_value_ls = []): 
        self.configuration = configuration
        self.goal_locations = goal_locations
        self.depth = depth
        self.f_value = f_value
        self.depth = depth
        self.num_nodes = num_nodes
        self.action_ls = action_ls
        self.f_value_ls = f_value_ls 
    def __eq__(self, other):
        for i in range(3):
            for j in range(4):
                if (self.configuration[i][j] != other.configuration[i][j]):
                    return False
        return True 
    def get_row(self, number):
        return self.configuration[number]
    def print_descriptor(self):
        print ("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")
        output_file.write("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")

        # print(self.action_ls)
        # print(self.f_value_ls)
        print(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
        output_file.write(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
    def print_node(self):
        for i in range(3):
            line = " ".join(self.configuration[i])
            print(line + "\n")
            output_file.write(line + "\n")

        print ("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")
        output_file.write("\n" + str(self.depth) + "\n" + str(self.num_nodes) + "\n")

        print(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
        output_file.write(" ".join(self.action_ls) + "\n" + " ".join(self.f_value_ls) + "\n")
    def find_pos(self, number):
        for i in range(3):
            for j in range(4):
                if (self.configuration[i][j] == number):
                    return (i,j)
        return(-1,-1)

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
                h_value += self.manhattan_distance(j, i, goal_location[1], goal_location[0])
        
        #print("H_VALUE IS: " + str(h_value))
        return h_value

    def manhattan_distance(self, x1,y1, x2, y2):
        return abs(x1 - x2) + abs(y1- y2)

    def calculate_f(self):
        # print("f(x) = g(x) + h(x)")
        # print(str(self.depth + self.heuristic()) + " = " + str(self.depth) + " + " + str(self.heuristic()))

        self.f_value = self.depth + self.heuristic()
        self.f_value_ls.append(str(self.f_value))
        

    def expand_node(self):
        # this will continue a list of states that are potential candidates for expansion from A* search 
        children = []          

        # find the position of the blank space in the current state
        blank_pos = self.find_pos(str(0))
        # potential spots that the blank space can swap to/move to
        potential_neighbors = []
        potential_neighbors.extend([
            (blank_pos[0],blank_pos[1] + 1, "R"),
            (blank_pos[0],blank_pos[1] - 1, "L"),
            (blank_pos[0] - 1,blank_pos[1], "U"),
            (blank_pos[0] + 1,blank_pos[1], "D")]   
        )
        # remove the elements in potential_neighers that put the blank space outside of the board
        for elem in potential_neighbors:
            if (elem[0] < 0 or elem[0] > 2):
                potential_neighbors.remove(elem)
                continue 
            if (elem[1] < 0 or elem[1] > 3):
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
        copy_of_config = copy.deepcopy(self.configuration)
        # now create those states and append it to the children class
        for ptn_child in potential_neighbors:
            temp_config = copy.deepcopy(copy_of_config)
            # print("THIS IS THE ELEM: ", ptn_child)

            x1 = int(blank_pos[0])
            y1 = int(blank_pos[1])
            x2 = int(ptn_child[0])
            y2 = int(ptn_child[1])
            
            
            # print("OLD TEMP CONFIG =============")
            # print(temp_config)
            # print("(" + str(x1) + "," + str(y1) + ")" + "(" + str(x2) + "," + str(y2) + ")")
            temp_old_number = temp_config[x2][y2]
            temp_config[x2][y2] = '0'
            temp_config[x1][y1] = temp_old_number

            # print("NEW TEMP CONFIG =============")
            # print(temp_config)
            

            temp_depth = self.depth + 1
            temp_num_nodes = self.num_nodes + len(potential_neighbors)
            temp_f_value = self.f_value

            temp_action_ls = copy.deepcopy(self.action_ls)
            # print(ptn_child[2])
            temp_action_ls.append(ptn_child[2])
            # print(temp_action_ls)

            temp_f_value_ls = copy.deepcopy(self.f_value_ls)

            # create a temporary variable the represents a potential state to expand upon 
            child = state(temp_config, self.goal_locations, temp_depth, temp_num_nodes, temp_f_value, temp_action_ls, temp_f_value_ls)
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
    
    
        

        
class puzzle: 
    def __init__(self, initial_state, goal_state, row = 3, col = 4):
        self.row = row
        self.col = col
        self.open = []
        self.close = []
        self.is_state = initial_state
        self.gl_state = goal_state
    def print_states(self):
        # Write the initial state into the output_file
        for i in range(3):
            line = " ".join(self.is_state.get_row(i))
            print(line)
            output_file.write(line + "\n")
        # Add a blank line
        output_file.write("\n")
        print("\n")
        # Write the goal state into the output_file
        for i in range(3):
            line = " ".join(self.gl_state.get_row(i))
            print(line)
            output_file.write(line + "\n")
    def a_star(self):
        # Put the initial state into the open list/queue
        self.open.append(is_state)
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
            for child_state in pot_for_exp:
                # remove it if it is a repeated state
                if(child_state in self.close):
                    pot_for_exp.remove(child_state)
                    continue
            # now add the not repeated into the open list 
            for child_state in pot_for_exp:
                self.open.append(child_state)
            
            for child_state in pot_for_exp:
                '''
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
            self.open.sort(key=lambda state:state.f_value)
            
            
        self.print_states()
        self.open[0].print_descriptor()

input_file = open("Sample_Input.txt", "r")
output_file = open("Output_Solution.txt", "w+")
 
# create 3 3x4 2D array repreresenting the initial state, the current state, and the goal state respectively
# each of these array show the corresponding states as the board 
initial_state = [[0 for i in range(4)] for j in range(3)] 
# curr_state = [[0 for i in range(4)] for j in range(3)] 
goal_state = [[0 for i in range(4)] for j in range(3)] 
# a list with tuples representing the coordinates of their goal location of the corressponding index
# ex. index 0 of goal_location is the goal_state position of the blank space 
# ex. index 1 of goal_location is the goal_state position of the number 1
goal_locations = [(0,0) for j in range(12)] 

# read the input file line by line to create the initial state
input_lines = input_file.readlines()                    
for i in range(3):                                          
    current_numbers = input_lines[i].strip().split() # split each line by spaces to get only the numbers 
    for j in range(4):     
        initial_state[i][j] = current_numbers[j]     # create the configuration/board representation of the numbers as a 2D list 

# read the input file line by line to create the final state
for i in range(4,7):                                    
    current_numbers = input_lines[i].split()
    for j in range(4):
        goal_state[i-4][j] = current_numbers[j]  
        goal_locations[ int(current_numbers[j]) ] = (i-4,j)
#curr_state = initial_state

# close the input file because we do not need to access it anymore
input_file.close()

# create the first initial state and the goal state into the State class. 
is_state = state(initial_state, goal_locations, 0,0, [], [])
is_state.calculate_f()
gl_state = state(goal_state, goal_locations, 0,0, [], [])

# create the puzzle solver to run the A* algorithmn 
new_puzzle = puzzle(is_state, gl_state, 3,4)
new_puzzle.a_star()



output_file.close()