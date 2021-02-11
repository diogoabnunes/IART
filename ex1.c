// Objetivo: manter temperatura entre 22 e 24 graus.
// TS: T1 (temperatura interior).
// TE: T2 (temperatura exterior).

int TS, TE;

#define M_QUENTE (TS > 26)
#define QUENTE (TS > 24 && TS <= 26)
#define NORMAL (TS >= 22 && TS <= 24)
#define FRIO (TS >= 20 && TS < 22)
#define M_FRIO (TS < 20)
#define FORA_UTIL ((TE < 24 && QUENTE) || (TE > 22 && FRIO))

void AQ() {  // Ligar aquecedor

}
void NAQ() { // Desligar aquecedor
}
void AC() {  // Ligar ar frio
}
void NAC() { // Desligar ar frio
}
void AJ() { // Abrir janelas
}
void NAJ() { // Fechar janelas
}

void getTS() { return TS; }
void getTE() { return TE; }

void controlex(TS, TE) {
    if (NORMAL) {
        NAQ();
        NAC();
        NAJ();
    }
    else if ((QUENTE || FRIO) && FORA_UTIL) {
        NAQ();
        AJ();
        NAC();
    }
    else if ((QUENTE && !FORA_UTIL) || M_QUENTE) {
        NAQ();
        NAJ();
        AC();
    }
    else if ((FRIO && !FORA_UTIL) || M_FRIO) {
        AQ();
        NAJ();
        NAC();
    }
}

void main() {
    for (;;) {

    }
}