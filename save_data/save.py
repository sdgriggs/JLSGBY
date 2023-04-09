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


    print("ni")

def saveGame(context):
    fp = open(SAVE_DATA_FP, "wb")
    gerald = pickle.dump(context, fp)
    fp.close()