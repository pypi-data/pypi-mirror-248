from bestErrors import OutOfRangeError, InvalidTypeError


class readabforms:
    def __init__(self) -> None:
        self.abbrs = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Qa",
        "Qt",
        "Sx",
        "Sp",
        "Oc",
        "No",
        "Dc",
        "UDc",
        "DDc",
        "TDc",
        "QaDc",
        "QiDc",
        "SxDc",
        "SpDc",
        "OcDc",
        "NmDc",
        "Vg",
        "UVg",
        "DVg",
        "TVg",
        "QaVg",
        "QiVg",
        "SxVg",
        "SpVg",
        "OcVg",
        "NmVg",
        "Tg",
        "UTg",
        "DTg",
        "TTg",
        "QaTg",
        "QiTg",
        "SxTg",
        "SpTg",
        "OcTg",
        "NmTg",
        "Qa",
        "UQa",
        "DQa",
        "TQa",
        "QaQa",
        "QiQa",
        "SxQa",
        "SpQa",
        "OcQa",
        "NoQa",
        "Qi",
        "UQi",
        "DQi",
        "TQi",
        "QaQi",
        "QiQi",
        "SxQi",
        "SpQi",
        "OcQi",
        "NoQi",
        "Se",
        "USe",
        "DSe",
        "TSe",
        "QaSe",
        "QiSe",
        "SxSe",
        "SpSe",
        "OcSe",
        "NoSe",
        "St",
        "USt",
    ]
    
    def readable_format(self, num: float) -> str:
        if type(num) != float:
            raise InvalidTypeError('Invalid type: {}'.format(type(num)))
        else:
            test_num = num
            num = float("{:.3g}".format(num))
            magnitude = 0
            
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            
            try:
                abbr = self.abbrs[magnitude]
            except Exception:
                raise OutOfRangeError(message="{} is too big! 🤯".format(test_num))
            
            return "{}{}".format("{:f}".format(num).rstrip("0").rstrip("."), abbr)


    def unreadable_format(self, readabform: str) -> int | float:
        if type(readabform) == str:
            numeric_part = float(readabform[:-1])
            abbr = readabform[-1]
    
            if abbr in self.abbrs:
                factor = 10 ** ((self.abbrs.index(abbr) + 1) * 3)
                return int(numeric_part * factor)
            else:
                raise OutOfRangeError(message='The suffix ' + str(abbr) + ' is not supported or found.')
        else:
            raise InvalidTypeError('Invalid type: {}'.format(type(readabform)))

ReadabForm : readabforms = readabforms()

abbreviations = ReadabForm.abbrs
abbrs = ReadabForm.abbrs

form = readabformat = ReadabForm.readable_format
unform = unreadabform = ReadabForm.unreadable_format
