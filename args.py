import argparse
import torch
from chemprop.features import get_available_features_generators

def add_args():
    """
    Adds predict arguments to an ArgumentParser.

    :param parser: An ArgumentParser.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # general arguments
    parser.add_argument('--gpu', type=int,
                        choices=list(range(torch.cuda.device_count())),
                        help='Which GPU to use')
    parser.add_argument('--no_cuda', action='store_true', default=False,
                        help='Turn off cuda')
    parser.add_argument('--mode', type=str, default='train',
                        choices=['train', 'inference'],
                        help='Mode to run script in')
    parser.add_argument('--data_path', type=str,
                        help='Path to CSV file containing training data',
                        default=None)
    parser.add_argument('--test_path', type=str,
                        help='Path to CSV file containing testing data for which predictions will be made',
                        default=None)
    parser.add_argument('--dataset_type', type=str, choices=['classification', 'regression', 'multiclass'],
                        help='Type of dataset')
    # parser.add_argument('--save_dir', type=str, default=None,
    #                     help='dir name in exp_results folder where predictions will be saved',
    #                     default='test')
    parser.add_argument('--seed', type=int, default=0,
                        help='Random seed')
    parser.add_argument('--split_type', type=str, default='moleculeACE',
                        choices=['random', 'scaffold_balanced', 'moleculeACE', 'predetermined'],
                        help='Method of splitting the data into training, validation, and test')
    parser.add_argument('--split_sizes', type=float, nargs='+',
                        default=[0.8, 0.1, 0.1],
                        help='Proportions of data to use for training, validation, and test')
    parser.add_argument('--features_scaling', action='store_true', default=False,
                        help='Turn on scaling of features')                  

    parser.add_argument('--features_generator', type=str, nargs='*',
                        choices=get_available_features_generators(),
                        help='Method of generating additional features')
    parser.add_argument('--features_path', type=str, nargs='*', default=None,
                        help='Path to features to use in FNN (instead of features_generator)')
    parser.add_argument('--no_features_scaling', action='store_true', default=False,
                        help='Turn off scaling of features')
    parser.add_argument('--max_data_size', type=int, default=None,
                        help='Maximum number of data points to load')
    
    # training arguments
    parser.add_argument('--checkpoint_path', type=str,
                        default='KANO_model/dumped/pretrained_graph_encoder/original_CMPN_0623_1350_14000th_epoch.pkl',
                        help='Path to model checkpoint (.pt file)')
    parser.add_argument('--batch_size', type=int, default=256,
                        help='Batch size')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of epochs')
    parser.add_argument('--lr', type=float, default=1e-4,
                        help='Learning rate')
    parser.add_argument('--encoder_name', type=str, default='CMPNN',
                        help='selected molecule encoder')
    parser.add_argument('--metric', type=str, default='auc',
                        choices=['auc', 'prc-auc', 'rmse', 'mae', 'r2', 'accuracy', 'cross_entropy'],
                        help='Metric to optimize during training')
    
    # model arguments
    # you may not able to change most of these arguments if you use a pretrained model
    parser.add_argument('--hidden_size', type=int, default=300)
    parser.add_argument('--ffn_hidden_size', type=int, default=300)
    parser.add_argument('--ffn_num_layers', type=int, default=2)
    parser.add_argument('--dropout', type=float, default=0.0)
    parser.add_argument('--activation', type=str, default='ReLU')
    parser.add_argument('--depth', type=int, default=3)
    parser.add_argument('--step', type=str, default='functional_prompt')
    parser.add_argument('--temperature', type=float, default=0.1)
    parser.add_argument('--warmup_epochs', type=int, default=2)
    
    args = parser.parse_args()
    # add and modify some args
    args.data_name = args.data_path.split('/')[-1].split('.')[0]
    if not args.no_cuda and torch.cuda.is_available():
        args.cuda = True
    args.atom_messages = False
    args.use_input_features = None
    args.bias = False
    args.undirected = False
    args.features_only = False
    args.max_lr = args.lr * 10
    args.init_lr = args.lr
    args.final_lr = args.lr
    args.num_lrs = 1
    args.num_runs = 1
    if args.metric in ['auc', 'prc-auc', 'accuracy', 'r2']:
        args.minimize_score = False
    elif args.metric in ['rmse', 'mae', 'cross_entropy']:
        args.minimize_score = True
    args.smiles_columns = ['smiles']
    args.target_columns = ['y']
    return args