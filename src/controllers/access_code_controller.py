from ..services.access_code_service import AccessCodeService


class AccessCodeController:
    def __init__(self, session):
        self.service = AccessCodeService(session)

    def get_all(self):
        return self.service.get_all()

    def generate(self):
        return self.service.generate()