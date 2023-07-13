import os
import shutil
from tqdm import tqdm
from utils import create_folder


def copy_picture_as_dataset(output_folder, bacteria_dataset, path_img, df):
    create_folder(os.path.join(output_folder, bacteria_dataset))
    filtered_df = df[df["Type"] == bacteria_dataset]

    for index, row in tqdm(filtered_df.iterrows(), total=filtered_df.shape[0]):
        src = os.path.join(path_img, row.Filename + ".jpg")
        dst = os.path.join(output_folder, bacteria_dataset, row.Filename + ".jpg")

        shutil.copy(src, dst)