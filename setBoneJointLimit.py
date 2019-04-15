import json
from collections import OrderedDict

BONE_OBJ = "{"

FILE_DIR = ""
USER_NAME = "sierra"
FILE_NAME = "file.json"

FLAG = "GET" # or GET

# ============================ GET用 ========================================
# アクティブのボーンの制限値を追記
def stockStr():
    global BONE_OBJ
    rom_x = xshade.scene().active_shape().bone_joint.get_limit(0) 
    rom_y = xshade.scene().active_shape().bone_joint.get_limit(1)
    rom_z = xshade.scene().active_shape().bone_joint.get_limit(2)
    bone_name = xshade.scene().active_shape().name
    
    BONE_OBJ = BONE_OBJ + r'"%s": {"X": {"min": %f, "max": %f}, "Y": {"min": %f, "max": %f}, "Z": {"min": %f, "max": %f}},' % (bone_name, rom_x[0]*180, rom_x[1]*180, rom_y[0]*180, rom_y[1]*180, rom_z[0]*180, rom_z[1]*180)

# jsonファイルに保存
def saveJson():

    global BONE_OBJ
    global FILE_DIR

    BONE_OBJ = BONE_OBJ[:-1] + "}"

    d  = json.loads(BONE_OBJ, object_pairs_hook=OrderedDict)
    with open(FILE_DIR, 'w') as f:
      json.dump(d, f, indent=2,encoding='utf-8')


# ============================ SET用 ========================================
# アクティブのボーンが"d"の中にあれば制限値を設定、なければスキップ
def setLimit(bone_name, d):


    if bone_name in d:
        xshade.scene().active_shape().bone_joint.set_limit(0, [d[bone_name]['X']['min']/180.0, d[bone_name]['X']['max']/180.0])
        xshade.scene().active_shape().bone_joint.set_limit(1, [d[bone_name]['Y']['min']/180.0, d[bone_name]['Y']['max']/180.0])
        xshade.scene().active_shape().bone_joint.set_limit(2, [d[bone_name]['Z']['min']/180.0, d[bone_name]['Z']['max']/180.0])
    else: 
        print 'Skip : ' + bone_name


# ===========================================================================
# ノードを浮上する
def risingNode(name):

    while(1):

        # 次の形状があるか
        if xshade.scene().active_shape().has_bro == True:
            xshade.scene().active_shape().bro.select()
            flag = False
            break

        # root_nameに戻った
        elif xshade.scene().active_shape().dad.name == name:
            flag = True
            break
        
        # 親の形状しかない
        else:
            xshade.scene().active_shape().dad.select()

    return flag


# ===========================================================================
def main():
    
    global FLAG
    global BONE_OBJ
    global FILE_DIR


    FILE_DIR = 'C:\\Users\\' + USER_NAME + "\\Documents\\" + FILE_NAME

    if FLAG == "SET":
        d = json.load(open(FILE_DIR, 'r'))

    # 初期設定
    root_name = xshade.scene().active_shape().name
    root_flag = False

    while(1):

        # rootまで戻った
        if root_flag == True:
            print "END"
            break
        else:
            if FLAG == "SET":
                setLimit(xshade.scene().active_shape().name, d)
            elif FLAG == "GET":
                stockStr()

        # 番兵まで到達したら浮上する
        if xshade.scene().active_shape().son.bro.name == "Sentinel":
            root_flag = risingNode(root_name)

        # 潜水する
        else:
            xshade.scene().active_shape().son.bro.select()
    
    if FLAG == "GET":
        saveJson()

main()