from internal.app.generator.handler import generate_from_archive


class GeneratorService:
    def generate(self, archive_bytes):
        return generate_from_archive(archive_bytes)

