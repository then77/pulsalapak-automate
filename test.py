from pulsalapak import Pulsalapak

pulsa = Pulsalapak('MjUyNzkx', '059b71ae1f9320212835bd1b54c66150')
pulsa.login()
print(pulsa.create_deposit('13000', 'qris_oke'))