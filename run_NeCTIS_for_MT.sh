domain="san"
# Path of pretrained embedding file
word_path=data/cc.NeCTIS.300.txt
# Path to store model and predictions  
saved_models=saved_models
declare -i num_epochs=100
declare -i word_dim=300
start_time=`date +%s`
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
touch $saved_models/base_log.txt
#model_path=Coarse_NeCTIS

label_type=Finegrain #Finegrain/Coarse

if [ "$label_type" == "Finegrain" ]; then
    model_path="Finegrain_NeCTIS"
else
    model_path="Coarse_NeCTIS"
fi


###############################################################
# DataConversion
echo "#################################################################"
echo "Converting the given data into NeCTIS data format for MT ..."
echo "#################################################################"
python examples/DataConversionForMT.py --input_format IAST --label_type Finegrain



###############################################################
# Inference
echo "#################################################################"
echo "Inference of converted data for MT ..."
echo "#################################################################"
python examples/GraphParser_MTL_POS.py --dataset ud --domain $domain --rnn_mode LSTM \
--num_epochs $num_epochs  --batch_size 128 --hidden_size 512 --arc_space 512 \
--arc_tag_space 128 --num_layers 2 --num_filters 100 --use_char --use_pos \
--word_dim $word_dim --char_dim 100 --pos_dim 100 --initializer xavier --opt adam \
--learning_rate 0.002 --decay_rate 0.5 --schedule 6 --clip 5.0 --gamma 0.0 \
--epsilon 1e-6 --p_rnn 0.1 0.1 --p_in 0.1 --p_out 0.1 --arc_decode mst \
--punct_set '.' '``'  ':' ','  --word_embedding fasttext --char_embedding random  --pos_embedding random --word_path $word_path \
--model_path $saved_models/$model_path 2>&1 \
--load_path $saved_models/$model_path/domain_san.pt 2>&1 --eval_mode \

mv $saved_models/base_log.txt $saved_models/$model_path/base_log.txt



echo "#################################################################"
echo "Ignore the UAS, LAS scores mentioned here, Check your prediction file in saved_models/$label_type/domain_san_test_model_domain_san_data_domain_san_pred.txt"
echo "#################################################################"

