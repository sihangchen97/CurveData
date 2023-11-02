def array_get_index(array, v, add=False):
    if v in array:
        return array.index(v)
    if add:
        array.append(v)
        return len(array)-1
    return -1

def str2float(v):
    try:
        return float(v)
    except:
        try:
            return float(int(v))
        except:
            return 0.0

def in_maya():
    try:
        import maya.mel as mel
        import maya.cmds as mc
    except:
        return False
    return True