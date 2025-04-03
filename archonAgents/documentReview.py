from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.exa import ExaTools
from dotenv import load_dotenv
load_dotenv()

def documentReviewAG(prompt):
    # Contract Analyzer Agent
    contractAnalyzer = Agent(
        name = "Contract Analyzer Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on contract analysis",
        instructions=[
            "Review contract terms and conditions to identify key provisions and obligations.",
            "Identify potential issues, ambiguities, or unfavorable clauses in contracts.",
            "Suggest specific revisions to improve contract language and protect client interests.",
            "Highlight missing provisions that should be included for better protection.",
            "Identify potential enforcement challenges in contractual language.",
            "Flag unusual terms that deviate from industry standards.",
            "Present analysis in a structured format with clear recommendations."
        ],
        markdown=True,
        debug_mode=True,
    )

    # NDA Specialist Agent
    ndaSpecialist = Agent(
        name = "NDA Specialist Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on non-disclosure agreements",
        instructions=[
            "Review non-disclosure agreements to assess overall effectiveness and protection.",
            "Identify issues related to scope, duration, and enforceability of NDAs.",
            "Analyze definition of confidential information for appropriate breadth and specificity.",
            "Evaluate exceptions to confidentiality obligations for reasonableness.",
            "Suggest modifications to strengthen confidentiality protection.",
            "Assess remedies and enforcement mechanisms in NDAs.",
            "Highlight jurisdiction-specific NDA requirements and issues."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Employment Document Reviewer Agent
    employmentDocumentReviewer = Agent(
        name = "Employment Document Reviewer Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on employment documents",
        instructions=[
            "Analyze employment contracts, policies, handbooks, and other employment documents.",
            "Check for compliance with federal, state, and local employment laws.",
            "Identify potential liability areas in employment documents.",
            "Evaluate clarity of employment terms, conditions, and expectations.",
            "Assess appropriate classification of employees vs. independent contractors.",
            "Review termination provisions and processes for legal compliance.",
            "Highlight missing employment policies that should be included."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Intellectual Property Document Analyst Agent
    ipDocumentAnalyst = Agent(
        name = "IP Document Analyzer",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on intellectual property documents",
        instructions=[
            "Review IP assignments, licenses, and protection documents.",
            "Analyze scope of IP protection in relevant documents.",
            "Identify potential gaps in IP coverage or protection.",
            "Evaluate IP ownership and transfer provisions.",
            "Assess licensing terms for appropriate restrictions and permissions.",
            "Review IP enforcement and remedies provisions.",
            "Highlight territorial limitations in IP protection documents."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Legal Document Formatter Agent
    legalDocumentFormatter = Agent(
        name = "Legal Document Formatter",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on document formatting and standards",
        instructions=[
            "Ensure documents follow jurisdiction-specific formatting requirements.",
            "Standardize citation formats according to appropriate legal style guides.",
            "Check for required legal language, disclaimers, and notices.",
            "Verify proper document structure and organization.",
            "Ensure consistent terminology usage throughout documents.",
            "Check for appropriate signature blocks and execution requirements.",
            "Format documents for maximum readability and legal effectiveness."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Document Review Team (Master Router)
    documentReviewTeam = Team(
        name="Document Review Team",
        mode="route",
        model=Gemini("gemini-2.0-flash"),
        members=[
            contractAnalyzer,
            ndaSpecialist,
            employmentDocumentReviewer,
            ipDocumentAnalyst,
            legalDocumentFormatter,
        ],
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "You are a document review router that directs questions to the appropriate specialized legal document agent.",
            "Analyze each user query to determine which type of document review is most appropriate.",
            "Route questions about general contracts and their terms to the Contract Analyzer.",
            "Route questions about confidentiality agreements to the NDA Specialist.",
            "Route questions about employment contracts and workplace policies to the Employment Document Reviewer.",
            "Route questions about intellectual property documents and protections to the IP Document Analyst.",
            "Route questions about document formatting, citations, and required language to the Legal Document Formatter.",
            "If a document spans multiple areas, route to the agent that addresses the primary document type.",
            "Always include a brief explanation of why you routed to a particular agent.",
            "If a user submits a document that doesn't fit within these categories, politely explain the team's capabilities and suggest which agent might be most helpful.",
            "Always remind users that these agents provide informational document review only and not legal advice.",
            "Request that users specify the jurisdiction relevant to their document when applicable."
        ],
        show_members_responses=True,
    )
    response = documentReviewTeam.run(prompt)
    print(response.content)

# # Question for the Contract Analyzer
# document_review_team.print_response(
#     "I received this SaaS agreement from a vendor and I'm concerned about the liability limitations. Could you analyze the indemnification and limitation of liability clauses to see if they're balanced or overly favorable to the vendor?",
#     stream=True
# )

# # Question for the NDA Specialist
# document_review_team.print_response(
#     "Our startup is about to share our proprietary algorithm with potential investors. I've attached the NDA they provided. Can you review it and tell me if the definition of confidential information is comprehensive enough to protect our IP, and if the term of confidentiality is appropriate?",
#     stream=True
# )

# # Question for the Employment Document Reviewer
# document_review_team.print_response(
#     "We're a growing tech company that's implementing a new remote work policy for our employees across multiple states. Can you review this draft policy to ensure it covers necessary work-from-home requirements and doesn't create unintended liability issues, particularly regarding working hours and equipment?",
#     stream=True
# )

# # Question for the IP Document Analyst
# document_review_team.print_response(
#     "My company is entering into a joint development agreement where we'll be combining our existing patents with another company's technology. Can you review the IP ownership and licensing sections to ensure our pre-existing IP remains protected and that the newly developed IP rights are allocated fairly?",
#     stream=True
# )

# # Question for the Legal Document Formatter
# document_review_team.print_response(
#     "I'm preparing to file a motion for summary judgment in federal court in the Eastern District of Texas. Can you check if my document conforms to the local rules for formatting, including margins, font size, citation format, and required sections? I'm especially concerned about properly formatting my table of authorities.",
#     stream=True
# )