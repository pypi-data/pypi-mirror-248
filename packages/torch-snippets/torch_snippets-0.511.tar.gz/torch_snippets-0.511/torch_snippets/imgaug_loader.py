# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/imgaug_loader.ipynb.

# %% auto 0
__all__ = ['do', 'bw', 'rotate', 'pad', 'get_size', 'rescale', 'crop', 'imgaugbbs2bbs', 'bbs2imgaugbbs']

# %% ../nbs/imgaug_loader.ipynb 2
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from .loader import BB, PIL, bbs2df, df2bbs, np, pd, Image
from torch_snippets.bb_utils import (
    split_bb_to_xyXY,
    combine_xyXY_to_bb,
    to_relative,
    to_absolute,
)

# %% ../nbs/imgaug_loader.ipynb 3
def do(img, bbs=None, aug=None, cval=255):
    if isinstance(img, PIL.Image.Image):
        _Image = True
        img = np.array(img)
    else:
        _Image = False
    no_bbs = False
    if bbs is None:
        no_bbs = True
        bbs = []
    H, W = img.shape[:2]
    if isinstance(bbs, pd.DataFrame):
        _df = bbs.copy()
        _separate = True if "x" in _df.columns else False
        if not _separate:
            _df = split_bb_to_xyXY(_df)
        _relative = True if _df["x"].max() < 1 else False
        if _relative:
            _df = to_absolute(_df, H, W)
        bbs = df2bbs(_df)
        remaining_columns = [c for c in _df.columns if c not in "xyXY"]
        __df = _df[remaining_columns]
        _data_frame = True
    else:
        _data_frame = False

    bbs = bbs2imgaugbbs(bbs, img)
    img, bbs = aug(images=[img], bounding_boxes=[bbs])
    img, bbs = (img[0], imgaugbbs2bbs(bbs))
    H, W = img.shape[:2]

    if _Image:
        img = Image.fromarray(img)
    if _data_frame:
        _df = bbs2df(bbs)
        __df[[*"xyXY"]] = _df.values
        if _relative:
            __df = to_relative(__df, H, W)
        if not _separate:
            __df = combine_xyXY_to_bb(__df)
        bbs = __df
    if no_bbs:
        return img
    return img, bbs


def bw(img, bbs):
    aug = iaa.Grayscale()
    return do(img, bbs, aug)


def rotate(img, bbs=None, angle=None, cval=255):
    aug = iaa.Rotate(angle, cval=cval, fit_output=True)
    return do(img, bbs=bbs, aug=aug)


def pad(img, bbs, sz=None, deltas=None, cval=0):
    if isinstance(img, np.ndarray):
        h, w = img.shape[:2]
    else:
        w, h = img.size
    if sz:
        H, W = sz
        deltas = (H - h) // 2, (W - w) // 2, (H - h) // 2, (W - w) // 2

    aug = iaa.Pad(deltas, pad_cval=cval)
    return do(img, bbs, aug)


def get_size(sz, h, w):
    if isinstance(sz, (tuple, list)) and isinstance(sz[0], str):
        signal, (H, W) = sz
        assert signal in "at-least,at-most".split(
            ","
        ), "Resize type must be one of `at-least` or `at-most`"
        if signal == "at-least":
            f = max(H / h, W / w)
        if signal == "at-most":
            f = min(H / h, W / w)
        H, W = [i * f for i in [h, w]]
    elif isinstance(sz, float):
        frac = sz
        H, W = [i * frac for i in [h, w]]
    elif isinstance(sz, int):
        H, W = sz, sz
    elif isinstance(sz, tuple):
        H, W = sz
        if H == -1:
            _, W = sz
            f = W / w
            H = f * h
        elif W == -1:
            H, _ = sz
            f = H / h
            W = f * w
        elif isinstance(H, float):
            H = H * h
        elif isinstance(W, float):
            W = W * h
    H, W = int(H), int(W)
    return H, W


def rescale(im, bbs, sz):
    if isinstance(im, PIL.Image.Image):
        to_pil = True
        im = np.array(im)
    else:
        to_pil = False
    h, w = im.shape[:2]
    H, W = get_size(sz, h, w)
    aug = iaa.Resize({"height": H, "width": W})
    im, bbs = do(im, bbs, aug)
    if to_pil:
        im = PIL.Image.fromarray(im)
    return im, bbs


def crop(img, bbs, deltas):
    aug = iaa.Crop(deltas)
    return do(img, bbs, aug)


def imgaugbbs2bbs(bbs):
    if bbs is None:
        return None
    return [
        BB([int(i) for i in (bb.x1, bb.y1, bb.x2, bb.y2)])
        for bb in bbs[0].bounding_boxes
    ]


def bbs2imgaugbbs(bbs, img):
    if bbs is None:
        return None
    return BoundingBoxesOnImage(
        [BoundingBox(x1=x, y1=y, x2=X, y2=Y) for x, y, X, Y in bbs], shape=img.shape
    )
