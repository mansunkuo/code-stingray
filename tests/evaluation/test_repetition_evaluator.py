# Copyright 2024 Mansun Kuo

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from code_stingray.evaluation.repetition_evaluator import RepetitionEvaluator


def test_repetition_evaluator():
    # Test data
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_repetition_evaluator")
    with open(
        os.path.join(test_data_dir, "reference.diff"), "r", encoding="utf-8"
    ) as f:
        reference = f.read()
    with open(
        os.path.join(test_data_dir, "prediction_repeated.md"), "r", encoding="utf-8"
    ) as f:
        prediction_repeated = f.read()
    with open(
        os.path.join(test_data_dir, "prediction_expected.md"), "r", encoding="utf-8"
    ) as f:
        prediction_expected = f.read()

    # Create the evaluator
    evaluator = RepetitionEvaluator()

    # Assertions
    eval_repeated = evaluator.evaluate_strings(
        prediction=prediction_repeated, reference=reference
    )
    assert eval_repeated["score"] > 0.8
    eval_expected = evaluator.evaluate_strings(
        prediction=prediction_expected, reference=reference
    )
    assert eval_expected["score"] < 0.3
