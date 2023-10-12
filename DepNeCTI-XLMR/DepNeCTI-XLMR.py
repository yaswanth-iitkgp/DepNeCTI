import sys
import os
import re
# sys.path.append('/content/drive/MyDrive/trankit-master')

from trankit import tpipeline
from trankit.tpipeline import TPipeline as tpip
from trankit.iterators.tagger_iterators import TaggerDataset
import torch
import logging

# Initialize a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Create a file handler and set the logging level
log_file = 'Saved_Models/training.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create a console handler for displaying logs in the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
            relation = [lst[0],lst[6],lst[7]]
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

def spans_from_comps(comps_list):
    comps_list_new = []
    for comps in comps_list:
        comps_new = []
        for comp in comps:
            comp = re.sub(',\w+$','',comp)
            comp_ = re.findall('\d+',comp)
            comps_new.append(comp_)
        comps_list_new.append(comps_new)

    return comps_list_new

def metric(true_lines, pred_lines,setting_name):
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
#         logger.info(true_relation_oneline)
        tr_copy = [','.join(lst) for lst in true_relation_oneline]
        pr_copy = [','.join(lst) for lst in pred_relation_oneline]

        tr_comps = comps_from_relations(tr_copy)
        pr_comps = comps_from_relations(pr_copy)
#         logger.info(tr_comps)
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
    metrics = [round(i,2) for i in metrics_list]
    logger.info(f'test[0] means test dataset and test[1] means outofdomain dataset\n')
    logger.info(f'Results for {setting_name} are:\n')
    logger.info(f'Precision: {metrics[0]}\nRecall: {metrics[1]}\nF1: {metrics[2]}\nExact match: {metrics[4]}\n\n')

    with open('results.txt','a') as f:
      f.write(f'Results for {setting_name} are:\n')
      f.write(f'Precision: {metrics[0]}\nRecall: {metrics[1]}\nF1: {metrics[2]}\nExact match: {metrics[4]}\n\n')
    
    return metrics

def train_and_test(setting_name):

  save_dir = './Saved_Models/'+setting_name
  train_file = './Trankit_Data/'+setting_name+'/train.conllu'
  dev_file = './Trankit_Data/'+setting_name+'/dev.conllu'
  test1 = './Trankit_Data/'+setting_name+'/test.conllu'
  test2 = './Trankit_Data/'+setting_name+'/outofDomain.conllu'
  if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

  test_files = [test1,test2]
  trainer = tpip(
      training_config={
      'category': 'customized-mwt-ner', # pipeline category
      'task': 'posdep', # task name
      'save_dir': save_dir, # directory for saving trained model
      'train_conllu_fpath': train_file, # annotations file in CONLLU format  for training
      'dev_conllu_fpath': dev_file, # annotations file in CONLLU format for development
      'max_epoch': 20
      }
  )

  # start training
  trainer.train()

  # start testing for test file as well as ood file
  for x in range(2):
    test_set = TaggerDataset(
        config=trainer._config,
        gold_conllu=test_files[x],
        input_conllu = test_files[x],
        evaluate=False
    )
    test_set.numberize()
    test_batch_num = len(test_set) // trainer._config.batch_size + (len(test_set) % trainer._config.batch_size != 0)
    result = trainer._eval_posdep(data_set=test_set, batch_num=test_batch_num,
                              name='test', epoch=-1)

    os.rename(os.path.join(save_dir,'xlm-roberta-base/customized-mwt-ner/preds/tagger.test.conllu.epoch--1'), os.path.join(save_dir,'xlm-roberta-base/customized-mwt-ner/preds/tagger.test'+str(x)+' '+setting_name+'.conllu.epoch--1'))
    pred_conllu = os.path.join(save_dir,'xlm-roberta-base/customized-mwt-ner/preds/tagger.test'+str(x)+' '+setting_name+'.conllu.epoch--1')
    gold_conllu = test_files[x]
    with open(gold_conllu) as t:
      with open(pred_conllu) as p:
          true_lines = t.readlines()
          pred_lines = p.readlines()
    metrics = metric(true_lines,pred_lines,setting_name+str(x))
    torch.cuda.empty_cache()
  return


# Main function

Data_folder = './Trankit_Data'
lst = []
with open('results.txt','w') as f:
    pass

for path,subdirs,files in os.walk(Data_folder):
  if 'Trankit' not in os.path.basename(path):
    setting_name = os.path.basename(path)
    logger.info(setting_name)
    with open('results.txt','a') as f:
        f.write(f'\n{setting_name}\n')
    train_and_test(setting_name)