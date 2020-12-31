from csvObject import write_csv, CsvObject
from FormattingMethods import flatten
import os


def rebase_year(date_of_birth, rebase_list):
    """
    Instead of working from jan-dec work from another month - month from within a year.
    """
    for i, y in enumerate(rebase_list):
        if (i > 0) and (rebase_list[i - 1] <= date_of_birth < y):
            return rebase_list[i - 1].year


def rate(phenotype, population, rates_per):
    """
    Method that computes a rate
    """
    return (phenotype / population) * rates_per


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
            place_lookup[row[0]] = rate(float(row[phe_index]), float(row[pop_index]), rates_per)
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


def within_date(date_min, date_max, current_date):
    """
    Test if a provided date is greater than or equal to a min date or less than max date
    """
    if date_min <= current_date < date_max:
        return True
    else:
        return False


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


def format_id_data_dict(id_data, phenotypes_dict):
    """
    Take id_data dict and extract the data into a list of lists format to write to csv. Performs different operations on
    lists, to ensure each element of the list is written out rather than writen as a list

    :param id_data: A dict containing values for each id of the study
    :type id_data: dict

    :param phenotypes_dict: The phenotype dict of type Name : column index
    :type phenotypes_dict: dict

    :return: List of lists, where each sub list is all the information that was extracted for a given individual in the
        formatting of this paper
    :rtype: list[list]
    """
    return [[ids] +                                                          # The id of the individual
            [value for value in ids_data.values() if type(value) != list] +  # Non list values
            flatten([ids_data[name] for name in phenotypes_dict.keys()])     # List values from Phenotypes
            for ids, ids_data in zip(id_data.keys(), id_data.values())]


def loaded_columns_dict(full_sample, phenotypes_dict):
    """
    For each of our list phenotypes, get the columns of the complete sample that they where constructed from.
    """
    return {key: [i for i, header in enumerate(full_sample.headers) if key in header] for key in phenotypes_dict.keys()}


def average_complete_sample(column_dict, average_list, cleaned_sample):
    """
    Once a sample has been cleaned, you may wish to average some of the columns, this method will do that

    :param column_dict: A dict of the phenotype name: index values of the columns of that name
    :type column_dict: dict

    :param average_list: A list of ints, indexes below that int will be averaged so should be of values
        1-len(columns - 1)
    :type average_list: list[int]

    :param cleaned_sample: The cleaned sample that we are going to use for the analysis

    :return: The averaged rows from the cleaned sample
    """

    return [[average_phenotypes([id_row[i] for i in value], average_list) for value in column_dict.values()]
            for id_row in cleaned_sample]


def construct_analysis_sample(original_headers, loaded_dict, end, cleaned_sample, write_directory, write_name,
                              averaged_rows=None, average_list=None):
    """
    If we have averaged rows, add these to our sample and allow us to cut of the columns that where used to construct
    them via setting and end index. If no averages where constructed, just write out the cleaned sample.
    """

    if averaged_rows and average_list:
        headers = original_headers[:end] + flatten(
            [[f"{name}_Average{i}" for i in average_list] for name in loaded_dict.keys()])
        reformed_row = [row[:end] + flatten(averages) for row, averages in zip(cleaned_sample, averaged_rows)]
    else:
        headers = original_headers
        reformed_row = cleaned_sample

    write_csv(write_directory, write_name, headers, reformed_row)
