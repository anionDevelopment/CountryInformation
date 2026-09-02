import os
import json
import shutil
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.Python.TFCPS_CodeUnitSpecific_Python import TFCPS_CodeUnitSpecific_Python_Functions,TFCPS_CodeUnitSpecific_Python_CLI


def assert_not_none(obj) -> None:
    GeneralUtilities.assert_condition(obj is not None, "Object is none")


@GeneralUtilities.check_arguments
def format_json_file(json_file: str) -> None:
    content_plain = GeneralUtilities.read_text_from_file(json_file)
    content = json.loads(content_plain)
    content_formatted = json.dumps(content, indent=4)
    GeneralUtilities.write_text_to_file(json_file, content_formatted)


@GeneralUtilities.check_arguments
def language_is_ignored(language_name:str) -> bool:
    if language_name=="Moldavian":
        return True#ignored because it has the same language-code as romanian so it would result in non-unique ISO639-abbreviations
    if language_name=="Southern Sotho":
        return True#ignored because it is the same as Sotho
    return False

@GeneralUtilities.check_arguments
def generate_language_file(target_file: str, datasets) -> None:
    file_content = """# The content of this file is generated.
from .Language import Language
from .LanguageCodeConversionUtilities import LanguageCodeConversionUtilities

class LanguageData:
    def get_all_languages(self)->list[Language]:
        result:list[Language]=[]

"""
    languages: set[tuple[str, str]] = set()
    for dataset in datasets:
        if dataset["independent"]:
            for language_abbreviation, language_name in dataset["languages"].items():
                if not language_is_ignored(language_name):
                    languages.add((language_abbreviation,language_name))
    for language in sorted(languages, key=lambda dataset: dataset):
        file_content = file_content+f'        if LanguageCodeConversionUtilities().iso639_3_code_is_supported("{language[0]}"):\n            result.append(Language(LanguageCodeConversionUtilities().get_iso639_1_code_from_iso639_3("{language[0]}"), "{language[0]}", "{language[1]}"))\n'
    file_content = file_content+"\n        return result\n"
    GeneralUtilities.ensure_file_exists(target_file)
    GeneralUtilities.write_text_to_file(target_file, file_content)


@GeneralUtilities.check_arguments
def generate_countries_file(target_file: str, datasets) -> None:
    file_content = """# The content of this file is generated.
from .Country import Country
from .Language import Language
from .LanguageUtilities import LanguageUtilities
from .LanguageCodeConversionUtilities import LanguageCodeConversionUtilities


class CountryData:
    def get_all_countries(self) -> list[Country]:
        result:list[Country] = []
        language_utilities: LanguageUtilities = LanguageUtilities(None)

"""
    for dataset in sorted(datasets, key=lambda dataset: dataset["name"]["common"]):
        if dataset["independent"]:
            common_name_in_english: str = dataset["name"]["common"]
            assert_not_none(common_name_in_english)
            official_name_in_english: str = dataset["name"]["official"]
            assert_not_none(official_name_in_english)
            country_code: str = dataset["cca2"]
            assert_not_none(country_code)
            flag_emoji: str = get_flag_emoji_for_country_code(country_code)
            file_content = file_content+f'        languages_for_{country_code}: list[Language] = []\n'
            for language_abbreviation_iso639_3, language_name in dataset["languages"].items():  # pylint:disable=unused-variable
                file_content = file_content+f'        if LanguageCodeConversionUtilities().iso639_3_code_is_supported("{language_abbreviation_iso639_3}"):\n            languages_for_{country_code}.append(language_utilities.get_language_from_code_iso639_3("{language_abbreviation_iso639_3}"))\n'
            file_content = file_content+f'        result.append(Country("{common_name_in_english}", "{official_name_in_english}", "{country_code}", "{flag_emoji}", languages_for_{country_code}))\n        \n'
    file_content = file_content+"\n        return result\n"
    GeneralUtilities.ensure_file_exists(target_file)
    GeneralUtilities.write_text_to_file(target_file, file_content)


