import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

# ── Azure OpenAI Client ───────────────────────────────────────────────────────
model_client = AzureOpenAIChatCompletionClient(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "gpt-4o",
        "structured_output": True,
    },
)

# ── Agents ────────────────────────────────────────────────────────────────────
patient_intake_agent = AssistantAgent(
    name="PatientIntakeAgent",
    model_client=model_client,
    system_message="""You are a medical intake specialist. Your job is to:
- Collect and structure patient information (age, gender, symptoms, duration, medical history, current medications)
- Output a structured patient summary for other agents
- Do NOT diagnose or recommend treatments""",
)

diagnosis_agent = AssistantAgent(
    name="DiagnosisAgent",
    model_client=model_client,
    system_message="""You are an experienced medical diagnostician. Based on the structured patient summary:
- List the top 3 most likely diagnoses with reasoning
- Mention red flag symptoms that need urgent attention
- Suggest necessary diagnostic tests (blood work, imaging, etc.)
- Always note: 'This is AI-assisted analysis, not a substitute for professional medical advice'""",
)

treatment_agent = AssistantAgent(
    name="TreatmentAgent",
    model_client=model_client,
    system_message="""You are a treatment planning specialist. Based on the diagnoses provided:
- Recommend first-line treatment options for each diagnosis
- Include both pharmacological and non-pharmacological approaches
- Specify dosage ranges and duration where applicable
- Flag any contraindications based on patient history""",
)

pharmacist_agent = AssistantAgent(
    name="PharmacistAgent",
    model_client=model_client,
    system_message="""You are a clinical pharmacist. Review the treatment plan and:
- Check for drug-drug interactions with current medications
- Check for drug-allergy conflicts
- Suggest safer alternatives if interactions are found
- Verify dosages are within safe ranges for the patient's profile""",
)

medical_reviewer_agent = AssistantAgent(
    name="MedicalReviewerAgent",
    model_client=model_client,
    system_message="""You are the senior medical reviewer. Synthesize all agent outputs and produce:
1. Final Patient Summary
2. Most Likely Diagnosis
3. Approved Treatment Plan (post pharmacist review)
4. Urgent Actions (if any)
5. Follow-up Recommendations
End with: 'DISCLAIMER: This AI system is for educational purposes only. Always consult a licensed physician.'
When done, write TERMINATE.""",
)

# ── Team Setup ────────────────────────────────────────────────────────────────
def create_medical_team():
    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        participants=[
            patient_intake_agent,
            diagnosis_agent,
            treatment_agent,
            pharmacist_agent,
            medical_reviewer_agent,
        ],
        termination_condition=termination,
        max_turns=10,
    )
    return team
