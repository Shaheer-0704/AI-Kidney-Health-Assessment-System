import pandas as pd
import numpy as np
import pickle

from tensorflow.keras.models import load_model

# ============================================
# LOAD MODEL AND SCALER
# ============================================

ann_model = load_model(
    "kidney_health_ann.keras"
)

with open(
    "kidney_scaler.pkl",
    "rb"
) as f:

    scaler = pickle.load(f)


# ============================================
# MODEL FEATURES
# ============================================

MODEL_FEATURES = [

    'age',
    'bp',

    'sg',
    'al',
    'su',

    'rbc',
    'pc',
    'pcc',
    'ba',

    'bgr',

    'bu',
    'sc',

    'sod',
    'pot',

    'hemo',
    'pcv',
    'wc',
    'rc',

    'htn',
    'dm',
    'cad',

    'appet',

    'pe',
    'ane'
]

# ============================================
# ANN PREDICTION
# ============================================

def ann_predict(patient_data):

    input_df = pd.DataFrame(
        [patient_data]
    )

    input_df = input_df.drop(
        columns=['gender'],
        errors='ignore'
    )

    input_df = input_df.reindex(
        columns=MODEL_FEATURES,
        fill_value=0
    )

    input_scaled = scaler.transform(
        input_df
    )

    probability = ann_model.predict(
        input_scaled,
        verbose=0
    )[0][0]

    return float(probability)


# ============================================
# AI RISK CATEGORY
# ============================================

def ai_risk_category(probability):

    if probability >= 0.90:
        return "Very High Risk"

    elif probability >= 0.70:
        return "High Risk"

    elif probability >= 0.50:
        return "Moderate Risk"

    elif probability >= 0.30:
        return "Low Risk"

    else:
        return "Very Low Risk"


# ============================================
# CKD-EPI eGFR CALCULATOR
# ============================================

def calculate_egfr(scr, age, gender):

    gender = gender.lower()

    if gender == "female":

        if scr <= 0.7:
            egfr = (
                144 *
                ((scr / 0.7) ** (-0.329)) *
                (0.993 ** age)
            )

        else:
            egfr = (
                144 *
                ((scr / 0.7) ** (-1.209)) *
                (0.993 ** age)
            )

    else:

        if scr <= 0.9:
            egfr = (
                141 *
                ((scr / 0.9) ** (-0.411)) *
                (0.993 ** age)
            )

        else:
            egfr = (
                141 *
                ((scr / 0.9) ** (-1.209)) *
                (0.993 ** age)
            )

    return round(egfr, 2)

# ============================================
# CKD STAGE CLASSIFIER
# ============================================

def classify_ckd_stage(egfr):

    if egfr >= 90:
        return "G1 - Normal Kidney Function"

    elif egfr >= 60:
        return "G2 - Mild Reduction"

    elif egfr >= 45:
        return "G3a - Mild to Moderate Reduction"

    elif egfr >= 30:
        return "G3b - Moderate to Severe Reduction"

    elif egfr >= 15:
        return "G4 - Severe Reduction"

    else:
        return "G5 - Kidney Failure"


# ============================================
# URINE ANALYSIS
# ============================================

def urine_analysis(data):

    findings = []

    # Albumin
    if data['al'] >= 3:
        findings.append("Severe Proteinuria")

    elif data['al'] >= 1:
        findings.append("Proteinuria Present")

    # Sugar
    if data['su'] >= 1:
        findings.append("Glucose Detected in Urine")

    # Blood
    if data['rbc'] == 1:
        findings.append("Hematuria (Blood in Urine)")

    # Infection Indicators
    if data['pc'] == 1:
        findings.append("Pus Cells Present")

    if data['pcc'] == 1:
        findings.append("Pus Cell Clumps Present")

    if data['ba'] == 1:
        findings.append("Bacteria Detected")

    # Specific Gravity
    if data['sg'] < 1.010:
        findings.append("Dilute Urine")

    elif data['sg'] > 1.025:
        findings.append("Highly Concentrated Urine")

    return findings


# ============================================
# BLOOD ANALYSIS
# ============================================

