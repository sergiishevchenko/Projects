"""
Zombie Apocalypse
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Apocalypse
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        __init__
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
    
    def clear(self):
        """
        clear
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        add_zombie
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        num_zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        zombies
        """
        for zombies in self._zombie_list:
        # replace with an actual generator
            yield zombies

    def add_human(self, row, col):
        """
        add_human
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        num_humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        humans
        """
        for human in self._human_list:
            yield human
        
        
    def compute_distance_field(self, entity_type):
        """
        compute_distance_field
        """
        grid_height = poc_grid.Grid.get_grid_height(self)
        grid_width  = poc_grid.Grid.get_grid_width(self)
        
        visited = [[EMPTY for dummy_col in range(grid_width)] 
                       for dummy_row in range(grid_height)]
        
        distance_field = []
        for dummy_row in range(grid_height):
            temp_row = []
            for dummy_col in range(grid_width):
                temp_row.append(grid_height*grid_width)
            distance_field.append(temp_row)
        
        boundary = poc_queue.Queue()
        
        if entity_type == ZOMBIE:
            for items in self._zombie_list:
                boundary.enqueue(items)
                visited[items[0]][items[1]] = FULL
                distance_field[items[0]][items[1]] = 0
        elif entity_type == HUMAN:
            for items in self._human_list:
                boundary.enqueue(items)
                visited[items[0]][items[1]] = FULL
                distance_field[items[0]][items[1]] = 0
        
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            for neighbor_cell in poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1]):
                if visited[neighbor_cell[0]][neighbor_cell[1]] == EMPTY \
                and poc_grid.Grid.is_empty (self, neighbor_cell[0], neighbor_cell[1]):
                    visited[neighbor_cell[0]][neighbor_cell[1]] = FULL
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] \
                        = distance_field[current_cell[0]][current_cell[1]] + 1
        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        move_humans
        """
        for dummy_idx, human in enumerate(self._human_list):
            max_dist = zombie_distance_field[human[0]][human[1]]
            for neighbor in poc_grid.Grid.eight_neighbors(self, human[0], human[1]):
                if poc_grid.Grid.is_empty (self, neighbor[0], neighbor[1]) \
                and zombie_distance_field[neighbor[0]][neighbor[1]] > max_dist:
                    self._human_list[dummy_idx] = neighbor
                    print neighbor, human
                    max_dist = zombie_distance_field[neighbor[0]][neighbor[1]] 
        
    
    def move_zombies(self, human_distance_field):
        """
        move_zombies
        """
        for dummy_idx, zombies in enumerate(self._zombie_list):
            min_dist = human_distance_field[zombies[0]][zombies[1]]
            for neighbor in poc_grid.Grid.four_neighbors(self, zombies[0], zombies[1]):
                if poc_grid.Grid.is_empty (self, neighbor[0], neighbor[1]) \
                and human_distance_field[neighbor[0]][neighbor[1]] < min_dist:
                    self._zombie_list[dummy_idx] = neighbor
                    min_dist = human_distance_field[neighbor[0]][neighbor[1]] 


poc_zombie_gui.run_gui(Apocalypse(30, 40))
