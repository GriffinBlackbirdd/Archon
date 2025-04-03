from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.exa import ExaTools
from dotenv import load_dotenv
load_dotenv()

def caseEvaluationAG(prompt):
    # Litigation Probability Assessor Agent
    litigationProbabilityAssessor = Agent(
        name = "Litigation Probability Assesor Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on litigation probability assessment",
        instructions=[
            "Evaluate strengths and weaknesses of potential litigation cases.",
            "Estimate probability of success based on facts provided and applicable law.",
            "Identify key legal hurdles that might affect case outcomes.",
            "Suggest evidence gathering strategies to strengthen case positions.",
            "Highlight precedent cases with similar fact patterns and their outcomes.",
            "Assess procedural and jurisdictional factors that may impact case success.",
            "Provide balanced analysis of both favorable and unfavorable case aspects."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Settlement Value Calculator Agent
    settlementValueCalculator = Agent(
        name = "Settlement Value Calculator Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on settlement value analysis",
        instructions=[
            "Analyze potential settlement values based on similar case precedents.",
            "Provide reasonable ranges for settlement amounts given case specifics.",
            "Identify factors that could increase or decrease settlement value.",
            "Compare potential settlement value against likely litigation costs.",
            "Analyze risk-adjusted values of proceeding to trial versus settling.",
            "Consider jurisdiction-specific settlement trends when relevant.",
            "Factor in both economic and non-economic damages in valuations."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Case Strategy Advisor Agent
    caseStrategyAdvisor = Agent(
        name = "Case Strategy Advisor Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on legal case strategy",
        instructions=[
            "Suggest potential legal strategies for specific case types.",
            "Identify optimal procedural approaches based on case circumstances.",
            "Outline realistic timelines and critical path for case resolution.",
            "Recommend strategic motions and filings appropriate to the case.",
            "Anticipate likely opposing strategies and suggest counter-approaches.",
            "Identify key decision points in the litigation process.",
            "Suggest appropriate alternative dispute resolution options when relevant."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Expert Witness Finder Agent
    expertWitnessFinder = Agent(
        name = "Export Witness Finder Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on expert witness selection",
        instructions=[
            "Identify types of expert witnesses needed for specific case types.",
            "Suggest qualifications and credentials to look for in potential experts.",
            "Outline key questions for expert witnesses based on case issues.",
            "Suggest areas of testimony where expert opinions would be most valuable.",
            "Identify potential challenges to expert witness credibility.",
            "Provide guidance on expert witness report requirements.",
            "Suggest strategies for effective expert witness preparation."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Client Intake Analyzer Agent
    clientIntakeAnalyzer = Agent(
        name = "Client Intake Analyzer Agent",
        model=Gemini("gemini-2.0-flash"),
        description="You are a specialized legal assistant focused on initial case assessment",
        instructions=[
            "Process initial client information to identify key legal issues.",
            "Identify relevant legal categories and potential claims from client descriptions.",
            "Suggest additional questions to clarify the legal situation.",
            "Identify potential jurisdictional and venue issues.",
            "Flag urgent deadlines or statute of limitations concerns.",
            "Recognize potential conflicts of interest from initial information.",
            "Organize client information in a structured format for attorney review."
        ],
        markdown=True,
        debug_mode=True,
    )

    # Case Evaluation Team (Master Router)
    caseEvaluationTeam = Team(
        name="Case Evaluation Team",
        mode="route",
        model=Gemini("gemini-2.0-flash"),
        members=[
            litigationProbabilityAssessor,
            settlementValueCalculator,
            caseStrategyAdvisor,
            expertWitnessFinder,
            clientIntakeAnalyzer
        ],
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "You are a case evaluation router that directs questions to the appropriate specialized legal case evaluation agent.",
            "Analyze each user query to determine which type of case evaluation is most appropriate.",
            "Route questions about case strength and success probability to the Litigation Probability Assessor.",
            "Route questions about potential settlement values and monetary compensation to the Settlement Value Calculator.",
            "Route questions about case approach, procedure, and timeline to the Case Strategy Advisor.",
            "Route questions about expert witnesses and specialized testimony to the Expert Witness Finder.",
            "Route questions about new client matters and initial case assessment to the Client Intake Analyzer.",
            "If a query spans multiple areas, route to the agent that addresses the primary concern.",
            "Always include a brief explanation of why you routed to a particular agent.",
            "If a user query doesn't fit within these categories, politely explain the team's capabilities and suggest rephrasing.",
            "Always remind users that these agents provide informational analysis only and not legal advice.",
            "Request additional case details when information provided is insufficient for proper routing."
        ],
        show_members_responses=True,
    )

    response = caseEvaluationTeam.run(prompt)
    print(response.content)


# # Question for the Litigation Probability Assessor
# case_evaluation_team.print_response(
#     "Our company is considering filing a breach of contract lawsuit against a supplier who failed to deliver critical components on time, causing us to miss our production deadlines and lose an estimated $500,000 in sales. We have the signed contract with clear delivery dates and documentation of all our communications requesting updates. What's our likelihood of success if we pursue litigation?",
#     stream=True
# )

# # Question for the Settlement Value Calculator
# case_evaluation_team.print_response(
#     "I was injured in a car accident where the other driver ran a red light. I have $30,000 in medical bills, missed 2 months of work (losing $15,000 in wages), and have ongoing pain that my doctor says might be permanent. The accident happened in Florida. What would be a reasonable settlement range to consider if the other driver's insurance company wants to negotiate?",
#     stream=True
# )

# # Question for the Case Strategy Advisor
# case_evaluation_team.print_response(
#     "We're defending a medium-sized tech company against a patent infringement claim. The plaintiff alleges our client's software violates two of their patents, but we believe there's prior art that invalidates their claims. What's the best strategic approach to this case, and what would a realistic timeline look like from filing our response through resolution?",
#     stream=True
# )

# # Question for the Expert Witness Finder
# case_evaluation_team.print_response(
#     "We're representing a client in a medical malpractice case involving a surgical error during a cardiac procedure. The hospital is claiming the complication was a known risk rather than negligence. What types of expert witnesses would strengthen our case, what qualifications should they have, and what key questions should we ask them?",
#     stream=True
# )

# # Question for the Client Intake Analyzer
# case_evaluation_team.print_response(
#     "A potential client just called about a situation with their neighbor. They built a fence that our potential client believes is partially on their property. They've had verbal arguments about it, and the neighbor has now installed security cameras that seem to be pointing at our potential client's backyard. The property is in a suburban area of Illinois. What legal issues should we be considering here?",
#     stream=True
# )