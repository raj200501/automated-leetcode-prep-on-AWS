from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from automated_leetcode_prep.artifacts import PipelineArtifacts
from automated_leetcode_prep.config import PipelineConfig
from automated_leetcode_prep.step_functions import run_state_machine


@dataclass(frozen=True)
class PipelineResult:
    steps_run: Iterable[str]
    artifacts: PipelineArtifacts


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    result = run_state_machine(config)
    return PipelineResult(steps_run=result.steps_run, artifacts=result.artifacts)
