from app.models.user.user import User


class UserMapper:
    def to_entity(self, row):
        return User(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            perfil=row["perfil"],
            ativo=bool(row["ativo"])
        )

    def to_dict(self, entity):
        return {
            "id": entity.id,
            "nome": entity.nome,
            "email": entity.email,
            "senha_hash": entity.senha_hash,
            "perfil": entity.perfil,
            "ativo": entity.ativo
        }