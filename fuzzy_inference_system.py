
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def build_fuzzy_system():
    security = ctrl.Antecedent(np.arange(0, 101, 1), 'security')
    privacy = ctrl.Antecedent(np.arange(0, 101, 1), 'privacy')
    performance = ctrl.Antecedent(np.arange(0, 101, 1), 'performance')
    trust_score = ctrl.Consequent(np.arange(0, 101, 1), 'trust_score')

    for var in [security, privacy, performance]:
        var['low'] = fuzz.trimf(var.universe, [0, 0, 50])
        var['medium'] = fuzz.trimf(var.universe, [25, 50, 75])
        var['high'] = fuzz.trimf(var.universe, [50, 100, 100])

    trust_score['low'] = fuzz.trimf(trust_score.universe, [0, 0, 50])
    trust_score['medium'] = fuzz.trimf(trust_score.universe, [25, 50, 75])
    trust_score['high'] = fuzz.trimf(trust_score.universe, [50, 100, 100])

    rules = [
        ctrl.Rule(security['high'] & privacy['high'] & performance['high'], trust_score['high']),
        ctrl.Rule(security['medium'] & privacy['medium'], trust_score['medium']),
        ctrl.Rule(security['low'] | privacy['low'], trust_score['low']),
        ctrl.Rule(performance['low'] & privacy['low'], trust_score['low']),
        ctrl.Rule(performance['medium'] & (privacy['medium'] | security['medium']), trust_score['medium']),
        ctrl.Rule(performance['high'] & privacy['high'], trust_score['high']),
    ]

    trust_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(trust_ctrl)
