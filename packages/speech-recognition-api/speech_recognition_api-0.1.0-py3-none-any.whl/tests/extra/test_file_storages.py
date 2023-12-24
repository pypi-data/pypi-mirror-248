from io import BytesIO

import pytest


@pytest.mark.parametrize(
    "storage",
    [
        pytest.lazy_fixture("local_storage"),
        pytest.lazy_fixture("google_cloud_storage"),
        pytest.lazy_fixture("s3_storage"),
    ],
)
def test_file_storage(storage, audio_file_generator):
    orig_content = next(audio_file_generator()).read()
    file_id = storage.save_file(BytesIO(orig_content))
    assert file_id

    read_file = storage.get_file(file_id)
    read_content = read_file.read()
    assert read_content == orig_content
    assert len(read_content) > 0
