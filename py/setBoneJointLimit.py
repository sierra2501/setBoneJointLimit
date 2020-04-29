import json
from collections import OrderedDict


# ============================ SET用 ========================================
# アクティブのボーンが"d"の中にあれば制限値を設定、なければスキップ
def setLimit(bone_name, bone_dict):

    if bone_name in bone_dict:
        xshade.scene().active_shape().bone_joint.set_limit(0, [bone_dict[bone_name]['X']['min']/180.0, bone_dict[bone_name]['X']['max']/180.0])
        xshade.scene().active_shape().bone_joint.set_limit(1, [bone_dict[bone_name]['Y']['min']/180.0, bone_dict[bone_name]['Y']['max']/180.0])
        xshade.scene().active_shape().bone_joint.set_limit(2, [bone_dict[bone_name]['Z']['min']/180.0, bone_dict[bone_name]['Z']['max']/180.0])
    else: 
        print 'Skip : ' + bone_name


# ============================ GET用 ========================================
# アクティブのボーンの制限値を追記
def getLimit(bone_dict):

    rom_x = xshade.scene().active_shape().bone_joint.get_limit(0) 
    rom_y = xshade.scene().active_shape().bone_joint.get_limit(1)
    rom_z = xshade.scene().active_shape().bone_joint.get_limit(2)
    bone_name = xshade.scene().active_shape().name
    
    return bone_dict + r'"%s": {"X": {"min": %f, "max": %f}, "Y": {"min": %f, "max": %f}, "Z": {"min": %f, "max": %f}},' % (bone_name, rom_x[0]*180, rom_x[1]*180, rom_y[0]*180, rom_y[1]*180, rom_z[0]*180, rom_z[1]*180)


# ===========================================================================
# jsonファイルに保存
def saveJson(bone_dict):

    bone_dict = bone_dict[:-1] + "}"

    dialog = xshade.create_dialog()
    file_dir = str(dialog.ask_path(False, "JSON/TEXT(.json .txt)|json;txt|JSON(.json)|json|TEXT(.txt)|txt")).decode('utf-8')

    if file_dir == None:
        file_dir = ""
    d  = json.loads(bone_dict, object_pairs_hook=OrderedDict)
    with open(file_dir, 'w') as f:
        json.dump(d, f, indent=2,encoding='utf-8')


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
    
    mode = TARGET_MODE # SET or GET

    # ファイル・ディレクトリ
    if mode == "SET":
        dialog = xshade.create_dialog()
        file_dir = str(dialog.ask_path(True, "JSON/TEXT(.json .txt)|json;txt|JSON(.json)|json|TEXT(.txt)|txt")).decode('utf-8')
        if file_dir == "":
            return

    # 辞書の作成
    if mode == "SET":
        bone_dict = json.load(open(file_dir, 'r'))
    elif mode == "GET":
        bone_dict = "{"

    # 初期設定
    root_name = xshade.scene().active_shape().name
    root_flag = False

    # 末端を選択した
    if xshade.scene().active_shape().son.bro.name == "Sentinel":
        if mode == "SET":
            setLimit(xshade.scene().active_shape().name, bone_dict)
        elif mode == "GET":
            bone_dict = getLimit(bone_dict)
        root_flag = True

    while(1):

        # rootまで戻った
        if root_flag == True:

            # 保存
            if mode == "GET":
                saveJson(bone_dict)

            print "END"
            break
        else:
            if mode == "SET":
                setLimit(xshade.scene().active_shape().name, bone_dict)
            elif mode == "GET":
                bone_dict = getLimit(bone_dict)

        # 番兵まで到達したら浮上するi
        if xshade.scene().active_shape().son.bro.name == "Sentinel":
            root_flag = risingNode(root_name)

        # 潜水する
        else:
            xshade.scene().active_shape().son.bro.select()
    

main()