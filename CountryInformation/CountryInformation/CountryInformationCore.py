from ScriptCollection.GeneralUtilities import GeneralUtilities
from .Country import Country
from .Language import Language
from .CulturedLanguage import CulturedLanguage
from .CountryUtilities import CountryUtilities
from .CultureUtilities import CultureUtilities
from .CacheForCountries import CacheForCountries
from .CacheForLanguages import CacheForLanguages

version = "1.0.13"
__version__ = version


class CountryInformationCore:
    __country_utilities: CountryUtilities
    __culture_utilities: CultureUtilities
    __cache_for_countries: CacheForCountries

    def __init__(self):
        self.__cache_for_countries = CacheForCountries()
        self.__cache_for_languages = CacheForLanguages()
        self.__country_utilities = CountryUtilities(self.__cache_for_countries)
        self.__culture_utilities = CultureUtilities(self.__cache_for_countries, self.__cache_for_languages)

    @GeneralUtilities.check_arguments
    def get_all_countries(self) -> list[Country]:
        return self.__cache_for_countries.get_all_countries()

    @GeneralUtilities.check_arguments
    def get_all_languages(self) -> list[Language]:
        return self.__cache_for_languages.get_all_languages()

    @GeneralUtilities.check_arguments
    def get_all_common_culture_language_combinations(self) -> list[CulturedLanguage]:
        return self.__country_utilities.get_all_common_culture_language_combinations()

    @GeneralUtilities.check_arguments
    def get_cultured_language_from_culture_code(self, culture_code: str) -> CulturedLanguage:
        return self.__culture_utilities.get_cultured_language_from_culture_code(culture_code)

    @GeneralUtilities.check_arguments
    def __getitem__(self, culture_code: str) -> CulturedLanguage:
        """Allows dict-like access, e.g. CountryInformationCore()["de-AT"]."""
        return self.__culture_utilities.get_cultured_language_from_culture_code(culture_code)
