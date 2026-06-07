import streamlit as st

from kidney_engine import generate_kidney_report
from pdf_generator import generate_pdf_report

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Kidney Health Assessment System",
    page_icon="🩺",
    layout="wide"
)


st.markdown(
    """
    <h1 style='text-align:center;font-size:60px;'>
    🩺 AI Kidney Health Assessment System
    </h1>
    """,
    unsafe_allow_html=True
)

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "🏠 Home",
        "📝 Assessment",
        "ℹ️ About Project"
    ]
)

st.markdown("""
    <style>
    
    button[data-baseweb="tab"] {
    
        font-size: 22px;
    
        font-weight: 600;
    
        padding: 15px 30px;
    }
    
    </style>
    """,
    unsafe_allow_html=True)

st.markdown("""
    <style>
    
    div[data-baseweb="tab-list"] {
    
        gap: 0px;
    
    }
    
    button[data-baseweb="tab"] {
    
        flex-grow: 1;
    
        justify-content: center;
    }
    
    </style>
    """,
    unsafe_allow_html=True)
    
# ============================================
# HEADER
# ============================================

    
    
with tab1:
    left, center, right = st.columns([1, 3, 1])

    with center:
    
        st.markdown(
            """
            <h3 style='text-align:center;'>
            AI-Powered Chronic Kidney Disease Risk Assessment
            </h3>
            """,
            unsafe_allow_html=True
        )
    
        st.markdown("""
        <style>
        
        html, body, [class*="css"]  {
        
            font-size: 18px;
        
        }
        
        </style>
        """,
        unsafe_allow_html=True)
            
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("🧠 ANN Prediction")
        
        with col2:
            st.info("🩺 Clinical Analysis")
        
        with col3:
            st.info("📈 eGFR & CKD Staging")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("⚠️ Risk Assessment")
        
        with col2:
            st.info("💡 Recommendations")
        
        with col3:
            st.info("📋 Reliability Analysis")
        
        st.warning(
            "⚠️ Educational Use Only. Not a substitute for professional medical diagnosis."
        )
    
        st.success(
            "📋 Application Loaded Successfully"
        )

        st.info(
            "🚀 Ready to begin? Move to the Assessment tab and enter the patient's clinical parameters to generate an AI-powered kidney health report."
        )


