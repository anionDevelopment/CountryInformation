from ScriptCollection.GeneralUtilities import GeneralUtilities
from .CacheForLanguages import CacheForLanguages
from .Language import Language


class LanguageUtilities:
    __cache_for_languages: CacheForLanguages

    # Some iso-639-3-codes (e.g. "bar", "gsw", "prs") are deliberately mapped to another language's
    # iso-639-1-code in LanguageCodeConversionUtilities, only to make country-specific culture-abbreviations
    # (e.g. "de-AT", "de-CH", "fa-AF") possible. Such regional variants must not win over the actual language
    # when a language is looked up by its bare iso-639-1-code, so they are excluded from that lookup here.
    __iso639_3_codes_of_regional_variants_used_for_culture_abbreviations_only = {"bar", "gsw", "prs"}

    def __init__(self, cache_for_languages: CacheForLanguages):
        if cache_for_languages is None:
            cache_for_languages = CacheForLanguages()
        self.__cache_for_languages = cache_for_languages

    @GeneralUtilities.check_arguments
    def get_language_from_iso639_1_code(self,  iso639_1_code: str) -> Language:
        matches = [language for language in self.__cache_for_languages.get_all_languages() if language.abbreviation_iso639_1 == iso639_1_code]
        primary_matches = [language for language in matches
                            if language.abbreviation_iso639_3 not in self.__iso639_3_codes_of_regional_variants_used_for_culture_abbreviations_only]
        if len(primary_matches) > 0:
            return primary_matches[0]
        if len(matches) > 0:
            return matches[0]
        raise ValueError(f"No language found with abbreviation \"{iso639_1_code}\".")

    @GeneralUtilities.check_arguments
    def get_language_from_code_iso639_3(self,  iso639_3_code: str) -> Language:
        for language in self.__cache_for_languages.get_all_languages():
            if language.abbreviation_iso639_3 == iso639_3_code:
                return language
        raise ValueError(f"No language found with abbreviation \"{iso639_3_code}\".")
