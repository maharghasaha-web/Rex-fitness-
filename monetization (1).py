from fastapi import APIRouter
from app.schemas.monetization import (
    UserTierStatus,
    UpgradeTierRequest,
    RewardedAdClaimRequest,
    RewardedAdClaimResponse,
    AdConfigResponse
)
from app.services.monetization_service import MonetizationService

router = APIRouter(prefix="/monetization", tags=["Monetization, Subscription & AdMob"])

@router.get("/tier/{user_id}", response_model=UserTierStatus)
def get_user_tier(user_id: int):
    """Returns active subscription tier, scan credits, and enabled perks."""
    return MonetizationService.get_user_tier(user_id)

@router.post("/upgrade", response_model=UserTierStatus)
def upgrade_tier(request: UpgradeTierRequest):
    """Upgrades user subscription tier (In-App Purchase verification)."""
    return MonetizationService.upgrade_user(request)

@router.post("/claim-reward", response_model=RewardedAdClaimResponse)
def claim_rewarded_ad(request: RewardedAdClaimRequest):
    """Credits +1 instant AI scan token upon successful AdMob rewarded video completion."""
    return MonetizationService.claim_rewarded_ad(request)

@router.get("/ad-config", response_model=AdConfigResponse)
def get_ad_config():
    """Returns AdMob Unit IDs and frequency capping configuration for iOS and Android."""
    return MonetizationService.get_ad_config()
