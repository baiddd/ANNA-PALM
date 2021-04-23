import os, sys
import tensorflow as tf
from AnetLib.options.train_options import Options
from AnetLib.models.models import create_model
from smlm_datasets import create_data_sources

default_workdir = './output/' + os.path.basename(sys.argv[0])
opt = Options().parse()
opt.fineSize = 256
opt.batchSize = 1  # batchSize = 1
opt.model = 'a_net_tensorflow'
opt.dim_ordering = 'channels_last'
opt.display_freq = 500
opt.save_latest_freq = 1000
opt.use_resize_conv = True
opt.norm_A = 'mean_std'
opt.norm_B = 'min_max[0,1]'
opt.lambda_A = 50
# opt.input_nc = 2
opt.lr_nc = 0
opt.lr_scale = 1.0/4.0
opt.lambda_LR = 25
opt.control_nc = 1
opt.add_data_type_control = True
opt.add_lr_channel = False
opt.use_random_channel_mask = False
opt.lr_loss_mode = 'lr_predict'

# assuming we have the following data with 2ch as input and 1 channel as output
# ├─ data_for_training/
# │  ├─ train/
# │  │  ├─ img1
# │  │  │  ├─ input_channel1.png
# │  │  │  ├─ input_channel2.png
# │  │  │  ├─ target_channel1.png
# │  │  ├─ img2
# │  │  │  ├─ input_channel1.png
# │  │  │  ├─ input_channel2.png
# │  │  │  ├─ target_channel1.png
# │  │  ...
# │  ├─ test/
# │  │  ├─ img57
# │  │  │  ├─ input_channel1.png
# │  │  │  ├─ input_channel2.png
# │  │  │  ├─ target_channel1.png
# │  │  ├─ img58
# │  │  │  ├─ input_channel1.png
# │  │  │  ├─ input_channel2.png
# │  │  │  ├─ target_channel1.png

opt.input_channels = 'input_channel1=input_channel1.png,input_channel1=input_channel1.png'
opt.output_channels = 'target_channel1=target_channel1.png'
opt.input_nc = len(opt.input_channels.split(','))
opt.output_nc = len(opt.output_channels.split(','))


if opt.phase == 'train':
    sources = create_data_sources('GenericTransformedImages', opt)
    d = sources['train']
    # noise_source = create_data_sources('NoiseCollection001', opt)['train']
    # d.set_addtional_source(noise_source)
    model = create_model(opt)
    model.train(d, verbose=1, max_steps=200000)

if opt.phase == 'test':
    model = create_model(opt)
    sources = create_data_sources('GenericTransformedImages', opt)
    d = sources['test']
    model.predict(d, verbose=1)
