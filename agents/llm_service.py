
import os

from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)
load_dotenv()


def generate_ai_explanation(
    recommendations,
    forecast_result=None,
    risk_result=None,
):
    """Generate explanations using Gemini, with a safe fallback."""

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )

    if not api_key:
        return None

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0,
            timeout=30,
            max_retries=1,
        )

        risk_records = []

        if risk_result is not None and not risk_result.empty:
            columns = [
                col for col in [
                    "product_id",
                    "risk_level",
                    "overall_risk_score",
                    "risk_factors",
                ]
                if col in risk_result.columns
            ]

            risk_records = risk_result[columns].to_dict(
                orient="records"
            )

        context = {
            "forecast": forecast_result,
            "risk_summary": risk_records,
            "recommendations": recommendations,
        }

        messages = [
            SystemMessage(
                content=(
                    "You are a supply-chain decision-support assistant. "
                    "Explain the provided analytics in simple business "
                    "language. Prioritize urgent actions and explain "
                    "the evidence behind them. Do not invent figures, "
                    "suppliers, or facts. Do not change calculated "
                    "metrics or recommended order quantities. "
                    "Mention missing information when relevant. "
                    "Purchasing decisions require human approval."
                )
            ),
            HumanMessage(
                content=(
                    "Analyze the following results and provide:\n"
                    "1. A short situation summary.\n"
                    "2. Prioritized actions.\n"
                    "3. Evidence supporting each action.\n"
                    "4. Data limitations.\n\n"
                    f"Analytics data:\n{context}"
                )
            ),
        ]

        response = llm.invoke(messages)
        return str(response.content)

    except Exception:
        logger.exception("Gemini explanation generation failed")
        return None