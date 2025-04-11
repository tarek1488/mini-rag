### RAG PROMPTS ###
from string import Template

# System prompt
SYSTEM_PROMPT = Template(
    "\n".join(["You are a assistant to generate a response for a user",
                 "You will be provided by a set of documents associated with the user's query",
                 "You have to generate a response based on the documents provided",
                 "Ignore the documents that are not relevant to the user's query",
                 "If the answer not in the associated documents say i answer not found and do not answer",
                 "You can applogize to the user if you are not able to generate a response.",
                 "You have to generate response in the same language as the user's query.",
                 "Be polite and respectful to the user.",
                 "Be precise and concise in your response. Avoid unnecessary information.",])
)

# Document prompt
DOCUMENT_PROMPT  =  Template(
    "\n".join([
        "## Document No: $doc_num",
        "## Content: $chunck_text"
    ])
)

#Footer prompt
FOOTER_PROMPT = Template(
    "\n".join([
        "Based only on the above documents, please generate an answer for the user.",
        "## Question:  $question",
        "",
        "## Answer:",
    ])
)