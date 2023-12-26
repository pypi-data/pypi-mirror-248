import torch
import torch.nn as nn

def save_checkpoint_simple(model:nn.Module, filename='checkpoint.pth.tar', optim=None, **kwargs):
    optim_state = optim.state_dict() if optim is not None else None
    model_state = model.module.state_dict() if isinstance(model, nn.DataParallel) else model.state_dict()
    state = {
        'model': model_state,
        'optim': optim_state
    }
    state.update(kwargs)
    torch.save(state, filename)


def load_checkpoint_simple(filename='checkpoint.pth.tar', model:nn.Module = None, optim=None):
    state = torch.load(filename)
    model_state = state.get('model')
    if model_state is None:
        raise ValueError('file (dict) not have key "model"')
    optim_state = state.get('optim')
    if model is not None:
        if isinstance(model, nn.DataParallel):
            raise ValueError('model should not be nn.DataParallel')
        model.load_state_dict(model_state)
    if optim is not None and optim_state is not None:
        optim.load_state_dict(optim_state)
    return state