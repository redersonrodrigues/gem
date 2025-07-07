from app.Model.Pessoa import Pessoa

class PessoaControl:
    def listar(self):
        try:
            pessoas = Pessoa.all()
            for pessoa in pessoas:
                print(f"{pessoa.id} - {pessoa.nome}<br>")
        except Exception as e:
            print(e)

    def show(self, param):
        if param.get('method') == 'listar':
            self.listar()