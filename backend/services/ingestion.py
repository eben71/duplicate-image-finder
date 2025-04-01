from backend.models.image import Image
from backend.db.session import engine
from backend.services.worker.tasks import generate_embedding
from sqlmodel import Session
from datetime import datetime
import uuid

def fake_scrape_images(user_id: int):
    fake_image_names = [f"photo_{uuid.uuid4().hex[:6]}.jpg" for _ in range(3)]
    created = []

    with Session(engine) as session:
        for name in fake_image_names:
            img = Image(
                user_id=user_id,
                file_name=name,
                file_path=f"/fake/path/{name}",
                uploaded_at=datetime.utcnow()
            )
            session.add(img)
            session.commit()
            session.refresh(img)
            generate_embedding.delay(img.id)
            created.append(img)

    return created
