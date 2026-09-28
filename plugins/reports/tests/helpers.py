"""
Helpers for the tests of the reports plugin: in-memory templates, and the raw
values a renderer emitted — what a template computed, before formatting.
"""


def make_template(bands: dict, **extra) -> dict:
    """Build an in-memory template from {band_name: [cell_content, ...]}.

    Each band gets one row; each content string becomes one text cell.
    """
    rows = []
    for name, contents in bands.items():
        cells = [
            {"id": f"{name}_{i}", "type": "text", "content": c, "width": 100}
            for i, c in enumerate(contents)
        ]
        rows.append({"name": name, "height": 20, "cells": cells})
    return {"rows": rows, **extra}


def emitted_values(r) -> list:
    """Values of all compiled records of renderer *r*, in emission order."""
    r.compile()
    return [v for rec in r._compiled for v in rec.get("values", [])]
