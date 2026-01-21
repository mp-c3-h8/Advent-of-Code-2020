import os.path
import re


def num_valid(data: str) -> int:
    res = 0
    regex = re.compile(r"[a-z]+:")
    passports = data.split("\n\n")
    for passport in passports:
        if sum(1 for key in regex.findall(passport) if key != "cid:") == 7:
            res += 1
    return res


def num_valid2(data: str) -> int:
    VALID_HEX_COLOR = re.compile(r"^#([A-Fa-f0-9]{6})$")
    VALID = {
        "byr": range(1920, 2003),
        "iyr": range(2010, 2021),
        "eyr": range(2020, 2031),
        "hgt": {
            "cm": range(150, 194),
            "in": range(59, 76)
        },
        "ecl": {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    }
    res = 0
    passports = data.split("\n\n")
    for passport in passports:
        valid_fields = 0
        for keyvalue in passport.replace("\n"," ").split(" "):
            key, value = keyvalue.split(":")

            if key in {"byr", "iyr", "eyr"}:
                if int(value) not in VALID[key]:
                    break

            match key:
                case "hgt":
                    n = value[:-2]
                    unit = value[-2:]
                    if unit not in VALID[key] or int(n) not in VALID[key][unit]:
                        break
                case "hcl":
                    if VALID_HEX_COLOR.search(value) is None:
                        break
                case "ecl":
                    if value not in VALID[key]:
                        break
                case "pid":
                    if len(value) != 9 or not value.isdigit():
                        break
                case "cid":
                    continue
            valid_fields += 1
        res += (valid_fields == 7)
    return res


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


print("Part 1:", num_valid(data))
print("Part 2:", num_valid2(data))
