"""Utils for serving and generating dictionary data."""

import re


def standardize_key(s: str) -> str:
    """Standardize the dictionary lookup key.

    Different dictionary authors follow different conventions when writing Sanskrit
    words. This function standardizes these conventions so that users have a better
    lookup experience.

    Right now, the only standardization we apply is to convert an anusvāra followed
    by a consonant to its appropriate parasavarṇa ("similar to the following") sound.

    For examples, see the unit tests.

    :param s: the key to standardize.
    :return: a standardize key
    """
    buf = list(s)
    # Always apply parasavaraNatva.
    for m in re.finditer("(M)(.)", s):
        anusvara_index = m.span(1)[0]
        consonant = m.group(2)

        res = "M"
        if consonant in "kKgGN":
            res = "N"
        if consonant in "cCjJY":
            res = "Y"
        if consonant in "wWqQR":
            res = "R"
        if consonant in "tTdDn":
            res = "n"
        if consonant in "pPbBm":
            res = "m"
        buf[anusvara_index] = res
    return "".join(buf)


def expand_apte_keys(key: str) -> list[str]:
    """Standardize Apte's conventions against the other dictionaries.

    Apte uses aH and aM to compactly encode the gender of -a stems.
    For those who don't know this convention, it can be difficult
    to look up a word. So, standardize by removing H/M from the end
    of nominal stems.
    """
    keys = [key]
    if key[-1] == "a":
        keys.append(key + "H")
        keys.append(key + "M")
    elif key[-1] in "AiIuUfFxXeEoO":
        keys.append(key + "H")
    if key[-1] == "m":
        keys.append(key[:-1] + "M")
    return keys
