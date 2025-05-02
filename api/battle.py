

class Battle:
    def __init__(self, attacking_fleet, defending_fleet):
        self.attacking_fleet = attacking_fleet
        self.defending_fleet = defending_fleet
        self.result = None

    def battle(self):
        attacking_fleet = [[ship.integrity, ship] for ship in self.attacking_fleet]
        defending_fleet = [[ship.integrity, ship] for ship in self.defending_fleet]

        ROUNDS = 3
        attacker_destroyed = []
        defending_destroyed = []

        total_attack_damage = 0
        total_defender_damage = 0

        destroyed_ship_ids = []

        report = ''

        for battle_round in range(ROUNDS):
            for atk_idx, attacking in enumerate(attacking_fleet):
                attacking_integrity, attacking_ship = attacking

                for def_idx, defending in enumerate(defending_fleet):
                    defending_integrity, defending_ship = defending

                    defender_damage = max((defending_ship.offense_power - attacking_ship.shield_power), 0)
                    attacker_damage = max((attacking_ship.offense_power - defending_ship.shield_power), 0)

                    attacking_integrity -= defender_damage
                    defending_integrity -= attacker_damage

                    total_attack_damage += attacker_damage
                    total_defender_damage += defender_damage

                    attacking_fleet[atk_idx][0] -= defender_damage
                    defending_fleet[def_idx][0] -= attacker_damage

                    battle_message = f'''
                    Round {battle_round+1}
                    Attacking {attacking_ship.name} [{attacking_integrity}] {attacker_damage} Damage VS Defending {defending_ship.name} [{defending_integrity}] {defender_damage}                    
                    '''
                    print(battle_message)
                    report += battle_message

                    if attacking_integrity <= 0:
                        attacker_destroyed.append(atk_idx)
                        destroyed_ship_ids.append(attacking_ship.id)
                        
                    else:
                        attacking_fleet[atk_idx][0] = attacking_integrity

                    if defending_integrity <= 0:
                        defending_destroyed.append(def_idx)
                        destroyed_ship_ids.append(defending_ship.id)

                    else:
                        defending_fleet[def_idx][0] = defending_integrity
            
                attacking_fleet = [i for i in attacking_fleet if i[0] > 0]
                defending_fleet = [i for i in defending_fleet if i[0] > 0]

                print(f'Attacking fleet number: {len(attacking_fleet)} VS Defendng fleet number {len(defending_fleet)}')

                if len(attacking_fleet) == 0 or len(defending_fleet) == 0:
                    batle_result = self.battle_result(attacking_fleet, defending_fleet),
                    report += str(batle_result)
                    return {
                        'rounds': battle_round + 1,
                        'total_attacker_damage': total_attack_damage,
                        'total_defender_damage': total_defender_damage,
                        'attacker_fleet_left': [ship[1].name for ship in attacking_fleet],
                        'defender_fleet_left': [ship[1].name for ship in defending_fleet],
                        'attacker_remaining_fleet': [ship[1] for ship in attacking_fleet],
                        'defender_remaining_fleet': [ship[1] for ship in defending_fleet],
                        'battle_result': self.battle_result,
                        'destroyed_ship_ids': destroyed_ship_ids,
                        'report': report
                    }

        attacking_fleet = [i for i in attacking_fleet if i[0] > 0]
        defending_fleet = [i for i in defending_fleet if i[0] > 0]
        batle_result = self.battle_result(attacking_fleet, defending_fleet)
        report += str(batle_result)
        return {
            'rounds': battle_round + 1,
            'total_attacker_damage': total_attack_damage,
            'total_defender_damage': total_defender_damage,
            'attacker_fleet_left': [ship[1].name for ship in attacking_fleet],
            'defender_fleet_left': [ship[1].name for ship in defending_fleet],
            'attacker_remaining_fleet': [ship[1] for ship in attacking_fleet],
            'defender_remaining_fleet': [ship[1] for ship in defending_fleet],
            'battle_result': self.battle_result(attacking_fleet, defending_fleet),
            'destroyed_ship_ids': destroyed_ship_ids,
            'report': report
        }

    def battle_result(self, attacking_fleet, defending_fleet):
        if  len(attacking_fleet) == 0 and len(defending_fleet) == 0:
            return 'NO_SURVIVORS'

        if len(attacking_fleet) == 0 and len(defending_fleet) > 0:
            return 'DEFENDER_WINS'

        if len(attacking_fleet) > 0 and len(defending_fleet) > 0:
            return 'DRAW'

        return 'ATTACKER_WINS'
