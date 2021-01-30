import numpy as np

d6 = lambda : np.random.randint(1,7)

class Unit:
    def __init__(self, attack, defense, id, cost, health=1):
        self.attack = attack
        self.defense = defense
        self.id = id
        self.cost = cost
        self.health = health

infantry = Unit(1,2,1,3)
armor = Unit(3,2,2,5)
fighter = Unit(3,4,3,12)
bomber = Unit(4,1,4,15)
anti_aircraft = Unit(0,1,5,5)
battleship = Unit(4,4,6,24,2)
aircraft_carrier = Unit(1,3,7,18)
transport = Unit(0,1,8,8)
submarine = Unit(2,2,9,8)

Unit_List = [infantry,armor,fighter,bomber,anti_aircraft,battleship,aircraft_carrier,transport,submarine]

class combat:
    def __init__(self, attacking_units, defending_units):
        self.attacking_units = attacking_units.copy()
        self.defending_units = defending_units.copy()
        self.combat_rounds = 0
        self.combat_log = {'tot_attack_loss':0,'tot_defence_loss':0}
        self.combat_simulation()
    
    def combat_simulation(self):
        self.round = 0
        self.combat_log[self.round] = {"attack_loss":[],"defence_loss":[]}
        self.special_round()
        self.settle_losses()
        while(True):
            try:
                self.combat_log['result']
                return self.combat_log
            except KeyError:
                self.round += 1                
            self.combat_log[self.round] = {"attack_loss":[],"defence_loss":[]}
            self.roll_damage()
            self.settle_losses()
            
    
    def special_round(self):
        self.att_losses, self.def_losses = 0, 0
        pop_list = []
        
        #attack
        for unit_index in range(len(self.attacking_units)):
            if( self.attacking_units[ unit_index ].id == submarine.id ):
                if( d6() <= submarine.attack ):
                    self.def_losses += 1
            elif( self.attacking_units[ unit_index ].id == battleship.id ):
                land_barrage = input( "Land Barage? True/False:" )
                if( d6() <= battleship.attack and land_barrage ):
                    self.def_losses += 1
                    pop_list.append(unit_index)
                elif(land_barrage):
                    pop_list.append(unit_index)

        # submarines
        for unit_index in range(len(self.defending_units)):
            if( self.defending_units[ unit_index ].id == submarine.id ):
                if( d6() < submarine.defense ):
                    self.def_losses += 1

        for unit in self.defending_units:
            if(unit.id == anti_aircraft.id):
                self.aa_gun_defense()
                break
           
    def aa_gun_defense(self):
        #identify airplanes
        attacking_airplane_index,dead_airplane_index = [],[]
        for unit_index in range(len( self.attacking_units )):
            if( self.attacking_units[unit_index].id == bomber.id or self.attacking_units[unit_index].id == fighter.id):
                attacking_airplane_index.append(unit_index)
        
        #roll against airplanes
        for index in attacking_airplane_index:
            if( d6() <= anti_aircraft.defense ):
                dead_airplane_index.append( index )
        
        #log elimination
        for index in dead_airplane_index:
            self.combat_log[self.round]['attack_loss'].append( self.attacking_units[index] )
            self.combat_log['tot_attack_loss'] += 1
        
        #eliminate airplanes
        self.attacking_units = list(np.delete(self.attacking_units, dead_airplane_index ))
        
        #remove aa_gun from defense
        for unit_index in range(len( self.defending_units )):
            if( self.defending_units[unit_index].id == anti_aircraft.id):
                removed_index = unit_index
        try:
            self.defending_units = list(np.delete( self.defending_units, removed_index ))
        except:
            self.defending_units


    def roll_damage(self):
        self.att_losses, self.def_losses = 0,0
        for unit in self.attacking_units:
            if( np.random.randint(1,7) <= unit.attack ):
                self.def_losses += 1
        
        for unit in self.defending_units:
            if( np.random.randint(1,7) <= unit.defense ):
                self.att_losses += 1

    def settle_losses(self):
        self.defending_units = sorted(self.defending_units, key=lambda x: x.cost, reverse=True)
        for unit in self.defending_units:
                if(unit.health>1):
                    unit.health-=1
                    self.def_losses -= 1
        for _ in range(self.def_losses):
            try:
                self.combat_log[self.round]['defence_loss'].append( self.defending_units.pop() )
                self.combat_log['tot_defence_loss'] += 1
            except IndexError:
                break
        
        self.attacking_units = sorted(self.attacking_units, key=lambda x: x.cost, reverse=True)
        for unit in self.attacking_units:
                if(unit.health>1):
                    unit.health-=1
                    self.att_losses -= 1
        for _ in range(self.att_losses):
            try:
                self.combat_log[self.round]['attack_loss'].append( self.attacking_units.pop() )
                self.combat_log['tot_attack_loss'] += 1
            except IndexError:
                break
        
        if( len(self.attacking_units) < 1 and len(self.defending_units) < 1 ):
            self.combat_log['result'] = 2
        elif( len(self.attacking_units) < 1 ):
            self.combat_log['result'] = 0
        elif( len(self.defending_units) < 1 ):
            self.combat_log['result'] = 1

def get_attacking_units():
    attacking_units = []
    attacking_unparsed = input("input multiples of attacking units by id.  e.g. 5x1,3x3,2x4:")
    for unit_set in attacking_unparsed.split(','):
        unit_set_split = unit_set.split('x')
        for _ in range(int(unit_set_split[0])):
            unit_list_index = int( unit_set_split[1] ) - 1
            attacking_units.append( Unit_List[ unit_list_index ] )
    return attacking_units

def get_defending_units():
    defending_units = []
    defending_unparsed = input("input multiples of defending units by id.  e.g. 5x1,3x3,2x4:")
    for unit_set in defending_unparsed.split(','):
        unit_set_split = unit_set.split('x')
        for _ in range(int(unit_set_split[0])):
            unit_list_index = int( unit_set_split[1] ) - 1
            defending_units.append( Unit_List[ unit_list_index ] )
    return defending_units

if __name__=="__main__":
    attacking_units = [fighter,bomber]
    defending_units = [anti_aircraft,infantry]
    test_combat = combat(attacking_units,defending_units)
    test_combat.combat_log
    print('done')
