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

from typing import Any, Optional, Union

from langchain.evaluation import StringEvaluator


# Define the function to detect repetition
def repetition_detector(input_text: str, output_text: str) -> float:
    input_words = set(input_text.lower().split())
    output_words = output_text.lower().split()
    overlap_count = sum(1 for word in output_words if word in input_words)
    repetition_ratio = float(overlap_count) / len(output_words)
    # return repetition_ratio > threshold
    return repetition_ratio


class RepetitionEvaluator(StringEvaluator):
    def _evaluate_strings(
        self,
        *,
        prediction: Union[str, Any],
        reference: Optional[Union[str, Any]] = None,
        input: Optional[Union[str, Any]] = None,  # pylint: disable=redefined-builtin
        **kwargs: Any,
    ) -> float:
        """Evaluate Chain or LLM output, based on optional input and label.

        Args:
            prediction (str): The LLM or chain prediction to evaluate.
            reference (Optional[str], optional): The reference label to evaluate against.
            input (Optional[str], optional): The input to consider during evaluation.
            kwargs: Additional keyword arguments, including callbacks, tags, etc.
        Returns:
            dict: The evaluation results containing the score or value.
                It is recommended that the dictionary contain the following keys:
                     - score: the score of the evaluation, if applicable.
                     - value: the string value of the evaluation, if applicable.
                     - reasoning: the reasoning for the evaluation, if applicable.
        """
        # Returns 1 if repetition is detected (bad), 0 otherwise
        return {"score": repetition_detector(reference, prediction)}
