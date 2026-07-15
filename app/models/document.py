from datetime import datetime, timezone

from sqlalchemy import(
    String,
    Integer,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import(
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key= True
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable= False
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    filepath: Mapped[str] = mapped_column(String(500), nullable= False)

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship("User", back_populates="documents")