@GeneralUtilities.check_arguments
def item_is_ignored(data)->bool:
    if data["name"]["common"]=="Moldova":
        return True#ignored because it has the same language-code as romanian so it would result in non-unique ISO639-abbreviations
    return False

@GeneralUtilities.check_arguments
def filter(data:list)->list:
    result=[]
    for item in data:
        if not item_is_ignored(item):
            result.append(item)
    return result

@GeneralUtilities.check_arguments
def generate_python_data_files(codeunit_folder: str) -> None:
    source_folder = GeneralUtilities.resolve_relative_path("./Other/Resources/RawData", codeunit_folder)
    source_file = os.path.join(source_folder, "Countries.json")
    data = json.loads(GeneralUtilities.read_text_from_file(source_file))
    #data=filter(data)
    python_folder: str = os.path.join(codeunit_folder, "CountryInformation")
    generate_language_file(os.path.join(python_folder, "LanguageData.py"), data)
    generate_countries_file(os.path.join(python_folder, "CountryData.py"), data)


@GeneralUtilities.check_arguments
def get_data_from_submodule(codeunit_folder: str) -> None:
    # it is ok to do that in this script and not in UpdateDependencies.py because after updating the submodule the codeunits will bebuilded and then this will be executed anyway. And without an updated submodule this function does not cause any change.
    repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
    upstream_folder = GeneralUtilities.resolve_relative_path("Other/Resources/Submodules/countries", repository_folder)
    target_folder = GeneralUtilities.resolve_relative_path("./Other/Resources/RawData", codeunit_folder)
    GeneralUtilities.ensure_folder_exists_and_is_empty(target_folder)
    src_file = GeneralUtilities.resolve_relative_path("./dist/countries.json", upstream_folder)
    GeneralUtilities.assert_file_exists(src_file)
    target_file = os.path.join(target_folder, "Countries.json")
    shutil.copyfile(src_file, target_file)
    format_json_file(target_file)
 
def common_tasks():
    file = str(Path(__file__).absolute())
    codeunit_folder = GeneralUtilities.resolve_relative_path("..", os.path.dirname(file))
    tf:TFCPS_CodeUnitSpecific_Python_Functions=TFCPS_CodeUnitSpecific_Python_CLI.parse(__file__)
    tf.do_common_tasks(tf.get_version_of_project())#codeunit-version should alsways be the same as project-version
    get_data_from_submodule(codeunit_folder)
    generate_python_data_files(codeunit_folder)

