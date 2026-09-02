"""INI-CET (AIIMS PG) curriculum: subjects, topics, 8-week study block."""

from __future__ import annotations

SUBJECTS = [
    {"id": "anatomy", "name": "Anatomy", "theory_marks": 15, "internal_marks": 0, "color": "#6B3A2E"},
    {"id": "physiology", "name": "Physiology", "theory_marks": 15, "internal_marks": 0, "color": "#2F5D50"},
    {"id": "biochem", "name": "Biochemistry", "theory_marks": 8, "internal_marks": 0, "color": "#5C4B8A"},
    {"id": "pharma", "name": "Pharmacology", "theory_marks": 18, "internal_marks": 0, "color": "#8A4B6B"},
    {"id": "pathology", "name": "Pathology", "theory_marks": 18, "internal_marks": 0, "color": "#8A3D3D"},
    {"id": "micro", "name": "Microbiology", "theory_marks": 12, "internal_marks": 0, "color": "#3D6B8A"},
    {"id": "medicine", "name": "Medicine", "theory_marks": 30, "internal_marks": 0, "color": "#2F4A8A"},
    {"id": "surgery", "name": "Surgery", "theory_marks": 25, "internal_marks": 0, "color": "#4A4A4A"},
    {"id": "psm", "name": "PSM", "theory_marks": 18, "internal_marks": 0, "color": "#6B6B2F"},
    {"id": "obg", "name": "OBG", "theory_marks": 20, "internal_marks": 0, "color": "#8A5A7A"},
    {"id": "peds", "name": "Pediatrics", "theory_marks": 12, "internal_marks": 0, "color": "#3A8A7A"},
    {"id": "ortho", "name": "Orthopedics", "theory_marks": 10, "internal_marks": 0, "color": "#7A6B55"},
    {"id": "ent_ophth", "name": "ENT & Ophthalmology", "theory_marks": 8, "internal_marks": 0, "color": "#557A8A"},
    {"id": "forensic", "name": "Forensic & Psychiatry", "theory_marks": 6, "internal_marks": 0, "color": "#5A5A5A"},
]

WEEK_PLAN = [
    {"week": 1, "title": "Anatomy foundations + General Physiology", "subjects": ["anatomy", "physiology"], "focus": "Upper/lower limb, thorax, cell & nerve-muscle physiology.", "mock": "50 MCQs - anatomy + physiology mix."},
    {"week": 2, "title": "Head & neck / Neuro + CVS & Respiratory", "subjects": ["anatomy", "physiology"], "focus": "Neuroanatomy, cranial nerves, cardiac cycle, lung volumes.", "mock": "50 MCQs timed - image-based anatomy."},
    {"week": 3, "title": "Biochemistry + Pharmacology core", "subjects": ["biochem", "pharma"], "focus": "Metabolism, ANS/CNS drugs, antibiotics, antihypertensives.", "mock": "50 MCQs - mechanism-of-action heavy."},
    {"week": 4, "title": "Pathology + Microbiology", "subjects": ["pathology", "micro"], "focus": "Inflammation, neoplasia, gram +/- bugs, HIV/TB.", "mock": "50 MCQs - slides + stains."},
    {"week": 5, "title": "General Medicine + PSM", "subjects": ["medicine", "psm"], "focus": "Cardiology, endocrine, epidemiology, national programmes.", "mock": "100 MCQs - half-length clinical block."},
    {"week": 6, "title": "General Surgery + Orthopedics", "subjects": ["surgery", "ortho"], "focus": "Acute abdomen, hernias, fractures, nerve injuries.", "mock": "50 MCQs - clinical vignettes."},
    {"week": 7, "title": "OBG + Pediatrics + ENT/Ophthalmology", "subjects": ["obg", "peds", "ent_ophth"], "focus": "Antenatal care, neonatal jaundice, CSOM, glaucoma.", "mock": "100 MCQs - mixed clinical subjects."},
    {"week": 8, "title": "Forensic/Psychiatry + Full revision & mocks", "subjects": ["forensic", "medicine", "surgery", "pharma"], "focus": "Medico-legal, weak-area drill, 200-Q full mocks.", "mock": "200 MCQs / 180 min - full INI-CET pattern."},
]

