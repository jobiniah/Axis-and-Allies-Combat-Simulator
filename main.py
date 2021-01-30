from units import *
from analysis import *
import pandas as pd
import concurrent.futures

attacking_units = get_attacking_units()
defending_units = get_defending_units()

group_combats = []
group_logs = []
win_loss = []
overall_df = pd.DataFrame(columns=['result','att_losses','def_losses'])

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    # Start the load operations and mark each future with its URL
    future_to_combat = {executor.submit(combat, attacking_units, defending_units): mini_combat for mini_combat in range(10000)}
concurrent.futures.wait(future_to_combat)
for future in list(future_to_combat.keys()):
        mini_combat = future.result()
        group_combats.append( mini_combat )
        group_logs.append( mini_combat.combat_log.copy() )
        win_loss.append( mini_combat.combat_log['result'] )
        
        losses  = mini_combat.combat_log
        df_result = losses.pop('result')
        att_arr = []
        def_arr = []
        overall_df = overall_df.append( {'result':df_result,'att_losses':losses['tot_attack_loss'] ,'def_losses':losses['tot_defence_loss']} , ignore_index=True)

win_loss_neut(overall_df)
loss_delta(overall_df)
cost_delta(group_logs)

print('All done')