# AI Medical Advisory System — AutoGen
A multi-agent AI system for medical case analysis using Microsoft AutoGen framework.

> ⚠️ **DISCLAIMER**: This system is for educational/research purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

## Architecture

```
User Input (Patient Case)
        │
        ▼
┌─────────────────────┐
│  PatientIntakeAgent │  ← Structures patient data
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   DiagnosisAgent    │  ← Analyzes symptoms, suggests diagnoses
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   TreatmentAgent    │  ← Recommends treatment plans
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   PharmacistAgent   │  ← Checks drug interactions & safety
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────┐
│  MedicalReviewerAgent    │  ← Final synthesis & recommendations
└──────────────────────────┘
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env and add your OpenAI API key

# 3. Run the system
python main.py
```

## Project Structure

```
Agentic-AIProject/
├── main.py           # Entry point
├── agents.py         # Agent definitions & group chat setup
├── patient_cases.py  # Sample patient test cases
├── requirements.txt
└── .env.example
```

## Sample Cases Included

| Case | Description |
|------|-------------|
| case_1 | 58M diabetic patient with chest pain & hypertension |
| case_2 | 28F with recurring migraines on oral contraceptives |
| case_3 | 72F with joint pain, NSAID allergy, and GERD |

## How It Works

1. You provide a patient case (or select a sample)
2. **PatientIntakeAgent** structures the information
3. **DiagnosisAgent** suggests top 3 differential diagnoses
4. **TreatmentAgent** recommends treatment options
5. **PharmacistAgent** reviews for drug interactions
6. **MedicalReviewerAgent** produces the final advisory report
