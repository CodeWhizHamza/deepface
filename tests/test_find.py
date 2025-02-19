import cv2
import pandas as pd
from deepface import DeepFace
from deepface.commons import distance
from deepface.commons.logger import Logger

logger = Logger("tests/test_find.py")


def test_find_with_exact_path():
    img_path = "dataset/img1.jpg"
    dfs = DeepFace.find(img_path=img_path, db_path="dataset", silent=True)
    assert len(dfs) > 0
    for df in dfs:
        assert isinstance(df, pd.DataFrame)

        # one is img1.jpg itself
        identity_df = df[df["identity"] == img_path]
        assert identity_df.shape[0] > 0

        # validate reproducability
        assert identity_df["VGG-Face_cosine"].values[0] == 0

        df = df[df["identity"] != img_path]
        logger.debug(df.head())
        assert df.shape[0] > 0
    logger.info("✅ test find for exact path done")


def test_find_with_array_input():
    img_path = "dataset/img1.jpg"
    img1 = cv2.imread(img_path)
    dfs = DeepFace.find(img1, db_path="dataset", silent=True)
    assert len(dfs) > 0
    for df in dfs:
        assert isinstance(df, pd.DataFrame)

        # one is img1.jpg itself
        identity_df = df[df["identity"] == img_path]
        assert identity_df.shape[0] > 0

        # validate reproducability
        assert identity_df["VGG-Face_cosine"].values[0] == 0

        df = df[df["identity"] != img_path]
        logger.debug(df.head())
        assert df.shape[0] > 0

    logger.info("✅ test find for array input done")


def test_find_with_extracted_faces():
    img_path = "dataset/img1.jpg"
    face_objs = DeepFace.extract_faces(img_path)
    img = face_objs[0]["face"]
    dfs = DeepFace.find(img, db_path="dataset", detector_backend="skip", silent=True)
    assert len(dfs) > 0
    for df in dfs:
        assert isinstance(df, pd.DataFrame)

        # one is img1.jpg itself
        identity_df = df[df["identity"] == img_path]
        assert identity_df.shape[0] > 0

        # validate reproducability
        assert identity_df["VGG-Face_cosine"].values[0] < (
            distance.findThreshold(model_name="VGG-Face", distance_metric="cosine")
        )

        df = df[df["identity"] != img_path]
        logger.debug(df.head())
        assert df.shape[0] > 0
    logger.info("✅ test find for extracted face input done")
