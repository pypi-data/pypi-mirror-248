"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


from typing import List
from kink import di
import json
from langchain.prompts.prompt import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import GuardrailsOutputParser
from ..tools import ExpandConceptsTool

from .. import MedPrompter
med_prompter = MedPrompter()
import logging
_logger = logging.getLogger(__name__)

main_llm = di["rag_chain_main_llm"]
clinical_llm = di["rag_chain_clinical_llm"]

rail_spec = """
<rail version="0.1">
<output>
    <object name="response" format="length: 1">
        <string
            name="concepts"
            description="The list of concepts extracted from the clinical document."
            format="list"
            on-fail-length="reask"
        />
    </object>
</output>


<prompt>

Given the following clinical document, extract the single main clinical concept and return it as a single item list.
If the concept has two words, return them as a single word joined by an underscore.

Clinical document: ${clinical_document}
${gr.complete_json_suffix_v2}

</prompt>
</rail>

"""


class ClinicalConceptInput(BaseModel):
    clinical_document: str = Field()
    word_count: str = Field()



clinical_concepts_output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, api=main_llm)

CLINICAL_CONCEPT_INPUT_PROMPT = PromptTemplate(
    template=clinical_concepts_output_parser.guard.prompt.escape(),
    input_variables=["clinical_document"],
)

CLINICAL_CONCEPT_SUMMARY_TEMPLATE = """
You are summarizing the clinical document below. These {clinical_concepts} may be included in the summary.

Clinical Document: {clinical_document}.
Summary:"""

CLINICAL_CONCEPT_SUMMARY_PROMPT = PromptTemplate(
    template=CLINICAL_CONCEPT_SUMMARY_TEMPLATE,
    input_variables=["clinical_concepts", "clinical_document"],
)


def extract_concepts(guardrails_output):
    """Extract the concepts from the clinical document."""
    _gr = json.loads(guardrails_output)
    return _gr["response"]

def concat_concepts(concepts: List[str]):
    """Concatenate the concepts."""
    return " ".join(concepts)



def get_runnable(**kwargs):
    """Get the runnable chain."""
    list_of_concepts = RunnablePassthrough.assign(
        clinical_document=lambda x: x["clinical_document"],
    ) | CLINICAL_CONCEPT_INPUT_PROMPT | main_llm | StrOutputParser() | extract_concepts |  ExpandConceptsTool().run | concat_concepts
    clinical_document = RunnablePassthrough.assign(
        clinical_document = lambda x: x["clinical_document"] + "\n" + "Summarize to " + x["word_count"] + " words. Summary: ",
    )
    _inputs = RunnableMap(
        clinical_concepts=list_of_concepts,
        clinical_document=clinical_document,
    )
    _chain = _inputs | CLINICAL_CONCEPT_SUMMARY_PROMPT | main_llm | StrOutputParser()
    chain = _chain.with_types(input_type=ClinicalConceptInput)
    return chain

@tool("clinical summary", args_schema=ClinicalConceptInput)
def get_summary_tool(**kwargs):
    """
    Summarize the clinical document to a given word count.

    Args:
        clinical_document (str): The clinical document to summarize.
        word_count (str): The number of words to summarize to.
    """
    return get_runnable().invoke(kwargs)
