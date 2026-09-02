from .Language import Language
from .Country import Country
from .CacheForCountries import get_associated_country_by_language_code


class CulturedLanguage:
    __language: Language
    __country: Country  # may be None if no (explicit or default) country is known for this culture
    # whether "country" was explicitly specified in the culture-code (e.g. "de-AT") instead of only being
    # defaulted for flag-purposes (e.g. "de" defaults to the country "Germany", just to be able to provide a flag-emoji)
    __country_is_explicit: bool

    def __init__(self, language: Language, country: Country = None, country_is_explicit: bool = True):
        self.__language = language
        self.__country = country
        self.__country_is_explicit = country_is_explicit

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, CulturedLanguage):
            return False
        return self.__language == other.__language and self.__country == other.__country

    def __hash__(self):
        return hash((self.__language, self.__country))

    def get_language(self) -> Language:
        return self.__language

    def country_is_available(self) -> bool:
        return self.__country is not None

    def get_country(self) -> Country:
        return self.__country

    def country_is_explicit(self) -> bool:
        return self.__country_is_explicit

    def get_abbreviation(self) -> str:
        if self.__country is None or not self.__country_is_explicit:
            return self.__language.abbreviation_iso639_1
        return f"{self.__language.abbreviation_iso639_1}-{self.__country.country_code}"

    def get_display_name_in_english(self) -> str:
        if self.__country is None or not self.__country_is_explicit:
            return self.__language.name_in_english
        else:
            return f"{self.__language.name_in_english} ({self.__country.common_name_in_english})"

    def get_country_or_associated_country(self) -> Country:
        if self.__country is None:
            return get_associated_country_by_language_code(self.__language.abbreviation_iso639_1)
        else:
            return self.__country
