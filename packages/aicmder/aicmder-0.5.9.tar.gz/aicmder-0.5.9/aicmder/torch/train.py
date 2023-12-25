from aicmder.torch import HyperParameters, DataModule, select_device
from aicmder.torch.dist_model import *
from torch.optim import lr_scheduler
from pathlib import Path
import torch.nn as nn
import torch
from copy import deepcopy
import pandas as pd
import matplotlib.pyplot as plt
from aicmder.utils.general import multiple_threaded
from matplotlib.ticker import MaxNLocator
try:

    import seaborn as sns
    sns.set_context("paper")

    bg_color = "#f1f1f2"
    grid_color = "#bcbabe"
    text_color = "#338494"
    tick_color = "#1995ad"

    sns.set(rc={
        #  'axes.axisbelow': False,
        'axes.edgecolor': 'lightgrey',
        'axes.facecolor': 'None',  # remove bg
        #  'axes.grid': False,
        'axes.labelcolor': 'dimgrey',
        #  'axes.spines.right': False,
        #  'axes.spines.top': False,
        'figure.facecolor': 'white',
        'lines.solid_capstyle': 'round',
        'patch.edgecolor': 'w',
        'patch.force_edgecolor': True,
        'text.color': 'dimgrey',
        #  'xtick.bottom': False,
        'xtick.color': 'dimgrey',
        'xtick.direction': 'out',
        #  'xtick.top': False,
        'ytick.color': 'dimgrey',
        'ytick.direction': 'out',
        #  'ytick.left': False,
        #  'ytick.right': False


        # add background
        'axes.facecolor': bg_color,
        'figure.facecolor': bg_color,
        "text.color": text_color,
        "xtick.color": tick_color,
        "ytick.color": tick_color,
        "axes.edgecolor": grid_color,

        "axes.labelcolor": text_color,
        "grid.color": grid_color,
    })
except:
    pass
from matplotlib import rcParams
rcParams['figure.figsize'] = 13, 8.27

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'
color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]


def write_frame(*p):
    d = p[0]
    temp_df = pd.read_csv(d['filename'])

    col_len = temp_df.columns.size
    columns = temp_df.columns
    # exclude epoch
    sub_size = math.ceil(math.sqrt(col_len - 1))
    
    df_idx = p[1]
    fig, axs = plt.subplots(nrows=sub_size, ncols=sub_size)
    idx, need_stop = 1, False
    for i in range(sub_size):
        for j in range(sub_size):
            dfm = temp_df[:df_idx].iloc[:, [0, idx]]
            metric = columns[idx]
            dfm.columns = ["epoch", metric]
            ax = axs[i][j]
            ax.title.set_text(metric)
            color_idx = idx % len(color_list)

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()
            sns.lineplot(x="epoch", y=metric, data=dfm, ax=ax, color=color_list[color_idx])

            idx += 1
            if idx >= col_len:
                need_stop = True
                break
        if need_stop:
            break
    plt.tight_layout()
    df_filename = f"/tmp/{df_idx}.png"
    plt.savefig(df_filename)
    # files.append(df_filename)
    return df_filename


_STA_CSV = 'statis.csv'

_STA_VALIDATING = 0
_STA_TRAINING = 1


