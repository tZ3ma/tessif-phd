import tessif.frused.namedtuples as nts
import numpy as np
import pandas as pd

# timeseries_fixed

# one source, two sinks
# sinks differ in parametrization of flow_rate and flow_costs
# sink1 has a capped flow rate given in a timeseries with an equal or lower value than the sources outflow
# sink2 has infinite flow rate (default parametrization) but higher flow costs than source1
# expected behaviour:   sink1 will be fed from source with max flow rate, remaining outflow will feed sink2
#                       (-> the flow rate argument will cap the flow from sink1)

mapping = {
    'sources': {
        'sourceA': {
            'name': 'source1',
            'outputs': ('electricity',),
            # force a flow rate of exactly 50
            'flow_rates': {'electricity': nts.MinMax(min=50, max=50)},
            'timeseries': {'electricity': nts.MinMax(min=10*[50], max=10*[50])},
        },
    },
    'transformers': {},
    'sinks': {
        'sinkA': {
            'name': 'sink1',
            'inputs': ('electricity',),
            # flow_costs = 0
            'flow_costs': {'electricity': 0},
            'flow_rates': {'electricity': nts.MinMax(min=0, max=50)},
            # flow_rate limited
            'timeseries': {
                'electricity': nts.MinMax(
                    min=[50, 40, 30, 20, 10, 0, 0, 0, 0, 0, ],
                    max=[50, 40, 30, 20, 10, 0, 0, 0, 0, 0, ],
                ),
            },
        },
        'sinkB': {
            'name': 'sink2',
            'inputs': ('electricity',),
            # flow_rate unlimited (default)
            'flow_rates': {'electricity': nts.MinMax(min=0, max=50)},
            'timeseries': {
                'electricity': nts.MinMax(
                    min=[0, 10, 20, 30, 40, 50, 50, 50, 50, 50, ],
                    max=[0, 10, 20, 30, 40, 50, 50, 50, 50, 50, ],
                ),
            },
            # flow_costs > 0
            'flow_costs': {'electricity': 1},
        },
    },
    'storages': {},
    'busses': {
        'busA': {
            'name': 'centralbus',
            'inputs': ('source1.electricity',),
            'outputs': ('sink1.electricity', 'sink2.electricity',),
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
}  # minimum working example sink - linear - timeseries_fixed
