
import math

class Crop:
    def __init__(self):
        self.name = "Parent crop."
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = 10       # Dummy value.
        self.safeUvLevels = {"High": False, "Moderate": False, "Low":False}          # Dummy value.
        self.sellValue = 0              # Dummy value.
        self.buyValue = 0      # Dummy value.
        self.foodPerHourPerPlant = 0        # Dummy value

    # Increases the number of plants of this crop by one. It is the implementing function's responsibility to check that there are sufficient funds.
    def addPlant(self):
        self.quantity += 1
        # Possibly increase price per plant on purchase?

    # Decreases the number of plants, if possible. Returns true on a success and false on a failure.
    def sellPlant(self):
        if self.quantity >= 1:
            self.quantity -= 1
            return True
        else:
            return False
    
    # Returns the total food value generated by this plant per tick.
    def getFoodPerTick(self, temp, uvLevel):
        valuePercent = 1.0

        if temp < self.minGoodTemp:
            valuePercent -= .5
        
        if not self.safeUvLevels[uvLevel]:
            valuePercent -= .5

        return self.quantity * self.foodPerHourPerPlant * valuePercent / Context.ticksPerHour
    
    # Returns a brief string description for the crop.
    def getDescription(self):
        uvTolerance = ""
        if self.safeUvLevels["High"]:
            uvTolerance += "High"
        elif self.safeUvLevels["Moderate"]:
            uvTolerance += "Moderate"
        elif self.safeUvLevels["Low"]:
            uvTolerance += "Low"

        return f"{self.name} (Cost: {self.pricePerPlant}):\n\Minimum Temperature: {self.minGoodTemp}\nUV Tolerance: {uvTolerance}"
    
class generic(Crop):

    def __init__(self):
        self.name = "Generic Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"High": False, "Moderate": True, "Low":True}     
        self.sellValue = 10              
        self.buyValue = 20     
        self.foodPerHourPerPlant = 5        


class uvResistant(Crop):

    def __init__(self):
        self.name = "UV Resistant Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"High": True, "Moderate": True, "Low":True}     
        self.sellValue = 15             
        self.buyValue = 25     
        self.foodPerHourPerPlant = 3.5        

class coldResistant(Crop):

    def __init__(self):
        self.name = "Cold Resistant Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -90      
        self.safeUvLevels = {"High": False, "Moderate": True, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 25     
        self.foodPerHourPerPlant = 2        

class hybrid(Crop):

    def __init__(self):
        self.name = "UV Resistant, Weak to Cold"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -30      
        self.safeUvLevels = {"High": True, "Moderate": True, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 6.5        

class cashcow(Crop):

    def __init__(self):
        self.name = "Cash cow"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -10      
        self.safeUvLevels = {"High": False, "Moderate": False, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 25     

class Context:
    # Resource Counters
    food = 50

    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 2
    ticksPerHour = 120
    ticksPerDay = 2880
    minuteIncrement = 10

    minPerHour = 60
    hourPerSol = 24
    solPerYear = 668   

    # defining colors

    white = (255, 255, 255)
    black = (0, 0, 0)


    # define click regions
    click_regions = []


   
    current_env = {'temp': 0, 'pressure': 0, 'uv': 'Low', 'sunrise': 540, 'sunset': 1440}

    def get_temp(self):
        return self.current_env['temp']
    
    def get_pressure(self):
        return self.current_env['pressure']
    
    def get_uv(self):
        return self.current_env['uv']
    
    def get_sunrise(self):
        return self._format_time(self.current_env['sunrise'])
         
    
    def get_sunset(self):
        return self._format_time(self.current_env['sunset'])


    def _format_time(self, min_since_midnight):
        hr = str(math.floor(min_since_midnight / 60))
        min = str(math.floor(min_since_midnight % 60))
        if len(hr) < 2:
            hr = '0' + hr
        if len(min) < 2:
            min = '0' + min
        return hr + ":" + min
    

    # define crop type objects. store as a list for easy iteration
    crops = [
        generic(),
        coldResistant(),
        uvResistant(),
        hybrid(),
        cashcow()
    ]

    cropDict = {}

    for crop in crops:
        cropDict.update({crop.name: crop})

    def doTickUpdate(self):
        gainedFood = 0
        for crop in self.crops:
            gainedFood += crop.getFoodPerTick(self.current_env['temp'], self.current_env['uv'])

        self.food += gainedFood


    def _handle_click_event(self, event, mouse):

        for region in self.click_regions:
            #print(region['desc'])
            #print(region['x'] <= mouse[0] <= region['x'] + region['width'])
            #print(region['y'] <= mouse[0] <= region['y'] + region['height'])
            if region['x'] <= mouse[0] <= region['x'] + region['width'] and region['y'] <= mouse[1] <= region['y'] + region['height']:

                command = region['desc'].split('-')

                crop = self.cropDict[command[0]]

                if command[1] == "sell":
                    if crop.sellPlant():
                        self.food += crop.sellValue

                elif command[1] == "buy":
                    if self.food >= crop.buyValue:
                        crop.addPlant()
                        self.food -= crop.buyValue

                else:
                    print(command[1])

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):
        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})