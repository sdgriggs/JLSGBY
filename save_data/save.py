import pickle
import Context

SAVE_DATA_FP = "save_data/save.data"

def getSaveData():
    try:
        fp = open(SAVE_DATA_FP, "rb")
        obj = pickle.load(fp)
        fp.close()
        return obj
    except Exception:
        return None

def saveGame(context):
    fp = open(SAVE_DATA_FP, "wb")
    context.sold_plants = True
    pickle.dump(context, fp)
    fp.close()