def blood_analysis(data):

    findings = []

    # Hemoglobin
    if data['hemo'] < 10:
        findings.append("Severe Anemia")

    elif data['hemo'] < 12:
        findings.append("Mild Anemia")

    # Packed Cell Volume
    if data['pcv'] < 35:
        findings.append("Low Packed Cell Volume")

    # White Blood Cells
    if data['wc'] > 11000:
        findings.append("Elevated White Blood Cell Count (Possible Infection)")

    elif data['wc'] < 4000:
        findings.append("Low White Blood Cell Count")

    # Red Blood Cells
    if data['rc'] < 4:
        findings.append("Low Red Blood Cell Count")

    elif data['rc'] > 6:
        findings.append("Elevated Red Blood Cell Count")

    # Blood Glucose
    if data['bgr'] >= 200:
        findings.append("Severely Elevated Blood Glucose")

    elif data['bgr'] >= 140:
        findings.append("Elevated Blood Glucose")

    return findings


# ============================================
# KIDNEY FUNCTION ANALYSIS
# ============================================

def kidney_function_analysis(data, egfr):

    findings = []

    # --------------------
    # Serum Creatinine
    # --------------------

    if data['sc'] >= 5:
        findings.append("Critically Elevated Serum Creatinine")

    elif data['sc'] >= 2:
        findings.append("High Serum Creatinine")

    elif data['sc'] > 1.2:
        findings.append("Mildly Elevated Serum Creatinine")

    # --------------------
    # Blood Urea
    # --------------------

    if data['bu'] > 80:
    
        findings.append(
            "Severely Elevated Blood Urea"
        )
    
    elif data['bu'] > 50:
    
        findings.append(
            "Elevated Blood Urea"
        )
    
    elif data['bu'] > 40:
    
        findings.append(
            "Mildly Elevated Blood Urea"
        )

    # --------------------
    # eGFR Interpretation
    # --------------------

    if egfr < 15:
        findings.append("Kidney Failure Risk (Stage G5)")

    elif egfr < 30:
        findings.append("Severe Kidney Function Reduction (Stage G4)")

    elif egfr < 45:
        findings.append("Moderate-Severe Kidney Function Reduction (Stage G3b)")

    elif egfr < 60:
        findings.append("Moderate Kidney Function Reduction (Stage G3a)")

    elif egfr < 90:
        findings.append("Mild Kidney Function Reduction (Stage G2)")

    return findings


# ============================================
# RISK FACTOR ANALYSIS
# ============================================

def risk_factor_analysis(data):

    risk_factors = []

    if data['htn'] == 1:
        risk_factors.append(
            "Hypertension - Major CKD Risk Factor"
        )

    if data['dm'] == 1:
        risk_factors.append(
            "Diabetes Mellitus - Major CKD Risk Factor"
        )

    if data['cad'] == 1:
        risk_factors.append(
            "Coronary Artery Disease"
        )

    if data['pe'] == 1:
        risk_factors.append(
            "Pedal Edema Present"
        )

    if data['ane'] == 1:
        risk_factors.append(
            "Anemia Present"
        )

    return risk_factors


# ============================================
# KIDNEY HEALTH SCORE
# ============================================

