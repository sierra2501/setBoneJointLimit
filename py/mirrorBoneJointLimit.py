import json
from collections import OrderedDict

# ===========================================================================
def mirrorLimit(bone_dict):

    new_bone_dict = "{"

    for i in bone_dict:
        new_bone_dict = new_bone_dict + r'"%s": {"X": {"min": %f, "max": %f}, "Y": {"min": %f, "max": %f}, "Z": {"min": %f, "max": %f}},' % (i, bone_dict[i]['X']['min'], bone_dict[i]['X']['max'], bone_dict[i]['Y']['max']*(-1), bone_dict[i]['Y']['min']*(-1), bone_dict[i]['Z']['max']*(-1), bone_dict[i]['Z']['min']*(-1))

    return new_bone_dict

# ===========================================================================
# jsonファイルに保存
def saveJson(bone_dict, file_dir):

    bone_dict = bone_dict[:-1] + "}"

    dialog = xshade.create_dialog()
    file_dir = dialog.ask_path(False, "JSON/TEXT(.json .txt)|json;txt|JSON(.json)|json|TEXT(.txt)|txt")
    
    d  = json.loads(bone_dict, object_pairs_hook=OrderedDict)
    with open(file_dir, 'w') as f:
        json.dump(d, f, indent=2,encoding='utf-8')

def main():

    # ファイル・ディレクトリ
    dialog = xshade.create_dialog()
    file_dir = dialog.ask_path(True, "JSON/TEXT(.json .txt)|json;txt|JSON(.json)|json|TEXT(.txt)|txt")
    if file_dir == "":
        return
    new_file_dir = 'C:\\Users\\sierra\\Documents\\new_file.json'

    # 辞書の作成
    bone_dict = json.load(open(file_dir, 'r'))

    # ミラーリング
    new_bone_dict = mirrorLimit(bone_dict)

    # 保存
    saveJson(new_bone_dict, new_file_dir)

    print("END")

main()