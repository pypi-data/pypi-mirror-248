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

def exists(x):
    return x is not None

class Frame2seqRunner():
    """
    Wrapper for Frame2seq predictions.
    """
    def __init__(self):
        # if exists(model_ckpts):
        #     num_models = len(model_ckpts)
        # else:
        #     project_path = os.path.dirname(
        #         os.path.realpath(frame2seq.__file__))
        #     ckpt_path = os.path.join(
        #         project_path,
        #         "trained_models/*.ckpt",
        #     )
        #     model_ckpts = list(glob(ckpt_path))
        #     model_ckpts = list(sorted(model_ckpts))[:num_models]

        module_path = os.path.abspath(__file__)
        print(module_path)

        # Set __file__ explicitly
        globals()['__file__'] = module_path

        project_path = os.path.dirname(os.path.abspath(__file__))
        # project_path = os.path.dirname(os.path.realpath(frame2seq.__file__))
        trained_models_dir = os.path.join(project_path, 'trained_models')

        CHECKPOINT_PATH = os.path.join(trained_models_dir, 'model1.ckpt')   

        # self.model = AntiBERTy.from_pretrained(CHECKPOINT_PATH).to(self.device)
        

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # self.models = []
        # for ckpt_file in model_ckpts:
        #     print(f"Loading {ckpt_file}...")
            # self.models.append(
        self.model = frame2seq.load_from_checkpoint(CHECKPOINT_PATH).eval().to(self.device)


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
            pred_seq = self.model.forward(X, seq_mask, input_aatype_onehot)
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
                sampled_seq_i = [residue_constants.ID_TO_AA[int(i)] for i in sampled_seq_i]
                sampled_seq_i = "".join(sampled_seq_i)
                print(sampled_seq_i)
        print(f"Designed {num_samples} sequences in {time() - start_time:.2f} seconds.")


pdb_file = "/Users/denizakpinaroglu/Desktop/2fra.pdb"
chain_id = "A"


runner = Frame2seqRunner()
runner.design(pdb_file, chain_id, temperature=1.0, num_samples=10)

