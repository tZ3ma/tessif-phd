import tessif.frused.namedtuples as nts
import numpy as np
import pandas as pd

# idle_changes_positive

# source, sink, storage
# sink demands a consistent inflow of 10
# source high flow_costs but no limited flow_rate (default)
# storage has low flow_costs, initial_soc of 50 and idle_changes of 2.5 per timestep
# expected behaviour: storage will feed sink with a flow_rate 10 for first four timesteps, because after 4 timesteps 10 entities will be lost due to idle changes

mapping = {
    'sources': {
        'sourceA': {
            'name': 'source1',
            'outputs': ('electricity',),
            # flow_costs higher than storage
            'flow_costs': {'electricity': 2},
        },
    },
    'transformers': {},
    'sinks': {
        'sinkA': {
            'name': 'sink1',
            'inputs': ('electricity',),
            # force an inflow of exactly 10
            'flow_rates': {'electricity': nts.MinMax(min=10, max=10)},
        },
    },
    'storages': {
        'storageA': {
            'name': 'storage1',
            'input': 'electricity',
            'output': 'electricity',
            'capacity': 100,
            'initial_soc': 0,
            # costs = 0
            'flow_costs': {'electricity': 1},
            # idle_changes are +2 per timestep
            'idle_changes': nts.PositiveNegative(negative=0, positive=22),
        },
    },
    'busses': {
        'bus': {
            'name': 'centralbus',
            'inputs': ('source1.electricity', 'storage1.electricity'),
            'outputs': ('sink1.electricity', 'storage1.electricity',),
            'component': 'bus',
        },
    },
    'timeframe': {
        'primary': pd.date_range('01/01/2022', periods=10, freq='H'),
    },
    'global_constraints': {
        'primary': {'name': 'default',
                    'emissions': float('+inf'),
                    'material': float('+inf')},
    },
}  # minimum working example storage - linear - idle_changes_positive