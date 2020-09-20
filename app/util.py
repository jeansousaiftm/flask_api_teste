from datetime import datetime
import re

def validaEmail(email):
	return re.match("[^@]+@[^@]+\.[^@]+", email)

def validaData(data):
    try:
        ano, mes, dia = map(int, str(data).split('-'))
        if mes < 1 or mes > 12 or ano <= 0:
            return False
        if mes in (1, 3, 5, 7, 8, 10, 12):
            ultimo_dia = 31
        elif mes == 2:
            if (ano % 4 == 0) and (ano % 100 != 0 or ano % 400 == 0):
                ultimo_dia = 29
            else:
                ultimo_dia = 28
        else:
            ultimo_dia = 30
        if dia < 1 or dia > ultimo_dia:
            return False
        return True
    except ValueError:
        return False

def validaCPF(cpf):

    if not isinstance(cpf, str):
        return False
		
    cpf = re.sub("[^0-9]",'',cpf)
    
    if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
        return False

    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False
	
def formataHora(total):
	h = int(total / 3600)
	m = int((total - (h * 3600)) / 60)
	s = int(total - (h * 3600) - (m * 60))
	return str(h) + ":" + "{:02d}".format(m) + ":" + "{:02d}".format(s)