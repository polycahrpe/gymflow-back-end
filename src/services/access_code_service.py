from ..models.repositories.access_code_repository import AccessCodeRepository


class AccessCodeService:
    def __init__(self, session):
        self.repo = AccessCodeRepository(session)

    def get_all(self):
        return self.repo.get_all()

    def generate(self):
        return self.repo.generate()