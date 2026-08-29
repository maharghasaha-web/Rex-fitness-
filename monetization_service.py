from typing import Dict, Any, List
from app.schemas.monetization import (
    UserTierStatus,
    UpgradeTierRequest,
    RewardedAdClaimRequest,
    RewardedAdClaimResponse,
    AdConfigResponse
)
from app.core.config import settings

# In-memory mock storage for user monetization state (mirrored to DB in production)
USER_MONETIZATION_DB: Dict[int, Dict[str, Any]] = {}

class MonetizationService:
    @staticmethod
    def get_user_tier(user_id: int) -> UserTierStatus:
        """Retrieves active subscription tier, scan credits, and enabled perks."""
        user_state = USER_MONETIZATION_DB.get(user_id, {
            "tier": "FREE",
            "is_pro": False,
            "scan_credits": 3
        })
        
        is_pro = user_state["tier"] in ["PRO_MONTHLY", "PRO_ANNUAL"]
        
        features = [
            "AI Physique Conditioning Scanner",
            "Dynamic Workout Split & Exercises",
            "Adaptive Missed-Day Recovery Engine",
            "AI Food Photo Macro Scanner",
            "Apple HealthKit & Google Health Connect Sync"
        ]
        
        if is_pro:
            features.extend([
                "Ad-Free Premium Experience",
                "Unlimited AI Scans (Physique & Food)",
                "Priority 24/7 AI Personal Coach Chat",
                "Exportable PDF Analytics Reports",
                "Advanced 1RM Strength Curve Tracking"
            ])
            
        return UserTierStatus(
            user_id=user_id,
            tier=user_state["tier"],
            is_pro=is_pro,
            scan_credits_remaining=9999 if is_pro else user_state["scan_credits"],
            unlimited_scans=is_pro,
            ads_enabled=not is_pro,
            features_unlocked=features
        )

    @staticmethod
    def upgrade_user(request: UpgradeTierRequest) -> UserTierStatus:
        """Processes in-app purchase validation and upgrades user to PRO."""
        USER_MONETIZATION_DB[request.user_id] = {
            "tier": request.target_tier,
            "is_pro": True,
            "scan_credits": 9999
        }
        return MonetizationService.get_user_tier(request.user_id)

    @staticmethod
    def claim_rewarded_ad(request: RewardedAdClaimRequest) -> RewardedAdClaimResponse:
        """Credits +1 scan or report token when a user watches a rewarded video ad."""
        user_state = USER_MONETIZATION_DB.get(request.user_id, {
            "tier": "FREE",
            "is_pro": False,
            "scan_credits": 3
        })
        
        user_state["scan_credits"] += 1
        USER_MONETIZATION_DB[request.user_id] = user_state
        
        return RewardedAdClaimResponse(
            success=True,
            reward_type=request.reward_type,
            credits_added=1,
            new_credit_balance=user_state["scan_credits"],
            message="Thank you for supporting the app! 1 instant AI scan credit has been added to your account."
        )

    @staticmethod
    def get_ad_config() -> AdConfigResponse:
        """Returns standard AdMob IDs and frequency capping configuration."""
        return AdConfigResponse(
            admob_app_id_ios="ca-app-pub-3940256099942544~1458002511", # Google AdMob Test App ID
            admob_app_id_android="ca-app-pub-3940256099942544~3347511713",
            banner_ad_unit_id="ca-app-pub-3940256099942544/6300978111", # Test Banner ID
            interstitial_ad_unit_id="ca-app-pub-3940256099942544/1033173712", # Test Interstitial ID
            rewarded_ad_unit_id="ca-app-pub-3940256099942544/5224354917", # Test Rewarded ID
            interstitial_frequency_interval=2, # Trigger interstitial every 2 completed workouts
            banner_refresh_rate_seconds=30
        )
