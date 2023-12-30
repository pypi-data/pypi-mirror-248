from .utils.normalization import normalization_ch as normalizer_ch


def normalize_address(address, structure_sign="", lang="ch"):

    if lang == "ch":

        minority_list = []
        with open("./data/minority_list.txt", "r", encoding="utf-8-sig") as f:
            for line in f.readlines():
                minority_list.append(line.strip())

        minority_postfix_list = []

        for minority in minority_list:
            if len(minority) > 2:
                minority_postfix_list.append(minority.replace("族", "") + "自治州")
                minority_postfix_list.append(minority.replace("族", "") + "自治区")
                minority_postfix_list.append(minority.replace("族", "") + "自治县")

        normalized_address = normalizer_ch.normalize_address(address,
                                                     structure_sign=structure_sign,
                                                     minority_list=minority_list, 
                                                     minority_postfix_list=minority_postfix_list)
    return normalized_address