def parse_vocabulary_metadata(vocabulary_metadata, dialect_id):
    core_metadata = []

    lesson_id = vocabulary_metadata["lessonNo"]
    vocabulary_number = int(vocabulary_metadata["vocabularyNum"])
    for i in range(vocabulary_number):
        text_key = f"Ab_{i+1}"
        mandarin_key = f"Ch_{i+1}"

        if (
            vocabulary_metadata[text_key] is None
            or len(vocabulary_metadata[text_key]) == 0
        ):
            continue

        core_metadata.append(
            {
                "text": vocabulary_metadata[text_key],
                "raw_text": None,
                "mandarin": vocabulary_metadata[mandarin_key],
                "audio_name": f"{dialect_id}_{lesson_id}_V{i+1}.mp3",
                "dialect_id": dialect_id,
            }
        )
    return core_metadata
