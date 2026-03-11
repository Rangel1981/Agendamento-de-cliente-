import json

class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        return f"Cliente: {self.nome}, Telefone: {self.telefone}"
    
class Agendamento:
    def __init__(self,data, horario, cliente, servico):
        self.cliente = cliente
        self.data = data
        self.horario = horario
        self.servico = servico

    def exibir_confirmacao(self):
       return f"Confirmação: {self.servico} para {self.cliente.nome} no dia {self.data} às {self.horario}."
    
class SistemaAgendamento:
    def __init__(self):
        self.agendamentos = []
    
    def adicionar_agendamento(self, novo_agendamento):
        for agendado in self.agendamentos:
            if agendado.data == novo_agendamento.data and agendado.horario == novo_agendamento.horario:
                print(f"❌ ERRO: Horário ocupado!")
                return False 
        
       
        self.agendamentos.append(novo_agendamento)
        print(f"✅ SUCESSO!")
        return True
       
    def salvar_dados(self):
        dados_para_salvar = []

        for agendamento in self.agendamentos:
            item = {
                "cliente": {
                    "nome": agendamento.cliente.nome,
                    "telefone": agendamento.cliente.telefone
                },
                "servico": agendamento.servico,
                "data": agendamento.data,
                "horario": agendamento.horario
            }
            dados_para_salvar.append(item)
        
        with open("agendamentos.json", "w") as arquivo:
            json.dump(dados_para_salvar, arquivo, indent=4, ensure_ascii=False)
        print("Dados salvos com sucesso!")

class Menu:
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir_menu(self):
        while True:
            print("\n1- Cadastrar Cliente | 2- Agendar | 3- Listar | 4- Sair")
            opcao = input("Escolha: ")

            if opcao == '1':
                nome = input("Nome: ")
                tel = input("Telefone: ")
                novo_c = Cliente(nome, tel)
                self.sistema.clientes.append(novo_c) # Guardamos no sistema!
                print("Cliente cadastrado!")

            elif opcao == '2':
                if not self.sistema.clientes:
                    print("Erro: Cadastre um cliente primeiro!")
                    continue
                
                # Para simplificar, vamos usar o último cliente cadastrado
                cliente = self.sistema.clientes[-1] 
                servico = input("Serviço: ")
                data = input("Data (dd/mm): ")
                hora = input("Hora (hh:mm): ")
                
                nova_reserva = Agendamento(data, hora, cliente, servico)
                self.sistema.adicionar_agendamento(nova_reserva)
            
            elif opcao == '3':
                for a in self.sistema.agendamentos:
                    print(a.exibir_confirmacao())

            elif opcao == '4':
                break