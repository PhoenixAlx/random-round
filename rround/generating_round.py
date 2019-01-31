from otree.models_concrete import ParticipantToPlayerLookup
from .models import Constants, Player, Group, Subsession
from django.db.models import Max


def one_more_round(view, page_sequence):
    player = view.player
    participant = view.participant
    highest_page_index = participant.participanttoplayerlookup_set.all().aggregate(max=Max('page_index'))[
                             'max'] or 0

    curround = player.round_number
    newround = curround + 1
    session = participant.session

    s, _ = Subsession.objects.get_or_create(
        round_number=newround, session=session)

    max_group_id = s.group_set.all().aggregate(max=Max('id_in_subsession'))['max']

    if max_group_id:
        id_in_subsession = max_group_id + 1
    else:
        id_in_subsession = 1
    g, _ = Group.objects.get_or_create(
        session=session,
        subsession=s,
        round_number=newround, defaults={'id_in_subsession': id_in_subsession}
    )

    p = Player(
        session=participant.session,
        subsession=s,
        round_number=newround,
        participant=participant,
        group=g,
        id_in_group=player.id_in_group
    )
    p.save()

    participant_to_player_lookups = []
    for v in page_sequence:
        highest_page_index += 1
        url = v.get_url(
            participant_code=participant.code,
            name_in_url=Constants.name_in_url,
            page_index=highest_page_index
        )
        participant_to_player_lookups.append(
            ParticipantToPlayerLookup(
                participant=participant,
                participant_code=participant.code,
                page_index=highest_page_index,
                app_name=participant._current_app_name,
                player_pk=p.id,
                subsession_pk=s.pk,
                session_pk=participant.session.pk,
                url=url))
        participant._max_page_index += 1
    ParticipantToPlayerLookup.objects.bulk_create(
        participant_to_player_lookups
    )
