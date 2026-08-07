# Technical Report

## AI Transcript Evaluation Framework

---

# 1. Project Overview

The objective of this project is to develop an AI-powered framework that evaluates the quality of automatically generated speech transcripts. Instead of relying on traditional string matching techniques, the framework performs semantic comparison between a generated transcript and a manually prepared ground truth transcript.

The system uses **Faster Whisper** for speech-to-text transcription and **Google Gemini AI** for semantic evaluation. The final output is a structured evaluation report containing detected transcription errors, an overall evaluation score, and a detailed score breakdown.

---

# 2. System Architecture

## Architecture

```text
                    User
                      │
                      ▼
           Web Interface (HTML/CSS/JS)
                      │
                      ▼
               FastAPI Backend
          ┌───────────┴───────────┐
          ▼                       ▼
   Faster Whisper            Gemini AI
(Audio Transcription)   (Semantic Comparison)
          │                       ▲
          │                       │
          ▼                       │
 Generated Transcript     Ground Truth Transcript
          └───────────────┬───────────────┘
                          ▼
                 Evaluation Report
                          │
                          ▼
                   Scoring Service
                          │
                          ▼
                   JSON API Response
```

## Workflow

1. The user uploads an audio file and provides the corresponding ground truth transcript.
2. Faster Whisper generates a transcript from the uploaded audio.
3. Gemini AI compares the generated transcript with the ground truth transcript.
4. The evaluator identifies:
   - Missing Information
   - Incorrect Information
   - Conflicting Information
   - Extra Information
5. The scoring service calculates the final evaluation score.
6. The API returns the structured evaluation report, which is displayed through the web interface.

---

# 3. Technologies Used

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Speech Recognition | Faster Whisper |
| LLM Evaluation | Google Gemini 3.5 Flash |
| Frontend | HTML, CSS, JavaScript |
| Data Format | JSON |
| Language | Python |

---

# 4. Approach Comparison

Several approaches were considered for transcript evaluation before selecting the final implementation.

| Approach | Advantages | Limitations |
|----------|------------|-------------|
| Exact String Matching | Simple and computationally efficient | Treats equivalent expressions as errors and cannot understand meaning |
| Edit Distance (Levenshtein) | Detects spelling differences | Unable to distinguish semantic equivalence from genuine errors |
| Rule-Based Comparison | Fully customizable | Requires numerous handcrafted rules and is difficult to maintain |
| **LLM-Based Semantic Evaluation (Chosen)** | Understands context, semantic meaning, and equivalent expressions while identifying genuine transcription errors | Depends on API availability and usage quotas |

The LLM-based approach was selected because transcript evaluation requires understanding language semantics rather than comparing individual characters or words. This significantly improves evaluation quality by reducing false positives caused by formatting variations.

---

# 5. Dataset and Evaluation

The evaluation dataset consists of **10 manually designed test cases**.

Each test case contains:

- Audio recording
- Ground truth transcript
- Generated transcript
- JSON evaluation report

The framework evaluates transcripts using the following categories:

- Missing Information
- Incorrect Information
- Conflicting Information
- Extra Information

A weighted scoring strategy is used to calculate the final evaluation score.

| Error Category | Penalty |
|---------------|--------:|
| Missing Information | 10 |
| Incorrect Information | 5 |
| Conflicting Information | 15 |
| Extra Information | 3 |

The score starts from **100**, and deductions are applied according to the detected errors.

---

# 6. Evaluation Results

The framework successfully generated structured evaluation reports for all test cases.

Each report includes:

- Generated Transcript
- Overall Score
- Score Breakdown
- Missing Information
- Incorrect Information
- Conflicting Information
- Extra Information

Example:

| Category | Count | Deduction |
|----------|------:|----------:|
| Missing Information | 1 | -10 |
| Incorrect Information | 2 | -10 |
| Conflicting Information | 0 | 0 |
| Extra Information | 1 | -3 |

Final Score:

```
100 - 10 - 10 - 3 = 77
```

The generated reports provide interpretable feedback, making it easier to understand why a particular transcript received its final score.

---

# 7. Trade-offs

## Advantages

- Modular architecture with clearly separated services.
- Local speech recognition using Faster Whisper.
- Semantic transcript evaluation instead of simple text comparison.
- Structured JSON reports suitable for further processing.
- Lightweight web interface for easy testing.

## Limitations

- Semantic evaluation depends on the availability of the Gemini API.
- Free-tier API usage is limited by request quotas.
- Penalty weights are manually defined and may require tuning for different applications.
- CPU-based transcription is slower than GPU execution for larger audio files.

---

# 8. Conclusion

This project presents an end-to-end framework for evaluating speech transcripts by combining local speech recognition with LLM-based semantic analysis. Compared with traditional text matching techniques, the proposed approach produces more meaningful evaluations by identifying genuine transcription errors while ignoring acceptable linguistic variations.

The modular design, structured JSON outputs, and lightweight web interface make the framework easy to extend and suitable for future improvements such as deployment, batch evaluation, and support for additional speech recognition models.