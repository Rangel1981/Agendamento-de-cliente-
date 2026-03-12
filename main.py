import json

class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        return f"Cliente: {self.nome}, Telefone: {self.telefone}"
    
class Agendamento:
    def __init__(self, data, horario, cliente, servico):
        self.cliente = cliente
        self.data = data
        self.horario = horario
        self.servico = servico

    def exibir_confirmacao(self):
       return f"Confirmacao: {self.servico} para {self.cliente.nome} no dia {self.data} as {self.horario}."
    
class SistemaAgendamento:
    def __init__(self):
        self.agendamentos = []
        self.clientes = []
        self.carregar_dados()
    
    def adicionar_agendamento(self, novo_agendamento):
        for agendado in self.agendamentos:
            if agendado.data == novo_agendamento.data and agendado.horario == novo_agendamento.horario:
                print("ERRO: Horario ocupado!")
                return False 
        
        self.agendamentos.append(novo_agendamento)
        self.salvar_dados()
        print("SUCESSO: Agendamento realizado.")
        return True
        
    def salvar_dados(self):
        dados_para_salvar = []
        for agendamento in self.agendamentos:
            item = {
                "cliente": {"nome": agendamento.cliente.nome, "telefone": agendamento.cliente.telefone},
                "servico": agendamento.servico,
                "data": agendamento.data,
                "horario": agendamento.horario
            }
            dados_para_salvar.append(item)
        
        with open("agendamentos.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados_para_salvar, arquivo, indent=4, ensure_ascii=False)
        print("Dados sincronizados com o arquivo.")

    def carregar_dados(self):
        try:
            with open("agendamentos.json", "r", encoding="utf-8") as arquivo:
                dados_carregados = json.load(arquivo)
                for item in dados_carregados:
                    c = Cliente(item["cliente"]["nome"], item["cliente"]["telefone"])
                    a = Agendamento(item["data"], item["horario"], c, item["servico"])
                    self.agendamentos.append(a)
                    if c.nome not in [cli.nome for cli in self.clientes]:
                        self.clientes.append(c)
        except FileNotFoundError:
            pass

    def cancelar_agendamento(self, indice):
        if 0 <= indice < len(self.agendamentos):
            removido = self.agendamentos.pop(indice) 
            print(f"Sucesso: Agendamento de {removido.cliente.nome} removido.")
            self.salvar_dados()
            return True
        else:
            print(f"Erro: Indice {indice} invalido.")
            return False

class Menu:
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir_menu(self):
        while True:
            print("\n1- Cadastrar Cliente | 2- Agendar | 3- Listar | 4- Cancelar | 5- Sair")
            opcao = input("Escolha: ")

            if opcao == '1':
                nome = input("Nome: ")
                tel = input("Telefone: ")
                novo_c = Cliente(nome, tel)
                self.sistema.clientes.append(novo_c)
                print("Cliente cadastrado.")

            elif opcao == '2':
                if not self.sistema.clientes:
                    print("Erro: Cadastre um cliente primeiro!")
                    continue
                
                cliente = self.sistema.clientes[-1]
                servico = input("Servico: ")
                data = input("Data (dd/mm): ")
                hora = input("Hora (hh:mm): ")
                
                nova_reserva = Agendamento(data, hora, cliente, servico)
                self.sistema.adicionar_agendamento(nova_reserva)
            
            elif opcao == '3':
                if not self.sistema.agendamentos:
                    print("Agenda vazia.")
                else:
                    for a in self.sistema.agendamentos:
                        print(a.exibir_confirmacao())

            elif opcao == '4':
                if not self.sistema.agendamentos:
                    print("Erro: Nao ha agendamentos para cancelar.")
                    continue
                for i, a in enumerate(self.sistema.agendamentos):
                    print(f"{i} - {a.exibir_confirmacao()}")
                
                try:
                    indice = int(input("Numero do agendamento para cancelar: "))
                    self.sistema.cancelar_agendamento(indice)
                except ValueError:
                    print("ERRO: Digite apenas numeros inteiros.")
            
            elif opcao == '5':
                self.sistema.salvar_dados()
                print("Encerrando sistema...")
                break

if __name__ == "__main__":
    meu_sistema = SistemaAgendamento()
    meu_menu = Menu(meu_sistema)
    meu_menu.exibir_menu()
