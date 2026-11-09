# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
"""Persist manually authored notes, then render the matching Encyclopedia entry."""
from pathlib import Path
from mine import atomic_json
from encyclopedia import write

def note(position, tag, problem, reasoning, impact, links, sources=None, confidence=None, status='draft'):
    value=dict(type=tag,status=status,problem=problem,reasoning=reasoning,impact=impact,links=links,
               source_notes=sources or 'No explicit external URL, paper, issue/PR number or HF repository is present in this commit message and diff. No external source was used for this entry. Evidence is the pinned raw diff and its parent context.',
               confidence=confidence or 'High confidence in the described code change. Purpose beyond the literal change is an inference, not an attributed statement of author intent. No GPU execution or benchmark reproduction was performed.')
    atomic_json(Path('seeds')/f'{position:06d}.json',value)
    write(position,value)