def calculate_kidney_health_score(
    urine_findings,
    blood_findings,
    kidney_findings,
    risk_factors,
    egfr
):

    score = 100

    # ----------------------------------
    # eGFR Penalty
    # ----------------------------------

    if egfr < 15:
        score -= 50

    elif egfr < 30:
        score -= 35

    elif egfr < 45:
        score -= 25

    elif egfr < 60:
        score -= 15

    elif egfr < 90:
        score -= 5

    # ----------------------------------
    # Urine Findings
    # ----------------------------------

    for item in urine_findings:

        if "Severe Proteinuria" in item:
            score -= 15

        elif "Proteinuria" in item:
            score -= 10

        elif "Hematuria" in item:
            score -= 8

        elif "Bacteria" in item:
            score -= 5

        elif "Pus" in item:
            score -= 5

    # ----------------------------------
    # Blood Findings
    # ----------------------------------

    for item in blood_findings:

        if "Severe Anemia" in item:
            score -= 10

        elif "Mild Anemia" in item:
            score -= 5

        elif "Severely Elevated Blood Glucose" in item:
            score -= 10

        elif "Elevated Blood Glucose" in item:
            score -= 5

        elif "Low Red Blood Cell Count" in item:
            score -= 5

    # ----------------------------------
    # Kidney Findings
    # ----------------------------------

    for item in kidney_findings:

        if "Critically Elevated" in item:
            score -= 15

        elif "High Serum Creatinine" in item:
            score -= 10

        elif "Mildly Elevated Serum Creatinine" in item:
            score -= 5

        elif "Severely Elevated Blood Urea" in item:
            score -= 10

        elif "Elevated Blood Urea" in item:
            score -= 5

    # ----------------------------------
    # Risk Factors
    # ----------------------------------

    score -= len(risk_factors) * 5

    # ----------------------------------
    # Prevent Negative Score
    # ----------------------------------

    score = max(0, score)

    # ----------------------------------
    # Health Category
    # ----------------------------------

    if score >= 90:
        category = "Excellent"

    elif score >= 75:
        category = "Good"

    elif score >= 60:
        category = "Moderate Risk"

    elif score >= 40:
        category = "High Risk"

    else:
        category = "Critical"

    return score, category


# ============================================
# RECOMMENDATION ENGINE
# ============================================

def generate_recommendations(
    urine_findings,
    blood_findings,
    kidney_findings,
    risk_factors,
    egfr
):

    recommendations = []

    # ----------------------------------
    # Kidney Function
    # ----------------------------------

    if egfr < 60:
        recommendations.append(
            "Consult a nephrologist for detailed kidney evaluation."
        )

    if egfr < 30:
        recommendations.append(
            "Urgent specialist consultation is strongly advised."
        )

    # ----------------------------------
    # Proteinuria
    # ----------------------------------

    for item in urine_findings:

        if "Proteinuria" in item:
            recommendations.append(
                "Monitor urine protein levels regularly."
            )

        if "Hematuria" in item:
            recommendations.append(
                "Further investigation for blood in urine is recommended."
            )

        if "Bacteria" in item:
            recommendations.append(
                "Urine culture test may be required."
            )

    # ----------------------------------
    # Blood Findings
    # ----------------------------------

    for item in blood_findings:

        if "Anemia" in item:
            recommendations.append(
                "Monitor hemoglobin and iron levels."
            )

        if "Blood Glucose" in item:
            recommendations.append(
                "Maintain strict blood sugar control."
            )

    # ----------------------------------
    # Kidney Findings
    # ----------------------------------

    for item in kidney_findings:

        if "Creatinine" in item:
            recommendations.append(
                "Repeat serum creatinine testing periodically."
            )

        if "Blood Urea" in item:
            recommendations.append(
                "Monitor kidney function tests regularly."
            )

    # ----------------------------------
    # Risk Factors
    # ----------------------------------

    for item in risk_factors:

        if "Hypertension" in item:
            recommendations.append(
                "Maintain blood pressure below recommended limits."
            )

        if "Diabetes" in item:
            recommendations.append(
                "Regular HbA1c and blood glucose monitoring is advised."
            )

    # ----------------------------------
    # General Advice
    # ----------------------------------

    recommendations.append(
        "Maintain adequate hydration unless otherwise advised by a physician."
    )

    recommendations.append(
        "Reduce excessive salt intake."
    )

    # Remove duplicates

    recommendations = list(dict.fromkeys(recommendations))

    return recommendations


# ============================================
# INPUT VALIDATION ENGINE
# ============================================

