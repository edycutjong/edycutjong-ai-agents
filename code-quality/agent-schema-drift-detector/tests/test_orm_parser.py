def test_parse_prisma(tmp_path):
    from lib.orm_parser import parse_orm_models
    
    d = tmp_path / "models"
    d.mkdir()
    f = d / "schema.prisma"
    f.write_text('''
    model User {
        id    Int     @id @default(autoincrement())
        email String  @unique
        name  String?
        posts Post[]
        
        @@map("users")
    }
    
    model Post {
        id       Int    @id
        title    String @map("post_title")
        authorId Int
        author   User   @relation(fields: [authorId], references: [id])
        @@map("posts")
    }
    ''')
    
    models = parse_orm_models(d)
    
    assert "users" in models
    assert "posts" in models
    
    # Check users
    users_cols = models["users"]["columns"]
    assert "id" in users_cols
    assert "email" in users_cols
    assert "name" in users_cols
    assert "posts" not in users_cols # Relation should be skipped
    
    assert users_cols["email"]["nullable"] is False
    assert users_cols["name"]["nullable"] is True
    
    # Check posts mapped column
    posts_cols = models["posts"]["columns"]
    assert "post_title" in posts_cols
    assert "title" not in posts_cols
    assert "author" not in posts_cols # Relation should be skipped

def test_parse_drizzle(tmp_path):
    from lib.orm_parser import parse_orm_models
    f = tmp_path / "schema.ts"
    f.write_text('''
    export const users = pgTable('users', {
        id: serial('id').primaryKey(),
        name: text('full_name').notNull(),
        age: integer('age')
    });
    ''')
    
    models = parse_orm_models(f)
    assert "users" in models
    cols = models["users"]["columns"]
    assert "id" in cols
    assert "full_name" in cols
    assert cols["full_name"]["nullable"] is False
    assert cols["age"]["nullable"] is True

def test_parse_sqlalchemy(tmp_path):
    from lib.orm_parser import parse_orm_models
    f = tmp_path / "models.py"
    f.write_text('''
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column('full_name', String, nullable=False)
        age = Column(Integer)
        
    class NoTable(Base):
        pass
    ''')
    
    models = parse_orm_models(f)
    assert "users" in models
    assert "NoTable" not in models
    
    cols = models["users"]["columns"]
    assert "id" in cols
    assert "full_name" in cols
    assert cols["full_name"]["nullable"] is False
    assert cols["age"]["nullable"] is True
