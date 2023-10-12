# Check if the saved_models folder doesn't exist
if [ ! -d "saved_models" ]; then
    # Create the saved_models folder
    mkdir saved_models
fi

domain="san"
# Path of pretrained embedding file
word_path=data/cc.NeCTIS.300.txt
# Path to store model and predictions  
saved_models=saved_models
declare -i num_epochs=100
declare -i word_dim=300
start_time=`date +%s`
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
model_path="Coarse_NeCTIS"
touch $saved_models/base_log.txt

###############################################################
# Running the base Biaffine Parser
echo "#################################################################"
echo "Currently base model in progress..."
echo "#################################################################"
python examples/GraphParser_MTL_POS.py --dataset ud --domain $domain --rnn_mode LSTM \
--num_epochs $num_epochs  --batch_size 128 --hidden_size 512 --arc_space 512 \
--arc_tag_space 128 --num_layers 2 --num_filters 100 --use_char --use_pos \
--word_dim $word_dim --char_dim 100 --pos_dim 100 --initializer xavier --opt adam \
--learning_rate 0.002 --decay_rate 0.5 --schedule 6 --clip 5.0 --gamma 0.0 \
--epsilon 1e-6 --p_rnn 0.1 0.1 --p_in 0.1 --p_out 0.1 --arc_decode mst \
--punct_set '.' '``'  ':' ','  --word_embedding fasttext --char_embedding random  --pos_embedding random --word_path $word_path \
--model_path $saved_models/$model_path 2>&1 | tee $saved_models/base_log.txt


mv $saved_models/base_log.txt $saved_models/$model_path/base_log.txt
