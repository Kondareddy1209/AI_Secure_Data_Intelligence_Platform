from typing import List, Dict, Tuple
from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level
from app.modules.policy.policy_engine import determine_action


def compute_risk(findings: List[Dict], options: Dict) -> Tuple[int, str, str]:
    """Thin wrapper to compute score, level and action.

    Returns a tuple (score:int, level:str, action:str)
    """
    score = calculate_risk_score(findings)
    level = get_risk_level(score)
    action = determine_action(level, options)
    return score, level, action

