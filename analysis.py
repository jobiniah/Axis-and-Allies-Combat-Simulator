from matplotlib import pyplot as plt
import matplotlib
import numpy as np

def win_loss_neut(df):
    result_arr = df.result.to_list()
    win_perc = (len([ele for ele in result_arr if ele == 1]) / len(result_arr)) * 100
    loss_perc = (len([ele for ele in result_arr if ele == 0]) / len(result_arr)) * 100
    neut_perc = (len([ele for ele in result_arr if ele == 2]) / len(result_arr)) * 100
    print(f'The percents for this combat are win:{win_perc}, loss:{loss_perc}, neutral:{neut_perc}')

def loss_delta(df):
    deltas = []
    for i, row in df.iterrows():
        deltas.append(row.def_losses - row.att_losses)

    plt.figure()
    plt.title('Unit Loss Delta (Att +)')
    plt.hist(deltas, bins=int(max(deltas)-min(deltas)), range=(min(deltas),max(deltas)) )
    plt.savefig('result.jpg')

def cost_delta(logs):
    combat_index=-1
    att_cost_arr, def_cost_arr =[],[]
    for combat in logs:
        combat_index+=1
        att_cost_arr.append(0)
        def_cost_arr.append(0)
        combat.pop('tot_attack_loss')
        combat.pop('tot_defence_loss')
        combat.pop('result')
        for round in combat.keys():
            for unit in combat[round]['attack_loss']:
                att_cost_arr[combat_index] += unit.cost 
            for unit in combat[round]['defence_loss']:
                def_cost_arr[combat_index] += unit.cost
    att_cost_arr,def_cost_arr = np.array(att_cost_arr),np.array(def_cost_arr)
    deltas = def_cost_arr - att_cost_arr

    plt.figure()
    plt.title('Loss Cost Delta (Att +)')
    plt.hist(deltas, bins=int(max(deltas)-min(deltas)), range=(min(deltas),max(deltas)) )
    plt.savefig('costs.jpg')

