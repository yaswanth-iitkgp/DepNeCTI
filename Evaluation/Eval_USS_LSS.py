import sys

def lines_to_relations(true_lines):
    
    relations_list = []
    relations_oneline = []
    for line in true_lines:
        if line == '\n':
            relations_oneline = [relation for relation in relations_oneline if (relation[2]!= 'No_rel' and relation[2]!= 'root')]
            relations_list.append(relations_oneline)
            relations_oneline = []
        else:
            lst = line.strip().split('\t')
            relation = [lst[0],lst[4],lst[5]]
            relations_oneline.append(relation)
    
    return relations_list

def comps_from_relations(relations):
    lst = []
    nested_comp = []
    for rel in relations:
        if 'Comp_root' in rel:
            lst.append(rel)
            nested_comp.append(lst)
            lst = []
        else:
            lst.append(rel)
    return nested_comp
    
def unlabeled_metric(true_lines,pred_lines):
    
    correct = 0
    true_count = 0
    pred_count = 0
    for i in range(len(true_lines)):
        if true_lines[i]!= '\n': 
            true_lst = true_lines[i].split('\t')
            pred_lst = pred_lines[i].split('\t')
            if true_lst[5]!='No_rel':
                true_span = [true_lst[0],true_lst[4]]
                pred_span = [pred_lst[0],pred_lst[4]]
                if true_span==pred_span:
                    correct += 1
                true_count += 1
                pred_count += 1
    p = correct / pred_count if pred_count != 0 else 0
    r = correct / true_count if true_count != 0 else 0
    f1 = 2 * p * r / (p + r) if p != 0 and r != 0 else 0
    
    return round(100*f1,2)

def metric(true_lines, pred_lines):
    true_relations = lines_to_relations(true_lines)
    pred_relations = lines_to_relations(pred_lines)
    correct = 0
    predict_count = 0
    true_count = 0
    match = []
    true_labels = []
    em = 0
    tot_comps = 0
    for i in range(len(pred_relations)):
        
        true_relation_oneline = true_relations[i]
        pred_relation_oneline = pred_relations[i]
        tr_copy = [','.join(lst) for lst in true_relation_oneline]
        pr_copy = [','.join(lst) for lst in pred_relation_oneline]
        
        tr_comps = comps_from_relations(tr_copy)
        pr_comps = comps_from_relations(pr_copy)
        for comp in pr_comps:
            if comp in tr_comps:
                em += 1
        tot_comps += len(tr_comps)
#         if set(tr_copy) == set(pr_copy):
#             em += 1
        for rel in pred_relation_oneline:
            if rel in true_relation_oneline:
                correct += 1
        predict_count += len(pred_relation_oneline)
        true_count += len(true_relation_oneline)

    if correct == 0:
        p = 0
        r = 0
    else:
        p = correct / predict_count
        r = correct / true_count
    if p == 0 or r == 0:
        f1 = 0
    else:
        f1 = 2 * p * r / (p + r)
    a = 1.0*correct/(predict_count+true_count-correct)
#     em_per = em/len(pred_relations)
    em_per = em/tot_comps
    metrics_list = [100*p, 100*r, 100*f1, 100*a, 100*em_per]
#     metrics_list = [100*p, 100*r, 100*f1]
    metrics_list = [round(i,2) for i in metrics_list]

    return metrics_list

def main():

    if len(sys.argv) != 3:
        print("Usage: python script_name.py <true_file_path> <pred_file_path>")
        sys.exit(1)

    true_file = sys.argv[1]
    pred_file = sys.argv[2]

    with open(true_file) as t:
        with open(pred_file) as p:
            true_lines = t.readlines()
            pred_lines = p.readlines()

    metrics = metric(true_lines, pred_lines)
    print(f'Results for {true_file} are:\n')
    print(f'USS: {unlabeled_metric(true_lines, pred_lines)}\nLSS: {metrics[2]}\nExact match: {metrics[4]}\n')


if __name__=='__main__':

    main()

