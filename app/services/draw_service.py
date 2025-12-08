from sqlalchemy.orm import Session
from app.models import Participant, Draw

def perform_draw(group_id: int, db: Session):
        participants = (
        db.query(Participant)
        .filter(Participant.group_id == group_id)
        .all()
    )

        if len(participants) < 2:
            raise Exception("É necessário pelo menos 2 participantes.")

        # Embaralhar a lista
        shuffled = participants[:]
        import random
        random.shuffle(shuffled)

        # Criar pares: cada um tira o próximo
        for i, giver in enumerate(shuffled):
            receiver = shuffled[(i + 1) % len(shuffled)]

            draw = Draw(
                group_id=group_id,
                giver_id=giver.id,
                receiver_id=receiver.id
            )

            db.add(draw)

            # Atualiza o participante para saber quem ele tirou
            giver.assigned_to_id = receiver.id

        db.commit()