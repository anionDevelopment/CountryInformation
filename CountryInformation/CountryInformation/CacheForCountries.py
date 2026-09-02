from .Country import Country
from .CountryData import CountryData


class CacheForCountries:
    __countries: list[Country] = None

    def get_all_countries(self) -> list[Country]:
        if self.__countries is None:
            self.__countries = CountryData().get_all_countries()
        return self.__countries

def get_associated_country_by_language_code(language_code_as_iso639_1_abbreviation: str) -> Country:
    """Returns the country which is usually associated with the given ISO-639-1-language-code
    (e.g. "de" -> Germany, "en" -> United States, "fr" -> France, "es" -> Spain). For a language which is not
    (solely) spoken in one specific country this is inevitably a simplification to one representative country."""
    match language_code_as_iso639_1_abbreviation.lower():
        case "af":
            country_code = "ZA"
        case "am":
            country_code = "ET"
        case "ar":
            country_code = "SA"
        case "ay":
            country_code = "BO"
        case "az":
            country_code = "AZ"
        case "be":
            country_code = "BY"
        case "bg":
            country_code = "BG"
        case "bi":
            country_code = "VU"
        case "bn":
            country_code = "BD"
        case "bs":
            country_code = "BA"
        case "ca":
            country_code = "AD"
        case "cs":
            country_code = "CZ"
        case "da":
            country_code = "DK"
        case "de":
            country_code = "DE"
        case "dv":
            country_code = "MV"
        case "dz":
            country_code = "BT"
        case "el":
            country_code = "GR"
        case "en":
            country_code = "US"
        case "es":
            country_code = "ES"
        case "et":
            country_code = "EE"
        case "fa":
            country_code = "IR"
        case "fi":
            country_code = "FI"
        case "fj":
            country_code = "FJ"
        case "fr":
            country_code = "FR"
        case "ga":
            country_code = "IE"
        case "gn":
            country_code = "PY"
        case "he":
            country_code = "IL"
        case "hi":
            country_code = "IN"
        case "ho":
            country_code = "PG"
        case "hr":
            country_code = "HR"
        case "ht":
            country_code = "HT"
        case "hu":
            country_code = "HU"
        case "hy":
            country_code = "AM"
        case "hz":
            country_code = "NA"
        case "id":
            country_code = "ID"
        case "is":
            country_code = "IS"
        case "it":
            country_code = "IT"
        case "ja":
            country_code = "JP"
        case "ka":
            country_code = "GE"
        case "kg":
            country_code = "CD"
        case "kk":
            country_code = "KZ"
        case "km":
            country_code = "KH"
        case "ko":
            country_code = "KR"
        case "ky":
            country_code = "KG"
        case "la":
            country_code = "VA"
        case "lb":
            country_code = "LU"
        case "ln":
            country_code = "CD"
        case "lo":
            country_code = "LA"
        case "lt":
            country_code = "LT"
        case "lv":
            country_code = "LV"
        case "mg":
            country_code = "MG"
        case "mh":
            country_code = "MH"
        case "mi":
            country_code = "NZ"
        case "mk":
            country_code = "MK"
        case "mn":
            country_code = "MN"
        case "ms":
            country_code = "MY"
        case "mt":
            country_code = "MT"
        case "my":
            country_code = "MM"
        case "na":
            country_code = "NR"
        case "nb":
            country_code = "NO"
        case "nd":
            country_code = "ZW"
        case "ne":
            country_code = "NP"
        case "ng":
            country_code = "NA"
        case "nl":
            country_code = "NL"
        case "nn":
            country_code = "NO"
        case "nr":
            country_code = "ZA"
        case "ny":
            country_code = "MW"
        case "pl":
            country_code = "PL"
        case "ps":
            country_code = "AF"
        case "pt":
            country_code = "PT"
        case "qu":
            country_code = "PE"
        case "rm":
            country_code = "CH"
        case "rn":
            country_code = "BI"
        case "ro":
            country_code = "RO"
        case "ru":
            country_code = "RU"
        case "rw":
            country_code = "RW"
        case "sg":
            country_code = "CF"
        case "si":
            country_code = "LK"
        case "sk":
            country_code = "SK"
        case "sl":
            country_code = "SI"
        case "sm":
            country_code = "WS"
        case "sn":
            country_code = "ZW"
        case "so":
            country_code = "SO"
        case "sq":
            country_code = "AL"
        case "sr":
            country_code = "RS"
        case "ss":
            country_code = "SZ"
        case "st":
            country_code = "LS"
        case "sv":
            country_code = "SE"
        case "sw":
            country_code = "TZ"
        case "ta":
            country_code = "LK"
        case "tg":
            country_code = "TJ"
        case "th":
            country_code = "TH"
        case "ti":
            country_code = "ER"
        case "tk":
            country_code = "TM"
        case "tn":
            country_code = "BW"
        case "to":
            country_code = "TO"
        case "tr":
            country_code = "TR"
        case "ts":
            country_code = "ZA"
        case "uk":
            country_code = "UA"
        case "ur":
            country_code = "PK"
        case "uz":
            country_code = "UZ"
        case "ve":
            country_code = "ZA"
        case "vi":
            country_code = "VN"
        case "xh":
            country_code = "ZA"
        case "zh":
            country_code = "CN"
        case "zu":
            country_code = "ZA"
        case _:
            raise ValueError(f"No country known which is usually associated with the language-code \"{language_code_as_iso639_1_abbreviation}\".")

    for country in CacheForCountries().get_all_countries():
        if country.country_code == country_code:
            return country
    raise ValueError(f"No country found with country-code \"{country_code}\" (associated with language-code \"{language_code_as_iso639_1_abbreviation}\").")
