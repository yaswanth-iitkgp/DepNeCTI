import re
import pandas as pd
import sys
import os

def raw_to_clean(line):
    line = re.sub('( {1,})',' ',line)
    line = re.sub('-$','',line) #to remove the - in the end
    line = re.sub('<','',line)
    line = re.sub('-',' ',line)
    line = re.sub('(>\w+)','',line)
    line = re.sub(' $','',line) #to remove the space in the end
    line = re.sub('^ ','',line) #to remove the space in the beginning
    line = re.sub('( {1,})',' ',line)
    return line

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
    em_per = em/tot_comps
    metrics_list = [100*p, 100*r, 100*f1, 100*a, 100*em_per]
    metrics_list = [round(i,2) for i in metrics_list]

    return metrics_list

def Conversion(infile,outfile):
    df = pd.read_csv(infile)
    with open(infile) as f:
        raw_lines = f.readlines()
        lines = [raw_to_clean(line) for line in raw_lines]
    with open(outfile,'w') as w:
        for k in range(df.shape[0]):
            raw_line = raw_lines[k].strip()
            line = lines[k]
            comps_and_words = raw_line.strip().split() #space separated raw line gives list of compounds and individual words
            clean_tokens = line.strip().split() #space separated clean line gives clean tokens
            outmost_comp_list = [token for token in comps_and_words if '<' in token] #identifying compounds from comps_and_words
            c = 0
            d = 0
            i = 0
            while i < len(clean_tokens):   ###traversing through sentence tokens
                if c< len(outmost_comp_list):
                    outcomp = outmost_comp_list[c]
                clean_outcomp = raw_to_clean(outcomp) ### clean tokens of the outermost/parent compound
                token = comps_and_words[d] ### choosing token i.e., compound and word from comps_and_words list
                word = clean_tokens[i]
                if word == token: ###for individual words other than compounds
                    w.write(f'{i+1}\t{word}\tCompNo\t_\t{len(clean_tokens)+1}\tNo_rel'+'\n')
                    i += 1
                    d += 1
                else:
                    rem_string = outcomp
                    comp_len = len(clean_outcomp.split())
                    for p in range(comp_len):
                        subword = clean_outcomp.split()[p] ### getting p-th subword of the compound
                        if p==comp_len-1:   ###for last subword of an out-most compound
                            w.write(f'{i+1}\t{subword}\tComp{comp_len}\t_\t{len(clean_tokens)+1}\tComp_root'+'\n')
                            i += 1
                        else:    ### for remaining subwords in compound
                            subword_end = re.search('[^>]'+subword,rem_string).end() #getting end of the subword
                            rem_string = rem_string[subword_end:] ### remaining string after the subword/token
                            n = 0
                            ind = 0
                            p = 0
                            if rem_string[0] == '>': ###if remaining string starts with tag >\w+
                                flag = 1
                            else:                   
                                flag = 0
                            for ind in range(len(rem_string)):
                                if rem_string[ind] == '<': ###adding 1 to n if encountered an open bracket
                                    n -= 1
                                elif rem_string[ind] == '>': ###subtracting 1 from n if encountered an open bracket
                                    n += 1
                                elif rem_string[ind] == '-': ###adding 1 if encountered hyphen
                                    p += 1
                                if n-flag == 0: ### setting p to 0 if a compound is completed i.e., n-flag==0
                                    p = 0
                                if rem_string[0] == '>': #case1: remaining string starts with tag => >\w+
                                    #subcase1: remaining string has no new compound/ has an immediate relation word i.e., -\w+
                                    if rem_string.count('<')==0 or len(re.findall('^>\w+-\w+',rem_string))>0:
                                        st = ind+re.search('-\w+>',rem_string).end()-1
                                        temp = rem_string[st:]
                                        tag = re.findall('>(\w+)',temp)[0]
                                        break
                                    else:
                                        if len(re.findall('^>\w+>\w+',rem_string))==0: #subcase2 counterpart
                                            if n-flag == 1 and p>=0:
                                                st = ind
                                                temp = rem_string[st:]
                                                tag = re.findall('>(\w+)',temp)[0]
                                                break
                                        else: #subcase2: multiple tags closing
                                            #subsubcase1: multiple tags closing after the relation word
                                            if len(re.findall('-\w+(?:>\w+)+>(\w+)',rem_string))>0:  
                                                st = re.search('-\w+(?:>\w+)+>(\w+)',rem_string).end()-1
                                                tag = re.findall('-\w+(?:>\w+)+>(\w+)',rem_string)[0]
                                            else: #subsubcase2: normal tags after relation word
                                                g = re.findall('^(?:>\w+)*>\w+',rem_string)[0].count('>')
                                                if n-flag-g==1:
                                                    st = ind
                                                    temp = rem_string[st:]
                                                    tag = re.findall('>(\w+)',temp)[0]
                                            break
                                #remaining cases: remaining string starting with related word => -\w+ (or) compound => -<\w+-\w+>\w+
                                else: 
                                    if n-flag == 1:
                                        st = ind
                                        temp = rem_string[st:]
                                        tag = re.findall('>(\w+)',temp)[0]
                                        break
                            pre_tag_string = rem_string[:st]
                            num = len(raw_to_clean(pre_tag_string).split())
                            w.write(f'{i+1}\t{subword}\tComp{comp_len}\t_\t{i+num+1}\t{tag}'+'\n')
                            i += 1
                    c += 1
                    d += 1
            w.write(f'{i+1}\tDUMMY\tCompNo\t_\t{0}\troot\n')
            w.write('\n')
    return

def evaluate():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    pred_file = os.path.join(script_dir, 'pred_file.txt')
    true_file = os.path.join(script_dir,'gold_input.txt')
    true_file_new = os.path.join(script_dir,'gold_input_NeCTIS_format.txt')

    Conversion(true_file,true_file_new)

    with open(true_file_new) as t:
        with open(pred_file) as p:
            true_lines = t.readlines()
            pred_lines = p.readlines()
        metrics = metric(true_lines,pred_lines)
        print(f'Results are:\n')
        print(f'Precision: {metrics[0]}\nRecall: {metrics[1]}\nF1: {metrics[2]}\nExact match: {metrics[4]}\n')
    return 

def main():
    evaluate()

if __name__ == '__main__':
    main()