TOPICS = [
    {"id": "a-upper", "subject_id": "anatomy", "chapter": "Upper Limb", "name": "Brachial plexus, spaces, clinical tests", "marks_weight": 5, "probability": 0.88, "ncert_priority": "must", "unit": "Anatomy", "study_week": 1},
    {"id": "a-lower", "subject_id": "anatomy", "chapter": "Lower Limb", "name": "Sciatic nerve, compartments, dermatomes", "marks_weight": 5, "probability": 0.85, "ncert_priority": "must", "unit": "Anatomy", "study_week": 1},
    {"id": "a-thorax", "subject_id": "anatomy", "chapter": "Thorax", "name": "Heart chambers, mediastinum, diaphragm", "marks_weight": 5, "probability": 0.82, "ncert_priority": "must", "unit": "Anatomy", "study_week": 1},
    {"id": "p-general", "subject_id": "physiology", "chapter": "General Physiology", "name": "Cell, nerve, muscle, body fluids", "marks_weight": 5, "probability": 0.80, "ncert_priority": "must", "unit": "Physiology", "study_week": 1},
    {"id": "a-head", "subject_id": "anatomy", "chapter": "Head & Neck", "name": "Cranial nerves, triangles, salivary glands", "marks_weight": 5, "probability": 0.90, "ncert_priority": "must", "unit": "Anatomy", "study_week": 2},
    {"id": "a-neuro", "subject_id": "anatomy", "chapter": "Neuroanatomy", "name": "Brainstem, cerebellum, blood supply", "marks_weight": 5, "probability": 0.92, "ncert_priority": "must", "unit": "Anatomy", "study_week": 2},
    {"id": "p-cvs", "subject_id": "physiology", "chapter": "CVS Physiology", "name": "Cardiac cycle, ECG, pressure curves", "marks_weight": 5, "probability": 0.91, "ncert_priority": "must", "unit": "Physiology", "study_week": 2},
    {"id": "p-resp", "subject_id": "physiology", "chapter": "Respiratory Physiology", "name": "Lung volumes, gas transport, hypoxia", "marks_weight": 5, "probability": 0.86, "ncert_priority": "must", "unit": "Physiology", "study_week": 2},
    {"id": "b-metab", "subject_id": "biochem", "chapter": "Metabolism", "name": "Glycolysis, TCA, urea cycle, lipids", "marks_weight": 4, "probability": 0.84, "ncert_priority": "must", "unit": "Biochemistry", "study_week": 3},
    {"id": "b-clinical", "subject_id": "biochem", "chapter": "Clinical Biochemistry", "name": "Enzymes, vitamins, acid-base markers", "marks_weight": 4, "probability": 0.78, "ncert_priority": "should", "unit": "Biochemistry", "study_week": 3},
    {"id": "ph-general", "subject_id": "pharma", "chapter": "General Pharmacology", "name": "PK/PD, receptors, ADR, clinical trials", "marks_weight": 6, "probability": 0.88, "ncert_priority": "must", "unit": "Pharmacology", "study_week": 3},
    {"id": "ph-ans", "subject_id": "pharma", "chapter": "ANS & CNS Drugs", "name": "Sympathomimetics, anticholinergics, antiepileptics", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "Pharmacology", "study_week": 3},
    {"id": "ph-cvsab", "subject_id": "pharma", "chapter": "CVS & Antimicrobials", "name": "Antihypertensives, diuretics, beta-lactams", "marks_weight": 6, "probability": 0.93, "ncert_priority": "must", "unit": "Pharmacology", "study_week": 3},
    {"id": "pa-general", "subject_id": "pathology", "chapter": "General Pathology", "name": "Inflammation, healing, neoplasia", "marks_weight": 6, "probability": 0.91, "ncert_priority": "must", "unit": "Pathology", "study_week": 4},
    {"id": "pa-hema", "subject_id": "pathology", "chapter": "Hematology", "name": "Anemias, leukemias, coagulation", "marks_weight": 6, "probability": 0.89, "ncert_priority": "must", "unit": "Pathology", "study_week": 4},
    {"id": "pa-systemic", "subject_id": "pathology", "chapter": "Systemic Pathology", "name": "Kidney, liver, lung pathology", "marks_weight": 6, "probability": 0.87, "ncert_priority": "must", "unit": "Pathology", "study_week": 4},
    {"id": "mi-bacteria", "subject_id": "micro", "chapter": "Bacteriology", "name": "Gram +/-, TB, atypical, sterilisation", "marks_weight": 4, "probability": 0.90, "ncert_priority": "must", "unit": "Microbiology", "study_week": 4},
    {"id": "mi-virology", "subject_id": "micro", "chapter": "Virology & Mycology", "name": "HIV, hepatitis, fungi, parasites", "marks_weight": 4, "probability": 0.85, "ncert_priority": "must", "unit": "Microbiology", "study_week": 4},
    {"id": "me-cardio", "subject_id": "medicine", "chapter": "Cardiology", "name": "Heart failure, ACS, arrhythmias, murmurs", "marks_weight": 8, "probability": 0.94, "ncert_priority": "must", "unit": "Medicine", "study_week": 5},
    {"id": "me-endo", "subject_id": "medicine", "chapter": "Endocrinology", "name": "Diabetes, thyroid, adrenal disorders", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "Medicine", "study_week": 5},
    {"id": "me-nephro", "subject_id": "medicine", "chapter": "Nephrology & GI", "name": "AKI/CKD, hepatitis, pancreatitis", "marks_weight": 6, "probability": 0.88, "ncert_priority": "must", "unit": "Medicine", "study_week": 5},
    {"id": "ps-epi", "subject_id": "psm", "chapter": "Epidemiology & Biostatistics", "name": "Rates, sensitivity, RCTs, screening", "marks_weight": 6, "probability": 0.86, "ncert_priority": "must", "unit": "PSM", "study_week": 5},
    {"id": "ps-programs", "subject_id": "psm", "chapter": "National Health Programmes", "name": "RNTCP, NTEP, immunisation, RMNCH", "marks_weight": 6, "probability": 0.92, "ncert_priority": "must", "unit": "PSM", "study_week": 5},
    {"id": "su-general", "subject_id": "surgery", "chapter": "General Surgery", "name": "Acute abdomen, hernias, breast, thyroid", "marks_weight": 8, "probability": 0.91, "ncert_priority": "must", "unit": "Surgery", "study_week": 6},
    {"id": "su-gi", "subject_id": "surgery", "chapter": "GI Surgery", "name": "Obstruction, perforation, anorectal", "marks_weight": 6, "probability": 0.87, "ncert_priority": "must", "unit": "Surgery", "study_week": 6},
    {"id": "or-trauma", "subject_id": "ortho", "chapter": "Traumatology", "name": "Fractures, nerve injuries, compartment syndrome", "marks_weight": 5, "probability": 0.88, "ncert_priority": "must", "unit": "Orthopedics", "study_week": 6},
    {"id": "or-spine", "subject_id": "ortho", "chapter": "Spine & Joints", "name": "Disc prolapse, arthritis, pediatric ortho", "marks_weight": 5, "probability": 0.80, "ncert_priority": "should", "unit": "Orthopedics", "study_week": 6},
    {"id": "ob-obs", "subject_id": "obg", "chapter": "Obstetrics", "name": "Antenatal care, labour, PIH, PPH", "marks_weight": 7, "probability": 0.93, "ncert_priority": "must", "unit": "OBG", "study_week": 7},
    {"id": "ob-gyn", "subject_id": "obg", "chapter": "Gynecology", "name": "PCOS, fibroids, CA cervix, contraception", "marks_weight": 6, "probability": 0.90, "ncert_priority": "must", "unit": "OBG", "study_week": 7},
    {"id": "pe-neonatal", "subject_id": "peds", "chapter": "Neonatology", "name": "Jaundice, sepsis, birth asphyxia", "marks_weight": 4, "probability": 0.88, "ncert_priority": "must", "unit": "Pediatrics", "study_week": 7},
    {"id": "pe-infections", "subject_id": "peds", "chapter": "Pediatric Infections", "name": "Measles, meningitis, malnutrition", "marks_weight": 4, "probability": 0.85, "ncert_priority": "must", "unit": "Pediatrics", "study_week": 7},
    {"id": "eo-ent", "subject_id": "ent_ophth", "chapter": "ENT", "name": "CSOM, vertigo, hearing loss", "marks_weight": 4, "probability": 0.82, "ncert_priority": "should", "unit": "ENT", "study_week": 7},
    {"id": "eo-ophth", "subject_id": "ent_ophth", "chapter": "Ophthalmology", "name": "Glaucoma, cataract, strabismus, red eye", "marks_weight": 4, "probability": 0.84, "ncert_priority": "should", "unit": "Ophthalmology", "study_week": 7},
    {"id": "fo-legal", "subject_id": "forensic", "chapter": "Forensic Medicine", "name": "Medico-legal, poisoning, autopsy findings", "marks_weight": 3, "probability": 0.78, "ncert_priority": "should", "unit": "Forensic", "study_week": 8},
    {"id": "fo-psych", "subject_id": "forensic", "chapter": "Psychiatry", "name": "Schizophrenia, depression, substance use", "marks_weight": 3, "probability": 0.75, "ncert_priority": "should", "unit": "Psychiatry", "study_week": 8},
    {"id": "me-revision", "subject_id": "medicine", "chapter": "Medicine Revision", "name": "High-yield medicine recall drill", "marks_weight": 5, "probability": 0.95, "ncert_priority": "must", "unit": "Medicine", "study_week": 8},
    {"id": "ph-revision", "subject_id": "pharma", "chapter": "Pharmacology Revision", "name": "Drug-of-choice and adverse effects marathon", "marks_weight": 5, "probability": 0.94, "ncert_priority": "must", "unit": "Pharmacology", "study_week": 8},
]

