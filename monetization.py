from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserTierStatus(BaseModel):
    user_id: int
    tier: str # 'FREE', 'PRO_MONTHLY', 'PRO_ANNUAL'
    is_pro: bool
    scan_credits_remaining: int
    unlimited_scans: bool
    ads_enabled: bool
    features_unlocked: List[str]

class UpgradeTierRequest(BaseModel):
    user_id: int
    target_tier: str = Field(..., description="'PRO_MONTHLY' or 'PRO_ANNUAL'")
    payment_provider: str = Field("apple_in_app_purchase", description="'apple_in_app_purchase' or 'google_play_billing'")
    purchase_token: str

class RewardedAdClaimRequest(BaseModel):
    user_id: int
    ad_unit_id: str
    reward_type: str = "ai_scan_credit" # 'ai_scan_credit', 'pdf_export', 'workout_variation'
    verification_token: Optional[str] = None

class RewardedAdClaimResponse(BaseModel):
    success: bool
    reward_type: str
    credits_added: int
    new_credit_balance: int
    message: str

class AdConfigResponse(BaseModel):
    admob_app_id_ios: str
    admob_app_id_android: str
    banner_ad_unit_id: str
    interstitial_ad_unit_id: str
    rewarded_ad_unit_id: str
    interstitial_frequency_interval: int # Show interstitial every X completed workouts
    banner_refresh_rate_seconds: int
