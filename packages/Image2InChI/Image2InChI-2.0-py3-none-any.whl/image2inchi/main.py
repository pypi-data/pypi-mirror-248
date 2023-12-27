import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from config import Config
from utils import get_logger, Tokenizer, get_transforms, TestDataset, seed_torch, Scorer, InChIQuery
from model import InCHImgAnalyzer

PARAM_PATHNAME = f'/log'

LOG = get_logger(Config.PATH.LOG_DIR + PARAM_PATHNAME + '.log')


def bms_collate(batch):
    imgs, inchi_texts = [], []
    for row in batch:
        imgs.append(row[0])
        inchi_texts.append(row[1])

    img = torch.stack(imgs)

    return img, inchi_texts


def sort_by_len_desc(img, seq, seq_lens, seq_texts):
    """
    按照seq的len进行排序
    """

    seq_lens, sorted_index = seq_lens.sort(dim=0, descending=True)
    img = img[sorted_index]
    seq = seq[sorted_index]

    texts = [None] * len(sorted_index)
    for i, j in enumerate(sorted_index.tolist()):
        texts[j] = seq_texts[i]

    return img, seq, seq_lens, texts


def get_test_data_loader(
        test_df: pd.DataFrame,
        img_dir: str) -> DataLoader:
    transforms = get_transforms()

    test_ds = TestDataset(test_df, img_dir, transforms)

    test_dl = DataLoader(
        test_ds,
        batch_size=Config.TRAIN.BATCH_SIZE,
        shuffle=False,
        num_workers=Config.TRAIN.NUM_WORKERS,
        pin_memory=True,
        drop_last=False,
        collate_fn=lambda batch: bms_collate(batch)
    )

    return test_dl


def do_valid(valid_dl, net, tokenizer):
    net.eval()

    label_texts = []
    label_text_preds = []
    for step, (img, label_text) in enumerate(valid_dl):
        img = img.to(Config.TRAIN.DEVICE)

        with torch.no_grad():
            preds = net.predict(
                img,
                Config.TRAIN.MAX_LEN,
                tokenizer.get_seq_of_sos(),
                tokenizer.get_seq_of_eos(),
                tokenizer.get_seq_of_pad()
            )

        label_text_pred = tokenizer.predict_captions(preds.detach().cpu().numpy())
        label_text_preds.append(label_text_pred)
        label_texts.append(label_text)

        if step % Config.TRAIN.PRINT_FREQ == 0 or step == (len(valid_dl) - 1):
            LOG.info(
                f'Valid: [{step + 1}/{len(valid_dl)}] '
            )

    label_texts = np.concatenate(label_texts)
    label_text_preds = np.concatenate(label_text_preds)
    label_text_preds = [InChIQuery.query(f'InChI=1S/{text}') for text in label_text_preds]

    return label_texts, label_text_preds


def init_net(net):
    net.to(Config.TRAIN.DEVICE)
    LOAD_WEIGHT_PATH = Config.PATH.LOAD_WEIGHT_PATH
    states = torch.load(Config.PATH.LOAD_WEIGHT_PATH, map_location=torch.device(Config.TRAIN.DEVICE))
    net.load_state_dict(states['net'], strict=False)
    LOG.info(f'加载权重文件: {LOAD_WEIGHT_PATH}')


def do_test(test_df, img_path, preds_save_path=None):
    seed_torch(Config.TRAIN.SEED)
    tokenizer = Tokenizer(Config.PATH.TOKEN_STOI_PICKLE)

    test_dl = get_test_data_loader(test_df, img_path)

    img, inchi_text = next(iter(test_dl))
    LOG.info(img.shape)  # torch.Size([b, 3, 224, 224])

    net = InCHImgAnalyzer(
        encoder_dim=Config.TRAIN.ENCODER_DIM,
        vocab_size=len(tokenizer),
        embed_dim=Config.TRAIN.EMBED_DIM,
        max_length=Config.TRAIN.MAX_LEN,
        num_head=Config.TRAIN.N_HEAD,
        ff_dim=Config.TRAIN.FF_DIM,
        num_layer=Config.TRAIN.NUM_LAYER
    )

    init_net(net)

    label_texts, label_text_preds = do_valid(test_dl, net, tokenizer)

    LOG.info(f"label_texts: {label_texts[:5]}")
    LOG.info(f"label_text_preds: {label_text_preds[:5]}")

    if preds_save_path:
        df_map = {
            'label_texts': label_texts,
            'label_text_preds': label_text_preds
        }
        df = pd.DataFrame(df_map)
        df.to_csv(preds_save_path)

    inchi_acc, morgan_fp, mcs, distance, lcs = Scorer.scoring(label_texts, label_text_preds)

    LOG.info(
        f'inchi_acc: {inchi_acc}, morgan_fp: {morgan_fp}, mcs: {mcs} - distance: {distance} - lcs: {lcs:.4f}')


def test_bms1000():
    print('bms1000')
    bms1000_df = pd.read_csv(Config.PATH.BMS1000_INCHI_CSV)
    preds_save_path = Config.PATH.BMS1000_DIR + '/bms1000_preds.csv'
    do_test(bms1000_df, Config.PATH.BMS1000_IMAGES_DIR, preds_save_path)


def test_jpo():
    print('jpo')
    jpo_df = pd.read_csv(Config.PATH.JPO_INCHI_CSV)
    preds_save_path = Config.PATH.JPO_DIR + '/jpo_preds.csv'
    do_test(jpo_df, Config.PATH.JPO_IMAGES_DIR, preds_save_path)


def test_clef():
    print('clef')
    jpo_df = pd.read_csv(Config.PATH.CLEF_INCHI_CSV)
    preds_save_path = Config.PATH.CLEF_DIR + '/clef_preds.csv'
    do_test(jpo_df, Config.PATH.CLEF_IMAGES_DIR, preds_save_path)


def test_uob():
    print('uob')
    jpo_df = pd.read_csv(Config.PATH.UOB_INCHI_CSV)
    preds_save_path = Config.PATH.UOB_DIR + '/uob_preds.csv'
    do_test(jpo_df, Config.PATH.UOB_IMAGES_DIR, preds_save_path)


def test_uspto():
    print('uspto')
    jpo_df = pd.read_csv(Config.PATH.USPTO_INCHI_CSV)
    preds_save_path = Config.PATH.USPTO_DIR + '/uspto_preds.csv'
    do_test(jpo_df, Config.PATH.USPTO_IMAGES_DIR, preds_save_path)


def main():
    test_bms1000()
    test_jpo()
    test_clef()
    test_uob()
    test_uspto()


if __name__ == '__main__':
    main()
