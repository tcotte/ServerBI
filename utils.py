import os
import re
from string import digits

import numpy as np
import typing

import pandas as pd


def tag2dict(tag):
    d = {}
    tag = str(tag)
    tag_list = tag.strip().split("###")[1:]

    for index, value in enumerate(tag_list):
        if index % 2 == 0:
            key = value.lower().strip()
        else:
            d[key] = value
    return d


def dictionary_2_df_format(d):
    if "lights" in d.keys():
        d["lights"] = list(map(str, re.findall(r'\d+', d["lights"])))

    if "image format" in d.keys():
        d["image format"] = list(map(str, re.findall(r'\d+', d["image format"])))

    if "user comment" in d.keys():
        d["colony_nb"] = int(re.search(r'\d+', d["user comment"]).group())
        d.pop("user comment")
    else:
        d["colony_nb"] = np.nan

    return d


def get_only_filename(x: str) -> str:
    """
    Transform image path to image filename without extension
    :param x: image path
    """
    _, x = os.path.split(x)
    return x.replace(".jpg", "")


def search_colony(split_name: typing.Union[str, typing.List]) -> typing.Union[str, None]:
    colony_strings = ["colonie", "colonies"]
    for i in colony_strings:
        if i in split_name:
            return i
    return None


def fill_in_nb_colony_through_title(df: pd.DataFrame) -> pd.DataFrame:
    # filter dataframe with "no colony number" as filter
    non_counted_colonies_df = df[df["Colony number"].isnull()]

    # Retrieve colony number through title
    for index, row in non_counted_colonies_df.iterrows():
        count = 1
        name = row.Filename
        splitted_name = name.split(" ")
        splitted_name = [x.lower() for x in splitted_name]

        colony_string = search_colony(split_name=splitted_name)
        if colony_string is not None:
            index_colonies = splitted_name.index(colony_string)

            count = splitted_name[index_colonies - 1]
            if not isinstance(count, int):
                count = count.split("_")[-1]

        # And write retrieved values in filtered DataFrame
        non_counted_colonies_df["Colony number"][index] = count

    # Fill in original DataFrame with retrieved values
    for index, row in non_counted_colonies_df.iterrows():
        df["Colony number"][index] = row["Colony number"]

    return df


def identify_bacteria_matrix(df: pd.DataFrame, excel_help_file: typing.Union[str, None]) -> pd.DataFrame:
    remove_digits = str.maketrans('', '', digits)

    df['Type'] = pd.Series(dtype='str')

    for index, row in df.iterrows():
        name = row.Filename

        splitted_name = name.replace(" ", "_").split("_")
        splitted_name = [x.lower() for x in splitted_name]
        # Remove digits for all chain strings in list
        splitted_name = [s.translate(remove_digits) for s in splitted_name]

        # for "lactique" nad "lactiques" -> https://stackoverflow.com/a/4843170/13235421
        if [y for y in splitted_name if "lactique" in y]:
            df["Type"][index] = "BL"
        elif [y for y in splitted_name if "bacterie" in y]:
            df["Type"][index] = "BL"
        elif "enterobacterie" in splitted_name:
            df["Type"][index] = "E"
        elif "entero" in splitted_name:
            df["Type"][index] = "E"
        elif "gt" in splitted_name:
            df["Type"][index] = "GT"
        else:
            df["Type"][index] = "Nan"

    if excel_help_file is not None:
        df_counted = pd.read_excel(excel_help_file)
        df_counted.Filename = df_counted.Filename.apply(lambda x: str(x).split("\\")[-1].replace(".jpg", ""))
        for index, row in df.iterrows():
            if row.Type == "Nan":
                if row.Filename in list(
                        df_counted.Filename.apply(lambda x: x.split("\\")[-1].replace(".jpg", "")).values):
                    df["Type"][index] = df_counted[df_counted['Filename'] == row.Filename].Type.values[0]

    return df

def create_folder(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)