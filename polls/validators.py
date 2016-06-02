class Validators():
    def rutValido(self, rut):
        validChars = "1234567890kK-."
        for v in rut:
            if v not in validChars:
                return False
        rfiltro = rut.replace(".","").replace("-","")
        rutx = str(rfiltro[0:len(rfiltro)-1])
        digito = str(rfiltro[-1])
        multiplo = 2
        total = 0
        div = ""
        for reverso in reversed(rutx):
            total += int(reverso) * multiplo
            if multiplo == 7:
                multiplo = 2
            else:
                multiplo += 1
            modulus = total % 11
            verificador = 11 - modulus
            if verificador == 10:
                div = "k"
            elif verificador == 11:
                div = "0"
            elif verificador < 10:
                div = verificador
        if str(div) == str(digito):
            return True
        else:
            return False
