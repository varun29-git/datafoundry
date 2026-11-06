"""Command line for the stock tokenizer in docs/hf-tokenizer."""

from __future__ import annotations

import argparse
import json
import sys

from tok65k.encoder import load


def _parse_ids(args: list[str]) -> list[int]:
    if len(args) == 1:
        text = args[0].strip()
        if text.startswith("["):
            data = json.loads(text)
            if isinstance(data, int) and not isinstance(data, bool):
                return [data]
            if not isinstance(data, list):
                raise ValueError("decode JSON must be a list of ids")
            return data
    parts: list[str] = []
    for arg in args:
        parts.extend(arg.replace(",", " ").split())
    if not parts:
        raise ValueError("decode needs token ids")
    return [int(part, 10) for part in parts]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tok65k",
        description="Encode and decode with the stock tokenizer in docs/hf-tokenizer.",
    )
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--dir",
        dest="tokenizer_dir",
        help="Hugging Face tokenizer directory. Defaults to docs/hf-tokenizer.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc_p = sub.add_parser("encode", parents=[shared], help="Print token ids as a JSON list.")
    enc_p.add_argument(
        "text",
        nargs="*",
        help="Text to encode. Separate words are joined with a space. Reads stdin if omitted.",
    )

    dec_p = sub.add_parser("decode", parents=[shared], help="Print the text for token ids.")
    dec_p.add_argument(
        "ids",
        nargs="*",
        help="Token ids, a comma-separated list, or one JSON list. Reads stdin if omitted.",
    )

    args = parser.parse_args(argv)
    try:
        tok = load(args.tokenizer_dir)
        if args.cmd == "encode":
            text = " ".join(args.text) if args.text else sys.stdin.read()
            json.dump(tok.encode(text), sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
            return 0
        raw = list(args.ids)
        if not raw:
            raw = [sys.stdin.read()]
        sys.stdout.write(tok.decode(_parse_ids(raw)))
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"tok65k: {exc}", file=sys.stderr)
        return 1
