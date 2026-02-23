import pytest

@pytest.fixture
def old_prisma_schema():
    return """
    model User {
      id    Int     @id @default(autoincrement())
      email String  @unique
      name  String?
    }
    """

@pytest.fixture
def new_prisma_schema():
    return """
    model User {
      id    Int     @id @default(autoincrement())
      email String  @unique
      name  String?
      role  String  @default("USER")
    }
    """
