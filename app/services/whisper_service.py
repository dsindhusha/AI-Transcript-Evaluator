from pathlib import Path

from faster_whisper import WhisperModel


class WhisperService:
    """
    Handles speech-to-text transcription using the Faster Whisper model.
    """

    def __init__(self):
        """
        Loads the Faster Whisper model for audio transcription.
        """

        print("Loading Whisper model...")

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper model loaded.\n")

    def transcribe_audio(
        self,
        audio_path: Path,
        output_path: Path | None = None
    ) -> str:
        """
        Transcribes an audio file and optionally saves the
        generated transcript to a text file.

        Args:
            audio_path: Path to the input audio file.
            output_path: Optional path to save the generated transcript.

        Returns:
            The generated transcript as a string.
        """

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5
        )

        transcript = ""

        for segment in segments:
            transcript += segment.text.strip() + " "

        transcript = transcript.strip()

        if output_path is not None:

            output_path.write_text(
                transcript,
                encoding="utf-8"
            )

        return transcript