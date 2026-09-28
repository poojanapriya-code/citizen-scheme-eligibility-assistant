from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class CitizenState(TypedDict, total=False):
    name: str
    age: int
    income: float
    occupation: str
    state: str
    category: str
    land_acres: float
    student_type: str
    first_generation: bool
    language: str
    profile_complete: bool
    missing_fields: list
    eligible_schemes: list
    documents: list
    application_draft: str
    final_response: str
SCHEMES = [
    {
        "name": "PM-KISAN",
        "category": "farmer",
        "description":
            "Income support scheme for eligible landholding farmer families.",
        "benefit":
            "Eligible farmer families may receive income support under PM-KISAN.",
        "conditions": [
            "Applicant should be a farmer/farmer family.",
            "Landholding and other scheme conditions must be satisfied.",
            "Exclusion conditions specified in official guidelines may apply."
        ],
        "documents": [
            "Land ownership / land record",
            "Identity document",
            "Bank account information when required by the official application process"
        ],
        "steps": [
            "Check the latest eligibility rules.",
            "Check farmer registration/status on the official PM-KISAN portal.",
            "Complete the official application/registration process if eligible.",
            "Complete required verification/eKYC through the official process."
        ],
        "source":
            "https://pmkisan.gov.in/"
    },
    {
        "name": "National Scholarship Portal Schemes",
        "category": "student",
        "description":
            "Scholarship schemes available through the National Scholarship Portal.",
        "benefit":
            "Financial assistance may be available under applicable scholarship schemes.",
        "conditions": [
            "Student must satisfy the eligibility conditions of the selected scheme.",
            "Academic, income, category and other scheme-specific conditions may apply.",
            "Application deadlines must be checked on the official portal."
        ],
        "documents": [
            "Student/institution details",
            "Income certificate if required",
            "Category certificate if required",
            "Other scheme-specific documents"
        ],
        "steps": [
            "Visit the National Scholarship Portal.",
            "Check available schemes and their eligibility criteria.",
            "Complete required registration/OTR process.",
            "Submit the scholarship application.",
            "Track application status on the official portal."
        ],

        "source":
            "https://scholarships.gov.in/"
    },
    {
        "name": "PMAY-Urban",
        "category": "low income",
        "description":
            "Housing assistance under the applicable PMAY-Urban provisions.",
        "benefit":
            "Housing-related assistance may be available to eligible beneficiaries.",
        "conditions": [
            "Eligibility depends on the applicable PMAY-Urban component.",
            "Income, housing and other scheme-specific conditions may apply.",
            "Final eligibility is determined by the concerned authorities."
        ],
        "documents": [
            "Identity document",
            "Address/residence proof",
            "Income-related documents if required",
            "Other component-specific documents"
        ],
        "steps": [
            "Check the applicable PMAY-Urban component.",
            "Review the latest eligibility requirements.",
            "Submit the required assessment/application.",
            "Track the application through the official portal."
        ],
        "source":
            "https://www.pmaymis.gov.in/"
    }
]
def profile_collector(state: CitizenState):

    print("\n================================")
    print("       PROFILE COLLECTOR")
    print("================================")
    required_fields = [
        "name",
        "age",
        "state",
        "category"
    ]
    missing = []
    for field in required_fields:
        if field not in state:
            missing.append(field)
    if missing:
        print("Missing information:", missing)
        return {
            "profile_complete": False,
            "missing_fields": missing
        }
    return {
        "profile_complete": True,
        "missing_fields": []
    }
def eligibility_agent(state: CitizenState):
    print("\n================================")
    print("       ELIGIBILITY AGENT")
    print("================================")
    category = state["category"].lower()
    state_name = state["state"].lower()
    schemes_found = []
    for scheme in SCHEMES:
        if state_name != "tamil nadu":
            continue
        if category == scheme["category"]:
            if scheme["name"] == "PM-KISAN":
                land = state.get("land_acres", 0)
                if land <= 0:
                    continue
            schemes_found.append(scheme)
    return {
        "eligible_schemes": schemes_found
    }
def document_agent(state: CitizenState):
    print("\n================================")
    print("         DOCUMENT AGENT")
    print("================================")
    all_documents = set()
    for scheme in state.get("eligible_schemes", []):
        for document in scheme["documents"]:
            all_documents.add(document)
    return {
        "documents": list(all_documents)
    }
