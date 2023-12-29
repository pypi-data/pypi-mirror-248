import inspect
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar

import hydra
from gymnasium import Env
from lightning import LightningModule, Trainer
from lightning.pytorch.callbacks import Callback as LightningCallback
from lightning.pytorch.loggers import Logger as LightningLogger
from loguru import logger
from pydantic import RootModel, field_validator
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic.dataclasses import is_pydantic_dataclass

InstanceClass = TypeVar("InstanceClass")


@pydantic_dataclass(frozen=True)
class InstantiatorClass(Generic[InstanceClass]):
    _target_: str

    @classmethod
    def is_instantiable(cls, obj: type) -> bool:
        if obj == InstantiatorClass or (
            inspect.isclass(obj) and issubclass(obj, InstantiatorClass)
        ):
            return True

    @classmethod
    def process_dict(
        cls,
        key_type: type,
        key: str,
        val: Any,
        info_dict: dict[str, Any],
        *,
        instantiate_children: bool,
    ) -> None:
        if key_type == list and instantiate_children:
            for list_item in val:
                logger.info(f"instantiating list item {list_item}")
        if cls.is_instantiable(key_type):
            schema: InstantiatorClass = key_type(**info_dict[key])
            if instantiate_children:
                schema = schema.instantiate()
            info_dict[key] = schema
        elif is_pydantic_dataclass(key_type):
            sub_info_dict = info_dict[key]
            cls.cast_type(
                RootModel(val), sub_info_dict, instantiate_children=instantiate_children,
            )
            info_dict[key] = key_type(**sub_info_dict)

    @classmethod
    def cast_type(
        cls,
        pydantic: RootModel,
        info_dict: dict[str, Any],
        *,
        instantiate_children: bool,
    ):
        for key in info_dict:
            val = pydantic.root.__getattribute__(key)
            key_type = type(val)
            if key_type == list:
                objs = []
                for list_item in val:
                    if cls.is_instantiable(type(list_item)):
                        objs.append(list_item.instantiate())
                    else:
                        objs.append(list_item)
                info_dict[key] = objs
            else:
                cls.process_dict(
                    key_type,
                    key,
                    val,
                    info_dict,
                    instantiate_children=instantiate_children,
                )

    def instantiate(self, *, _recursive_: bool | None = None) -> InstanceClass:
        pydantic_model = RootModel(self)
        info_dict = pydantic_model.model_dump(exclude="_target_")
        if _recursive_ is None:
            _recursive_ = info_dict.pop("_recursive_", True)
        self.cast_type(pydantic_model, info_dict, instantiate_children=_recursive_)
        fabric = hydra.utils.instantiate({"_target_": self._target_}, _partial_=True)
        return fabric(**info_dict)


@pydantic_dataclass(frozen=True)
class MCTSConfigSchema:
    simulations: int


@pydantic_dataclass(frozen=True)
class AgentSchema(InstantiatorClass[Env]):
    pass


@pydantic_dataclass(frozen=True)
class MCTSAgentSchema(InstantiatorClass[Env]):
    cfg: MCTSConfigSchema | None


@pydantic_dataclass(frozen=True)
class EnvSchema(InstantiatorClass[Env]):
    id: str
    opponent: None | AgentSchema | MCTSAgentSchema = None
    val: bool | None = None


@pydantic_dataclass
class BufferSchema:
    batch_size: int
    max_size: int


@pydantic_dataclass(frozen=True)
class ModelConfigSchema:
    seed: int
    lr: float
    gamma: float
    warm_start_steps: int
    hidden_size: int
    n_hidden_layers: int
    buffer: BufferSchema
    epsilon: float
    target_entropy: float
    tau: float
    env_fabric: EnvSchema
    val_env_fabric: EnvSchema

    @field_validator("lr")
    def validate_lr(cls, lr: float) -> float:
        if lr < 0:
            raise ValueError(f"'lr' can't be less than 0, got: {lr}")
        return lr


@pydantic_dataclass(frozen=True)
class ModelSchema(InstantiatorClass[LightningModule]):
    _target_: str
    cfg: ModelConfigSchema
    _recursive_: Literal[False] = False


@pydantic_dataclass(frozen=True)
class LoggerSchema(InstantiatorClass[LightningLogger]):
    _target_: str
    log_model: bool
    tags: dict[str, str]


@pydantic_dataclass(frozen=True)
class CallbackSchema(InstantiatorClass[LightningCallback]):
    _target_: str


@pydantic_dataclass(frozen=True)
class TrainerSchema(InstantiatorClass[Trainer]):
    _target_: str
    log_every_n_steps: int
    limit_train_batches: int
    max_epochs: int
    logger: LoggerSchema
    callbacks: list[CallbackSchema]


@pydantic_dataclass
class ConfigSchema:
    model: ModelSchema
    trainer: TrainerSchema
    tags: dict[str, str]
    load: None | str
    _recursive_: Literal[False] = False

    @field_validator("load")
    def load(cls, load: str) -> str | None:
        if load is None or load == "latest":
            return load
        elif Path(load).exists():
            return load
        else:
            raise ValueError(f"Path {load} does not exist")
