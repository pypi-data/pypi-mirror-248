import os
from glob import glob
from time import time
from tqdm import tqdm
import torch

import frame2seq
from frame2seq.utils import residue_constants
from frame2seq.utils.util import get_neg_pll
from frame2seq.utils.pdb2input import get_inference_inputs
from frame2seq.model.Frame2seq import frame2seq 

import tarfile
# def extract_tar(tar_path, extract_path):
#     with tarfile.open(tar_path, 'r:gz') as tar:
#         tar.extractall(extract_path)


class Frame2seqRunner():
    """
    Wrapper for Frame2seq predictions.
    """
    def __init__(self):

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        module_path = os.path.abspath(__file__)
        globals()['__file__'] = module_path
        project_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Project path: {project_path}")
        trained_models_dir = os.path.join(project_path, 'trained_models')
        # model1_path = os.path.join(trained_models_dir, 'model1.ckpt')
        # if not os.path.exists(model1_path):
        #     extract_tar(os.path.join(trained_models_dir, 'trained_model1.tar.gz'), trained_models_dir)
        #     # extract_tar(os.path.join(trained_models_dir, 'trained_model2.tar.gz'), trained_models_dir)
        #     # extract_tar(os.path.join(trained_models_dir, 'trained_model3.tar.gz'), trained_models_dir)

        self.models = []
        model_ckpts = glob(os.path.join(trained_models_dir, '*.ckpt'))
        for ckpt_file in model_ckpts:
            print(f"Loading {ckpt_file}...")
            self.models.append(frame2seq.load_from_checkpoint(ckpt_file).eval().to(self.device))


    def design(self, pdb_file, chain_id, temperature, num_samples):
        start_time = time()
        seq_mask, aatype, X = get_inference_inputs(pdb_file, chain_id)
        seq_mask = seq_mask.to(self.device)
        aatype = aatype.to(self.device)
        X = X.to(self.device)
        str_form = [residue_constants.ID_TO_AA[int(i)] for i in aatype[0]]
        input_aatype_onehot = residue_constants.sequence_to_onehot(
                sequence=str_form,
                mapping=residue_constants.AA_TO_ID,)
        input_aatype_onehot = torch.from_numpy(input_aatype_onehot).float()
        input_aatype_onehot = input_aatype_onehot.unsqueeze(0)
        input_aatype_onehot = input_aatype_onehot.to(self.device)
        input_aatype_onehot = torch.zeros_like(input_aatype_onehot)
        input_aatype_onehot[:, :, 20] = 1 # all positions are masked (set to unknown)
        # forwards pass
        model_outs, scores = [], []
        with torch.no_grad():
            pred_seq1 = self.models[0].forward(X, seq_mask, input_aatype_onehot)
            pred_seq2 = self.models[1].forward(X, seq_mask, input_aatype_onehot)
            pred_seq3 = self.models[2].forward(X, seq_mask, input_aatype_onehot)
            # ensemble
            pred_seq = (pred_seq1 + pred_seq2 + pred_seq3) / 3
            pred_seq = pred_seq/temperature
            pred_seq = torch.nn.functional.softmax(pred_seq, dim=-1)
            pred_seq = pred_seq[seq_mask]
            sampled_seq = torch.multinomial(pred_seq, num_samples=num_samples, replacement=True)
            # write each sample to a file here:
            for sample in tqdm(range(num_samples)):
                sampled_seq_i = sampled_seq[:,sample]
                neg_pll, avg_neg_pll = get_neg_pll(pred_seq, sampled_seq_i)
                recovery = torch.sum(sampled_seq_i == aatype[seq_mask]) / torch.sum(seq_mask)
                sampled_seq_i = [residue_constants.ID_TO_AA[int(i)] for i in sampled_seq_i]
                sampled_seq_i = "".join(sampled_seq_i)
                print(f"Recovery : {recovery}")
                print(f"Average negative pseudo-log-likelihood : {avg_neg_pll}")
                print(f"Sequence: {sampled_seq_i}")
        print(f"Designed {num_samples} sequences in {time() - start_time:.2f} seconds.")


pdb_file = "/Users/denizakpinaroglu/Desktop/2fra.pdb"
chain_id = "A"


runner = Frame2seqRunner()
runner.design(pdb_file, chain_id, temperature=1.0, num_samples=10)

