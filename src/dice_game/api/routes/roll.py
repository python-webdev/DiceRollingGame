from fastapi import APIRouter, HTTPException

from dice_game.services.game_session_service import play_session_turn

from ..schemas import RollRequest, RollResponse

router = APIRouter(prefix="/sessions", tags=["roll"])


@router.post("/{game_session_id}/roll", response_model=RollResponse)
def roll(game_session_id: str, request: RollRequest):
    try:
        result = play_session_turn(
            game_session_id=game_session_id,
            mode_name=request.mode,
            dice_type=request.dice_type,
            num_dice=request.num_dice,
        )
        return result
    except ValueError as e:
        error_message = str(e)
        if error_message == "Game session not found":
            raise HTTPException(status_code=404, detail=error_message) from e
        if error_message == "Invalid dice type":
            raise HTTPException(status_code=400, detail=error_message) from e
        if error_message == "Invalid game mode":
            raise HTTPException(status_code=400, detail=error_message) from e

        raise HTTPException(status_code=500, detail="Internal server error") from e
