import argparse
import os

import exifread
import pandas as pd
from imutils import paths
from tqdm import tqdm

from dataset_creation import copy_picture_as_dataset
from plots import graphic_nb_photos_by_matrix, graphic_nb_samples_by_matrix
from utils import tag2dict, dictionary_2_df_format, fill_in_nb_colony_through_title, identify_bacteria_matrix, \
    get_only_filename

path_img = r"A:\02-FOOD\02-Microbio RN"


def get_exif_data(path_dataset: str) -> pd.DataFrame:
    filenames = []
    authors = []
    exp_times = []
    lightings = []
    img_formats = []
    colony_numbers = []

    # Iterate through pictures
    for img_path in tqdm(list(paths.list_images(path_dataset))):
        filename = img_path.split("/")[-1]

        f = open(img_path, 'rb')
        tags = exifread.process_file(f)
        user_comment = tag2dict(tags["EXIF UserComment"])
        user_comment = dictionary_2_df_format(user_comment)

        filenames.append(filename)
        authors.append(tags["Image Artist"])
        exp_times.append(tags["EXIF ExposureTime"])
        lightings.append(", ".join(user_comment["lights"]))
        img_formats.append(", ".join(user_comment["image format"]))
        colony_numbers.append(user_comment["colony_nb"])

    return pd.DataFrame(data={
        "Filename": filenames,
        "Author": authors,
        "Exposure time(s)": exp_times,
        "Lighting [B, D, UV]": lightings,
        "Image format": img_formats,
        "Colony number": colony_numbers}).reset_index(drop=True)

parser = argparse.ArgumentParser(
                    prog='ServerAnalyzer4Microbio_RN',
                    description="The program analyses pictures sent into one server's folder.",
                    epilog='--- SGS France - Operational Excellence ---')
parser.add_argument("-xl", "--excel", type=str, help="Path of excel help file")
parser.add_argument("-b", "--bacteria_matrix", type=str, help="Bacteria matrix used to create a new dataset. User has "
                                                              "the choice between BL, GT and E.")
parser.add_argument('-csv', '--export_csv', action='store_true', help="Create csv file which sums up")
parser.add_argument('-visu', '--visualisation', action='store_true', help="Pass this argument if you want to visualize "
                                                                          "data")

args = parser.parse_args()

excel_help_file = args.excel

export_csv = args.export_csv
visualisation = args.visualisation

output_folder = "Output"

bacteria_dataset = args.bacteria_matrix

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("[INFO] Getting picture's metadata ...")
    df = get_exif_data(path_dataset=path_img)
    print("[SUCCESS] Picture's metadata retrieved ...")

    df.Filename = df.Filename.apply(get_only_filename)

    # Get non counted colony in DataFrame
    df = fill_in_nb_colony_through_title(df)

    df = identify_bacteria_matrix(df, excel_help_file)

    if export_csv:
        df.to_csv("visu_RN_microbio.csv")

    if visualisation:
        graphic_nb_photos_by_matrix(df)
        graphic_nb_samples_by_matrix(df)

    if bacteria_dataset in df.Type.value_counts().index.tolist():
        print("[INFO] Dataset creation ...")
        copy_picture_as_dataset(output_folder, bacteria_dataset, path_img, df)

    else:
        print("[ERROR] Bacteria matrix abbreviation does not exist un this dataset")
