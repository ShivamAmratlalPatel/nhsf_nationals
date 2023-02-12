from ..models import FootballPitch, FootballSchedule


def get_football_schedule() -> dict:
    """Return a dict of football schedules by pitches"""
    schedule = FootballSchedule.objects.all().order_by("time")
    pitches = FootballPitch.objects.all()
    output = {}
    for pitch in pitches:
        output[pitch.name] = []
        for game in schedule:
            if game.pitch_id == pitch:
                entry = {"game": str(game),
                         "time": game.get_time,
                         "result": game.get_result}
                output[pitch.name].append(entry)
    return output