def validate_patient_inputs(data):

    errors = []
    warnings = []

    # -----------------------
    # Age
    # -----------------------

    if data['age'] <= 0:
        errors.append(
            "Age must be greater than 0."
        )

    elif data['age'] > 100:
        warnings.append(
            "Age is outside most training samples."
        )

    # -----------------------
    # Blood Pressure
    # -----------------------

    if data['bp'] < 50 or data['bp'] > 180:
        warnings.append(
            "Blood Pressure outside dataset range (50-180)."
        )

    # -----------------------
    # Specific Gravity
    # -----------------------

    valid_sg = [
        1.005,
        1.010,
        1.015,
        1.020,
        1.025
    ]

    if round(data['sg'],3) not in valid_sg:
        warnings.append(
            "Specific Gravity value not present in training dataset."
        )

    # -----------------------
    # Creatinine
    # -----------------------

    if data['sc'] <= 0:
        errors.append(
            "Serum Creatinine must be greater than 0."
        )

    elif data['sc'] > 20:
        warnings.append(
            "Creatinine extremely high compared to training data."
        )

    # -----------------------
    # Blood Urea
    # -----------------------

    if data['bu'] <= 0:
        errors.append(
            "Blood Urea must be greater than 0."
        )

    # -----------------------
    # Hemoglobin
    # -----------------------

    if data['hemo'] <= 0:
        errors.append(
            "Hemoglobin must be greater than 0."
        )

    # -----------------------
    # Sodium
    # -----------------------

    if data['sod'] <= 0:
        errors.append(
            "Sodium must be greater than 0."
        )

    # -----------------------
    # Potassium
    # -----------------------

    if data['pot'] <= 0:
        errors.append(
            "Potassium must be greater than 0."
        )

    return errors, warnings

# ============================================
# RELIABILITY ASSESSMENT
# ============================================

def calculate_reliability(data):

    score = 100

    reasons = []

    # BP

    if data['bp'] < 50 or data['bp'] > 180:

        score -= 10

        reasons.append(
            "Blood Pressure outside training range"
        )

    # SG

    if round(data['sg'],3) not in [
        1.005,
        1.010,
        1.015,
        1.020,
        1.025
    ]:

        score -= 10

        reasons.append(
            "Specific Gravity outside dataset values"
        )

    # Creatinine

    if data['sc'] > 20:

        score -= 10

        reasons.append(
            "Creatinine far outside training distribution"
        )

    # Age

    if data['age'] > 100:

        score -= 10

        reasons.append(
            "Age outside typical dataset range"
        )

    # ------------------------

    if score >= 90:

        level = "High"

    elif score >= 75:

        level = "Moderate"

    else:

        level = "Low"

    return score, level, reasons


# ============================================
# AI CLINICAL AGREEMENT
# ============================================

def ai_clinical_agreement(
    probability,
    health_score
):

    # AI Risk

    ai_positive = probability >= 0.5

    # Clinical Risk

    clinical_positive = health_score < 60

    if ai_positive and clinical_positive:

        return (
            "Strong Agreement",
            "AI prediction and clinical findings indicate kidney disease risk."
        )

    elif not ai_positive and not clinical_positive:

        return (
            "Strong Agreement",
            "AI prediction and clinical findings indicate healthy kidney status."
        )

    else:

        return (
            "Weak Agreement",
            "AI prediction and clinical findings are not fully aligned. Clinical evaluation is recommended."
        )


# ============================================
# KEY FINDINGS GENERATOR
# ============================================

def generate_key_findings(report):

    findings = []

    # Kidney Function

    if report['egfr'] < 15:
        findings.append(
            f"Severe Kidney Failure Risk (eGFR {report['egfr']})"
        )

    elif report['egfr'] < 30:
        findings.append(
            f"Severely Reduced Kidney Function (eGFR {report['egfr']})"
        )

    elif report['egfr'] < 60:
        findings.append(
            f"Reduced Kidney Function (eGFR {report['egfr']})"
        )

    # Urine Findings

    if "Severe Proteinuria" in report['urine_findings']:
        findings.append(
            "Severe Proteinuria Detected"
        )

    elif "Proteinuria Present" in report['urine_findings']:
        findings.append(
            "Proteinuria Detected"
        )

    if any(
        "Hematuria" in item
        for item in report['urine_findings']
    ):
        findings.append(
            "Blood Detected in Urine"
        )

    # Blood Findings

    if "Severe Anemia" in report['blood_findings']:
        findings.append(
            "Severe Anemia Detected"
        )

    elif "Mild Anemia" in report['blood_findings']:
        findings.append(
            "Anemia Detected"
        )

    # Kidney Findings

    if any(
        "High Serum Creatinine" in item
        for item in report['kidney_findings']
    ):
        findings.append(
            "Elevated Serum Creatinine"
        )

    if any(
        "Blood Urea" in item
        for item in report['kidney_findings']
    ):
        findings.append(
            "Elevated Blood Urea"
        )

    # Risk Factors

    if any(
        "Diabetes" in item
        for item in report['risk_factors']
    ):
        findings.append(
            "Diabetes Mellitus"
        )

    if any(
        "Hypertension" in item
        for item in report['risk_factors']
    ):
        findings.append(
            "Hypertension"
        )

    return findings[:5]


