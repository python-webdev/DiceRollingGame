from fastapi import APIRouter, HTTPException

from dice_game.services.game_session_service import play_session_turn

from ...services.exceptions import (
    GameSessionNotFoundError,
    InternalServerError,
    InvalidDiceTypeError,
    InvalidGameModeError,
)
from ..schemas import RollRequest, RollResponse

router = APIRouter(prefix="/sessions", tags=["roll"])


@router.post("/{game_session_id}/roll", response_model=RollResponse)
def roll(game_session_id: str, request: RollRequest):
    try:
        result = play_session_turn(
            game_session_id=game_session_id,
            mode_name=request.mode.value,
            dice_type=request.dice_type.value,
            num_dice=request.num_dice,
        )
        return result
    except GameSessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except InvalidDiceTypeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InvalidGameModeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InternalServerError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
