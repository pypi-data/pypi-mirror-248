import re
from typing import List, Union, Optional

from faker import Generator

from presidio_evaluator.data_generator.faker_extensions import (
    FakerSpansResult,
    FakerSpan,
)

_re_token = re.compile(r"\{\{\s*(\w+)(:\s*\w+?)?\s*\}\}")


class SpanGenerator(Generator):
    """Generator which also returns the indices of fake values.

    :example:
    >>>from faker import Faker
    >>>from presidio_evaluator.data_generator.faker_extensions import SpanGenerator

    >>>generator = SpanGenerator()
    >>>faker = Faker(generator=generator)
    >>>res = faker.parse("My child's name is {{name}}", add_spans=True)

    >>>res.spans
        [{"value": "Daniel Gallagher", "start": 19, "end": 35, "type": "name"}]
    >>>res.fake
        "My child's name is Daniel Gallagher"
    >>>str(res)
        "My child's name is Daniel Gallagher"
    """

    def parse(
        self, text: str, add_spans: bool = False, template_id: Optional[int] = None
    ) -> Union[str, FakerSpansResult]:
        """Parses a Faker template.

        This replaces the original parse method to introduce spans.
        :param text: Text holding the faker template, e.g. "My name is {{name}}".
        :param add_spans: Whether to return the spans of each fake value in the output string
        :param template_id: Template ID to be returned with the output
        """

        # Create Span objects for original placeholders
        spans = self._match_to_span(text)

        # Reverse for easier index handling while replacing
        spans = sorted(spans, reverse=True, key=lambda x: x.start)

        fake_text = ""
        prev_end = len(text)  # we are going backwards

        # Update indices and fake text based on new values
        for i, span in enumerate(spans):
            formatter = span.type
            old_len = len(formatter) + 4  # adding two curly brackets
            new_len = len(str(span.value))

            # Update full text
            fake_text = str(text[span.end: prev_end]) + str(fake_text)
            fake_text = str(span.value) + str(fake_text)
            prev_end = span.start

            if add_spans:  # skip if spans aren't required
                # Update span indices
                delta = new_len - old_len
                span.end = span.end + delta
                span.type = formatter.strip()

                # Update previously inserted spans since indices shifted
                for j in range(0, i):
                    spans[j].start += delta
                    spans[j].end += delta

        # Add the beginning of the sentence
        fake_text = text[0:prev_end] + fake_text

        return (
            FakerSpansResult(
                fake=fake_text, spans=spans, template=text, template_id=template_id
            )
            if add_spans
            else fake_text
        )

    def _match_to_span(self, text: str, **kwargs) -> List[FakerSpan]:
        matches = _re_token.finditer(text)

        results: List[FakerSpan] = []
        for match in matches:
            formatter = match.group()[2:-2].lower()
            results.append(
                FakerSpan(
                    type=formatter,
                    start=match.start(),
                    end=match.end(),
                    value=str(self.format(formatter.strip(), **kwargs)),
                )
            )

        return results
