from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, PositiveInt, conint
import stripe
from app.core.config import settings

# Configurar Stripe con clave secreta
stripe.api_key = settings.stripe_secret_key

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    amount: PositiveInt = Field(..., description="Monto en centavos")
    currency: str = Field(default="usd", min_length=3, max_length=4)

@router.post("/create-payment-intent")
def create_payment_intent(data: PaymentIntentRequest):
    try:
        # Crear el PaymentIntent en Stripe
        intent = stripe.PaymentIntent.create(
            amount=data.amount,
            currency=data.currency.lower(),
            payment_method_types=["card"],
        )

        return {
            "clientSecret": intent.client_secret,
            "publishableKey": settings.stripe_publishable_key
        }

    except stripe.error.StripeError as e:
        # Error manejado por Stripe
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.user_message or str(e)
        )
    except Exception as e:
        # Error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar el pago"
        )
