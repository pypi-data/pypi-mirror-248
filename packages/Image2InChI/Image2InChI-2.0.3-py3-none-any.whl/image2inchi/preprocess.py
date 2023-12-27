import cv2
import pandas as pd
from tqdm.auto import tqdm
from config import Config
import os
from rdkit import Chem

tqdm.pandas()


def read_sdf_or_mol(filepath):
    # 读取单个sdf文件方式一
    m1 = Chem.MolFromMolFile(filepath)  # 这个可以读取mol文件的,但是也可以读取单个sdf文件。
    inchi = Chem.inchi.MolToInchi(m1)

    return inchi


def preprocess(label_dir):
    df = pd.DataFrame()

    image_id_list = []
    InChI_list = []
    img_path_list = []

    for file in os.listdir(label_dir):
        filepath = label_dir + '/' + file
        try:
            inchi = read_sdf_or_mol(filepath)
            if inchi:
                image_id = file.split('.')[0]
                img_path = f'/{image_id}.png'

                image_id_list.append(image_id)
                InChI_list.append(inchi)
                img_path_list.append(img_path)

        except Exception as e:
            print(f'失败filepath: {filepath}')

    df['image_id'] = image_id_list
    df['InChI'] = InChI_list
    df['img_path'] = img_path_list

    return df


def get_inchi_count(dir):
    right = 0
    err = 0

    for file in os.listdir(dir):
        filepath = dir + '/' + file
        try:
            inchi = read_sdf_or_mol(filepath)
            if inchi:
                right += 1
            else:
                err += 1

        except Exception as e:
            print(f'失败filepath: {filepath}')

    return right + err, right, err


def print_all_inchi_count():
    clef_total, clef_right, clef_err = get_inchi_count(Config.PATH.CLEF_LABELS_DIR)
    jpo_total, jpo_right, jpo_err = get_inchi_count(Config.PATH.JPO_LABELS_DIR)
    uob_total, uob_right, uob_err = get_inchi_count(Config.PATH.UOB_LABELS_DIR)
    uspto_total, uspto_right, uspto_err = get_inchi_count(Config.PATH.USPTO_LABELS_DIR)

    print('clef')
    print(f'total: {clef_total}, right: {clef_right}, err: {clef_err}')
    print('jpo')
    print(f'total: {jpo_total}, right: {jpo_right}, err: {jpo_err}')
    print('uob')
    print(f'total: {uob_total}, right: {uob_right}, err: {uob_err}')
    print('uspto')
    print(f'total: {uspto_total}, right: {uspto_right}, err: {uspto_err}')

    """
    clef
    total: 977, right: 891, err: 86

    jpo
    total: 449, right: 449, err: 0

    uob
    total: 5740, right: 5740, err: 0

    uspto
    total: 5704, right: 5704, err: 0
    """


def preprocess_clef():
    df = preprocess(Config.PATH.CLEF_LABELS_DIR)
    df.to_csv(Config.PATH.CLEF_INCHI_CSV)


def preprocess_jpo():
    df = preprocess(Config.PATH.JPO_LABELS_DIR)
    df.to_csv(Config.PATH.JPO_INCHI_CSV)


def preprocess_uob():
    df = preprocess(Config.PATH.UOB_LABELS_DIR)
    df.to_csv(Config.PATH.UOB_INCHI_CSV)


def preprocess_uspto():
    df = preprocess(Config.PATH.USPTO_LABELS_DIR)
    df.to_csv(Config.PATH.USPTO_INCHI_CSV)


def preprocess_dataset():
    preprocess_clef()
    preprocess_jpo()
    preprocess_uob()
    preprocess_uspto()


def valid_img_exists(img_path_sr: pd.Series, img_dir: str):
    for img_path in img_path_sr:
        img_full_path = img_dir + img_path
        img = cv2.imread(img_full_path)

        if img is None:
            print(f'图片不存在: {img_full_path}')


def valid_dataset():
    bms1000_df = pd.read_csv(Config.PATH.BMS1000_INCHI_CSV)
    clef_df = pd.read_csv(Config.PATH.CLEF_INCHI_CSV)
    jpo_df = pd.read_csv(Config.PATH.JPO_INCHI_CSV)
    uob_df = pd.read_csv(Config.PATH.UOB_INCHI_CSV)
    uspto_df = pd.read_csv(Config.PATH.USPTO_INCHI_CSV)

    valid_img_exists(bms1000_df['img_path'], Config.PATH.BMS1000_IMAGES_DIR)
    valid_img_exists(clef_df['img_path'], Config.PATH.CLEF_IMAGES_DIR)
    valid_img_exists(jpo_df['img_path'], Config.PATH.JPO_IMAGES_DIR)
    valid_img_exists(uob_df['img_path'], Config.PATH.UOB_IMAGES_DIR)
    valid_img_exists(uspto_df['img_path'], Config.PATH.USPTO_IMAGES_DIR)


def main():
    valid_dataset()


if __name__ == '__main__':
    main()
