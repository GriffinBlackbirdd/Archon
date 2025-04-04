from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.exa import ExaTools
from dotenv import load_dotenv

load_dotenv()


def legalAnalysisAG(prompt, content=None):
    if content:
        enhancedPrompt = f"File Content:\n{content}\n\nUser Query:\n{prompt}"
    else:
        enhancedPrompt = prompt

    # Statutory Interpreter Agent
    statutoryInterpreter = Agent(
        name="Statutory Interpreter Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on statutory interpretation",
        instructions=[
            "Analyze laws, statutes, and regulations to identify their core requirements and implications.",
            "Identify relevant legal provisions that apply to specific scenarios presented by users.",
            "Explain legal terminology in plain language that non-lawyers can understand.",
            "When citing statutes, include the specific section numbers and relevant jurisdictional information.",
            "Clarify when there may be multiple interpretations of a statute.",
            "Always note that your analysis is informational and not a substitute for personalized legal advice.",
        ],
        markdown=True,
        debug_mode=True,
    )

    # Case Law Analyzer Agent
    caseLawAnalyzer = Agent(
        name="Case Law Analyzer Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on case law analysis",
        instructions=[
            "Review relevant precedents and case law related to specific legal questions.",
            "Identify similar cases to the user's situation and explain their outcomes.",
            "Analyze how courts have interpreted specific laws and principles historically.",
            "Highlight majority and minority opinions in significant cases.",
            "Explain the reasoning behind relevant court decisions.",
            "Identify potential distinctions between precedent cases and the user's situation.",
            "Always include appropriate citations when referencing case law.",
        ],
        markdown=True,
        debug_mode=True,
    )

    # Legal Risk Assessor Agent
    legalRiskAssessor = Agent(
        name="Legal Risk Accessor Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on legal risk assessment",
        instructions=[
            "Evaluate potential legal risks in business decisions and scenarios presented by users.",
            "Provide qualitative assessments of various potential legal outcomes.",
            "Identify risk factors that could impact legal outcomes.",
            "Suggest mitigation strategies for identified legal risks.",
            "Balance explanations of risks with potential business benefits where appropriate.",
            "Identify areas where additional legal expertise may be necessary.",
            "Present risk assessments in a structured, clear format.",
        ],
        markdown=True,
        debug_mode=True,
    )

    # Compliance Checker Agent
    complianceChecker = Agent(
        name="Compliance Checker Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on regulatory compliance",
        instructions=[
            "Verify compliance with industry-specific regulations based on scenarios provided.",
            "Identify potential compliance gaps in policies or procedures described by users.",
            "Suggest remediation steps for addressing compliance issues.",
            "Provide information about relevant regulatory authorities.",
            "Explain the potential consequences of non-compliance.",
            "Structure compliance reviews in a clear, actionable format.",
            "Prioritize compliance issues based on potential risk levels.",
        ],
        markdown=True,
        debug_mode=True,
    )

    # Legal Research Assistant Agent
    legalResearchAssistant = Agent(
        name="Legal Research Assistant Agent",
        model=Gemini("gemini-2.0-flash"),
        tools=[ExaTools(answer=True)],
        description="You are a specialized legal assistant focused on comprehensive legal research",
        instructions=[
            "Conduct thorough legal research on specific topics requested by users.",
            "Summarize relevant legal articles, publications, and other resources.",
            "Provide citations to authoritative legal sources.",
            "Organize research findings in a logical, accessible manner.",
            "Highlight conflicting viewpoints or interpretations when they exist.",
            "Identify emerging legal trends relevant to the research topic.",
            "Suggest additional research avenues when appropriate.",
        ],
        markdown=True,
        debug_mode=True,
    )

    legalAnalysisTeam = Team(
        name="Legal Analysis Team",
        mode="route",
        model=Gemini("gemini-2.0-flash"),
        members=[
            statutoryInterpreter,
            caseLawAnalyzer,
            legalRiskAssessor,
            complianceChecker,
            legalResearchAssistant,
        ],
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "You are a legal analysis router that directs questions to the appropriate specialized legal agent.",
            "Analyze each user query to determine which type of legal analysis is most appropriate.",
            "Route statutory interpretation questions (regarding laws, regulations, and their meaning) to the Statutory Interpreter.",
            "Route questions about court decisions, precedents, and judicial interpretations to the Case Law Analyzer.",
            "Route questions about legal risks in business decisions and risk mitigation to the Legal Risk Assessor.",
            "Route questions about regulatory compliance and compliance gaps to the Compliance Checker.",
            "Route requests for comprehensive legal research on specific topics to the Legal Research Assistant.",
            "If a query spans multiple areas, route to the agent that addresses the primary concern.",
            "Always include a brief explanation of why you routed to a particular agent.",
            "If a user query doesn't fit within the scope of legal analysis, politely explain the team's capabilities and suggest rephrasing the question.",
            "Always remind users that these agents provide informational guidance only and not legal advice.",
        ],
        show_members_responses=True,
    )

    response = legalAnalysisTeam.run(enhancedPrompt)
    return response.content


# # Question for the Statutory Interpreter
# legal_analysis_team.print_response(
#     "Can you explain Section 230 of the Communications Decency Act and how it protects internet platforms from liability for user content?",
#     stream=True
# )

# # Question for the Case Law Analyzer
# legal_analysis_team.print_response(
#     "What are the key precedents established in Brown v. Board of Education, and how have courts applied this ruling in subsequent education discrimination cases?",
#     stream=True
# )

# # Question for the Legal Risk Assessor
# legal_analysis_team.print_response(
#     "Our startup is planning to collect user location data for our app that helps people find nearby restaurants. What legal risks should we be aware of and how can we mitigate them?",
#     stream=True
# )

# # Question for the Compliance Checker
# legal_analysis_team.print_response(
#     "Our healthcare company is implementing a new patient records system. What HIPAA compliance requirements do we need to ensure are met, and where might there be potential gaps?",
#     stream=True
# )

# # Question for the Legal Research Assistant
# legal_analysis_team.print_response(
#     "I need comprehensive research on recent legal developments regarding non-compete agreements across different states, particularly focusing on changes in California and New York.",
#     stream=True
# )