class Trainer(HyperParameters):

    def __init__(self, model, device='', max_epochs=100, batch_size=32, gradient_clip_val=10.0, verbose=True,
                 evaluate_func=evaluate_func, patience=5, optim=None, save_dir="./", save_state_dict_only=True,
                 lrf=0.01, use_lr_scheduler=True, save_statistic=False,
                 criterion=nn.CrossEntropyLoss()):
        self.save_hyperparameters()
        self.trainable = Trainable(batch_size, gradient_clip_val=self.gradient_clip_val)
        self.trainable.on_pretrain_routine_start(self.model, verbose=verbose)
        self.device = select_device(device=device, batch_size=batch_size)
        if hasattr(model, "_get_name"):
            self.model_name = model._get_name()
        else:
            self.model_name = ''

        self.best_pt_name = self.model_name + 'best.pt'
        self.last_pt_name = self.model_name + 'last.pt' 

        self.model, self.device, self.amp, self.scaler, self.ema = self.trainable.on_train_start(
            model=self.model, device=self.device, evaluate_func=evaluate_func, patience=patience)
        save_dir = Path(save_dir)
        print("--------------------------------------------------------------------------------------")
        print("warning:", "AMP [{}]".format(self.amp))
        print("--------------------------------------------------------------------------------------")
        self.weight_dir = save_dir / 'train'  # weights dir
        self.weight_dir.mkdir(parents=True, exist_ok=True)  # make dir
        self.last, self.best = self.weight_dir / self.last_pt_name, self.weight_dir / self.best_pt_name
        self.val_save = False
        if self.optim is not None:
            if use_lr_scheduler:
                def lr_lambda(x): return (1 - x / self.max_epochs) * (1.0 - lrf) + lrf  # linear
                self.scheduler = lr_scheduler.LambdaLR(self.optim, lr_lambda=lr_lambda)
            else:
                self.scheduler = self.optim

    def to_csv(self):
        if self.save_statistic:
            self.df.to_csv(self.weight_dir / self.statis_csv, index=False)

    def save_statistic_epoch(self):
        if self.save_statistic:
            self.setValueByRowIdx(self.epoch, self.df_epoch, self.epoch)
            self.setValueByRowIdx(self.epoch, self.df_acc, self.epoch_acc)
            self.setValueByRowIdx(self.epoch, self.df_loss, self.epoch_loss)

            if hasattr(self, "need_val") and self.need_val:
                self.setValueByRowIdx(self.epoch, self.df_val_acc, self.val_acc)
                self.setValueByRowIdx(self.epoch, self.df_val_loss, self.val_loss)

    def setValueByRowIdx(self, row_idx, key, val):
        if self.save_statistic:
            if isinstance(val, torch.Tensor):
                val = '%.3g' % val.item()
            self.df.at[row_idx, key] = val

    def create_dataframe(self):
        self.df_epoch = 'epoch'
        self.df_acc = 'acc'
        self.df_loss = 'loss'

        self.df_val_acc = 'val_acc'
        self.df_val_loss = 'val_loss'

        self.df[self.df_epoch] = ''
        self.df[self.df_acc] = ''
        self.df[self.df_loss] = ''

        self.df[self.df_val_acc] = ''
        self.df[self.df_val_loss] = ''

    def configure_statistic(self):
        if self.save_statistic:
            import pandas as pd
            self.df = pd.DataFrame()
            self.create_dataframe()

    def configure_criterion(self):
        pass

    def configure_optimizers(self, opt='SGD',
                             #  opt='Adam',
                             lr=0.01,
                             lrf=0.01,
                             momentum=0.937,
                             weight_decay=0.0005):
        self.optim = smart_optimizer(self.model, opt, lr, momentum, weight_decay)
        if self.use_lr_scheduler:
            def lr_lambda(x): return (1 - x / self.max_epochs) * (1.0 - lrf) + lrf  # linear
            self.scheduler = lr_scheduler.LambdaLR(self.optim, lr_lambda=lr_lambda)
        else:
            self.scheduler = self.optim

    def prepare_data(self, data):
        assert isinstance(data, DataModule)
        self.train_dataloader = data.train_dataloader()
        self.val_dataloader = data.val_dataloader()
        self.num_train_batches = len(self.train_dataloader)
        self.num_val_batches = (len(self.val_dataloader)
                                if self.val_dataloader is not None else 0)

    def clip_gradients(self, grad_clip_val, model):
        """Defined in :numref:`sec_rnn-scratch`"""
        params = [p for p in model.parameters() if p.requires_grad]
        norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params))
        if norm > grad_clip_val:
            for param in params:
                param.grad[:] *= grad_clip_val / norm

    def get_current_metrics(self):
        if not hasattr(self, 'best_train_acc'):
            self.best_train_acc = self.epoch_acc

        if not hasattr(self, 'best_train_loss'):
            self.best_train_loss = self.epoch_loss

        if self.epoch_acc > self.best_train_acc or (
                self.epoch_acc == self.best_train_acc and self.best_train_loss is not None and self.epoch_loss < self.best_train_loss):
            self.best_train_acc = self.epoch_acc
            self.best_train_loss = self.epoch_loss
            self.trainable.on_model_save(self.model, self.epoch, self.optim, (self.best_train_acc,
                                        self.best_train_loss), self.best, save_state_dict_only=True)

        return self.best_train_acc, self.best_train_loss
        # raise NotImplementedError("please rewrite this method!")
    #    return (best_train_acc, best_train_loss)

    def run_model(self, batch, is_train=True):
        raise NotImplementedError("please rewrite [run_model] method!")

    def eval_model(self, batch):
        raise NotImplementedError("please rewrite [eval_model] method!")

    def to_device(self, batch):
        if isinstance(batch, torch.Tensor):
            batch = batch.to(self.device)
        if isinstance(batch, list) or isinstance(batch, tuple):
            device_batch = []
            for b in batch:
                if isinstance(b, torch.Tensor):
                    b = b.to(self.device)
                    device_batch.append(b)
            batch = device_batch
        return batch

    def print_val_metrics(self):
        pass

    def is_training(self):
        return self.status == _STA_TRAINING

    def eval(self, data):
        self.prepare_data(data)
        self.model.eval()
        self.epoch = 0
        self.max_epochs = 0
        self.status = _STA_VALIDATING
        if RANK in {-1, 0}:
            self.val_count_in_epoch = len(self.val_dataloader.dataset)
            self.val_corrects_in_epoch = 0

            val_pbar = enumerate(self.val_dataloader)
            nb = len(self.val_dataloader)  # number of batches
            val_pbar = tqdm(val_pbar, total=nb, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')
            for idx, batch in val_pbar:
                with torch.no_grad():
                    batch = self.to_device(batch)
                    self.eval_model(batch)

                    self.val_acc = self.val_corrects_in_epoch / self.val_count_in_epoch if self.val_count_in_epoch != 0 else 0
                    try:
                        mem = f'{torch.cuda.memory_reserved() / 1E9 if torch.cuda.is_available() else 0:.3g}G'  # (GB)
                        val_desc = (
                            '%15s' * 1 + '%15s' * 3) % (f'Mem:{mem}',
                                                        "Correct: {}".format(self.val_corrects_in_epoch),
                                                        "Cnt: {}".format(self.val_count_in_epoch),
                                                        "Acc: {:2f}".format(self.val_acc))
                    except Exception as e:
                        val_desc = ''
                    val_desc = 'Validate:' + val_desc
                    val_pbar.set_description(val_desc)

            # for
            self.print_val_metrics()


    def train(self, data, need_val=True, filename=_STA_CSV, save_png_epoch_interval=0):
        if self.optim is None:
            self.configure_optimizers()

        if data is not None and type(data).__name__ != '':
            self.dataset_name = type(data).__name__


        self.status = _STA_TRAINING
        self.need_val = need_val

        if filename == _STA_CSV: 
            pass
        else:
            filename, _ = os.path.splitext(filename)

        self.prefix = filename
        self.statis_csv = f"{filename}{self.dataset_name}_{self.model_name}.csv"
        self.statis_fig = f"{filename}{self.dataset_name}_{self.model_name}.png"
        self.statis_gif = f"{filename}{self.dataset_name}_{self.model_name}.gif"

        if self.statis_csv != _STA_CSV:
            self.last, self.best = self.weight_dir / (filename + f"{self.dataset_name}_" + self.last_pt_name), self.weight_dir / (filename +  f"{self.dataset_name}_" + self.best_pt_name)

        self.configure_statistic()
        self.configure_criterion()
        self.prepare_data(data)

        # self.optim = model.configure_optimizers()
        self.epoch = 0
        self.train_batch_idx = 0
        self.val_batch_idx = 0
        for self.epoch in range(self.max_epochs):

            if RANK in {-1, 0}:
                self.train_loss_in_epoch = 0.0
                self.train_corrects_in_epoch = 0
                self.train_count_in_epoch = len(self.train_dataloader.dataset)

            self.train_epoch()
            # epoch end

            if RANK in {-1, 0}:
                self.epoch_loss = self.train_loss_in_epoch / self.train_count_in_epoch
                self.epoch_acc = self.train_corrects_in_epoch.double() / self.train_count_in_epoch

                print('training {} Loss: {:.4f} Acc: {:.4f} Count: {} Train_size: {}'.format(
                    self.epoch, self.epoch_loss, self.epoch_acc, self.train_count_in_epoch, self.train_size))

                self.save_statistic_epoch()

            stop = self.trainable.on_train_epoch_end(self.epoch, self.get_current_metrics(), scheduler=self.scheduler)
            if stop:
                break
            if self.save_statistic and save_png_epoch_interval > 0:
                if self.epoch % save_png_epoch_interval == 0:
                    self.save_fig()

        self.trainable.on_model_save(self.model, self.epoch, self.optim, self.get_current_metrics(),
                                     self.last, save_state_dict_only=self.save_state_dict_only)
        self.trainable.on_train_end()
        self.to_csv()

    def train_epoch(self):
        """Defined in :numref:`sec_linear_scratch`"""
        # self.model.train()
        pbar, self.train_size = self.trainable.on_train_epoch_start(self.model, self.epoch, self.train_dataloader)
        for batch_idx, batch in pbar:
            ni = batch_idx + self.epoch * self.train_size

            batch = self.to_device(batch)
            # loss = self.model.training_step(self.prepare_batch(batch))
            with torch.cuda.amp.autocast(self.amp):
                loss, desc = self.run_model(batch)

            try:
                mem = f'{torch.cuda.memory_reserved() / 1E9 if torch.cuda.is_available() else 0:.3g}G'  # (GB)
                desc = desc + (
                    '%15s' * 2 + '%15s' * 4) % (
                    f'{self.epoch}/{self.max_epochs - 1}', f'Mem:{mem}', "Loss: {:.2f}".format(self.train_loss_in_epoch),
                    "Correct: {}".format(self.train_corrects_in_epoch),
                    "Cnt: {}".format(self.train_count_in_epoch),
                    "Acc: {:2f}".format(
                        self.train_corrects_in_epoch / self.train_count_in_epoch if self.train_count_in_epoch != 0 else 0))
            except Exception as e:
                desc = ''

            if RANK != -1:
                loss *= WORLD_SIZE  # gradient averaged between devices in DDP mode
            self.trainable.on_train_batch_end(self.model, self.scaler, self.optim, loss, desc=desc, ni=ni)

            # self.optim.zero_grad()
            # with torch.no_grad():
            #     loss.backward()
            #     if self.gradient_clip_val > 0:  # To be discussed later
            #         self.clip_gradients(self.gradient_clip_val, self.model)
            #     self.optim.step()

            self.train_batch_idx += 1
        # eval
        if self.need_val:
            if self.val_dataloader is None:
                return
            self.model.eval()
            if RANK in {-1, 0}:
                self.val_count_in_epoch = len(self.val_dataloader.dataset)
                self.val_loss_in_epoch = 0.0
                self.val_corrects_in_epoch = 0

                val_pbar = enumerate(self.val_dataloader)
                nb = len(self.val_dataloader)  # number of batches
                val_pbar = tqdm(val_pbar, total=nb, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')
                for idx, batch in val_pbar:
                    with torch.no_grad():
                        # self.model.validation_step(self.prepare_batch(batch))
                        batch = self.to_device(batch)
                        self.run_model(batch, is_train=False)
                        if self.val_save:
                            self.trainable.on_model_save(
                                self.model, self.epoch, self.optim, self.get_current_metrics(),
                                self.best, save_state_dict_only=self.save_state_dict_only)

                        self.val_acc = self.val_corrects_in_epoch / self.val_count_in_epoch if self.val_count_in_epoch != 0 else 0
                        try:
                            mem = f'{torch.cuda.memory_reserved() / 1E9 if torch.cuda.is_available() else 0:.3g}G'  # (GB)
                            val_desc = (
                                '%15s' * 1 + '%15s' * 4) % (f'Mem:{mem}',
                                                            "Loss: {:.2f}".format(self.val_loss_in_epoch),
                                                            "Correct: {}".format(self.val_corrects_in_epoch),
                                                            "Cnt: {}".format(self.val_count_in_epoch),
                                                            "Acc: {:2f}".format(self.val_acc))
                        except Exception as e:
                            val_desc = ''
                        val_desc = 'Validate:' + val_desc
                        val_pbar.set_description(val_desc)
                    self.val_batch_idx += 1
                
                # for
                self.print_val_metrics()

                self.val_loss = self.val_loss_in_epoch

    def save_fig(self, debug=False, csv_file=_STA_CSV):
        if debug:
            self.save_statistic = True
            self.df = pd.read_csv(self.weight_dir / csv_file)

        if self.save_statistic:

            import importlib
            _loader = importlib.find_loader('seaborn')
            found = _loader is not None
            if found:
                self.to_csv()

                temp_df = pd.read_csv(self.weight_dir / self.statis_csv)

                col_len = temp_df.columns.size
                columns = temp_df.columns
                # exclude epoch
                sub_size = math.ceil(math.sqrt(col_len - 1))

                fig, axs = plt.subplots(nrows=sub_size, ncols=sub_size)
                idx, need_stop = 1, False
                for i in range(sub_size):
                    for j in range(sub_size):
                        # dfm = deepcopy(self.df.iloc[:, [0, idx]])
                        dfm = temp_df.iloc[:, [0, idx]]
                        metric = columns[idx]
                        dfm.columns = ["epoch", metric]
                        ax = axs[i][j]
                        ax.title.set_text(metric)
                        color_idx = idx % len(color_list)
                        # axs[i][j].plot(dfm["epoch"], dfm[metric], color=color_list[color_idx])
                        # sns.pointplot(x="epoch", y=metric, data=dfm, ax=ax, color=color_list[color_idx])

                        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                        plt.tight_layout()
                        sns.lineplot(x="epoch", y=metric, data=dfm, ax=ax, color=color_list[color_idx])

                        idx += 1
                        if idx >= col_len:
                            need_stop = True
                            break
                    if need_stop:
                        break
                plt.tight_layout()
                plt.savefig(self.weight_dir / self.statis_fig)
            else:
                print("[Warning]: seaborn not found! Can not save plot!")

    def save_gif(self, debug=False, csv_file=_STA_CSV, last_frame_repeat=40):
        if debug:
            self.save_statistic = True
            self.df = pd.read_csv(self.weight_dir / csv_file)

        self.to_csv()
        temp_df = pd.read_csv(self.statis_csv)

        col_len = temp_df.columns.size
        columns = temp_df.columns
        # exclude epoch
        sub_size = math.ceil(math.sqrt(col_len - 1))

        # files = []
        length = len(temp_df)

        param = {'filename': self.statis_csv}
        files = multiple_threaded(write_frame, param, range(1, length + 1))
        # from tqdm import tqdm
        # for df_idx in tqdm(range(1, length + 1), total=length):

        #     fig, axs = plt.subplots(nrows=sub_size, ncols=sub_size)
        #     idx = 1
        #     for i in range(sub_size):
        #         for j in range(sub_size):
        #             dfm = temp_df[:df_idx].iloc[:, [0, idx]]
        #             metric = columns[idx]
        #             dfm.columns = ["epoch", metric]
        #             ax = axs[i][j]
        #             ax.title.set_text(metric)
        #             color_idx = idx % len(color_list)
        #             plt.tight_layout()
        #             sns.lineplot(x="epoch", y=metric, data=dfm, ax=ax, color=color_list[color_idx])

        #             idx += 1
        #             if idx > col_len:
        #                 break
        #     plt.tight_layout()
        #     df_filename = f"/tmp/{df_idx}.png"
        #     plt.savefig(df_filename)
        #     files.append(df_filename)

        import imageio

        for _ in range(last_frame_repeat):
            files.append(files[-1])
        with imageio.get_writer(self.weight_dir / self.statis_gif, mode='I') as writer:
            for f in files:
                image = imageio.imread(f)
                writer.append_data(image)
