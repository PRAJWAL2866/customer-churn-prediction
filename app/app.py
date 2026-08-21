import streamlit as st
import requests

API_URL = "https://customer-churn-api-ie3c.onrender.com/predict"
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }

    .metric-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #2A2F3A;
        text-align: center;
    }

    .metric-title {
        color: #9CA3AF;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: white;
        font-size: 30px;
        font-weight: bold;
    }

    .big-title {
        font-size: 38px;
        font-weight: 700;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<p class="big-title">📊 Customer Churn Prediction</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'AI-powered telecom customer retention dashboard using XGBoost'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("👤 Customer Profile")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.slider(
        "Tenure (Months)",
        0,
        72,
        12
    )

    phone = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple = st.selectbox(
        "Multiple Lines",
        [
            "Yes",
            "No",
            "No phone service"
        ]
    )

    internet = st.selectbox(
        "Internet Service",
        [
            "DSL",
            "Fiber optic",
            "No"
        ]
    )

    security = st.selectbox(
        "Online Security",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    backup = st.selectbox(
        "Online Backup",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

with right:
    st.subheader("📡 Services & Billing")

    protection = st.selectbox(
        "Device Protection",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    tech = st.selectbox(
        "Tech Support",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    tv = st.selectbox(
        "Streaming TV",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    movies = st.selectbox(
        "Streaming Movies",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless = st.selectbox(
        "Paperless Billing",
        [
            "Yes",
            "No"
        ]
    )

    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly = st.number_input(
        "Monthly Charges",
        min_value=18.25,
        max_value=120.0,
        value=70.0
    )

    total = st.number_input(
        "Total Charges",
        min_value=0.0,
        max_value=9000.0,
        value=800.0
    )

st.divider()

predict_button = st.button(
    "🚀 Predict Customer Churn",
    use_container_width=True
)

if predict_button:

    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": tech,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to FastAPI. "
            "Make sure the API server is running on port 8000."
        )
        st.stop()

    except requests.exceptions.RequestException as error:
        st.error(
            f"❌ API request failed: {error}"
        )
        st.stop()

    probability = result["churn_probability"] * 100
    risk = result["risk_level"]

    prediction = (
        "Churn"
        if result["prediction"] == 1
        else "Stay"
    )

    st.divider()

    st.subheader("📈 Prediction Result")

    if risk == "High":
        st.error(
            f"🔴 HIGH RISK • {probability:.2f}% probability"
        )

    elif risk == "Medium":
        st.warning(
            f"🟠 MEDIUM RISK • {probability:.2f}% probability"
        )

    else:
        st.success(
            f"🟢 LOW RISK • {probability:.2f}% probability"
        )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Risk Level
                </div>
                <div class="metric-value">
                    {risk}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Churn Probability
                </div>
                <div class="metric-value">
                    {probability:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Prediction
                </div>
                <div class="metric-value">
                    {prediction}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("💡 Retention Recommendation")

    if risk == "High":
        st.markdown(
            """
            - 🎯 Offer a **12-month discounted contract**
            - 🛠️ Provide **free Tech Support** for 3 months
            - 🔐 Recommend an **Online Security** bundle
            - 💳 Encourage automatic payment methods
            - 🤝 Contact the customer with a personalized retention offer
            """
        )

    elif risk == "Medium":
        st.markdown(
            """
            - 🎁 Offer a small loyalty discount
            - 📦 Promote value-added service bundles
            - 💳 Encourage automatic payment methods
            - 📞 Schedule a proactive customer check-in
            """
        )

    else:
        st.markdown(
            """
            - 🟢 Customer currently shows relatively low churn risk
            - 🎁 Maintain engagement through loyalty rewards
            - 📧 Continue personalized customer communication
            """
        )

    st.divider()

    st.subheader("🔍 Why did the model predict this?")

    st.caption(
        "These are the five features with the strongest "
        "influence on this individual prediction."
    )

    for item in result["top_features"]:

        feature_name = (
            item["feature"]
            .replace("cat__", "")
            .replace("num__", "")
            .replace("_", " ")
        )

        impact = float(item["impact"])

        if impact > 0:
            direction = "🔴 Increases churn risk"
        else:
            direction = "🟢 Reduces churn risk"

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(
                f"**{feature_name}**"
            )

        with col2:
            st.markdown(
                f"{direction}  \n"
                f"SHAP impact: `{impact:+.3f}`"
            )

    st.divider()

    st.subheader("📋 Customer Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.write(f"**Contract:** {contract}")
        st.write(f"**Tenure:** {tenure} months")
        st.write(f"**Internet Service:** {internet}")
        st.write(f"**Monthly Charges:** €{monthly:.2f}")

    with summary_col2:
        st.write(f"**Payment Method:** {payment}")
        st.write(f"**Online Security:** {security}")
        st.write(f"**Tech Support:** {tech}")
        st.write(f"**Total Charges:** €{total:.2f}")