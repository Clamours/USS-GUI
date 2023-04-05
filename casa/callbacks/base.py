import os
import lightning.pytorch as pl


class CheckpointEveryNSteps(pl.Callback):
    """
    Save a checkpoint every N steps, instead of Lightning's default that checkpoints
    based on validation loss.
    """

    def __init__(
        self,
        save_step_frequency,
    ):
        """
        Args:
            save_step_frequency: how often to save in steps
            prefix: add a prefix to the name, only used if
                use_modelcheckpoint_filename=False
            use_modelcheckpoint_filename: just use the ModelCheckpoint callback's
                default filename, don't use ours.
        """
        self.save_step_frequency = save_step_frequency

    def on_train_batch_end(self, *args, **kwargs):
        """ Check if we should save a checkpoint after every train batch """
        trainer = args[0]
        epoch = trainer.current_epoch
        global_step = trainer.global_step

        if global_step == 1 or global_step % self.save_step_frequency == 0:
            
            ckpt_path = os.path.join(
                trainer.checkpoint_callback.dirpath, 
                "step={}.ckpt".format(global_step)
            )
            trainer.save_checkpoint(ckpt_path)
            print("Save checkpoint to {}".format(ckpt_path))