#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script temporário para executar todos os diálogos seguidos.
Útil para visualizar toda a progressão da história.
"""

import dialogo_pygame

def main():
    dialogs = [
        ("1. Diálogo Térreo (NPC)", dialogo_pygame.dialogo_terreo),
        ("2. Introdução com Mestre Cleyton", dialogo_pygame.dialogo_intro_cleyton),
        ("3. Nível 1 - Goblin da Administração", dialogo_pygame.dialogo_nivel_1),
        ("4. Pós-Batalha Nível 1 (Cleyton)", dialogo_pygame.dialogo_pos_nivel_1),
        ("5. Nível 2 - Robô Natureza", dialogo_pygame.dialogo_nivel_2),
        ("6. Pós-Batalha Nível 2 (Cleyton)", dialogo_pygame.dialogo_pos_nivel_2),
        ("7. Nível 3 - Mago Místico", dialogo_pygame.dialogo_nivel_3),
        ("8. Pós-Batalha Nível 3 (Cleyton)", dialogo_pygame.dialogo_pos_nivel_3),
        ("9. Nível 4 - Robô Python", dialogo_pygame.dialogo_nivel_4),
        ("10. Conclusão (Cleyton)", dialogo_pygame.dialogo_conclusao),
    ]
    
    print("\n" + "="*60)
    print("EXECUTANDO TODOS OS DIÁLOGOS SEGUIDOS")
    print("="*60)
    
    for i, (name, dialog_func) in enumerate(dialogs, 1):
        print(f"\n[{i}/{len(dialogs)}] Iniciando: {name}")
        print("-" * 60)
        
        try:
            result = dialog_func()
            status = "✓ Concluído" if result else "⊘ Cancelado"
            print(f"Status: {status}")
        except Exception as e:
            print(f"✗ Erro ao executar: {e}")
        
        if i < len(dialogs):
            input("\nPressione ENTER para continuar ao próximo diálogo...")
    
    print("\n" + "="*60)
    print("TODOS OS DIÁLOGOS FORAM EXIBIDOS!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
