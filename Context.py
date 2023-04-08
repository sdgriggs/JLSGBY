class Context:
    # Resource Counters
    food = 0
    autoIncrement = .1 #(dummy value, will be calculated in increment function)
    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 20
    ticksPerHour = 120
    ticksPerDay = 2880

    # defining colors

    white = (255, 255, 255)
    black = (0, 0, 0)

    def _handle_click_event(self, event):
        pass