TARGETS = {
    "qualifying": {"label": "Qualifying rank", "percent": 55, "blurb": "Secure a clinical seat with buffer on negative marking."},
    "good_rank": {"label": "Good rank (top institutes)", "percent": 70, "blurb": "Competitive for major institutes outside the very top band."},
    "aiims_band": {"label": "AIIMS / top-tier band", "percent": 85, "blurb": "Leave almost no high-yield clinical topic cold."},
    "top_rank": {"label": "Top 100 chase", "percent": 92, "blurb": "Full syllabus depth + recent advances + mock stamina."},
}

TARGET_MASTERY = {
    "qualifying": 50,
    "good_rank": 68,
    "aiims_band": 82,
    "top_rank": 90,
}

PREREQS = {
    "a-neuro": ["a-head"],
    "a-head": ["a-upper"],
    "p-cvs": ["p-general"],
    "p-resp": ["p-general"],
    "ph-ans": ["ph-general"],
    "ph-cvsab": ["ph-general", "ph-ans"],
    "pa-hema": ["pa-general"],
    "pa-systemic": ["pa-general"],
    "mi-virology": ["mi-bacteria"],
    "me-cardio": ["p-cvs", "ph-cvsab"],
    "me-endo": ["b-metab", "ph-general"],
    "me-nephro": ["pa-systemic"],
    "su-gi": ["su-general"],
    "or-spine": ["or-trauma"],
    "ob-gyn": ["ob-obs"],
    "pe-infections": ["pe-neonatal", "mi-bacteria"],
    "me-revision": ["me-cardio", "me-endo"],
    "ph-revision": ["ph-cvsab"],
}
