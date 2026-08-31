from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level
from app.modules.policy.policy_engine import determine_action


def test_risk_scoring_and_levels_and_actions():
    assert calculate_risk_score([]) == 0
    assert get_risk_level(0) == "low"

    assert calculate_risk_score([{"risk": "critical"}]) == 4
    assert get_risk_level(4) == "medium"

    assert calculate_risk_score([{"risk": "critical"}, {"risk": "high"}]) == 7
    assert get_risk_level(7) == "high"

    assert calculate_risk_score([{"risk": "critical"}, {"risk": "critical"}, {"risk": "critical"}]) == 12
    assert get_risk_level(12) == "critical"

    # actions
    assert determine_action("critical", {"block_on_critical": True, "mask_output": True}) == "blocked"
    assert determine_action("high", {"block_on_critical": True, "mask_output": True}) == "masked"
    assert determine_action("low", {"block_on_critical": False, "mask_output": False}) == "allowed"

