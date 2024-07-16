def parse_content_metadata(content_metadata, dialect_id):
    core_metadata = []

    sententce_count = 1
    lesson_id = content_metadata["lessonId"]
    while True:
        text_key = f"con_AB{sententce_count}"
        mandarin_key = f"con_CH{sententce_count}"
        if text_key not in content_metadata:
            break

        if (
            content_metadata[text_key] is not None
            and len(content_metadata[text_key]) > 0
        ):
            core_metadata.append(
                {
                    "text": content_metadata[text_key],
                    "raw_text": None,
                    "mandarin": content_metadata[mandarin_key],
                    "audio_name": f"{dialect_id}c{lesson_id}s{sententce_count}.mp3",
                }
            )
        sententce_count += 1
    return core_metadata


def parse_word_metadata(word_metadata, dialect_id):
    core_metadata = []
    word_count = 1
    lesson_id = word_metadata["lessonId"]
    while True:
        text_key = f"word_AB{word_count}"
        mandarin_key = f"word_CH{word_count}"

        if text_key not in word_metadata:
            break

        if word_metadata[text_key] is not None and len(word_metadata[text_key]) > 0:
            normalized_text = word_metadata[text_key]
            if "/" in normalized_text:
                normalized_text = normalized_text.replace("/", " ")

            core_metadata.append(
                {
                    "text": normalized_text,
                    "raw_text": word_metadata[text_key],
                    "mandarin": word_metadata[mandarin_key],
                    "audio_name": f"{dialect_id}c{lesson_id}w{word_count}.mp3",
                }
            )
        word_count += 1
    return core_metadata
