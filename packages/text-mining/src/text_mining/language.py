from enum import Enum

# { support matrix based on downloaded files in ~/nltk_data/[corpora, tokenizers]
#         'hungarian',
#         'italian',
#         'azerbaijani',
#         'dutch',
#         'turkish',
#         'hinglish',
#         'french',
#         'danish',
#         'finnish',
#         'portuguese',
#         'malayalam',
#         'russian',
#         'swedish',
#         'norwegian',
#         'hebrew',
#         'czech',
#         'tajik',
#         'kazakh',
#         'basque',
#         'estonian',
#         'romanian',
#         'spanish',
#         'german',
#         'english',
#         'chinese',
#         'indonesian',
#         'greek',
#         'slovene'
#         }


class Language(Enum):
    """
    Langauage enum/mapper for 2-char characters to NLTK compatible strings
    Example:
        >>> from text_mining.language import Language
        >>> Language.en.value
        'english'
        >>> l = Language.fr
        >>> l.value
        'french'

        >>> # Or use to_string()
        >>> l.to_string()
        'french'
        >>> Language.da.to_string()
        'danish'

        >>> # Or use from_string()
        >>> Language.from_string('en')
        <Language.en: 'english'>
        >>> Language.from_string('fr').to_string()
        'french'
        >>>
    """
    en = "english"
    pt = "portuguese"
    es = "spanish"
    fr = "french"
    nl = "dutch"
    sv = "swedish"
    da = "danish"
    tr = "turkish"
    de = "german"
    it = "italian"
    fi = "finnish"
    ro = "romanian"
    ru = "russian"
    no = "norwegian"
    und = "english"  # if unknown or undefined, use english
    et = "estonian"
    ind = "indonesian"  # 'in' conflicts with python 'in'->'ind'
    eu = "basque"
    hu = "hungarian"
    cs = "czech"
    el = "greek"
    sl = "slovene"
    zh = "chinese"
    iw = "hebrew"

    @classmethod
    def from_string(cls, language_code: str):
        """ex: language_code s are 'en', 'fr' etc."""

        if language_code == "in":
            return cls["ind"]
        else:
            try:
                return cls[language_code.lower()]
            except KeyError:
                return cls["und"]  # und is 'undefined' or unknown

    def to_string(self) -> str:
        """
        Equivilent to Enum.value
        Returns:
            full language string (str)
        """
        return self.value
