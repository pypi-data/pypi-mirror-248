import importlib
import json
import os.path
import sys
from typing import Dict, List, Type

from project_dilemma.config import ProjectDilemmaConfig
from project_dilemma.interfaces import Algorithm, Node, Simulation, SimulationRounds
from project_dilemma.simulations import simulations_map


def create_nodes(config: ProjectDilemmaConfig, algorithms_map: Dict[str, Type[Algorithm]]) -> List[Node]:
    """create the simulation nodes

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :param algorithms_map: map of algorithm class names to algorithms
    :type algorithms_map: Dict[str, Type[Algorithm]]
    :return:
    """
    nodes = []

    for node in config['nodes']:
        nodes.append(Node(node['node_id'], algorithms_map[node['algorithm']['object']]))

    return nodes


def load_algorithms(config: ProjectDilemmaConfig) -> Dict[str, Type[Algorithm]]:
    """load all algorithms used

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :return: map of algorithm class names to algorithms
    :rtype: Dict[str, Type[Algorithm]]
    """
    sys.path.append(config['algorithms_directory'])

    algorithms = [node['algorithm'] for node in config['nodes']]
    algorithm_map: Dict[str, Type[Algorithm]] = {}

    for algorithm in algorithms:
        if algorithm_map.get(algorithm['object']):
            continue

        if not os.path.exists(os.path.join(config['algorithms_directory'], algorithm['file'])):
            print(f"Algorithm file {algorithm['file']} could not be found")
            sys.exit(1)

        algorithm_module = importlib.import_module(algorithm['file'].strip('.py'))
        algorithm_map[algorithm['object']] = getattr(algorithm_module, algorithm['object'])

    return algorithm_map


def load_rounds(config: ProjectDilemmaConfig) -> SimulationRounds:
    round_data = {}

    if config.get('rounds_data'):
        try:
            with open(config['rounds_data'], 'r') as f:
                round_data = json.load(f)
        except FileNotFoundError:
            print('Rounds data file not found')
            sys.exit(1)

    return round_data


def load_simulation(config: ProjectDilemmaConfig) -> Type[Simulation]:
    """load the simulation

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :return: the configured simulation
    :rtype: Simulation
    """
    if config['simulation'].get('file'):
        if not config.get('simulations_directory'):
            print('A simulations directory is required to use user provided simulations')
            sys.exit(1)

        sys.path.append(config['simulations_directory'])

        if not os.path.exists(os.path.join(config['simulations_directory'], config['simulation']['file'])):
            print('Simulation file could not be found')
            sys.exit(1)

        simulation_module = importlib.import_module(config['simulation']['file'].strip('.py'))
        simulation = getattr(simulation_module, config['simulation']['object'])
    else:
        simulation = simulations_map[config['simulation']['object']]

    return simulation
