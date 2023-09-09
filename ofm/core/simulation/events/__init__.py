#      Openfoot Manager - A free and open source soccer management simulation
#      Copyright (C) 2020-2023  Pedrenrique G. Guimarães
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional
from .cross_event import CrossEvent
from .dribble_event import DribbleEvent
from .free_kick_event import FreeKickEvent
from .corner_kick_event import CornerKickEvent
from .pass_event import PassEvent
from .foul_event import FoulEvent
from .goal_kick_event import GoalKickEvent
from .penalty_kick_event import PenaltyKickEvent
from .shot_event import ShotEvent
from ..event import EventOutcome, SimulationEvent
from ..event_type import EventType, FoulType, FreeKickType
from ...football.player import PlayerSimulation, PlayerInjury
from ...football.team_simulation import Goal, TeamSimulation
from .. import OFF_POSITIONS, PITCH_EQUIVALENTS, PitchPosition
from ..game_state import GameState


class EventFactory:
    def get_possible_events(
        self,
        teams: tuple[TeamSimulation, TeamSimulation],
        state: GameState,
        last_event: Optional[SimulationEvent],
    ) -> list[list[EventType] | list[float]]:
        if last_event is None:
            return [[EventType.PASS], [1.0]]

        if last_event.outcome == EventOutcome.GOAL:
            return [[EventType.PASS], [1.0]]
        elif last_event.outcome == EventOutcome.SHOT_GOAL_KICK:
            return [[EventType.GOAL_KICK], [1.0]]
        elif last_event.outcome in [
            EventOutcome.SHOT_LEFT_CORNER_KICK,
            EventOutcome.SHOT_RIGHT_CORNER_KICK,
        ]:
            return [[EventType.CORNER_KICK], [1.0]]
        elif isinstance(last_event, FoulEvent):
            if (
                last_event.foul_type == FoulTypes.DEFENSIVE_FOUL
                and state.position == PitchPosition.OFF_BOX
            ):
                return [[EventType.PENALTY_KICK], [1.0]]
            else:
                return [[EventType.FREE_KICK], [1.0]]

        attacking_team = teams[0]
        transition_matrix = team_general_strategy(attacking_team.team_strategy, state)

        return [
            [
                EventType(i)
                for i, _ in enumerate(transition_matrix[last_event.event_type.value])
            ],
            list(transition_matrix[last_event.event_type.value]),
        ]

    def get_event(self, _state: GameState, event_type: EventType) -> SimulationEvent:
        state = deepcopy(_state)
        if event_type == EventType.PASS:
            return PassEvent(EventType.PASS, state)
        elif event_type == EventType.DRIBBLE:
            return DribbleEvent(EventType.DRIBBLE, state)
        elif event_type == EventType.FOUL:
            return FoulEvent(EventType.FOUL, state)
        elif event_type == EventType.SHOT:
            return ShotEvent(EventType.SHOT, state)
        elif event_type == EventType.CROSS:
            return CrossEvent(EventType.CROSS, state)
        elif event_type == EventType.CORNER_KICK:
            return CornerKickEvent(EventType.CORNER_KICK, state)
        elif event_type == EventType.FREE_KICK:
            return FreeKickEvent(EventType.FREE_KICK, state)
        elif event_type == EventType.GOAL_KICK:
            return GoalKickEvent(EventType.GOAL_KICK, state)
        elif event_type == EventType.PENALTY_KICK:
            return PenaltyKickEvent(EventType.PENALTY_KICK, state)

        return NotImplemented
