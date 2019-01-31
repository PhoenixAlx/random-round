from otree.models_concrete import ParticipantToPlayerLookup
from .models import Constants, Player, Group, Subsession
from django.db.models import Max
from .pages import page_sequence
from django.apps import apps
from rround import cp

def preparing_db(session):
    max_round = session.vars.get('max_round', 1)
    for r in range(2, max_round + 1):
        s = Subsession(round_number=r, session=session)
        s.save()  # todo: move to bulk_create
        g = Group(
            session=session,
            subsession=s,
            round_number=r,
            id_in_subsession=1
        )
        g.save()
        for i, part in enumerate(session.get_participants()):
            p = Player(
                session=session,
                subsession=s,
                round_number=r,
                participant=part,
                group=g,
                id_in_group=i + 1
            )
            p.save()
            if r <= part.vars['final_round']:
                one_more_round(
                    participant=part,
                    player=p,
                    group=g,
                    subsession=s,
                    session=session
                )


def one_more_round(participant, player, group, subsession, session):
    app_name = player._meta.app_label
    highest_page_index = participant.participanttoplayerlookup_set.all().aggregate(max=Max('page_index'))[
                             'max'] or 0

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
                app_name=app_name,
                player_pk=player.id,
                subsession_pk=subsession.pk,
                session_pk=participant.session.pk,
                url=url))
        participant._max_page_index += 1
    ParticipantToPlayerLookup.objects.bulk_create(
        participant_to_player_lookups
    )
