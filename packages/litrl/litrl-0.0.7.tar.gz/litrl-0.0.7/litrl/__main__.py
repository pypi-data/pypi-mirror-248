import hydra
from omegaconf import DictConfig

from litrl.common.hydra import omegaconf_to_schema
from litrl.common.mlflow import get_load_path


@hydra.main(config_path="../config", config_name="default", version_base="1.3.2")
def main(omegaconf_cfg: DictConfig):
    """Main entrypoint of the project"""
    cfg = omegaconf_to_schema(omegaconf_cfg)
    load_path = get_load_path(cfg.tags, cfg.load)
    model = cfg.model.instantiate()
    trainer = cfg.trainer.instantiate()
    trainer.fit(model, ckpt_path=load_path)


if __name__ == "__main__":
    main()
