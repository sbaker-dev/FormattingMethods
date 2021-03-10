from miscSupports import flatten, chunk_list


def assigned_exposure(unique_place_list, phenotype_keys, database, age, average_exposures=None,
                      population_name="Estimated_population", place_delimiter="__", rate_per=100):
    """
    Calculates the exposures at a given age and the average exposure by a given age

    :param unique_place_list: A list of unique places dates where each element is year__month__gid__place, deliminator
        is by default __ but can be overridden via place_delimiter
    :type unique_place_list: list[str]
        
    :param place_delimiter: The delimiter to be used to split a place in unique_place_list
    :type place_delimiter: str

    :param phenotype_keys: The keys of the database you want to extract, is case sensitive
    :type phenotype_keys: list[str]

    :param database: A loaded json database where the first level of keys represents the unique places gid__place
    :type database: dict

    :param age: The age you want to construct age specific effects up to
    :type age: int

    :param average_exposures: A list of ints, where each int represents an age you would like to create an average
        exposures up to. May also be None which is also the default
    :type average_exposures: list[int] | None

    :param population_name: The population you want to calculate your exposure rate as, defaults to Estimated_population
    :type population_name: str

    :param rate_per: The rates per population you wish to use, defaults to 100
    :type rate_per: int | float

    :return: A dict of type unique_place: age exposure list + average exposure list, with the later only being added on
        if it was set.
    :rtype: dict
    """
    link_ref_dict = {}
    for index, unique in enumerate(unique_place_list):
        if index % 1000 == 0:
            print(f"{index} / {len(unique_place_list)}")

        year, month, gid, place = unique.split(place_delimiter)
        birth_date = year + month + "01"
        place_data = database[f"{gid}__{place}"]

        for phenotype in phenotype_keys:

            # Divide each year into months, then start from the month of birth a sum the month population values into
            # new years
            relevant_pop = [pop for date, pop in place_data[population_name].items() if date[:4] >= year]
            relevant_pop = flatten([[pop / 12 for _ in range(12)] for pop in relevant_pop])[age:]
            relevant_pop = [sum(year_pop) for year_pop in chunk_list(relevant_pop, 12) if len(year_pop) == 12][:age]

            # isolate the weekly values then chunk them into years
            phenotype_weeks = [v for date, v in place_data[phenotype].items() if date >= birth_date]

            # Chunk them into years
            phenotype_years = chunk_list(phenotype_weeks, 52)
            phenotype_years = [sum(week_chunk) if i < age and len(week_chunk) == 52 else "NA"
                               for i, week_chunk in enumerate(phenotype_years)][:age]

            # If we do not have a valid set of answers, return NA for each row that could be set
            if (len(phenotype_years) < age) or ("NA" in phenotype_years) or len(relevant_pop) < age:
                if average_exposures:
                    link_ref_dict[f"{year}__{month}__{gid}__{place}"] = ["NA" for _ in range(age)] + \
                                                                        ["NA" for _ in range(len(average_exposures))]
                else:
                    link_ref_dict[f"{year}__{month}__{gid}__{place}"] = ["NA" for _ in range(age)]

            # Otherwise calculate the exposure at each given age up to the total of age and averages, if set, by each
            # age in the average_exposure list.
            else:
                exposures = []
                averages = []
                for i, (exposure, population) in enumerate(zip(phenotype_years, relevant_pop)):
                    exposures.append((exposure / population) * rate_per)

                    # If we want the average by a given age, iterate the totals up to the current age to determine the
                    # average exposure
                    if average_exposures and (i + 1 in average_exposures):
                        average = (sum([phenotype_years[ii] for ii in range(i + 1)]) / sum(
                            relevant_pop[ii] for ii in range(i + 1))) * rate_per
                        averages.append(average)

                link_ref_dict[f"{year}__{month}__{gid}__{place}"] = exposures + averages

    return link_ref_dict
