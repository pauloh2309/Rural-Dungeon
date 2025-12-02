from personagem1 import Personagem
from heroi import Heroi
from dialogo import Dialogos, texto
from util import Util

def verificar_final(npc1, npc2, dialogos):
    estatos_vivos = 0
    if npc1.estatos == 1:
        estatos_vivos += 1
    if npc2.estatos == 1:
        estatos_vivos += 1

    Util.limpar_tela()
    Util.separacao_cabecalho()
    print("{:^70}".format("FIM DA AVENTURA"))
    Util.separacao_cabecalho()

    if estatos_vivos == 2:
        print("{:^70}".format("FINAL BOM"))
        dialogos.dialogo_heroi_npc(dialogos.finais[0]['Bom'])
    elif estatos_vivos == 1:
        print("{:^70}".format("FINAL MEDIANO"))
        if npc1.estatos == 2 and npc2.estatos == 1:
            dialogos.dialogo_heroi_npc(dialogos.finais[1]['medio_edran'])
        elif npc1.estatos == 1 and npc2.estatos == 2:
            dialogos.dialogo_heroi_npc(dialogos.finais[2]['medio_kael'])
    else: 
        print("{:^70}".format("FINAL RUIM"))
        dialogos.dialogo_heroi_npc(dialogos.finais[3]['ruim'])
    
    Util.pausa(5)

def main():
    heroi = Heroi()
    heroi.personalizacao()
    
    edran = Personagem('Edran', 40, 10, 50, 0, 1) 
    kael = Personagem('Kael', 55, 25, 20, 0, 1) 
    
    dialogo_jogo = Dialogos(texto, heroi, edran, kael)
    dialogo_jogo.introducao()
    
    verificar_final(edran, kael, dialogo_jogo)

if __name__ == "__main__":
    
    main()