@GeneralUtilities.check_arguments
def get_flag_emoji_for_country_code(country_code: str) -> str:
    match country_code:
        case "AD":
            return "🇦🇩"
        case "AE":
            return "🇦🇪"
        case "AF":
            return "🇦🇫"
        case "AG":
            return "🇦🇬"
        case "AL":
            return "🇦🇱"
        case "AM":
            return "🇦🇲"
        case "AO":
            return "🇦🇴"
        case "AR":
            return "🇦🇷"
        case "AT":
            return "🇦🇹"
        case "AU":
            return "🇦🇺"
        case "AZ":
            return "🇦🇿"
        case "BA":
            return "🇧🇦"
        case "BB":
            return "🇧🇧"
        case "BD":
            return "🇧🇩"
        case "BE":
            return "🇧🇪"
        case "BF":
            return "🇧🇫"
        case "BG":
            return "🇧🇬"
        case "BH":
            return "🇧🇭"
        case "BI":
            return "🇧🇮"
        case "BJ":
            return "🇧🇯"
        case "BN":
            return "🇧🇳"
        case "BO":
            return "🇧🇴"
        case "BR":
            return "🇧🇷"
        case "BS":
            return "🇧🇸"
        case "BT":
            return "🇧🇹"
        case "BW":
            return "🇧🇼"
        case "BY":
            return "🇧🇾"
        case "BZ":
            return "🇧🇿"
        case "CA":
            return "🇨🇦"
        case "CD":
            return "🇨🇩"
        case "CF":
            return "🇨🇫"
        case "CG":
            return "🇨🇬"
        case "CH":
            return "🇨🇭"
        case "CI":
            return "🇨🇮"
        case "CL":
            return "🇨🇱"
        case "CM":
            return "🇨🇲"
        case "CN":
            return "🇨🇳"
        case "CO":
            return "🇨🇴"
        case "CR":
            return "🇨🇷"
        case "CU":
            return "🇨🇺"
        case "CV":
            return "🇨🇻"
        case "CY":
            return "🇨🇾"
        case "CZ":
            return "🇨🇿"
        case "DE":
            return "🇩🇪"
        case "DJ":
            return "🇩🇯"
        case "DK":
            return "🇩🇰"
        case "DM":
            return "🇩🇲"
        case "DO":
            return "🇩🇴"
        case "DZ":
            return "🇩🇿"
        case "EC":
            return "🇪🇨"
        case "EE":
            return "🇪🇪"
        case "EG":
            return "🇪🇬"
        case "ER":
            return "🇪🇷"
        case "ES":
            return "🇪🇸"
        case "ET":
            return "🇪🇹"
        case "FI":
            return "🇫🇮"
        case "FJ":
            return "🇫🇯"
        case "FM":
            return "🇫🇲"
        case "FR":
            return "🇫🇷"
        case "GA":
            return "🇬🇦"
        case "GB":
            return "🇬🇧"
        case "GD":
            return "🇬🇩"
        case "GE":
            return "🇬🇪"
        case "GH":
            return "🇬🇭"
        case "GM":
            return "🇬🇲"
        case "GN":
            return "🇬🇳"
        case "GQ":
            return "🇬🇶"
        case "GR":
            return "🇬🇷"
        case "GT":
            return "🇬🇹"
        case "GW":
            return "🇬🇼"
        case "GY":
            return "🇬🇾"
        case "HN":
            return "🇭🇳"
        case "HR":
            return "🇭🇷"
        case "HT":
            return "🇭🇹"
        case "HU":
            return "🇭🇺"
        case "ID":
            return "🇮🇩"
        case "IE":
            return "🇮🇪"
        case "IL":
            return "🇮🇱"
        case "IN":
            return "🇮🇳"
        case "IQ":
            return "🇮🇶"
        case "IR":
            return "🇮🇷"
        case "IS":
            return "🇮🇸"
        case "IT":
            return "🇮🇹"
        case "JM":
            return "🇯🇲"
        case "JO":
            return "🇯🇴"
        case "JP":
            return "🇯🇵"
        case "KE":
            return "🇰🇪"
        case "KG":
            return "🇰🇬"
        case "KH":
            return "🇰🇭"
        case "KI":
            return "🇰🇮"
        case "KM":
            return "🇰🇲"
        case "KN":
            return "🇰🇳"
        case "KP":
            return "🇰🇵"
        case "KR":
            return "🇰🇷"
        case "KW":
            return "🇰🇼"
        case "KZ":
            return "🇰🇿"
        case "LA":
            return "🇱🇦"
        case "LB":
            return "🇱🇧"
        case "LC":
            return "🇱🇨"
        case "LI":
            return "🇱🇮"
        case "LK":
            return "🇱🇰"
        case "LR":
            return "🇱🇷"
        case "LS":
            return "🇱🇸"
        case "LT":
            return "🇱🇹"
        case "LU":
            return "🇱🇺"
        case "LV":
            return "🇱🇻"
        case "LY":
            return "🇱🇾"
        case "MA":
            return "🇲🇦"
        case "MC":
            return "🇲🇨"
        case "MD":
            return "🇲🇩"
        case "ME":
            return "🇲🇪"
        case "MG":
            return "🇲🇬"
        case "MH":
            return "🇲🇭"
        case "MK":
            return "🇲🇰"
        case "ML":
            return "🇲🇱"
        case "MM":
            return "🇲🇲"
        case "MN":
            return "🇲🇳"
        case "MR":
            return "🇲🇷"
        case "MT":
            return "🇲🇹"
        case "MU":
            return "🇲🇺"
        case "MV":
            return "🇲🇻"
        case "MW":
            return "🇲🇼"
        case "MX":
            return "🇲🇽"
        case "MY":
            return "🇲🇾"
        case "MZ":
            return "🇲🇿"
        case "NA":
            return "🇳🇦"
        case "NE":
            return "🇳🇪"
        case "NG":
            return "🇳🇬"
        case "NI":
            return "🇳🇮"
        case "NL":
            return "🇳🇱"
        case "NO":
            return "🇳🇴"
        case "NP":
            return "🇳🇵"
        case "NR":
            return "🇳🇷"
        case "NZ":
            return "🇳🇿"
        case "OM":
            return "🇴🇲"
        case "PA":
            return "🇵🇦"
        case "PE":
            return "🇵🇪"
        case "PG":
            return "🇵🇬"
        case "PH":
            return "🇵🇭"
        case "PK":
            return "🇵🇰"
        case "PL":
            return "🇵🇱"
        case "PT":
            return "🇵🇹"
        case "PW":
            return "🇵🇼"
        case "PY":
            return "🇵🇾"
        case "QA":
            return "🇶🇦"
        case "RO":
            return "🇷🇴"
        case "RS":
            return "🇷🇸"
        case "RU":
            return "🇷🇺"
        case "RW":
            return "🇷🇼"
        case "SA":
            return "🇸🇦"
        case "SB":
            return "🇸🇧"
        case "SC":
            return "🇸🇨"
        case "SD":
            return "🇸🇩"
        case "SE":
            return "🇸🇪"
        case "SG":
            return "🇸🇬"
        case "SI":
            return "🇸🇮"
        case "SK":
            return "🇸🇰"
        case "SL":
            return "🇸🇱"
        case "SM":
            return "🇸🇲"
        case "SN":
            return "🇸🇳"
        case "SO":
            return "🇸🇴"
        case "SR":
            return "🇸🇷"
        case "SS":
            return "🇸🇸"
        case "ST":
            return "🇸🇹"
        case "SV":
            return "🇸🇻"
        case "SY":
            return "🇸🇾"
        case "SZ":
            return "🇸🇿"
        case "TD":
            return "🇹🇩"
        case "TG":
            return "🇹🇬"
        case "TH":
            return "🇹🇭"
        case "TJ":
            return "🇹🇯"
        case "TL":
            return "🇹🇱"
        case "TM":
            return "🇹🇲"
        case "TN":
            return "🇹🇳"
        case "TO":
            return "🇹🇴"
        case "TR":
            return "🇹🇷"
        case "TT":
            return "🇹🇹"
        case "TV":
            return "🇹🇻"
        case "TZ":
            return "🇹🇿"
        case "UA":
            return "🇺🇦"
        case "UG":
            return "🇺🇬"
        case "US":
            return "🇺🇸"
        case "UY":
            return "🇺🇾"
        case "UZ":
            return "🇺🇿"
        case "VA":
            return "🇻🇦"
        case "VC":
            return "🇻🇨"
        case "VE":
            return "🇻🇪"
        case "VN":
            return "🇻🇳"
        case "VU":
            return "🇻🇺"
        case "WS":
            return "🇼🇸"
        case "YE":
            return "🇾🇪"
        case "ZA":
            return "🇿🇦"
        case "ZM":
            return "🇿🇲"
        case "ZW":
            return "🇿🇼"
        case _:
            raise ValueError(f"No flag-emoji known for country-code \"{country_code}\".")
        
if __name__ == "__main__":
    common_tasks()