# ============================================
# OVERALL ASSESSMENT
# ============================================

def generate_overall_assessment(report):

    probability = report['ckd_probability']
    score = report['health_score']
    egfr = report['egfr']

    # Severe Cases

    if score < 20 or egfr < 15:

        return (
            "Critical kidney health concerns detected. "
            "Clinical findings and kidney function indicators "
            "suggest advanced kidney disease requiring immediate "
            "medical evaluation."
        )

    # High Risk

    elif score < 40 or egfr < 30:

        return (
            "Significant kidney abnormalities detected. "
            "The assessment indicates high risk of chronic kidney "
            "disease progression and specialist consultation is advised."
        )

    # Moderate Risk

    elif score < 60 or egfr < 60:

        return (
            "Moderate kidney health concerns detected. "
            "Regular monitoring of kidney function and management "
            "of risk factors is recommended."
        )

    # Mild Risk

    elif score < 80:

        return (
            "Mild kidney health concerns identified. "
            "Current findings suggest the need for lifestyle "
            "modifications and periodic health monitoring."
        )

    # Healthy

    else:

        return (
            "Kidney health appears satisfactory. "
            "No major abnormalities were detected. "
            "Continue maintaining a healthy lifestyle and routine checkups."
        )


# ============================================
# MASTER REPORT GENERATOR
# ============================================

def generate_kidney_report(data):

    errors, warnings = validate_patient_inputs(data)

    reliability_score, reliability_level, reliability_reasons = (
        calculate_reliability(data)
    )

    probability = ann_predict(data)

    risk_level = ai_risk_category(
        probability
    )

    egfr = calculate_egfr(
        scr=data['sc'],
        age=data['age'],
        gender=data['gender']
    )

    stage = classify_ckd_stage(
        egfr
    )

    urine_findings = urine_analysis(data)

    blood_findings = blood_analysis(data)

    kidney_findings = kidney_function_analysis(
        data,
        egfr
    )

    risk_factors = risk_factor_analysis(
        data
    )

    health_score, health_category = (
        calculate_kidney_health_score(
            urine_findings,
            blood_findings,
            kidney_findings,
            risk_factors,
            egfr
        )
    )

    recommendations = (
        generate_recommendations(
            urine_findings,
            blood_findings,
            kidney_findings,
            risk_factors,
            egfr
        )
    )

    agreement_level, agreement_message = (
        ai_clinical_agreement(
            probability,
            health_score
        )
    )

    report = {

        "ckd_probability":
        round(probability * 100, 2),

        "ai_risk_level":
        risk_level,

        "validation_errors":
        errors,

        "validation_warnings":
        warnings,

        "reliability_score":
        reliability_score,

        "reliability_level":
        reliability_level,

        "reliability_reasons":
        reliability_reasons,

        "egfr":
        round(egfr, 2),

        "ckd_stage":
        stage,

        "urine_findings":
        urine_findings,

        "blood_findings":
        blood_findings,

        "kidney_findings":
        kidney_findings,

        "risk_factors":
        risk_factors,

        "health_score":
        health_score,

        "health_category":
        health_category,

        "agreement_level":
        agreement_level,

        "agreement_message":
        agreement_message,

        "recommendations":
        recommendations

    }

    report["key_findings"] = (
        generate_key_findings(report)
    )

    report["overall_assessment"] = (
        generate_overall_assessment(report)
    )

    return report


def get_risk_color(category):

    if category == "Excellent":
        return "green"

    elif category == "Good":
        return "blue"

    elif category == "Moderate":
        return "orange"

    else:
        return "red"
