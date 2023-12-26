import numbers
from typing import Any
from ray.rllib.utils.typing import EnvActionType as Action, PolicyID, MultiAgentDict

RealNumber = float | int | numbers.Real

Agent = str
AgentOrAll = str
Observation = Any
Reward = RealNumber

del Any, numbers