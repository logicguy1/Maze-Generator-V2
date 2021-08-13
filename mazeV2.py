from PIL import Image, ImageDraw, ImageFont
import random
import time
import numpy

class Stack:
    """Stack used to keep track of backstepping"""

    def __init__(self):
        self.stack = [] # Stack used in the maze generating algarythem

    def stack_pop(self):
        item = self.stack[-1] # Get the last element in the stack
        del self.stack[-1] # Remove the last element
        return item # Return the element

    def stack_push(self, item):
        self.stack.append(item) # Add the element to the top of the stack

class Pointer:
    """docstring for Pointer."""

    def __init__(self):
        self.X = 0
        self.Y = 0

        self.stack = Stack()
        self.locations = []

    def run_check(self, grid):
        print(grid.shape[0] * grid.shape[1] / (len(self.locations) + 1))
        if grid.shape[0] * grid.shape[1] / (len(self.locations) + 1) == 1: # Check if all of the squares on the grid has been visited
            return False
        return True

    def get_free_neighbor(self, grid):
        # WSAD
        neighbors = ((self.X, self.Y-1, "1"), (self.X, self.Y+1, "2"), (self.X-1, self.Y, "3"), (self.X+1, self.Y, "4")) # All the posible neighborsat our current location

        validNeighbors = [] # Initialise a list that will keep track of the found avaliable neighbors
        for i in neighbors: # Loop over our avaliable neighbors
            try:
                item = grid[i[1]][i[0]] # Get the item at our index
            except IndexError: # If the neighbor exeeds the bounds of the grid
                continue # We discord the neighbor and continue to the next

            if i[0] < 0 or i[1] < 0 or (i[0], i[1]) in self.locations: # If the pointer is out of bounds or has been visited before
                continue

            if item == "": # If the locaiton is empty
                validNeighbors.append(i) # Add the neighbor to the list

        if len(validNeighbors) == 0: # If there are no neighbors to choose from
            try:
                item = self.stack.stack_pop() # Remove the top of the stack
            except IndexError: # If the stack is empty it cant go thruthere
                return

            self.X = item[0] # Apply the changes
            self.Y = item[1]

        else:
            chosenItem = random.choice(validNeighbors) # Choose from one of the avaliable neighbors

            grid[self.Y][self.X] += chosenItem[2] # Set the tile we moved to the direcontion

            self.X = chosenItem[0] # Apply the changes
            self.Y = chosenItem[1]

            self.stack.stack_push((self.X, self.Y)) # Add the locatin to the stack

        if (self.X, self.Y) not in self.locations:
            self.locations.append((self.X, self.Y)) # Mark the spot as visited

    def translate_grid(self, grid):
        pixelSize = 20 # Set the size of each pixel (in pixels lol)
        size = (grid.shape[1] * pixelSize * 2 - pixelSize, # Define the size of the canvas
                grid.shape[0] * pixelSize * 2 - pixelSize)

        im = Image.new('RGB', size, (200, 200, 200)) # Create image object with the size element referanced before
        draw = ImageDraw.Draw(im)

        for y in range(grid.shape[0] * 2): # Loop over the X and Y axis to create a grid that is used for the generation later
            if y % 2 == 1: # Every odd row we add a black line
                draw.rectangle( # Draw the line
                              ((0, y * pixelSize), (size[0], y * pixelSize + pixelSize)),
                              fill=(0, 0, 0)
                              )

        for x in range(grid.shape[1] * 2): # Repeat from line 83
            if x % 2 == 1:
                draw.rectangle(
                              ((x * pixelSize, 0), (x * pixelSize + pixelSize, size[1]))
                              , fill=(0, 0, 0)
                              )

        for y2 in range(grid.shape[0]): # Loop over x and y agein to create all the hallways aka modifying the grid it generated erlier
            for x2 in range(grid.shape[1]):
                item = grid[y2][x2] # Get the state of the item aka element

                y = y2 * 2 # Multiply with two because the walls of the maze takes up as much space as the hallways
                x = x2 * 2

                # print(item)

                if "1" in item: # Check if each of the statements match and create the responsible opening
                    draw.rectangle(
                                  ((x * pixelSize, y * pixelSize - pixelSize), (x * pixelSize + pixelSize, y * pixelSize))
                                  , fill=(200,200,200)
                                  )
                if "2" in item:
                    draw.rectangle(
                                  ((x * pixelSize, y * pixelSize + pixelSize), (x * pixelSize + pixelSize, y * pixelSize + pixelSize * 2))
                                  , fill=(200,200,200)
                                  )
                if "3" in item:
                    draw.rectangle(
                                  ((x * pixelSize - pixelSize, y * pixelSize), (x * pixelSize, y * pixelSize + pixelSize))
                                  , fill=(200,200,200)
                                  )
                if "4" in item:
                    draw.rectangle(
                                  ((x * pixelSize + pixelSize, y * pixelSize), (x * pixelSize + pixelSize * 2, y * pixelSize + pixelSize))
                                  , fill=(200,200,200)
                                  )

        im.save('image.png', quality=95) # Save the image

if __name__ == '__main__':
    grid = numpy.zeros((80,80), dtype = 'U100') # Create the grid area we are working with

    Pointer1 = Pointer()
    while Pointer1.run_check(grid):
        Pointer1.get_free_neighbor(grid)
        # Pointer1.translate_grid(grid)
        # time.sleep(.15)

    Pointer1.translate_grid(grid)
