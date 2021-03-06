import random
import time
import _pickle as cPickle



def unique(inst, cars):
    """
    Algorithm that forces unique configurations on every turn. 
    """
    
    start=time.time()
    # Copy of the main game instance
    instance_copy = cPickle.loads(cPickle.dumps(inst, -1))

    movements = 0

    def save_board(instance_copy):
        # Saves car coordinates of current move in a dictionary
        key = movements
        step = {instance_copy.cars[car]: (
            instance_copy.cars[car].col, instance_copy.cars[car].row) for car in instance_copy.cars}

        instance_copy.version[key] = step

        return instance_copy.version
    
    def empty_saves(instance_copy):
        # Empties the saves dictionary
        instance_copy.version.clear()
        return instance_copy.version

    def check_move(instance_copy):
        # Checks if move configuration has been achieved in earlier step and returns False if this is the case
        current = {instance_copy.cars[car]: (instance_copy.cars[car].col, instance_copy.cars[car].row) for car in instance_copy.cars}

        for board in instance_copy.version:
            if instance_copy.version[board] == current:
                return False

        return True
    
    # Run loop while game not winnable
    while not instance_copy.cars["X"].row == instance_copy.win_location:

        # Select random car
        randomcar = random.choice(list(cars))

        # Check movable spaces of the car
        movementspace = instance_copy.check_space(randomcar)

        # Choose a move randomly
        randommovement = random.choice(movementspace)
        
        if instance_copy.move(randomcar, randommovement):
            # Check if move leads to a configuration that has been seen before
            if check_move(instance_copy):
                # Count movements made
                movements += 1
                # Reload board
                save_board(instance_copy)

            # If the move was valid (and therefore excecuted) but the configuration has been seen before the movement is reverted
            else:
                instance_copy.move(randomcar, (-randommovement))
            # Reload board
            empty_board = instance_copy.create_board()
            result=instance_copy.load_board(empty_board)

        # If producing a result has been tried for more than 0.1s the function is reinitated, because it's very likely that there is no new unique move to be made
        if time.time()-start > 0.3:
            start=time.time()
            empty_saves(instance_copy)
            return unique(inst, cars)
 
    instance_copy.car_output()
    empty_saves(instance_copy)
    return (movements, result)
    

    