with tab2:
    
    left, center, right = st.columns([1, 3, 1])

    with center:
        
        # ============================================
        # PATIENT INFORMATION
        # ============================================
        
        with st.expander(
            "👤 Patient Information",
            expanded=True
        ):
        
            age = st.number_input(
                "Age (Years)",
                min_value=1,
                max_value=120,
                value=25
            )
            
            bp = st.number_input(
                "Blood Pressure (mmHg)",
                min_value=50,
                max_value=180,
                value=80
            )
            
            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )
        
        
        # ============================================
        # URINE PARAMETERS
        # ============================================
        
        with st.expander(
            "🧪 Urine Parameters"
        ):
        
            sg = st.selectbox(
                "Specific Gravity",
                [1.005, 1.010, 1.015, 1.020, 1.025],
                index=3
            )
            
            al = st.selectbox(
                "Albumin",
                [0, 1, 2, 3, 4, 5]
            )
            
            su = st.selectbox(
                "Sugar",
                [0, 1, 2, 3, 4, 5]
            )
            
            rbc = st.selectbox(
                "Red Blood Cells",
                ["Normal", "Abnormal"]
            )
            
            pc = st.selectbox(
                "Pus Cells",
                ["Normal", "Abnormal"]
            )
            
            pcc = st.selectbox(
                "Pus Cell Clumps",
                ["Not Present", "Present"]
            )
            
            ba = st.selectbox(
                "Bacteria",
                ["Not Present", "Present"]
            )
        
        # ============================================
        # ENCODING
        # ============================================
        
        rbc = 0 if rbc == "Normal" else 1
        
        pc = 0 if pc == "Normal" else 1
        
        pcc = 0 if pcc == "Not Present" else 1
        
        ba = 0 if ba == "Not Present" else 1
        
        # ============================================
        # BLOOD PARAMETERS
        # ============================================
        
        with st.expander(
            "🩸 Blood Parameters"
        ):
        
            bgr = st.number_input(
                "Blood Glucose Random (mg/dL)",
                min_value=0.0,
                value=120.0
            )
            
            hemo = st.number_input(
                "Hemoglobin (g/dL)",
                min_value=0.0,
                value=13.5
            )
            
            pcv = st.number_input(
                "Packed Cell Volume (%)",
                min_value=0.0,
                value=40.0
            )
            
            wc = st.number_input(
                "White Blood Cell Count (cells/cumm)",
                min_value=0.0,
                value=8000.0
            )
            
            rc = st.number_input(
                "Red Blood Cell Count (millions/cmm)",
                min_value=0.0,
                value=4.8
            )
        
        # ============================================
        # KIDNEY FUNCTION PARAMETERS
        # ============================================
        
        with st.expander(
            "🧠 Kidney Function Parameters"
        ):
        
            bu = st.number_input(
                "Blood Urea (mg/dL)",
                min_value=0.0,
                value=30.0
            )
            
            sc = st.number_input(
                "Serum Creatinine (mg/dL)",
                min_value=0.1,
                value=1.0
            )
            
            sod = st.number_input(
                "Sodium (mEq/L)",
                min_value=0.0,
                value=140.0
            )
            
            pot = st.number_input(
                "Potassium (mEq/L)",
                min_value=0.0,
                value=4.5
            )
        
        # ============================================
        # MEDICAL HISTORY
        # ============================================
        
        with st.expander(
            "📋 Medical History"
        ):
        
            htn = st.selectbox(
                "Hypertension",
                ["No", "Yes"]
            )
            
            dm = st.selectbox(
                "Diabetes Mellitus",
                ["No", "Yes"]
            )
            
            cad = st.selectbox(
                "Coronary Artery Disease",
                ["No", "Yes"]
            )
            
            appet = st.selectbox(
                "Appetite",
                ["Good","Poor"]
            )
            
            pe = st.selectbox(
                "Pedal Edema",
                ["No", "Yes"]
            )
            
            ane = st.selectbox(
                "Anemia",
                ["No", "Yes"]
            )
        
        # ============================================
        # ENCODING MEDICAL HISTORY
        # ============================================
        
        htn = 1 if htn == "Yes" else 0
        
        dm = 1 if dm == "Yes" else 0
        
        cad = 1 if cad == "Yes" else 0
        
        appet = 1 if appet == "Good" else 0
        
        pe = 1 if pe == "Yes" else 0
        
        ane = 1 if ane == "Yes" else 0

    # ============================================
    # ANALYZE BUTTON
    # ============================================
    
        st.divider()
        
        analyze = st.button(
            "🔍 Analyze Kidney Health",
            use_container_width=True
        )
    
    if analyze:
    
        patient_data = {
    
            'age': age,
            'gender': gender,
    
            'bp': bp,
    
            'sg': sg,
            'al': al,
            'su': su,
    
            'rbc': rbc,
            'pc': pc,
            'pcc': pcc,
            'ba': ba,
    
            'bgr': bgr,
    
            'bu': bu,
            'sc': sc,
    
            'sod': sod,
            'pot': pot,
    
            'hemo': hemo,
            'pcv': pcv,
            'wc': wc,
            'rc': rc,
    
            'htn': htn,
            'dm': dm,
            'cad': cad,
    
            'appet': appet,
        
            'pe': pe,
            'ane': ane
        }
    
        report = generate_kidney_report(
            patient_data
        )

        st.session_state["report"] = report
        st.session_state["patient_data"] = patient_data

    if "report" in st.session_state:

        report = st.session_state["report"]
     
          
        st.divider()
    
        st.header("📊 Kidney Health Dashboard")
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
    
            st.metric(
                "CKD Risk",
                f"{report['ckd_probability']}%"
            )
    
        with col2:
    
            st.metric(
                "Health Score",
                f"{report['health_score']}/100"
            )
    
        with col3:
    
            st.metric(
                "eGFR",
                report['egfr']
            )

        col1, col2, col3 = st.columns(3)
    
        with col1:
        
            st.info(
                f"CKD Stage\n\n{report['ckd_stage']}"
            )
        
        with col2:
        
            st.info(
                f"Health Category\n\n{report['health_category']}"
            )
        
        with col3:
        
            st.info(
                f"AI Risk Level\n\n{report['ai_risk_level']}"
            )
    
        st.divider()
    
        st.header("📋 Executive Summary")
        
        st.success(
            report["overall_assessment"]
        )
    
        st.header("🔍 Key Findings")
    
        if report["key_findings"]:
        
            for finding in report["key_findings"]:
        
                st.warning(finding)
        
        else:
        
            st.success(
                "No significant abnormalities detected."
            )
    
        with st.expander("🧪 Urine Findings"):
    
            if report["urine_findings"]:
        
                for item in report["urine_findings"]:
        
                    st.write(f"• {item}")
        
            else:
        
                st.success(
                    "No urine abnormalities detected."
                )
    
        with st.expander("🩸 Blood Findings"):
    
            if report["blood_findings"]:
        
                for item in report["blood_findings"]:
        
                    st.write(f"• {item}")
        
            else:
        
                st.success(
                    "No blood abnormalities detected."
                )
    
    
        with st.expander("🧠 Kidney Findings"):
    
            if report["kidney_findings"]:
        
                for item in report["kidney_findings"]:
        
                    st.write(f"• {item}")
        
            else:
        
                st.success(
                    "No kidney abnormalities detected."
                )
    
    
        with st.expander("⚠️ Risk Factors"):
    
            if report["risk_factors"]:
        
                for item in report["risk_factors"]:
        
                    st.write(f"• {item}")
        
            else:
        
                st.success(
                    "No major risk factors detected."
                )
    
        st.divider()
        
        col1, col2, col3 = st.columns(3)
    
        with col1:
        
            st.metric(
                "CKD Stage",
                report["ckd_stage"]
            )
        
        with col2:
        
            st.metric(
                "AI Risk Level",
                report["ai_risk_level"]
            )
        
        with col3:
        
            st.metric(
                "Reliability",
                report["reliability_level"]
            )
    
    
        st.divider()
    
        st.header("💡 Recommendations")
        
        for rec in report["recommendations"]:
        
            st.write(f"• {rec}")

        if "report" in st.session_state:

            pdf_buffer = generate_pdf_report(
        
                st.session_state["patient_data"],
        
                st.session_state["report"]
        
            )
        
            st.download_button(
        
                label="📄 Download Full Assessment Report",
        
                data=pdf_buffer,
        
                file_name="Kidney_Health_Report.pdf",
        
                mime="application/pdf"
            )

with tab3:

    left, center, right = st.columns([1,2,1])

    with center:

        st.title("ℹ️ About Project")

        st.subheader("Project Overview")

        st.write(
            """
            AI-assisted Kidney Health Assessment System
            that combines Artificial Neural Networks,
            eGFR calculation, CKD staging,
            clinical rule-based analysis,
            reliability assessment,
            and personalized recommendations.
            """
        )

        st.subheader("Dataset")

        st.write(
            "UCI Chronic Kidney Disease Dataset"
        )

        st.subheader("Technology Stack")

        st.write(
            """
            • Python

            • TensorFlow / Keras

            • Streamlit

            • Pandas

            • Scikit-Learn
            """
        )

        st.subheader("Model Architecture")

        st.code(
            """
Input Layer (24 Features)

↓

Dense Layer (64)

↓

Dense Layer (32)

↓

Dense Layer (16)

↓

Output Layer
            """
        )

        st.subheader("Key Features")

        st.write(
            """
            • CKD Prediction

            • eGFR Calculation

            • CKD Stage Classification

            • Reliability Assessment

            • Personalized Recommendations
            """
        )