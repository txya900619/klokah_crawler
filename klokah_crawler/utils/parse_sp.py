import re

TYPE_ID_MP3_IDS_MAP = {
    "2": ["A", "B", "C"],
    "4": ["A", "B", "C"],
    "5": ["A", "B", "C"],
    "6": ["A", "B", "C", "D", "E"],
    "8": ["A", "B", "C", "D", "E"],
    "9": ["A", "B", "C", "D", "E"],
}

TYPE_ID_TYPE_NAME_MAP = {
    "1": "word",
    "2": "sentence",
    "3": "recognize",
    "4": "choiceOne",
    "5": "choiceTwo",
    "6": "match",
    "7": "choiceThree",
    "8": "oralReading",
    "9": "dialogue",
    "10": "pictureTalk",
}


def get_metadata_info(metadata):
    order_key = next(filter(lambda x: x.endswith("Order"), metadata.keys()))
    type_id = metadata["typeId"]
    type_name = TYPE_ID_TYPE_NAME_MAP[type_id]
    mp3_ids = TYPE_ID_MP3_IDS_MAP.get(type_id)

    return order_key, type_id, type_name, mp3_ids


def parse_metadata_with_multiple_text_one_audio(metadata):
    order_key, _, type_name, mp3_ids = get_metadata_info(metadata)

    raw_text_list = [metadata[f"{type_name}{mp3_id}Ab"] for mp3_id in mp3_ids]
    mandarin_list = [metadata[f"{type_name}{mp3_id}Ch"] for mp3_id in mp3_ids]

    # filter out None
    raw_text_list = [text for text in raw_text_list if text is not None]
    mandarin_list = [text for text in mandarin_list if text is not None]

    # let the length of raw_text_list and mandarin_list be the same
    min_length = min(len(raw_text_list), len(mandarin_list))
    raw_text_list = raw_text_list[:min_length]
    mandarin_list = mandarin_list[:min_length]

    parsed_text_list = []

    # dialect_id 15 has a special format, we need to parse it differently
    if metadata["dialectId"] == "15":
        parsed_text_list = parse_slash_horizontally(raw_text_list)
    else:
        for text in raw_text_list:
            if "/" in text:
                parsed_text_list.append(parse_slash(text))
            else:
                parsed_text_list.append(text)

    parsed_slash_text = " ".join(parsed_text_list)
    # normalized_text = normalized_text.replace("坐下", "")
    # normalized_text = normalize_text(normalized_text)

    return [
        {
            "audio_name": f"{metadata['classNo']}_{metadata[order_key]}.mp3",
            "text": parsed_slash_text,
            "raw_text": " ".join(raw_text_list),  # raw text remains slashes
            "mandarin": "".join(mandarin_list),
        }
    ]


def parse_metadata_with_multiple_text(metadata):
    order_key, type_id, type_name, mp3_ids = get_metadata_info(metadata)

    metadata_list = []
    for mp3_id in mp3_ids:
        # type_id 6 has two text, question and answer, so we need to concat them
        if type_id == "6":
            text = (
                metadata[f"{type_name}{mp3_id}AbA"]
                + " "
                + metadata[f"{type_name}{mp3_id}AbB"]
            )
            mandarin = (
                metadata[f"{type_name}{mp3_id}ChA"]
                + metadata[f"{type_name}{mp3_id}ChB"]
            )
        else:
            text = metadata[f"{type_name}{mp3_id}Ab"]
            mandarin = metadata[f"{type_name}{mp3_id}Ch"]

        parsed_slash_text = text
        if "/" in parsed_slash_text:
            parsed_slash_text = parse_slash(parsed_slash_text)

        # normalized_text = normalize_text(normalized_text)

        metadata_list.append(
            {
                "audio_name": f"{metadata['classNo']}_{metadata[order_key]}_{mp3_id}.mp3",
                "raw_text": text,
                "text": parsed_slash_text,
                "mandarin": mandarin,
            }
        )
    return metadata_list


def parse_metadata_with_single_text(metadata):
    order_key, type_id, type_name, _ = get_metadata_info(metadata)

    if metadata[f"{type_name}Ab"] is None:
        return None

    text = metadata[f"{type_name}Ab"]

    if type_id in ["1", "10"]:
        text = text.replace("/", " ")

    if type_id in ["3", "7"]:
        if "/" in text:
            text = parse_slash(text)

    # normalized_text = normalize_text(normalized_text)

    if (
        metadata["dialectId"] == "15"
        and type_id == "1"
        and metadata["classNo"] == "16"
        and metadata[order_key] == "9"
    ):
        text = "na"

    if (
        metadata["dialectId"] == "15"
        and type_id == "3"
        and metadata["classNo"] == "2"
        and metadata[order_key] == "9"
    ):
        text = "Qbhni ka ni."

    return [
        {
            "audio_name": f"{metadata['classNo']}_{metadata[order_key]}.mp3",
            "text": text,
            "raw_text": metadata[f"{type_name}Ab"],
            "mandarin": metadata[f"{type_name}Ch"],
        }
    ]


def parse_slash(text):
    """
    Parses the given text and replaces slashes (/) with spaces, while preserving certain patterns.

    Args:
        text (str): The input text to be parsed.

    Returns:
        str: The parsed text with slashes replaced by spaces, preserving certain patterns.

    Examples:
    >>> parse_slash("Hello/World")
    'Hello World'
    >>> parse_slash("aaa Hello/World bbb")
    'aaa Hello bbb aaa World bbb'
    """
    options = re.findall(r"\s?(\w+)\s*\/\s*(\w+)\s?", text)
    static_parts = re.split(r"\w+\s*\/\s*\w+", text)
    if len(options) == 0:
        return text.replace("/", " ")

    option1_text = ""
    option2_text = ""
    for static_parts_index, (option1, option2) in enumerate(options):
        static_part = static_parts[static_parts_index]
        option1_text += f"{static_part}{option1}"
        option2_text += f"{static_part}{option2}"

    return option1_text + static_parts[-1] + " " + option2_text + static_parts[-1]


def parse_slash_horizontally(raw_text_list: list[str]) -> list[str]:
    """
    Parses a list of raw text strings by splitting them at each '/' character and
    combining the corresponding parts horizontally.

    Args:
        raw_text_list (list[str]): A list of raw text strings to be parsed.

    Returns:
        list[str]: A list of parsed text strings, where each string is the result of
        combining the corresponding parts horizontally.

    Example:
    >>> raw_text_list = ['apple/banana', 'cat/dog', 'elephant/frog']
    >>> parse_slash_horizontally(raw_text_list)
    ['apple cat elephant', 'banana dog frog']
    """

    split_text_list = [text.strip().split("/") for text in raw_text_list]
    parsed_text_list = []
    for split_index in range(len(split_text_list[0])):
        parsed_text_list.append(
            " ".join(
                [split_text[split_index].strip() for split_text in split_text_list]
            )
        )

    return parsed_text_list


def parse_metadata(raw_metadata, type_id: str, only_one_audio: bool = False):
    if type_id in TYPE_ID_MP3_IDS_MAP.keys():
        if only_one_audio:
            return parse_metadata_with_multiple_text_one_audio(raw_metadata)

        return parse_metadata_with_multiple_text(raw_metadata)
    else:
        return parse_metadata_with_single_text(raw_metadata)