def application_agent(state: CitizenState):
    print("\n================================")
    print("       APPLICATION AGENT")
    print("================================")
    schemes = state.get("eligible_schemes", [])
    if not schemes:
        return {
            "application_draft":
                "No application draft generated because no matching scheme was found."
        }
    scheme_names = []
    for scheme in schemes:
        scheme_names.append(scheme["name"])
    draft = f"""
-----------------------------------------
DRAFT APPLICATION
-----------------------------------------
Applicant Name : {state["name"]}
Age            : {state["age"]}
State          : {state["state"]}
Category       : {state["category"]}
Possible Scheme(s):
{", ".join(scheme_names)}
Declaration:
I request consideration for the applicable government
scheme based on the information provided by me.
I understand that this is only a draft and that the
concerned government department will verify my details
and make the final eligibility decision.

-----------------------------------------
"""
    return {
        "application_draft": draft
    }
def response_agent(state: CitizenState):

    schemes = state.get("eligible_schemes", [])
    language = state.get("language", "English").lower()

    if not schemes:
        if language == "tamil":
            response = """
========== RESULT ==========

உங்கள் தகவலுக்கு பொருந்தக்கூடிய திட்டம் கிடைக்கவில்லை.
"""
        elif language == "tanglish":
            response = """
========== RESULT ==========

Ungal information-ku matching scheme kidaikkavillai.
"""
        else:
            response = """
========== RESULT ==========

No matching scheme found.
"""
        return {"final_response": response}

    response = """
========================================
       CITIZEN SCHEME ASSISTANT
========================================
"""

    for scheme in schemes:
        response += f"""
Scheme:
{scheme["name"]}

Benefit:
{scheme["benefit"]}

Documents Needed:
"""

        for document in scheme["documents"]:
            response += f"- {document}\n"

        response += f"""
Application:
{scheme["steps"][0]}

Official Website:
{scheme["source"]}

----------------------------------------
"""

    response += """
Note:
Final eligibility is decided by the concerned
government department.
"""

    return {"final_response": response}


def profile_router(state: CitizenState):
    if state.get("profile_complete"):
        return "eligibility"
    return "end"
graph = StateGraph(CitizenState)
graph.add_node(
    "profile_collector",
    profile_collector
)
graph.add_node(
    "eligibility",
    eligibility_agent
)
graph.add_node(
    "documents",
    document_agent
)
graph.add_node(
    "application",
    application_agent
)
graph.add_node(
    "response",
    response_agent
)
graph.add_edge(
    START,
    "profile_collector"
)
graph.add_conditional_edges(
    "profile_collector",
    profile_router,
    {
        "eligibility": "eligibility",
        "end": END
    }
)
graph.add_edge(
    "eligibility",
    "documents"
)
graph.add_edge(
    "documents",
    "application"
)
graph.add_edge(
    "application",
    "response"
)
graph.add_edge(
    "response",
    END
)
app = graph.compile()
if __name__ == "__main__":
    print("\n")
    print("================================================")
    print("       CITIZEN SCHEME ELIGIBILITY ASSISTANT")
    print("================================================")
    print("\nPlease provide basic information.")
    print("Do NOT enter Aadhaar number, bank account number,")
    print("OTP, password or other sensitive information.\n")
    name = input("Enter your name: ")
    age = int(
        input("Enter your age: ")
    )
    state_name = input(
        "Enter your state: "
    )
    category = input(
        "\nCategory:\n"
        "1. Farmer\n"
        "2. Student\n"
        "3. Low Income\n"
        "Enter category: "
    )
    if category == "1":
        category = "Farmer"
        land = float(
            input("Enter land area in acres: ")
        )
    elif category == "2":
        category = "Student"
        land = 0
    elif category == "3":
        category = "Low Income"
        land = 0
    else:
        print("\nInvalid category.")
        exit()
    print("\nPreferred language:")
    print("1. English")
    print("2. Tamil")
    print("3. Tanglish")
    language_choice = input(
        "Enter choice: "
    )
    if language_choice == "2":
        language = "Tamil"
    elif language_choice == "3":
        language = "Tanglish"
    else:
        language = "English"
    citizen = {
        "name": name,
        "age": age,
        "state": state_name,
        "category": category,
        "land_acres": land,
        "language": language
    }
    result = app.invoke(citizen)
    print(
        result["final_response"]
    )