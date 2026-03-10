from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..domain.config import GameConfig
from ..domain.constants import DICE_TYPES
from ..domain.models import RollContext, TurnState
from ..domain.modes import GameMode
from ..domain.stats import Stats
from ..services.logic import (
    apply_turn_effects,
    build_temp_result,
    finalize_result,
    resolve_turn,
    roll_dice,
)
from ..storage.sqlite_storage import (
    clear_rolls,
    count_rolls,
    export_rolls_to_csv,
    init_db,
    paginated_rolls,
    save_roll,
)

app = FastAPI(title="Dice Game API", version="1.0.0")

init_db()

state = TurnState(
    game_config=GameConfig(),
    stats=Stats(),
    player_points=0,
)


# ------------- Request Models ------------- #
class RollRequest(BaseModel):
    mode: str
    dice_type: str
    num_dice: int


# ------------- Post/roll ------------- #
@app.post("/roll")
def roll(request: RollRequest):

    if request.dice_type not in DICE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid dice type")

    try:
        mode = GameMode[request.mode.upper()]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Invalid game mode") from exc

    sides = DICE_TYPES[request.dice_type]

    context = RollContext(
        mode=mode,
        dice_type=request.dice_type,
        num_dice=request.num_dice,
        sides=sides,
    )

    rolls = roll_dice(context)

    temp_result = build_temp_result(context, rolls, state.player_points)

    outcome, delta = resolve_turn(state.game_config, temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)

    result = finalize_result(temp_result, outcome, delta, state.player_points)

    save_roll(result)

    return {
        "rolls": result.rolls,
        "total": result.total,
        "outcome": result.outcome,
        "points_delta": result.points_delta,
        "points_total": result.points_total,
        "extra_turn": extra_turn,
    }


# ------------- Get/history ------------- #
@app.get("/history")
def get_history(limit: int = 10, offset: int = 0):

    rows = paginated_rolls(limit=limit, offset=offset)

    return rows


# ------------- Get/stats ------------- #
@app.get("/stats")
def get_stats():

    total = count_rolls()

    return {"total_rolls": total}


# ------------- Delete/history ------------- #
@app.delete("/history")
def delete_history():

    deleted = clear_rolls(reset_ids=True)

    return {"deleted_records": deleted}


# ------------- Get/history/export ------------- #
@app.get("/history/export")
def export_history():

    exported = export_rolls_to_csv()

    if exported == 0:
        raise HTTPException(status_code=404, detail="No rolls to export")

    return {
        "message": f"Exported {exported} rolls to CSV file",
        "records": exported,
        "file": "roll_history.csv",
    }
