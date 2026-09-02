from ScriptCollection.GeneralUtilities import GeneralUtilities
from .Country import Country
from .CulturedLanguage import CulturedLanguage
from .CacheForCountries import CacheForCountries
from .CacheForLanguages import CacheForLanguages
from .LanguageUtilities import LanguageUtilities


class CultureUtilities:
    __cache_for_countries: CacheForCountries
    __language_utilities: LanguageUtilities

    def __init__(self, cache_for_countries: CacheForCountries = None, cache_for_languages: CacheForLanguages = None):
        if cache_for_countries is None:
            cache_for_countries = CacheForCountries()
        self.__cache_for_countries = cache_for_countries
        self.__language_utilities = LanguageUtilities(cache_for_languages)

    @GeneralUtilities.check_arguments
    def get_cultured_language_from_culture_code(self, culture_code: str) -> CulturedLanguage:
        """Parses a culture-code like "de" or "de-AT" and resolves the according language and (if available) country.
        For a bare language-code (e.g. "de") the country is only defaulted for flag-purposes (see CulturedLanguage.get_country_or_associated_country)
        to the country whose ISO-3166-1-alpha-2-code equals the language-code (e.g. "de" -> "DE"/Germany), if such a country
        exists. That defaulted country is not treated as explicit, so CulturedLanguage.get_display_name_in_english and
        CulturedLanguage.get_abbreviation ignore it (e.g. "de" stays "German" instead of "German (Germany)")."""
        language_code, separator, country_part = culture_code.partition("-")
        language = self.__language_utilities.get_language_from_iso639_1_code(language_code.lower())

        if separator:
            country_code = country_part.upper()
            country = self.__get_country_by_country_code(country_code)
            return CulturedLanguage(language, country, True)
        else:
            default_country = self.__get_country_by_country_code(language_code.upper())
            return CulturedLanguage(language, default_country, False)

    @GeneralUtilities.check_arguments
    def __getitem__(self, culture_code: str) -> CulturedLanguage:
        """Allows dict-like access, e.g. CultureUtilities()["de-AT"]."""
        return self.get_cultured_language_from_culture_code(culture_code)

    def __get_country_by_country_code(self, country_code: str) -> Country:
        for country in self.__cache_for_countries.get_all_countries():
            if country.country_code == country_code:
                return country
        raise ValueError(f"No country found with country-code \"{country_code}\".")
