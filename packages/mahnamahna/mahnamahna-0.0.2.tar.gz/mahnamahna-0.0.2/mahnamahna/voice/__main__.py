"""Transcription command line application."""

import sys

from mahnamahna import voice


def transcribe():
    print("\r\n\r\n".join(". ".join(phrases) + "." for phrases in voice.transcribe()))
    sys.exit()


if __name__ == "__main__":
    transcribe()
