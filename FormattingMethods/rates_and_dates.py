from csvObject import write_csv, CsvObject
from IPython.display import clear_output
import pandas as pd
import csv
from itertools import chain
from datetime import datetime
import os


def extract_headers(path):
    """
    Extract the first row from the file and return it as a list
    """
    with open(path) as header_extract:
        csv_data = csv.reader(header_extract)
        for row in csv_data:
            return row


def write_chunks(csv_path, header_list, header_type, write_directory, file_name, chunk_size=1000):
    """
    This iterates through a section of a csv file by using the header_list to only uses certain columns and loads them
    in the type specified in header type.

    :param csv_path: Path to the csv you want to iterate through
    :param header_list: Headers you want to extract from the master csv file
    :param header_type: The type of each column
    :param chunk_size: The number of rows you want to chunk load at a time
    :param write_directory: Write directory
    :param file_name: Write Name
    :return: Nothing, write out the file and then stop.
    """
    row_data = []
    for index, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size, usecols=header_list, dtype=header_type)):
        print((index + 1) * chunk_size)

        raw_list = [chunk[header].to_list() for header in header_list]
        transposed_list = [[row[i] for row in raw_list] for i in range(len(raw_list[0]))]
        for row in transposed_list:
            row_data.append(row)

    write_csv(write_directory, file_name, header_list, row_data)
    clear_output(wait=True)
    print(f"Finished writing {file_name}")


def parse_int(age):
    """
    Try isolating converting to int, unless its nan then return zero.
    """
    try:
        return int(age)
    except ValueError:
        return 0


def rebase_year(date_of_birth, rebase_list):
    """
    Instead of working from jan-dec work from another month - month from within a year.
    """
    for i, y in enumerate(rebase_list):
        if (i > 0) and (rebase_list[i - 1] <= date_of_birth < y):
            return rebase_list[i - 1].year


def compute_rates(load_directory, file_to_load, phe_index, pop_index, rates_per=1000):
    """
    This will assign the rates of a given phenotype to a dictionary if the row has the required information on
    population and the phenotype in question
    """

    load_file = CsvObject(f"{load_directory}/{file_to_load}")

    place_lookup = {}
    for row in load_file.row_data:
        if (row[pop_index] != "NA") and (row[phe_index] != "NA") and (row[pop_index] != "Failed") \
                and (row[phe_index] != "Failed"):
            place_lookup[row[0]] = ((float(row[phe_index]) / float(row[pop_index])) * rates_per)
        else:
            place_lookup[row[0]] = ""
    return place_lookup


def assign_rates(data_dict, rates_data, data_dict_key):
    """
    Attempt to assign a rate to a given unless we don't have data for this year
    """
    for data in data_dict.keys():
        try:
            data_dict[data][data_dict_key].append(rates_data[data])
        except KeyError:
            pass


def average_exposure(row):
    """
    Calculate an average exposure based on there being non empty rows
    """
    if "" not in row:
        return sum([float(r) for r in row]) / len(row)
    else:
        return ""


def flatten(list_of_lists):
    """
    Flatten a list of lists into a list
    """
    return list(chain(*list_of_lists))


def average_phenotypes(row, average_list_lengths):
    """
    For each phenotype in the loaded_phenotype dictionary get the average based on the average list and return these
    values
    """
    return [average_exposure([r for i, r in enumerate(row) if i < average]) for average in average_list_lengths]


def check_date(date, date_to_check):
    """
    Check to see if the date of birth is before or after the date to check
    """
    if date < date_to_check:
        return 0
    else:
        return 1


def terminal_time():
    """
    A way to remember when you initialised a cell by return the current hour and minute as a string
    """
    return f"{datetime.now().time().hour}:{datetime.now().time().minute}"


def exposure_years(file_dir, phenotypes_dict, population_index, id_data, rates_per=1000):
    """

    :param file_dir: The directory of exposure data, where file names should have a numeric prefix for sorting purposes
    :type file_dir: str

    :param phenotypes_dict: Phenotype name to the index that name is in terms of zero based columns in the file.
    :type phenotypes_dict: dict

    :param population_index: The index of the population key, should be common across all files
    :type population_index: int

    :param id_data: The data dictionary to append the information too.
    :type id_data: dict

    :key rates_per: We calculate rates as the phenotype per 'rates_per' individuals, defaults to 1000.
    :type rates_per: int

    :return: Nothing, information is appended to id_data dict then stops
    :rtype: None
    """
    # Sort of file list to be ordered from 1-max year
    year_list = [[int(file[19:-4]), file] for file in os.listdir(file_dir)]
    year_list.sort(key=lambda x: x[0])

    # For each phenotype
    for name, phenotype_i in zip(phenotypes_dict.keys(), phenotypes_dict.values()):
        print(name, phenotype_i)

        # For each year of exposure we calculate the rates for each individual and then assign it to them.
        for ii, file in year_list:
            print(ii, file)
            year_rates = compute_rates(file_dir, file, phenotype_i, population_index, rates_per)
            assign_rates(id_data, year_rates, name)
