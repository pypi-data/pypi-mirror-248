import json
import pathlib
import tempfile
import uuid

from importlib_resources import files

from screenshot_ocr import cli


def test_tesseract_extract(
    capsys, caplog, equal_ignore_whitespace, collapse_whitespace
):
    # arrange
    spreadsheet_id = str(uuid.uuid4())
    input_dir = files("tests").joinpath("resources", "examples")

    expected_text = (
        collapse_whitespace(
            files("tests")
            .joinpath(
                "resources",
                "examples",
                "Screenshot 2023-06-16 at 18-49-13 Facebook.txt",
            )
            .read_text(),
        )
        .replace("QUESTION 17", "")
        .strip()
    )

    # act
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = pathlib.Path(temp_dir)

        output_dir = temp_path / "output"
        output_dir.mkdir()

        google_dir = temp_path / "google-oauth-creds"
        google_dir.mkdir()

        google_credentials = google_dir / "credentials.json"
        google_credentials.write_text(json.dumps({}))

        google_token = google_dir / "token.json"

        result = cli.main(
            [
                spreadsheet_id,
                "--input-dir",
                str(input_dir),
                "--output-dir",
                str(output_dir),
                "--google-credentials",
                str(google_credentials),
                "--google-token",
                str(google_token),
                "--no-move-images",
            ],
        )

    # assert
    assert result == 1

    cap_stdout, cap_stderr = capsys.readouterr()
    assert cap_stderr == ""
    equal_ignore_whitespace(cap_stdout, "")
    assert caplog.record_tuples == [
        ("screenshot_ocr.app", 20, "Starting Screenshot OCR."),
        (
            "screenshot_ocr.trivia",
            20,
            "Looking for screenshot images in " f"'{input_dir}'.",
        ),
        (
            "screenshot_ocr.app",
            20,
            f'"Screenshot 2023-06-16 at 18-49-13 Facebook.png": Q17) "{expected_text}"',
        ),
        ("screenshot_ocr.google_sheets", 20, "Starting authorisation flow."),
        (
            "screenshot_ocr.app",
            40,
            "Error: ValueError - Client secrets must be for a web or installed app.",
        ),
    ]
