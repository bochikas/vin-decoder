from pydantic import BaseModel


class Vehicle(BaseModel):
    """Vehicle information."""

    id: int
    year: int
    make: str
    model: str
    type: str
    color: str
    weight: float

    class Config:
        from_attributes = True

    def __repr__(self):
        print(f'<class Vehicle :[model={self.model}, year={self.year}]>')
