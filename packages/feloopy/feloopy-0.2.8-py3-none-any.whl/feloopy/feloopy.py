# Copyright (c) 2022-2024, Keivan Tafakkori. All rights reserved.
# See the file LICENSE file for licensing details.

__author__ = ['Keivan Tafakkori']


from .helpers.empty import *
from .helpers.error import *
from .helpers.formatter import *
from .operators.data_handler import *
from .operators.fix_operators import *
from .operators.heuristic_operators import *
from .operators.math_operators import *
from .operators.random_operators import *
from .operators.set_operators import *
from .operators.update_operators import *

from collections import defaultdict
from tabulate import tabulate as tb
from typing import Literal, List, Dict, Tuple, Union, Optional, Any, Callable
import importlib
import itertools as it
import math as mt
import numpy as np
import platform
import sys
import time
import warnings

from .classes.tensor_variable import *
from .classes.tensor_variable_collection import *
from .classes.multidim_variable import *
from .classes.multidim_variable_collection import *
from .classes.event_variable import *
from .classes.event_variable_collection import *
from .classes.special_constraint import *
from .classes.linearization import *
from .classes.constraint_programming import *

warnings.filterwarnings("ignore")

class ModelObject:
    pass

class AgentObject:
    pass

class ConditionalObject:
    pass

class TensorVariableCollection:
    pass

class MultidimVariableCollection:
    pass

class EventVariable:
    pass

class Model(TensorVariableClass,
            TensorVariableCollectionClass,
            MultidimVariableClass,
            MultidimVariableCollectionClass,
            EventVariableClass,
            EventVariableCollectionClass,
            SpecialConstraintClass,
            LinearizationClass,
            ConstraintProgrammingClass):
    
    def __init__(self,
                 solution_method: Literal[
                     'constraint', 
                     'convex', 
                     'exact', 
                     'heuristic', 
                     'uncertain',
                 ],
                 model_name: str,
                 interface_name: Literal[
                     'copt',
                     'cplex',
                     'cplex_cp',
                     'cvxpy',
                     'cylp',
                     'feloopy',
                     'gekko',
                     'gurobi',
                     'linopy',
                     'mealpy',
                     'mip',
                     'niapy',
                     'ortools',
                     'ortools_cp'
                     'picos',
                     'pulp',
                     'pygad',
                     'pymoo',
                     'pymprog',
                     'pymultiobjective',
                     'pyomo',
                     'rsome_dro',
                     'rsome_ro',
                     'xpress',
                 ],
                 agent: Optional[Union[AgentObject, None]] = None,
                 scens: Optional[int] = 1,
                 no_agents: Optional[int] = None,
                 ) -> None:
        """
        Creates and initializes the mathematical modeling environment.

        Parameters
        ----------
        solution_method : Literal['exact', 'heuristic', 'constraint', 'convex', 'uncertain']
            The desired solution method for optimization.
        model_name : str
            The name of the optimization model.
        interface_name : Literal[
            'copt', 'cplex', 'cplex_cp', 'cvxpy', 'cylp', 'feloopy', 'gekko', 'gurobi', 'linopy',
            'mealpy', 'mip', 'niapy', 'ortools', 'ortools_cp', 'picos', 'pulp', 'pygad', 'pymoo',
            'pymprog', 'pymultiobjective', 'pyomo', 'rsome_dro', 'rsome_ro', 'xpress',
        ]
            The selected solver interface for optimization.
        agent : Optional[Union[AgentObject, None]] (default=None)
            An optional search agent object. If not provided, the optimization will be agentless.
        scens : Optional[int] (default=1)
            The number of scenarios for the optimization problem. Defaults to 1 if not specified.
        no_agents : Optional[int] (default=None)
            The number of search agents to use in the optimization. If not specified, the default behavior will be applied.
        """
        
        if solution_method not in {'exact', 'heuristic', 'constraint', 'convex', 'uncertain'}:
            raise ValueError("Invalid solution method. Please choose from 'exact', 'heuristic', 'constraint', 'convex', or 'uncertain'.")
        
        if interface_name not in {'copt', 'cplex', 'cplex_cp', 'cvxpy', 'cylp', 'feloopy', 'gekko', 'gurobi', 'linopy',
                                  'mealpy', 'mip', 'niapy', 'ortools', 'ortools_cp', 'picos', 'pulp', 'pygad', 'pymoo',
                                  'pymprog', 'pymultiobjective', 'pyomo', 'rsome_dro', 'rsome_ro', 'xpress'}:
            raise ValueError("Invalid solver interface. Please choose from the provided options.")
        
        if not isinstance(scens, int) or scens < 1:
            raise ValueError("The number of scenarios (scens) must be a positive integer (>=1).")
        
        if no_agents is not None and (not isinstance(no_agents, int) or no_agents < 1):
            raise ValueError("The number of search agents (no_agents) must be a positive integer (>=1) or None.")

        self.no_agents = no_agents

        if solution_method == 'constraint':
            self.solution_method_was = 'constraint'
            solution_method = 'exact'

        elif solution_method == 'convex':
            self.solution_method_was = 'convex'
            solution_method = 'exact'

        elif solution_method == 'uncertain':
            self.solution_method_was = 'uncertain'
            solution_method = 'exact'

        else:
            self.solution_method_was=None

        self.features = {
            'solution_method': solution_method,
            'model_name': model_name,
            'interface_name': interface_name,
            'solver_name': None,
            'constraints': [],
            'constraint_labels': [],
            'objectives': [],
            'objective_labels': [],
            'directions': [],
            'positive_variable_counter': [0, 0],
            'integer_variable_counter': [0, 0],
            'binary_variable_counter': [0, 0],
            'free_variable_counter': [0, 0],
            'event_variable_counter': [0, 0],
            'sequential_variable_counter': [0,0],
            'dependent_variable_counter': [0,0],
            'total_variable_counter': [0, 0],
            'objective_counter': [0, 0],
            'constraint_counter': [0, 0],
            'objective_being_optimized': 0,
            'scens': scens,
        }

        if solution_method == 'heuristic':
            
            self.agent = agent
            
            self.features.update(
                {
                'agent_status': self.agent[0],
                'variable_spread': self.agent[2] if self.agent[0] != 'idle' else dict(),
                'variable_type': dict() if self.agent[0] == 'idle' else None,
                'variable_bound': dict() if self.agent[0] == 'idle' else None,
                'variable_dim': dict() if self.agent[0] == 'idle' else None,
                'pop_size': 1 if self.agent[0] == 'idle' else len(self.agent[1]),
                'penalty_coefficient': 0 if self.agent[0] == 'idle' else self.agent[3],
                'vectorized': None,
                }
            )

            self.features['vectorized'] = interface_name in ['feloopy', 'pymoo']

            if self.agent[0] != 'idle':

                self.agent = self.agent[1].copy()

            if self.features['agent_status']!='idle':
                self.access = True
                
            else:
                self.access = False

        if solution_method == 'exact':

            self.mainvars = defaultdict()
            self.maindims = defaultdict()

            from .generators import model_generator
            self.model = model_generator.generate_model(self.features)
            self.sm = self.link_to_interface = self.lti = self.model
            
        # Alias methods
        
        # Binary variable aliases
        self.binary_variable = self.binary = self.bool = self.add_bool = self.add_binary = self.add_binary_variable = self.boolean_variable = self.add_boolean_variable = self.bvar
        
        # Positive variable aliases
        self.positive_variable = self.positive = self.add_positive = self.add_positive_variable = self.pvar
        
        # Integer variable aliases
        self.integer_variable = self.integer = self.add_integer = self.add_integer_variable = self.ivar
        
        # Free variable aliases
        self.free_variable = self.free = self.float = self.add_free = self.add_float = self.real = self.add_real = self.add_free_variable = self.fvar
        
        # Sequential variable aliases
        self.sequential_variable = self.sequence = self.sequential = self.add_sequence = self.add_sequential = self.add_sequential_variable = self.permutation_variable = self.add_permutation_variable = self.svar
        
        # Positive tensor variable aliases
        self.positive_tensor_variable = self.positive_tensor = self.add_positive_tensor = self.add_positive_tensor_variable = self.ptvar
        
        # Binary tensor variable aliases
        self.binary_tensor_variable = self.binary_tensor = self.add_binary_tensor = self.add_binary_tensor_variable = self.add_boolean_tensor_variable = self.boolean_tensor_variable = self.btvar
        
        # Integer tensor variable aliases
        self.integer_tensor_variable = self.integer_tensor = self.add_integer_tensor = self.add_integer_tensor_variable = self.itvar
        
        # Free tensor variable aliases
        self.free_tensor_variable = self.free_tensor = self.float_tensor = self.add_free_tensor = self.add_float_tensor = self.add_free_tensor_variable = self.ftvar
        
        # Random variable aliases
        self.random_variable = self.add_random_variable = self.rvar
        
        # Random tensor variable aliases
        self.random_tensor_variable = self.add_random_tensor_variable = self.rtvar
        
        # Dependent variable aliases
        self.dependent_variable = self.array = self.add_array = self.add_dependent_variable = self.dvar
        
        # Objective aliases
        self.objective = self.reward = self.hypothesis = self.fitness = self.goal = self.add_objective = self.loss = self.gain = self.obj
        
        # Constraint aliases
        self.constraint = self.equation = self.add_constraint = self.add_equation = self.st = self.subject_to = self.cb = self.computed_by = self.penalize = self.pen = self.eq = self.con
        
        # Solve aliases
        self.solve = self.implement = self.run = self.optimize = self.sol
        
        # Query aliases
        self.get_obj = self.get_objective
        self.get_stat = self.get_status
        self.get_tensor = self.get_numpy_var
        self.get_var = self.value = self.get = self.get_variable

    def __getitem__(self, agent: AgentObject) -> ConditionalObject:
        """
        Retrieve the required features of the model object.

        Parameters
        ----------
        agent : AgentObject
            The search agent object used to determine the feature retrieval method.

        Returns
        -------
        ConditionalObject
            The requested features or the model object itself based on the agent's status.

        Notes
        -----
        - If the agent's status is 'idle', the method returns the model object.
        - If the agent's status is 'feasibility_check', the method invokes `_feasibility_check()` and returns its result.
        - For other statuses, the method calls `_get_result(vectorized, interface_name)` and returns the result.
        """

        agent_status = self.features['agent_status']
        vectorized = self.features['vectorized']
        interface_name = self.features['interface_name']

        if agent_status == 'idle':
            return self
        
        elif agent_status == 'feasibility_check':
            return self._feasibility_check()
        
        else:
            return self._get_result(vectorized, interface_name)

    def _feasibility_check(self) -> str:
        """
        Perform a feasibility check based on the model's features.

        Returns
        -------
        str
            The feasibility status:
            - 'feasible (unconstrained)' if the penalty coefficient is 0.
            - 'infeasible (constrained)' if the penalty value is greater than 0.
            - 'feasible (constrained)' otherwise.
        """
        
        if self.features['penalty_coefficient'] == 0:
            return 'feasible (unconstrained)'
        else:
            return 'infeasible (constrained)' if self.penalty > 0 else 'feasible (constrained)'

    def _get_result(self, vectorized: bool, interface_name: str) -> ConditionalObject:
        """
        Retrieve the optimization result based on the specified parameters.

        Parameters
        ----------
        vectorized : bool
            A boolean indicating whether the result should be vectorized.
        interface_name : str
            The name of the solver interface.

        Returns
        -------
        ConditionalObject
            The optimization result:
            - If vectorized is True and the interface is 'feloopy', returns the search agent.
            - If vectorized is True and the interface is not 'feloopy', returns the singular result.
            - If vectorized is False, returns the response.
        """
        
        if vectorized:
            return self.agent if interface_name == 'feloopy' else self.sing_result
        else:
            return self.response
        
    def obj(self, expression=0, direction=None, label=None):
            """
            Defines the objective function for the optimization problem.

            Parameters
            ----------
            expression : formula
                The terms of the objective function.
            direction : str, optional
                The direction for optimizing this objective ("min" or "max").
            label : str, optional
                The label for this objective function.

            """
            
            if self.features['solution_method'] == 'exact' or (self.features['solution_method'] == 'heuristic' and self.features['agent_status'] == 'idle'):

                self.features['directions'].append(direction)
                self.features['objectives'].append(expression)
                self.features['objective_labels'].append(label)

                self.features['objective_counter'][0] += 1
                self.features['objective_counter'][1] += 1

            elif self.features['solution_method'] == 'heuristic' and self.features['agent_status'] != 'idle':

                self.features['directions'].append(direction)
                self.features['objectives'].append(expression)
                self.features['objective_counter'][0] += 1

    def con(self, expression, label=None):
        """
        Constraint Definition
        ~~~~~~~~~~~~~~~~~~~~~
        To define a constraint.

        Args:
            expression (formula): what are the terms of this constraint?
            label (str, optional): what is the label of this constraint?. Defaults to None.
        """

        match self.features['solution_method']:

            case 'exact':

                self.features['constraint_labels'].append(label)
                self.features['constraint_counter'][0] = len(
                    set(self.features['constraint_labels']))
                self.features['constraints'].append(expression)
                self.features['constraint_counter'][1] = len(
                    self.features['constraints'])

            case 'heuristic':

                if self.features['agent_status'] == 'idle':

                    self.features['constraint_labels'].append(label)

                    self.features['constraint_counter'][0] = len(
                        set(self.features['constraint_labels']))

                    self.features['constraints'].append(expression)

                    self.features['constraint_counter'][1] = len(
                        self.features['constraints'])

                else:

                    if self.features['vectorized']:

                        self.features['constraints'].append(
                            np.reshape(expression, [np.shape(self.agent)[0], 1]))

                    else:
                        self.features['constraints'].append(expression)

    def sol(self, directions=None, solver_name=None, solver_options=dict(), obj_id=0, email=None, debug=False, time_limit=None, cpu_threads=None, absolute_gap=None, relative_gap=None, show_log=False, save_log=False, save_model=False, max_iterations=None, obj_operators=[]):
        """
        Solve Command Definition
        ~~~~~~~~~~~~~~~~~~~~~~~~
        To define solver and its settings to solve the problem.

        Args:
            directions (list, optional): please set the optimization directions of the objectives, if not provided before. Defaults to None.
            solver_name (_type_, optional): please set the solver_name. Defaults to None.
            solver_options (dict, optional): please set the solver options using a dictionary with solver specific keys. Defaults to None.
            obj_id (int, optional): please provide the objective id (number) that you wish to optimize. Defaults to 0.
            email (_type_, optional): please provide your email address if you wish to use cloud solvers (e.g., NEOS server). Defaults to None.
            debug (bool, optional): please state if the model should be checked for feasibility or logical bugs. Defaults to False.
            time_limit (seconds, optional): please state if the model should be solved under a specific timelimit. Defaults to None.
            cpu_threads (int, optional): please state if the solver should use a specific number of cpu threads. Defaults to None.
            absolute_gap (value, optional): please state an abolute gap to find the optimal objective value. Defaults to None.
            relative_gap (%, optional): please state a releative gap (%) to find the optimal objective value. Defaults to None.
        """

        if self.no_agents!=None:
            if self.features['interface_name'] in ['mealpy' , 'feloopy', 'niapy', 'pygad']:
                solver_options['pop_size'] = self.no_agents

        if len(self.features['objectives']) !=0 and len(directions)!=len(self.features['objectives']):
            raise MultiObjectivityError("The number of directions and the provided objectives do not match.")

        self.features['objective_being_optimized'] = obj_id
        self.features['solver_options'] = solver_options
        self.features['debug_mode'] = debug
        self.features['time_limit'] = time_limit
        self.features['thread_count'] = cpu_threads
        self.features['absolute_gap'] = absolute_gap
        self.features['relative_gap'] = relative_gap
        self.features['log'] = show_log
        self.features['write_model_file'] = save_model
        self.features['save_solver_log'] = save_log
        self.features['email_address'] = email
        self.features['max_iterations'] = max_iterations
        self.features['obj_operators'] = obj_operators
        self.features['solver_name'] = solver_name

        try:
            if type(obj_id) != str and directions != None:

                if self.features['directions'][obj_id] == None:

                    self.features['directions'][obj_id] = directions[obj_id]
                for i in range(len(self.features['objectives'])):
                    if i != obj_id:
                        del self.features['directions'][i]
                        del directions[i]
                        del self.features['objectives'][i]
                obj_id = 0

                self.features['objective_counter'] = [1, 1]

            else:

                for i in range(len(self.features['directions'])):

                    self.features['directions'][i] = directions[i]
        except:
            pass

        match self.features['solution_method']:

            case 'exact':

                self.features['model_object_before_solve'] = self.model

                from .generators import solution_generator

                try:
                    if len(self.features['objectives'])==0:
                        self.obj()
                        self.features['objective_counter'][1] = 0
                        self.features['directions'] = ["nan"]
                        self.features['solver_name'] = directions
        
                    self.solution = solution_generator.generate_solution(
                        self.features)
                
                except:

                    if len(self.features['objectives'])==0:
                        self.obj()
                        self.features['objective_counter'][1] = 0
                        self.features['directions'] = ["min"]
                        self.features['solver_name'] = directions
        
                    self.solution = solution_generator.generate_solution(self.features)
                    


                try:
                    self.obj_val = self.get_objective()
                    self.status = self.get_status()
                    self.cpt = self.get_time()*10**6

                except:
                    "None"

            case 'heuristic':

                if self.features['agent_status'] == 'idle':

                    "Do nothing"

                else:

                    if self.features['vectorized']:

                        if self.features['interface_name']=='feloopy':

                            self.penalty = np.zeros(np.shape(self.agent)[0])

                            if self.features['penalty_coefficient'] != 0 and len(self.features['constraints']) == 1:

                                self.features['constraints'][0] = np.reshape(
                                    self.features['constraints'][0], [np.shape(self.agent)[0], 1])
                                self.features['constraints'].append(
                                    np.zeros(shape=(np.shape(self.agent)[0], 1)))
                                self.penalty = np.amax(np.concatenate(
                                    self.features['constraints'], axis=1), axis=1)

                                self.agent[np.where(self.penalty == 0), -2] = 1
                                self.agent[np.where(self.penalty > 0), -2] = -1

                            if self.features['penalty_coefficient'] != 0 and len(self.features['constraints']) > 1:

                                self.features['constraints'].append(
                                    np.zeros(shape=(np.shape(self.agent)[0], 1)))
                                self.penalty = np.amax(np.concatenate(
                                    self.features['constraints'], axis=1), axis=1)
                                self.agent[np.where(self.penalty == 0), -2] = 1
                                self.agent[np.where(self.penalty > 0), -2] = -1

                            else:

                                self.agent[:, -2] = 2

                            if type(obj_id) != str:

                                if directions[obj_id] == 'max':
                                    self.agent[:, -1] = np.reshape(self.features['objectives'][obj_id], [self.agent.shape[0],]) - np.reshape(
                                        self.features['penalty_coefficient'] * (self.penalty)**2, [self.agent.shape[0],])

                                if directions[obj_id] == 'min':
                                    self.agent[:, -1] = np.reshape(self.features['objectives'][obj_id], [self.agent.shape[0],]) + np.reshape(
                                        self.features['penalty_coefficient'] * (self.penalty)**2, [self.agent.shape[0],])

                            else:

                                self.agent[:, -1] = 0

                                total_obj = self.features['objective_counter'][0]
                                
                                self.features['objectives'] = np.array(self.features['objectives']).T

                                for i in range(self.features['objective_counter'][0]):

                                    if directions[i] == 'max':
                                        self.agent[:, -2-total_obj+i] = self.features['objectives'][:,i] - self.features['penalty_coefficient'] * (self.penalty)**2

                                    if directions[i] == 'min':
                                        self.agent[:, -2-total_obj+i] = self.features['objectives'][:,i] + self.features['penalty_coefficient'] * (self.penalty)**2
                        else:

                            self.penalty = np.zeros(np.shape(self.agent)[0])

                            if self.features['penalty_coefficient'] != 0 and len(self.features['constraints']) == 1:

                                self.features['constraints'][0] = np.reshape(self.features['constraints'][0], [np.shape(self.agent)[0], 1])
                                self.features['constraints'].append(np.zeros(shape=(np.shape(self.agent)[0], 1)))
                                self.penalty = np.amax(np.concatenate(self.features['constraints'], axis=1), axis=1)

                            if self.features['penalty_coefficient'] != 0 and len(self.features['constraints']) > 1:

                                self.features['constraints'].append(np.zeros(shape=(np.shape(self.agent)[0], 1)))
                                self.penalty = np.amax(np.concatenate(self.features['constraints'], axis=1), axis=1)

                            if type(obj_id) != str:

                                if directions[obj_id] == 'max':
                                    self.sing_result = np.reshape(self.features['objectives'][obj_id], [self.agent.shape[0],]) - np.reshape(self.features['penalty_coefficient'] * (self.penalty)**2, [self.agent.shape[0],])

                                if directions[obj_id] == 'min':
                                    self.sing_result = np.reshape(self.features['objectives'][obj_id], [self.agent.shape[0],]) + np.reshape(self.features['penalty_coefficient'] * (self.penalty)**2, [self.agent.shape[0],])

                            else:

                                total_obj = self.features['objective_counter'][0]

                                self.sing_result = []
                                

                                for i in range(self.features['objective_counter'][0]):

                                    
                                    if directions[i] == 'max':
                                        self.sing_result.append(self.features['objectives'][i] - self.features['penalty_coefficient'] * (self.penalty)**2)

                                    if directions[i] == 'min':
                                        self.sing_result.append(self.features['objectives'][i] + self.features['penalty_coefficient'] * (self.penalty)**2)
                    else:

                        self.penalty = 0

                        if len(self.features['constraints']) >= 1:

                            self.penalty = np.amax(
                                np.array([0]+self.features['constraints'], dtype=object))

                        if type(obj_id) != str:

                            if directions[obj_id] == 'max':
                                self.response = self.features['objectives'][obj_id] - \
                                    self.features['penalty_coefficient'] * \
                                    (self.penalty-0)**2

                            if directions[obj_id] == 'min':
                                self.response = self.features['objectives'][obj_id] + \
                                    self.features['penalty_coefficient'] * \
                                    (self.penalty-0)**2

                        else:

                            total_obj = self.features['objective_counter'][0]

                            self.response = [None for i in range(total_obj)]

                            for i in range(total_obj):

                                if directions[i] == 'max':

                                    self.response[i] = self.features['objectives'][i] - \
                                        self.features['penalty_coefficient'] * \
                                        (self.penalty)**2

                                if directions[i] == 'min':

                                    self.response[i] = self.features['objectives'][i] + \
                                        self.features['penalty_coefficient'] * \
                                        (self.penalty)**2

    def healthy(self):
        try:
            status = self.get_status().lower()
            return ('optimal' in status or 'feasible' in status) and 'infeasible' not in status
        except:
            try:
                status = self.get_status()[0].lower()
                return ('feasible' in status or 'optimal' in status) and 'infeasible' not in status
            except:
                return True

    # Get values

    def get_variable(self, variable_with_index):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'variable', variable_with_index)

    def get_rc(self, variable_with_index):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'rc', variable_with_index)

    def get_dual(self, constraint_label_with_index):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'dual', constraint_label_with_index)

    def get_iis(self):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'iis', '')

    def get_slack(self, constraint_label_with_index):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'slack', constraint_label_with_index)
    
    def get_objective(self):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'objective', None)

    def get_status(self):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'status', None)

    def get_time(self):
        from .generators import result_generator
        return result_generator.get(self.features, self.model, self.solution, 'time', None)

    def get_start(self, invterval_variable):

        if self.features['interface_name'] == 'cplex_cp':
            return self.solution[0].get_var_solution(invterval_variable).get_start()
        
        if self.features['interface_name'] == 'ortools_cp':

            ""

    def get_interval(self, invterval_variable):

        if self.features['interface_name'] == 'cplex_cp':
            return self.solution[0].get_var_solution(invterval_variable)
        
        if self.features['interface_name'] == 'ortools_cp':
            ""

    def get_end(self, invterval_variable):

        if self.features['interface_name'] == 'cplex_cp':
            return self.solution[0].get_var_solution(invterval_variable).get_end()
        if self.features['interface_name'] == 'ortools_cp':
            ""

    def dis_time(self):

        hour = round((self.get_time()), 3) % (24 * 3600) // 3600
        min = round((self.get_time()), 3) % (24 * 3600) % 3600 // 60
        sec = round((self.get_time()), 3) % (24 * 3600) % 3600 % 60

        print(f"cpu time [{self.features['interface_name']}]: ", self.get_time(
        )*10**6, '(microseconds)', "%02d:%02d:%02d" % (hour, min, sec), '(h, m, s)')

    def scen_probs(self):
        """
        Returns an array of scenario probabilities
        """
        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            return self.model.p

    def exval(self,expr):

        """
        Expected Value
        --------------
        1) Returns the expected value of random variables if the uncertainty set of expectations is being determined.
        2) Returns the worst case expected values of an expression that has random variables inside.

        """
        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import E
            return E(expr)

    def norm(self,expr_or_1D_array_of_variables, degree):
        
        """
        Returns the first, second, or infinity norm of a 1-D array.
        """

        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import norm
            return norm(expr_or_1D_array_of_variables, degree)
    
    def sumsqr(self,expr_or_1D_array_of_variables):


        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
        
            from rsome import sumsqr
            return sumsqr(expr_or_1D_array_of_variables)
    
    def state_function(self):
        
        """

        Creates and returns a state function.

        """

        return self.model.state_function()

    def report(self, all_metrics: bool = False, feloopy_info: bool = True, math_info: bool = False, sys_info: bool = False, model_info: bool = True, sol_info: bool = True, obj_values: bool = True, dec_info: bool = True, metric_info: bool = True, ideal_pareto: Optional[np.ndarray] = [], ideal_point: Optional[np.array] = [], show_tensors = False, show_detailed_tensors=False, save=None):


        if not self.healthy():
            print()
            print()
            print('WARNING: Model is not healthy!')
            print()
            print()
            
            
        self.interface_name = self.features['interface_name']
        if self.solution_method_was==None:
            self.solution_method = self.features['solution_method']
        else:
            self.solution_method = self.solution_method_was
        self.model_name = self.features['model_name']
        self.solver_name = self.features['solver_name']
        self.model_constraints = self.features['constraints']
        self.model_objectives = self.features['objectives']
        self.objectives_directions = self.features['directions']
        self.pos_var_counter = self.features['positive_variable_counter']
        self.bin_var_counter = self.features['binary_variable_counter']
        self.int_var_counter = self.features['integer_variable_counter']
        self.free_var_counter = self.features['free_variable_counter']
        self.event_var_counter = self.features['event_variable_counter']
        self.tot_counter = self.features['total_variable_counter']
        self.con_counter = self.features['constraint_counter']
        self.obj_counter = self.features['objective_counter']

        if save is not None:
            stdout_origin = sys.stdout
            sys.stdout = open(save, "w")

        status = self.get_status()
        hour, min, sec = calculate_time_difference(length=self.get_time())

        if len(str(status)) == 0:
            status = ['infeasible (constrained)']

        box_width = 80
        vspace()

        if feloopy_info:
            
            import datetime
            now = datetime.datetime.now()
            date_str = now.strftime("Date: %Y-%m-%d")
            time_str = now.strftime("Time: %H:%M:%S")
            tline_text("FelooPy v0.2.8")
            empty_line()
            two_column(date_str, time_str)
            two_column(f"Interface: {self.interface_name}", f"Solver: {self.solver_name}")
            empty_line()
            bline()

        if sys_info:
            try:
                import psutil
                import cpuinfo
                import platform
                tline_text("System")
                empty_line()
                cpu_info = cpuinfo.get_cpu_info()["brand_raw"]
                cpu_cores = psutil.cpu_count(logical=False)
                cpu_threads = psutil.cpu_count(logical=True)
                ram_info = psutil.virtual_memory()
                ram_total = ram_info.total
                os_info = platform.system()
                os_version = platform.version()
                left_align(f"OS: {os_version} ({os_info})")
                left_align(f"CPU   Model: {cpu_info}")
                left_align(f"CPU   Cores: {cpu_cores}")
                left_align(f"CPU Threads: {cpu_threads}")
                try:
                    import GPUtil
                    gpus = GPUtil.getGPUs()
                    for gpu in gpus:
                        left_align(f"GPU   Model: {gpu.name}")
                        left_align(f"GPU    VRAM: {gpu.memoryTotal / 1024:.2f} GB")
                except:
                    pass
                left_align(f"SYSTEM  RAM: {ram_total / (1024 ** 3):.2f} GB")
            except:
                pass
            empty_line()
            bline()

        if model_info:
            tline_text("Model")
            empty_line()
            left_align(f"Name: {self.model_name}")
            list_three_column([
                ("Feature:         ", "Class:", "Total:"),
                ("Positive variable", self.pos_var_counter[0], self.pos_var_counter[1]),
                ("Binary variable  ", self.bin_var_counter[0], self.bin_var_counter[1]),
                ("Integer variable ", self.int_var_counter[0], self.int_var_counter[1]),
                ("Free variable    ", self.free_var_counter[0], self.free_var_counter[1]), 
                ("Event variable   ", self.event_var_counter[0], self.event_var_counter[1]),
                ("Total variables  ", self.tot_counter[0], self.tot_counter[1]), 
                ("Objective        ", "-", self.obj_counter[1]), 
                ("Constraint       ", self.con_counter[0], self.con_counter[1]) ])
            empty_line()
            bline()

        if math_info:
            try:
                import textwrap
                tline_text('Math', box_width=80)
                empty_line()
                obdirs = 0
                for objective in self.features['objectives']:
                    wrapped_objective = textwrap.fill(str(objective), width=80)
                    boxed(str(f"obj: {self.features['directions'][obdirs]} {wrapped_objective}"))
                    obdirs += 1
                left_align('s.t.')
                if self.features['constraint_labels'][0] != None:
                    for constraint in sorted(zip(self.features['constraint_labels'], self.features['constraints']), key=lambda x: x[0]):
                        wrapped_constraint = textwrap.fill(str(constraint[1]), width=80)
                        boxed(str(f"con {constraint[0]}: {wrapped_constraint}"))
                else:
                    counter = 0
                    for constraint in self.features['constraints']:
                        wrapped_constraint = textwrap.fill(str(constraint), width=80)
                        boxed(str(f"con {counter}: {wrapped_constraint}"))
                        counter += 1
                empty_line()
                bline()
            except:
                ""

        if self.healthy() == False:
            tline_text("Debug")
            empty_line()
            try:
                print(self.get_iis())
            except:
                ''
            empty_line()
            bline()

        if sol_info:
            tline_text("Solve")
            empty_line()
            try:
                two_column(f"Method: {self.solution_method}", "Objective value")
                status_row_print(self.objectives_directions, status)
                if obj_values:
                    if len(self.objectives_directions) != 1:
                        try:
                            solution_print(self.objectives_directions, status, self.get_obj(), self.get_payoff())
                        except:
                            left_align("Nothing found.")
                    else:
                        solution_print(self.objectives_directions, status, self.get_obj())
            except:
                ""
            empty_line()
            bline()

        if metric_info:
            tline_text("Metric")
            empty_line()
            self.calculated_indicators = None
            try:
                self.get_indicators(ideal_pareto=ideal_pareto, ideal_point=ideal_point)
            except:
                pass
            try:
                metrics_print(self.objectives_directions, all_metrics, self.get_obj(), self.calculated_indicators, length=self.get_time())
            except:
                pass
            empty_line()
            bline()

        if dec_info:
            tline_text("Decision")
            empty_line()
            try:
                self.decision_information_print(status, show_tensors, show_detailed_tensors)
            except:
                ""
            empty_line()
            bline()

        if save is not None:
            sys.stdout.close()
            sys.stdout = stdout_origin

    def get_numpy_var(self, var_name):

        for i,j in self.mainvars.keys():
            if j==var_name:
                if self.maindims[j]==0:
                    output = self.get(self.mainvars[(i,j)])
                elif len(self.maindims[j])==1:
                    output = np.zeros(shape=len(fix_dims(self.maindims[j])[0]))
                    for k in fix_dims(self.maindims[j])[0]:
                        try:
                            output[k] = self.get(self.mainvars[(i,j)][k])
                        except:
                            output[k] = self.get(self.mainvars[(i,j)])[k]
                else:
                    output = np.zeros(shape=tuple([len(dim) for dim in fix_dims(self.maindims[j])]))
                    for k in it.product(*tuple(fix_dims(self.maindims[j]))):
                        try:
                            output[k] = self.get(self.mainvars[(i,j)][k])
                        except:
                            output[k] =  self.get(self.mainvars[(i,j)])[k]
        return output

    def decision_information_print(self,status, show_tensors, show_detailed_tensors, box_width=80):
        
        if show_detailed_tensors: show_tensors=True
        
        if not show_tensors:

            for i,j in self.mainvars.keys():

                if i!='evar':

                    if self.maindims[j] == 0:

                        if self.get(self.mainvars[(i,j)]) not in [0, None]:

                            print(f"│ {j} =", self.get(self.mainvars[(i,j)]), " "* (box_width-(len(f"│ {j} =") + len(str(self.get(self.mainvars[(i,j)]))))-1) + "│")

                    elif len(self.maindims[j])==1:
                        try:
                            for k in fix_dims(self.maindims[j])[0]:
                                if self.get(self.mainvars[(i,j)][k]) not in [0, None]:
                                    print(f"│ {j}[{k}] =", self.get(self.mainvars[(i,j)][k]), " "* (box_width-(len(f"│ {j}[{k}] =") + len(str(self.get(self.mainvars[(i,j)][k])))) - 1) + "│")
                        except:
                            for k in fix_dims(self.maindims[j])[0]:
                                if self.get(self.mainvars[(i,j)])[k] not in [0, None]:
                                    print(f"│ {j}[{k}] =", self.get(self.mainvars[(i,j)])[k], " "* (box_width-(len(f"│ {j}[{k}] =") + len(str(self.get(self.mainvars[(i,j)])[k]))) - 1) + "│")
                    else:
                        try:
                            for k in it.product(*tuple(fix_dims(self.maindims[j]))):
                                if self.get(self.mainvars[(i,j)][k]) not in [0, None]:
                                    print(f"│ {j}[{k}] =".replace("(", "").replace(")", ""), self.get(self.mainvars[(i,j)][k]), " "* (box_width-(len(f"│ {j}[{k}] =".replace("(", "").replace(")", "")) + len(str(self.get(self.mainvars[(i,j)][k])))) - 1) + "│")
                        except:
                            for k in it.product(*tuple(fix_dims(self.maindims[j]))):
                                if self.get(self.mainvars[(i,j)])[k] not in [0, None]:
                                    print(f"│ {j}[{k}] =".replace("(", "").replace(")", ""), self.get(self.mainvars[(i,j)])[k], " "* (box_width-(len(f"│ {j}[{k}] =".replace("(", "").replace(")", "")) + len(str(self.get(self.mainvars[(i,j)])[k]))) - 1) + "│")

                else:

                    if self.maindims[j] == 0:
                            if self.get_start(self.mainvars[(i,j)])!=None:
                                print(f"│ {j} =", [self.get_start(self.mainvars[(i,j)]), self.get_end(self.mainvars[(i,j)])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)]), self.get_end(self.mainvars[(i,j)])])))-1) + "│")


                    elif len(self.maindims[j])==1:                    
                        for k in fix_dims(self.maindims[j])[0]:
                            if self.get_start(self.mainvars[(i,j)][k])!=None:
                                print(f"│ {j}[{k}] =", [self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])])))-1) + "│")

                    else:                    
                        for k in it.product(*tuple(fix_dims(self.maindims[j]))):
                            if self.get_start(self.mainvars[(i,j)][k])!=None:
                                print(f"│ {j}[{k}] =", [self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])])))-1) + "│")
                    
        else:
            
            if show_detailed_tensors: np.set_printoptions(threshold=np.inf)
            
            for i,j in self.mainvars.keys():
                
                if i!='evar':
                    
                    numpy_var = self.get_numpy_var(j) 

                    if type(numpy_var)==np.ndarray:

                        numpy_str = np.array2string(numpy_var, separator=', ', prefix='│ ', style=str)
                        rows = numpy_str.split('\n')
                        first_row_len = len(rows[0])
                        for i, row in enumerate(rows):
                            if i == 0:
                                left_align(f"{j} = {row}")
                            else:
                                left_align(" "*(len(f"{j} =")-1)+row)
                    else:
                        left_align(f"{j} = {numpy_var}")
                        
                else:

                    if self.maindims[j] == 0:
                            if self.get_start(self.mainvars[(i,j)])!=None:
                                print(f"│ {j} =", [self.get_start(self.mainvars[(i,j)]), self.get_end(self.mainvars[(i,j)])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)]), self.get_end(self.mainvars[(i,j)])])))-1) + "│")

                    elif len(self.maindims[j])==1:                    
                        for k in fix_dims(self.maindims[j])[0]:
                            if self.get_start(self.mainvars[(i,j)][k])!=None:
                                print(f"│ {j}[{k}] =", [self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])])))-1) + "│")

                    else:                    
                        for k in it.product(*tuple(fix_dims(self.maindims[j]))):
                            if self.get_start(self.mainvars[(i,j)][k])!=None:
                                print(f"│ {j}[{k}] =", [self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])], " "* (box_width-(len(f"│ {j} =") + len(str([self.get_start(self.mainvars[(i,j)][k]), self.get_end(self.mainvars[(i,j)][k])])))-1) + "│")
                            
    # Methods to work with input and output data.

    def max(self, *args):

        if self.features['interface_name'] == 'cplex_cp':
            return self.model.max(*args)

    def set(self, index='', bound=None, step=1, to_list=False):
        """
        Define a set. If bound is provided, the set will be a range from bound[0] to bound[1] with a step of step.
        If index is provided, the set will be created using the label index.

        Parameters
        ----------
        index : str, optional
            Label index to create the set.
        bound : list of int, optional
            Start and end values of the range. If provided, the set will be a range from bound[0] to bound[1].
        step : int, default 1
            Step size of the range.
        to_list : bool, default False
            If True, return the set as a list.

        Returns
        -------
        set or list
            The created set.

        Raises
        ------
        ValueError
            If neither bound nor index is provided.
        """

        # Check if index is an empty string
        if index == '':
            if not to_list:
                return set(range(bound[0], bound[1], step))
            else:
                return list(range(bound[0], bound[1], step))

        # Check if bound is provided
        if bound is not None:
            if not to_list:
                return set(f'{index}{i}' for i in range(bound[0], bound[1], step))
            else:
                return list(f'{index}{i}' for i in range(bound[0], bound[1], step))

        # Check if index is provided
        elif index:
            if not to_list:
                return set(f'{index}{i}' for i in range(0, len(index), step))
            else:
                return list(f'{index}{i}' for i in range(0, len(index), step))

        # Raise an error if neither bound nor index is provided
        else:
            raise ValueError('Either bound or index must be provided.')

    def ambiguity_set(self,*args,**kwds):
        """
        Ambiguity set defintion
        """
        return self.model.ambiguity(*args,**kwds)

    def sum(self, input):
        """
        Calculate the sum of all values in the input.

        :param input: List of values to be summed.
        :return: The sum of the input values.
        """
        if self.features['interface_name'] == 'cplex':
            return self.model.Sum(input)
        
        elif self.features['interface_name'] == 'gurobi':
            return self.model.quicksum(input)
        
        else:
            return sum(input)


    def card(self, set):
        """
        Card Definition
        ~~~~~~~~~~~~~~~~
        To measure size of the set, etc.
        """

        return len(set)
    
    def abs(self, input):

        if self.features['interface_name'] in ['cplex_cp', 'gekko']:

            return self.model.abs(input)

        else:

            return abs(input)

    def acos(self, input):
        """

        Inverse cosine

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.acos(input)

    def acosh(self, input):
        """

        Inverse hyperbolic cosine

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.acosh(input)

    def asin(self, input):
        """

        Inverse sine

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.acos(input)

    def asinh(self, input):
        """

        Inverse hyperbolic sine

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.acos(input)

    def atan(self, input):
        """

        Inverse tangent

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.acos(input)

    def atanh(self, input):
        """

        Inverse hyperbolic tangent

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.atanh(input)

    def cos(self, input):
        """

        Cosine

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.cos(input)

    def erf(self, input):
        """

        Error function

        """

        if self.features['interface_name'] == 'gekko':

            return self.model.erf(input)

    def erfc(self, input):
        """

        complementary error function

        """
        if self.features['interface_name'] == 'gekko':

            return self.model.erfc(input)

    def plus(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.plus(input1, input2)

        else:

            return input1+input2

    def minus(self, input1, input2):
        """

        Creates an expression that represents the product of two expressions.

        """

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.minus(input1, input2)

        else:

            return input1-input2

    def times(self, input1, input2):
        """

        Creates an expression that represents the product of two expressions.

        """

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.times(input1, input2)

        else:

            return input1*input2

    def true(self):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.true()

        else:

            return True

    def false(self):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.false()

        else:

            return False

    def trunc(self, input):
        '''
        Builds the truncated integer parts of a float expression
        '''

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.trunc(input)

        else:

            return "None"

    def int_div(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.int_div(input)

        else:

            return input1//input2

    def float_div(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.int_div(input)

        else:

            return input1/input2

    def mod(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.mod(input1, input2)

        else:

            return input1 % input2

    def square(self, input):

        if self.features['interface_name'] == 'cplex_cp':
            return self.model.square(input)
        
        elif self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import square
            return square(input)
        
        else:
            return input * input

    def quad(self,expr_or_1D_array_of_variables, positive_or_negative_semidefinite_matrix):

        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import quad
            return quad(expr_or_1D_array_of_variables,positive_or_negative_semidefinite_matrix)

    def expcone(self,rhs,a,b):
        """
        Returns an exponential cone constraint in the form: b*exp(a/b) <= rhs.

        Args
        rhs : array of variables or affine expression
        a : Scalar.
        b : Scalar.
        """

        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import expcone
            return expcone(rhs,a,b)

    def power(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.power(input1, input2)

        else:

            return input1 ** input2

    def kldive(self, input, emprical_rpob, ambiguity_constant):

        """
        Returns KL divergence
        
        input: an 1D array of variables, an affine expression, or probabilities. 
        emprical_rpob: an 1D array of emprical probabilities.
        ambiguity_constant: Ambiguity constant.
        """

        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:
            from rsome import kldiv
            return kldiv(input, emprical_rpob, ambiguity_constant)

    def entropy(self, input):

        """
        Returns an entropy expression like sum(input*log(input))
        """

        if self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:

            from rsome import entropy
            return entropy(input)

    def log(self, input):
        """

        Natural Logarithm

        """

        if self.features['interface_name'] in ['cplex_cp']:

            return self.model.log(input)

        elif self.features['interface_name'] in ['gekko']:

            return self.model.log(input)
        
        elif self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:

            from rsome import log
            return log(input)

        else:

            return np.log(input)

    def log10(self, input):
        """

        Logarithm Base 10

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.log10(input)

    def sin(self, input):
        """

        Sine

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.sin(input)

    def sinh(self, input):
        """

        Hyperbolic sine

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.sinh(input)

    def sqrt(self, input):
        """

        Square root

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.sqrt(input)

    def tan(self, input):
        """

        Tangent

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.tan(input)

    def tanh(self, input):
        """

        Hyperbolic tangent

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.tanh(input)

    def sigmoid(self, input):
        """

        Sigmoid function

        """

        if self.features['interface_name'] in ['gekko']:

            return self.model.sigmoid(input)

    def exponent(self, input):

        if self.features['interface_name'] in ['cplex_cp', 'gekko']:

            return self.model.exp(input)
        
        elif self.features['interface_name'] in ['rsome_ro', 'rsome_dro']:

            from rsome import exp
            return exp(input)
    
        else:

            return np.exp(input)

    def count(self, input, value):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.count(input, value)

        else:

            return input.count(value)

    def scal_prod(self, input1, input2):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.scal_prod(input1, input2)

        else:

            return np.dot(input1, input2)

    def range(self, x, lb=None, ub=None):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.range(x, lb, ub)

        else:

            return [x >= lb] + [x <= ub]

    def floor(self, x):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.floor(x)

        else:

            return np.floor(x)

    def ceil(self, x):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.ceil(x)

        else:

            return np.ceil(x)

    def round(self, x):

        if self.features['interface_name'] == 'cplex_cp':

            return self.model.round(x)

        else:

            return np.round(x)

# Alternatives for defining this class:

model = mdl = add_model = deterministic_model = certain_model = create_environment = env = feloopy = representor_model = learner_model = target_model = uncertain_target_model = uncertain_learner_model = uncertain_representor_model = optimizer = uncertain_model = stochastic_model = robust_model = possibilistic_model = Model

warnings.simplefilter(action='ignore', category=FutureWarning)

class Implement:

    def __init__(self, ModelFunction):
        '''
        Creates and returns an implementor for the representor model.
        '''

        self.model_data = ModelFunction(['idle'])
        self.ModelFunction = ModelFunction
        self.interface_name = self.model_data.features['interface_name']
        self.solution_method = self.model_data.features['solution_method']
        self.model_name = self.model_data.features['model_name']
        self.solver_name = self.model_data.features['solver_name']
        self.model_constraints = self.model_data.features['constraints']
        self.model_objectives = self.model_data.features['objectives']
        self.objectives_directions = self.model_data.features['directions']
        self.pos_var_counter = self.model_data.features['positive_variable_counter']
        self.bin_var_counter = self.model_data.features['binary_variable_counter']
        self.int_var_counter = self.model_data.features['integer_variable_counter']
        self.free_var_counter = self.model_data.features['free_variable_counter']
        self.tot_counter = self.model_data.features['total_variable_counter']
        self.con_counter = self.model_data.features['constraint_counter']
        self.obj_counter = self.model_data.features['objective_counter']
        self.AlgOptions = self.model_data.features['solver_options']
        self.VariablesSpread = self.model_data.features['variable_spread']
        self.VariablesType = self.model_data.features['variable_type']
        self.ObjectiveBeingOptimized = self.model_data.features['objective_being_optimized']
        self.VariablesBound = self.model_data.features['variable_bound']
        self.VariablesDim = self.model_data.features['variable_dim']
        self.status = 'Not solved'
        self.response = None
        self.AgentProperties = [None, None, None, None]
        self.get_objective = self.get_obj
        self.get_var = self.get_variable = self.get
        self.search = self.solve = self.optimize = self.run = self.sol

        match self.interface_name:

            case 'mealpy':

                from .generators.model import mealpy_model_generator
                self.ModelObject = mealpy_model_generator.generate_model(
                    self.solver_name, self.AlgOptions)

            case 'niapy':

                from .generators.model import niapy_model_generator
                self.ModelObject = niapy_model_generator.generate_model(
                    self.solver_name, self.AlgOptions)

            case 'pygad':

                self.ModelObject = None

            case 'pymultiobjective':

                self.ModelObject = None

            case 'pymoo':

                self.ModelObject = None

            case 'feloopy':

                from .generators.model import feloopy_model_generator
                self.ModelObject = feloopy_model_generator.generate_model(
                    self.tot_counter[1], self.objectives_directions, self.solver_name, self.AlgOptions)

    def remove_infeasible_solutions(self):

        self.BestAgent = np.delete(self.BestAgent, self.remove, axis=0)
        self.BestReward = np.delete(self.BestReward, self.remove, axis=0)

    def sol(self, penalty_coefficient=0, number_of_times=1, show_plots=False, save_plots=False, show_log=False):

        self.penalty_coefficient = penalty_coefficient

        match self.interface_name:

            case 'mealpy':

                from .generators.solution import mealpy_solution_generator
                self.BestAgent, self.BestReward, self.start, self.end = mealpy_solution_generator.generate_solution(
                    self.ModelObject, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, save_plots,show_log, self.AlgOptions)

            case 'niapy':

                from .generators.solution import niapy_solution_generator
                self.BestAgent, self.BestReward, self.start, self.end = niapy_solution_generator.generate_solution(
                    self.ModelObject, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, save_plots,show_log, self.AlgOptions)

            case 'pygad':

                from .generators.solution import pygad_solution_generator
                self.BestAgent, self.BestReward, self.start, self.end = pygad_solution_generator.generate_solution(
                    self.ModelObject, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, save_plots,show_log, self.AlgOptions)

            case 'pymultiobjective':

                from .generators.solution import pymultiobjective_solution_generator
                self.BestAgent, self.BestReward, self.start, self.end = pymultiobjective_solution_generator.generate_solution(
                    self.solver_name, self.AlgOptions, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, save_plots,show_log)
                self.remove = []

                for i in range(np.shape(self.BestReward)[0]):

                    if 'infeasible' in self.Check_Fitness(self.BestAgent[i]):

                        self.remove.append(i)

                if len(self.remove) != 0:
                    self.remove_infeasible_solutions()

            case 'pymoo':

                from .generators.solution import pymoo_solution_generator
                self.BestAgent, self.BestReward,self.start, self.end = pymoo_solution_generator.generate_solution(self.solver_name, self.AlgOptions, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, save_plots, show_log)
                self.remove = []

                for i in range(np.shape(self.BestReward)[0]):

                    if 'infeasible' in self.Check_Fitness(np.array([self.BestAgent[i]])):

                        self.remove.append(i)

                if len(self.remove) != 0:
                    self.remove_infeasible_solutions()
            
            case 'feloopy':

                from .generators.solution import feloopy_solution_generator
                self.BestAgent, self.BestReward, self.start, self.end, self.status = feloopy_solution_generator.generate_solution(
                    self.ModelObject, self.Fitness, self.tot_counter, self.objectives_directions, self.ObjectiveBeingOptimized, number_of_times, show_plots, show_log)

    def dis_plots(self, ideal_pareto: Optional[np.ndarray] = [], step: Optional[tuple] = (0.1,)):

        """
        Calculates selected Pareto front metrics and displays the results in a tabulated format.

        :param ideal_pareto: An array of shape (n_samples, n_objectives) containing the ideal Pareto front. Default is None.
        """

        obtained_pareto = self.BestReward

        try:
            from pyMultiobjective.util import graphs
        except:
            ""
        ObjectivesDirections = [-1 if direction =='max' else 1 for direction in self.objectives_directions]
        def f1(X): return ObjectivesDirections[0]*self.Fitness(np.array(X))[0]
        def f2(X): return ObjectivesDirections[1]*self.Fitness(np.array(X))[1]
        def f3(X): return ObjectivesDirections[2]*self.Fitness(np.array(X))[2]
        def f4(X): return ObjectivesDirections[3]*self.Fitness(np.array(X))[3]
        def f5(X): return ObjectivesDirections[4]*self.Fitness(np.array(X))[4]
        def f6(X): return ObjectivesDirections[5]*self.Fitness(np.array(X))[5]
        my_list_of_functions = [f1, f2, f3, f4, f5, f6]
        parameters = dict()
        list_of_functions = []
        for i in range(len(ObjectivesDirections)): list_of_functions.append(my_list_of_functions[i])
        
        solution = np.concatenate((self.BestAgent, self.BestReward*ObjectivesDirections), axis=1)
    
        parameters = {
        'min_values': (0,)*self.tot_counter[1],
        'max_values': (1,)*self.tot_counter[1],
        'step': step*self.tot_counter[1],
        'solution': solution, 
        'show_pf': True,
        'show_pts': True,
        'show_sol': True,
        'pf_min': True, 
        'custom_pf': ideal_pareto*ObjectivesDirections if type(ideal_pareto) == np.ndarray else [],
        'view': 'browser'
        }
        graphs.plot_mooa_function(list_of_functions = list_of_functions, **parameters)

        parameters = {
            'min_values': (0,)*self.tot_counter[1],
            'max_values': (1,)*self.tot_counter[1],
            'step': step*self.tot_counter[1],
            'solution': solution, 
            'show_pf': True,
            'pf_min': True,  
            'custom_pf': ideal_pareto*ObjectivesDirections if type(ideal_pareto) == np.ndarray else [],
            'view': 'browser'
        }
        graphs.parallel_plot(list_of_functions = list_of_functions, **parameters)

    def dis_status(self):
        print('status:', self.get_status())

    def get_status(self):

        if len(self.objectives_directions)==1:

            if self.interface_name in ['mealpy', 'niapy', 'pygad']:

                return self.Check_Fitness(self.BestAgent)
        
            else:

                if self.status[0] == 1:
                    return 'feasible (constrained)'
                elif self.status[0] == 2:
                    return 'feasible (unconstrained)'
                elif self.status[0] == -1:
                    return 'infeasible'

        else:

            status = []
            
            if self.interface_name in ['feloopy', 'pymoo']:

                for i in range(np.shape(self.BestReward)[0]):
                    status.append(self.Check_Fitness(np.array([self.BestAgent[i]])))

            else:

                for i in range(np.shape(self.BestReward)[0]):
                    status.append(self.Check_Fitness(self.BestAgent[i]))
            

            return status

    def Check_Fitness(self, X):

        self.AgentProperties[0] = 'feasibility_check'
        self.AgentProperties[1] = X
        self.AgentProperties[2] = self.VariablesSpread
        self.AgentProperties[3] = self.penalty_coefficient

        return self.ModelFunction(self.AgentProperties)

    def Fitness(self, X):

        self.AgentProperties[0] = 'active'
        self.AgentProperties[1] = X
        self.AgentProperties[2] = self.VariablesSpread
        self.AgentProperties[3] = self.penalty_coefficient

        return self.ModelFunction(self.AgentProperties)

    def evaluate(self, show_fig=True, save_fig=False, file_name=None, dpi=800, fig_size=(18, 4), opt=None, opt_features=None, pareto=None, abs_tol=0.001, rel_tol=0.001):

        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=fig_size)

        m = self.ModelObject.epsiode

        no_epochs = self.AlgOptions['epoch']
        no_episodes = self.AlgOptions['episode']

        max_epoch_time = []
        for epoch in range(0, no_epochs):
            episode_time = []
            for episode in range(0, no_episodes):
                episode_time.append(m[episode]['epoch_time'][epoch])
            max_epoch_time.append(np.max(episode_time))
        max_epoch_time = np.array(max_epoch_time)

        min_epoch_time = []
        for epoch in range(0, no_epochs):
            episode_time = []
            for episode in range(0, no_episodes):
                episode_time.append(m[episode]['epoch_time'][epoch])
            min_epoch_time.append(np.min(episode_time))
        min_epoch_time = np.array(min_epoch_time)

        ave_epoch_time = []
        for epoch in range(0, no_epochs):
            episode_time = []
            for episode in range(0, no_episodes):
                episode_time.append(m[episode]['epoch_time'][epoch])
            ave_epoch_time.append(np.average(episode_time))
        ave_epoch_time = np.array(ave_epoch_time)

        std_epoch_time = []
        for epoch in range(0, no_epochs):
            episode_time = []
            for episode in range(0, no_episodes):
                episode_time.append(m[episode]['epoch_time'][epoch])
            std_epoch_time.append(np.std(episode_time))
        std_epoch_time = np.array(std_epoch_time)

        axs = fig.add_subplot(1, 5, 5)
        x = np.arange(no_epochs)
        axs.plot(x, max_epoch_time, 'blue', alpha=0.4)
        axs.plot(x, ave_epoch_time, 'blue', alpha=0.8)
        axs.plot(x, min_epoch_time, 'blue', alpha=0.4)
        axs.fill_between(x, ave_epoch_time - std_epoch_time,
                         ave_epoch_time + std_epoch_time, color='blue', alpha=0.3)
        axs.set_xlabel('Epoch')
        axs.set_ylabel('Time (second)')
        axs.set_xlim(-0.5, no_epochs-1+0.5)

        max_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
            max_epoch_obj.append(np.max(max_episode_obj))
        max_epoch_obj = np.array(max_epoch_obj)

        min_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
            min_epoch_obj.append(np.min(max_episode_obj))
        min_epoch_obj = np.array(min_epoch_obj)

        ave_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
            ave_epoch_obj.append(np.average(max_episode_obj))
        ave_epoch_obj = np.array(ave_epoch_obj)

        std_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
            std_epoch_obj.append(np.std(max_episode_obj))
        std_epoch_obj = np.array(std_epoch_obj)

        axs = fig.add_subplot(1, 5, 4)
        x = np.arange(no_epochs)
        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'max':
            axs.plot(x, max_epoch_obj, 'green', alpha=0.4)
            axs.plot(x, ave_epoch_obj, 'green', alpha=0.8)
            axs.plot(x, min_epoch_obj, 'green', alpha=0.4)
            axs.fill_between(x, ave_epoch_obj - std_epoch_obj,
                             ave_epoch_obj + std_epoch_obj, color='green', alpha=0.3)
        else:
            axs.plot(x, max_epoch_obj, 'red', alpha=0.4)
            axs.plot(x, ave_epoch_obj, 'red', alpha=0.8)
            axs.plot(x, min_epoch_obj, 'red', alpha=0.4)

            axs.fill_between(x, ave_epoch_obj - std_epoch_obj,
                             ave_epoch_obj + std_epoch_obj, color='red', alpha=0.3)
        axs.set_xlabel('Epoch')
        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'max':
            axs.set_ylabel('Maximum reward')
        else:
            axs.set_ylabel('Maximum loss')
        axs.set_xlim(-0.5, no_epochs-1+0.5)

        max_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(np.average(
                    m[episode]['epoch_solutions'][epoch][:, -1]))
            max_epoch_obj.append(np.max(max_episode_obj))
        max_epoch_obj = np.array(max_epoch_obj)

        min_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(np.average(
                    m[episode]['epoch_solutions'][epoch][:, -1]))
            min_epoch_obj.append(np.min(max_episode_obj))
        min_epoch_obj = np.array(min_epoch_obj)

        ave_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(np.average(
                    m[episode]['epoch_solutions'][epoch][:, -1]))
            ave_epoch_obj.append(np.average(max_episode_obj))
        ave_epoch_obj = np.array(ave_epoch_obj)

        std_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(np.average(
                    m[episode]['epoch_solutions'][epoch][:, -1]))
            std_epoch_obj.append(np.std(max_episode_obj))
        std_epoch_obj = np.array(std_epoch_obj)

        axs = fig.add_subplot(1, 5, 3)
        x = np.arange(no_epochs)
        axs.plot(x, max_epoch_obj, 'orange', alpha=0.4)
        axs.plot(x, ave_epoch_obj, 'orange', alpha=0.8)
        axs.plot(x, min_epoch_obj, 'orange', alpha=0.4)
        axs.fill_between(x, ave_epoch_obj - std_epoch_obj,
                         ave_epoch_obj + std_epoch_obj, color='orange', alpha=0.3)
        axs.set_xlabel('Epoch')
        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'max':
            axs.set_ylabel('Average reward')
        else:
            axs.set_ylabel('Average loss')
        axs.set_xlim(-0.5, no_epochs-1+0.5)

        max_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
            max_epoch_obj.append(np.max(max_episode_obj))
        max_epoch_obj = np.array(max_epoch_obj)

        min_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
            min_epoch_obj.append(np.min(max_episode_obj))
        min_epoch_obj = np.array(min_epoch_obj)

        ave_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
            ave_epoch_obj.append(np.average(max_episode_obj))
        ave_epoch_obj = np.array(ave_epoch_obj)

        std_epoch_obj = []
        for epoch in range(0, no_epochs):
            max_episode_obj = []
            for episode in range(0, no_episodes):
                max_episode_obj.append(
                    np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
            std_epoch_obj.append(np.std(max_episode_obj))
        std_epoch_obj = np.array(std_epoch_obj)

        axs = fig.add_subplot(1, 5, 2)
        x = np.arange(no_epochs)
        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'max':
            axs.plot(x, max_epoch_obj, 'red', alpha=0.4)
            axs.plot(x, ave_epoch_obj, 'red', alpha=0.8)
            axs.plot(x, min_epoch_obj, 'red', alpha=0.4)
            axs.fill_between(x, ave_epoch_obj - std_epoch_obj,
                             ave_epoch_obj + std_epoch_obj, color='red', alpha=0.3)
        else:
            axs.plot(x, max_epoch_obj, 'green', alpha=0.4)
            axs.plot(x, ave_epoch_obj, 'green', alpha=0.8)
            axs.plot(x, min_epoch_obj, 'green', alpha=0.4)
            axs.fill_between(x, ave_epoch_obj - std_epoch_obj,
                             ave_epoch_obj + std_epoch_obj, color='green', alpha=0.3)
        axs.set_xlabel('Epoch')
        axs.set_xlim(-0.5, no_epochs-1+0.5)
        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'max':
            axs.set_ylabel('Minimum reward')
        else:
            axs.set_ylabel('Minimum loss')

        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'min':
            best_min_min = np.inf
            best_min_min_t = []
            best_sol_t = []
            best_per_episode = []
            no_features = self.tot_counter[1]
            for epoch in range(0, no_epochs):
                best_min = []
                best_sol = []
                for episode in range(0, no_episodes):
                    best_min.append(
                        np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
                    best_sol.append(m[episode]['epoch_solutions'][epoch][np.argmin(
                        m[episode]['epoch_solutions'][epoch][:, -1]), :])
                    best_track = np.min(best_min)
                    for x in best_sol:
                        if x[-1] == best_track:
                            best_sol_found = x[:no_features]
                if best_track <= best_min_min:
                    best_min_min = best_track
                    best_min_min_t.append(best_track)
                    if no_features == 1:
                        best_sol_t.append(best_sol_found[0])
                    if no_features == 2:
                        best_sol_t.append(
                            [best_sol_found[0], best_sol_found[1]])
                    else:
                        best_sol_t.append(
                            [best_sol_found[0], best_sol_found[1], best_sol_found[2]])
                else:
                    best_min_min_t.append(best_min_min)
                    best_sol_t.append(best_sol_t[-1])

                    if epoch == no_epochs-1:
                        best_per_episode.append(best_track)

            best_min_min_t = np.array(best_min_min_t)
        else:
            best_min_min = -np.inf
            best_min_min_t = []
            best_sol_t = []
            best_per_episode = []
            no_features = self.tot_counter[1]
            for epoch in range(0, no_epochs):
                best_min = []
                best_sol = []
                for episode in range(0, no_episodes):
                    best_min.append(
                        np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
                    best_sol.append(m[episode]['epoch_solutions'][epoch][np.argmax(
                        m[episode]['epoch_solutions'][epoch][:, -1]), :])
                    best_track = np.max(best_min)
                    for x in best_sol:
                        if x[-1] == best_track:
                            best_sol_found = x[:no_features]
                if best_track >= best_min_min:
                    best_min_min = best_track
                    best_min_min_t.append(best_track)
                    if no_features == 1:
                        best_sol_t.append(best_sol_found[0])
                    if no_features == 2:
                        best_sol_t.append(
                            [best_sol_found[0], best_sol_found[1]])
                    else:
                        best_sol_t.append(
                            [best_sol_found[0], best_sol_found[1], best_sol_found[2]])
                else:
                    best_min_min_t.append(best_min_min)
                    best_sol_t.append(best_sol_t[-1])

                    if epoch == no_epochs-1:
                        best_per_episode.append(best_track)

            best_min_min_t = np.array(best_min_min_t)

        if no_features == 1:
            axs = fig.add_subplot(1, 5, 1)
            axs.plot(np.arange(no_epochs), best_sol_t, c='black', lw=1)
            if opt_features != None:
                axs.scatter(np.arange(no_epochs),
                            opt_features[0], c='black', marker='*', lw=1)

            axs.set_ylim(-0.5, 1.5)
            axs.set_xlim(-0.5, no_epochs-1+0.5)
            axs.set_xlabel('Epoch')
            axs.set_ylabel('Feature')

        if no_features == 2:
            axs = fig.add_subplot(1, 5, 1)
            from matplotlib.patches import Rectangle
            for i in range(0, no_epochs):
                hg = 0.1+i/(no_epochs)
                axs.scatter(best_sol_t[i][0], best_sol_t[i]
                            [1], c='black', lw=1, alpha=hg)
            if opt_features != None:
                axs.scatter(opt_features[0], opt_features[1],
                            c='black', marker='*', lw=1)

            axs.add_patch(Rectangle((0, 0), 1, 1, fill=None, alpha=1))

            axs.set_ylim(-0.5, 1.5)
            axs.set_xlim(-0.5, 1.5)
            axs.set_xlabel('Feature 1')
            axs.set_ylabel('Feature 2')

        if no_features == 3:
            axs = fig.add_subplot(1, 5, 1, projection='3d')
            for i in range(0, no_epochs):
                hg = 0.1+i/(no_epochs)
                axs.scatter(best_sol_t[i][0], best_sol_t[i][1],
                            best_sol_t[i][2], lw=1, alpha=hg, color='black')
            if opt_features != None:
                axs.scatter(opt_features[0], opt_features[1],
                            opt_features[2], c='red', marker='*', lw=1)
            axs.set_xlabel('Feature 1')
            axs.set_ylabel('Feature 2')
            axs.set_zlabel('Feature 3')
            axs.set_ylim(-0.5, 1.5)
            axs.set_xlim(-0.5, 1.5)
            axs.set_zlim(-0.5, 1.5)

            axs.view_init(azim=30)

        if no_features <= 2:
            plt.subplots_adjust(left=0.071, bottom=0.217,
                                right=0.943, top=0.886, wspace=0.35, hspace=0.207)
        else:
            plt.subplots_adjust(left=0.03, bottom=0.252,
                                right=0.945, top=0.886, wspace=0.421, hspace=0.22)

        if save_fig:
            if file_name == None:
                plt.savefig('evaluation_results.png', dpi=dpi)
            else:
                plt.savefig(file_name, dpi=dpi)

        if show_fig:
            plt.show()

        obj = []
        time = []
        for episode in range(0, no_episodes):
            obj.append(m[episode]['best_single'][0][-1])
            time.append(m[episode]['episode_time'][0])

        opt = np.array([opt])
        if opt != 0:
            accuracy = (1-np.abs(opt-best_min_min_t)/opt)*100
        else:
            opt = opt + 1
            best_min_min_t = best_min_min_t+1
            accuracy = (1-np.abs(opt-best_min_min_t)/opt)*100
            accuracy[np.where(accuracy < 0)] = 0

        from math import isclose

        opt = np.array([opt])
        prob_per_epoch = []

        findbest = np.zeros(shape=(no_episodes, no_epochs))

        if self.objectives_directions[self.ObjectiveBeingOptimized] == 'min':
            for episode in range(0, no_episodes):
                episode_tracker = []
                best = np.inf
                for epoch in range(0, no_epochs):
                    if np.min(m[episode]['epoch_solutions'][epoch][:, -1]) <= best:
                        best = np.min(
                            m[episode]['epoch_solutions'][epoch][:, -1])
                        episode_tracker.append(
                            np.min(m[episode]['epoch_solutions'][epoch][:, -1]))
                    else:
                        episode_tracker.append(best)
                for epoch in range(0, no_epochs):
                    if opt == 0:
                        if isclose(episode_tracker[epoch], opt, abs_tol=abs_tol):
                            findbest[episode, epoch] = 1
                    else:
                        if isclose(episode_tracker[epoch], opt, rel_tol=rel_tol):
                            findbest[episode, epoch] = 1
        else:
            for episode in range(0, no_episodes):
                episode_tracker = []
                best = -np.inf
                for epoch in range(0, no_epochs):
                    if np.max(m[episode]['epoch_solutions'][epoch][:, -1]) >= best:
                        best = np.max(
                            m[episode]['epoch_solutions'][epoch][:, -1])
                        episode_tracker.append(
                            np.max(m[episode]['epoch_solutions'][epoch][:, -1]))
                    else:
                        episode_tracker.append(best)
                for epoch in range(0, no_epochs):
                    if opt == 0:
                        if isclose(episode_tracker[epoch], opt, abs_tol=abs_tol, rel_tol=rel_tol):
                            findbest[episode, epoch] = 1
                    else:
                        if isclose(episode_tracker[epoch], opt, abs_tol=abs_tol, rel_tol=rel_tol):
                            findbest[episode, epoch] = 1

        # abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

        prob_per_epoch = [sum(findbest[episode, epoch] for episode in range(
            0, no_episodes))/no_episodes for epoch in range(0, no_epochs)]

        return [obj, time, accuracy, prob_per_epoch]

    def get(self, *args):
        if self.obj_counter[0] == 1:
            match self.interface_name:
                case _ if self.interface_name in ['mealpy', 'niapy', 'pygad']:
                    for i in args:
                        if len(i) >= 2:
                            match self.VariablesType[i[0]]:
                                case 'pvar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])
                                case 'fvar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])
                                case 'bvar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])
                                case 'ivar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])
                                case 'svar':
                                    return np.argsort(self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])[i[1]]

                        else:
                            match self.VariablesType[i[0]]:
                                case 'pvar':
                                    return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                case 'fvar':
                                    return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                case 'bvar':
                                    return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                case 'ivar':
                                    return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))[0]
                                case 'svar':
                                    return np.argsort(self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])
                case 'feloopy':
                    for i in args:
                        if len(i) >= 2:
                            match self.VariablesType[i[0]]:
                                case 'pvar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])
                                case 'fvar':

                                    if self.VariablesDim[i[0]] == 0:
                                        return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]

                                        return var(*i[1])

                                case 'bvar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]

                                        return var(*i[1])
                                case 'ivar':
                                    if self.VariablesDim[i[0]] == 0:
                                        return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                                    else:
                                        def var(*args):
                                            self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                                self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                            return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                        return var(*i[1])

                                case 'svar':
                                    return np.argsort(self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])[i[1]]

                        else:
                            match self.VariablesType[i[0]]:

                                case 'pvar':
                                    return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                case 'fvar':
                                    return (self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                case 'bvar':
                                    return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                case 'ivar':
                                    return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                case 'svar':
                                    return np.argsort(self.BestAgent[self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])
        else:

            for i in args:
                if len(i) >= 2:

                    match self.VariablesType[i[0]]:

                        case 'pvar':

                            if self.VariablesDim[i[0]] == 0:
                                return (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                            else:
                                def var(*args):
                                    self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                        self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                    return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]

                                return var(*i[1])

                        case 'fvar':
                            if self.VariablesDim[i[0]] == 0:
                                return (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                            else:
                                def var(*args):
                                    self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                        self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                    return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]

                                return var(*i[1])

                        case 'bvar':
                            if self.VariablesDim[i[0]] == 0:
                                return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))

                            else:
                                def var(*args):
                                    self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                        self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                    return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]

                                return var(*i[1])
                        case 'ivar':
                            if self.VariablesDim[i[0]] == 0:
                                return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                            else:
                                def var(*args):
                                    self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                        self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                    return self.NewAgentProperties[sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                                return var(*i[1])

                        case 'svar':

                            return np.argsort(self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])[i[1]]

                else:

                    match self.VariablesType[i[0]]:
                        case 'pvar':
                            return (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        case 'fvar':
                            return (self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        case 'bvar':
                            return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        case 'ivar':
                            return np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        case 'svar':
                            return np.argsort(self.BestAgent[:, self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])

    def dis_indicators(self, ideal_pareto: Optional[np.ndarray] = [], ideal_point: Optional[np.array] = [], step: Optional[tuple] = (0.1,), epsilon: float = 0.01, p: float = 2.0, n_clusters: int = 5, save_path: Optional[str] = None, show_log: Optional[bool] = False):

        """
        Calculates selected Pareto front metrics and displays the results in a tabulated format.

        :param ideal_pareto: An array of shape (n_samples, n_objectives) containing the ideal Pareto front. Default is None.
        :param epsilon: A float value for the epsilon value used in the epsilon metric. Default is 0.01.
        :param p: A float value for the power parameter used in the weighted generational distance and weighted inverted generational distance metrics. Default is 2.0.
        :param n_clusters: An integer value for the number of clusters used in the knee point distance metric. Default is 5.
        :param save_path: A string value for the path where the results should be saved. Default is None.
        """


        self.get_indicators(ideal_pareto, ideal_point, step, epsilon, p, n_clusters, save_path, show_log = True)

    def get_indicators(self, ideal_pareto: Optional[np.ndarray] = [], ideal_point: Optional[np.array] = [], step: Optional[tuple] = (0.2,), epsilon: float = 0.01, p: float = 2.0, n_clusters: int = 5, save_path: Optional[str] = None, show_log: Optional[bool] = False, normalize_hv: Optional[bool] = False, bypass_limit=False):

        """
        Calculates selected Pareto front metrics and displays the results in a tabulated format.

        :param ideal_pareto: An array of shape (n_samples, n_objectives) containing the ideal Pareto front. Default is None.
        :param epsilon: A float value for the epsilon value used in the epsilon metric. Default is 0.01.
        :param p: A float value for the power parameter used in the weighted generational distance and weighted inverted generational distance metrics. Default is 2.0.
        :param n_clusters: An integer value for the number of clusters used in the knee point distance metric. Default is 5.
        :param save_path: A string value for the path where the results should be saved. Default is None.
        """
        if len(self.get_obj())!=0:

            obtained_pareto = self.BestReward
            try:
                from pyMultiobjective.util import indicators
            except:
                ""

            ObjectivesDirections = [-1 if direction =='max' else 1 for direction in self.objectives_directions]

            def f1(X): return ObjectivesDirections[0]*self.Fitness(np.array(X))[0]
            def f2(X): return ObjectivesDirections[1]*self.Fitness(np.array(X))[1]
            def f3(X): return ObjectivesDirections[2]*self.Fitness(np.array(X))[2]
            def f4(X): return ObjectivesDirections[3]*self.Fitness(np.array(X))[3]
            def f5(X): return ObjectivesDirections[4]*self.Fitness(np.array(X))[4]
            def f6(X): return ObjectivesDirections[5]*self.Fitness(np.array(X))[5]

            list_of_functions = [f1, f2, f3, f4, f5, f6]

            solution = np.concatenate((self.BestAgent, self.BestReward*ObjectivesDirections), axis=1)
            self.calculated_indicators = dict()

            #Does not require the ideal_pareto
            parameters = {
                'solution': solution,
                'n_objs': len(ObjectivesDirections),
                'ref_point': ideal_point,
                'normalize': normalize_hv
            }
            hypervolume = indicators.hv_indicator(**parameters)
            self.calculated_indicators['hv'] = hypervolume

            parameters = {
                'min_values': (0,)*self.tot_counter[1],
                'max_values': (1,)*self.tot_counter[1],
                'step': step*self.tot_counter[1],
                'solution': solution,
                'pf_min': True,
                'custom_pf': ideal_pareto*ObjectivesDirections if type(ideal_pareto) == np.ndarray else []
            }

            sp = indicators.sp_indicator(list_of_functions=list_of_functions, **parameters)
            self.calculated_indicators['sp'] = sp

            #Computationally efficient only if ideal_pareto exists
            if self.tot_counter[1]<=3 or ideal_pareto != [] or bypass_limit:
                gd = indicators.gd_indicator(list_of_functions=list_of_functions, **parameters)
                gdp = indicators.gd_plus_indicator(list_of_functions=list_of_functions, **parameters)
                igd = indicators.igd_indicator(list_of_functions=list_of_functions, **parameters)
                igdp = indicators.igd_plus_indicator(list_of_functions=list_of_functions, **parameters)
                ms = indicators.ms_indicator(list_of_functions=list_of_functions, **parameters)
                self.calculated_indicators['gd'] = gd
                self.calculated_indicators['gdp'] = gdp
                self.calculated_indicators['igd'] = igd
                self.calculated_indicators['igdp'] = igdp
                self.calculated_indicators['ms'] = ms

            return self.calculated_indicators

    def dis_time(self):

        hour = round(((self.end-self.start)), 3) % (24 * 3600) // 3600
        min = round(((self.end-self.start)), 3) % (24 * 3600) % 3600 // 60
        sec = round(((self.end-self.start)), 3) % (24 * 3600) % 3600 % 60

        print(f"cpu time [{self.interface_name}]: ", (self.end-self.start)*10 **
              6, '(microseconds)', "%02d:%02d:%02d" % (hour, min, sec), '(h, m, s)')
  
    def get_time(self):
        """

        Used to get solution time in seconds.


        """

        return self.end-self.start

    def get_obj(self):
        return self.BestReward

    def dis(self, input):
        if len(input) >= 2:
            print(input[0]+str(input[1])+': ', self.get(input))
        else:
            print(str(input[0])+': ', self.get(input))

    def dis_obj(self):
        print('objective: ', self.BestReward)

    def get_bound(self, *args):

        for i in args:

            if len(i) >= 2:
            
                match self.VariablesType[i[0]]:

                    case 'pvar':

                        if self.VariablesDim[i[0]] == 0:
                            UB = np.max((self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            LB = np.min((self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            return [LB,UB]

                        else:
                            def var(*args):
                                self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                    self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                return self.NewAgentProperties[:,sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                            return [np.min(var(*i[1])),np.max(var(*i[1]))]

                    case 'fvar':

                        if self.VariablesDim[i[0]] == 0:
                            LB = np.min(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                            UB = np.max(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                            return [LB,UB]

                        else:
                            def var(*args):
                                self.NewAgentProperties = (self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                    self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                return self.NewAgentProperties[:,sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                            return [np.min(var(*i[1])),np.max(var(*i[1]))]

                    case 'bvar':
                        if self.VariablesDim[i[0]] == 0:
                            LB = np.min(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            UB = np.max(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            return [LB,UB]

                        else:
                            def var(*args):
                                self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                    self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                return self.NewAgentProperties[:,sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                            return [np.min(var(*i[1])),np.max(var(*i[1]))]
                        
                    case 'ivar':
                        if self.VariablesDim[i[0]] == 0:
                            LB = np.min(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            UB = np.min(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                            return [LB,UB]

                        else:
                            def var(*args):
                                self.NewAgentProperties = np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (
                                    self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                                return self.NewAgentProperties[:,sum(args[k]*mt.prod(len(self.VariablesDim[i[0]][j]) for j in range(k+1, len(self.VariablesDim[i[0]]))) for k in range(len(self.VariablesDim[i[0]])))]
                            return [np.min(var(*i[1])),np.max(var(*i[1]))]
                        
                    case 'svar':
                        return np.argsort(self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])[i[1]]

            else:

                match self.VariablesType[i[0]]:

                    case 'pvar':
                        UB = np.max((self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        LB = np.min((self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        return [LB,UB]

                    case 'fvar':
                        UB = np.max(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        LB = np.min(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0]))
                        return [LB,UB]

                    case 'bvar':
                        UB = np.max(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        LB = np.min(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        return [LB,UB]

                    case 'ivar':
                        UB = np.max(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        LB= np.min(np.round(self.VariablesBound[i[0]][0] + self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]] * (self.VariablesBound[i[0]][1] - self.VariablesBound[i[0]][0])))
                        return [UB,LB]

                    case 'svar':
                        return np.argsort(self.BestAgent[:,self.VariablesSpread[i[0]][0]:self.VariablesSpread[i[0]][1]])
                    
    def get_payoff(self):

        payoff=[]
        for i in range(len(self.objectives_directions)):
            if self.objectives_directions[i]=='max':
                ind =np.argmax(self.get_obj()[:, i])
                val = self.get_obj()[ind, :]
            elif self.objectives_directions[i] =='min':
                ind = np.argmin(self.get_obj()[:, i])
                val = self.get_obj()[ind, :]
            payoff.append(val)
        return np.array(payoff)

    def report(self, all_metrics: bool = False, feloopy_info: bool = True, sys_info: bool = False, model_info: bool = True, sol_info: bool = True, obj_values: bool = True, dec_info: bool = True, metric_info: bool = True, ideal_pareto: Optional[np.ndarray] = [], ideal_point: Optional[np.array] = [], show_tensors = False, show_detailed_tensors=False, save=None):

        if not self.healthy():
            print()
            print()
            print('WARNING: Model is not healthy!')
            print()
            print()
            
        if save is not None:
            stdout_origin = sys.stdout
            sys.stdout = open(save, "w")

        status = self.get_status()
        hour, min, sec = calculate_time_difference(self.start,self.end)

        if len(str(status)) == 0:
            status = ['infeasible (constrained)']

        box_width = 80
        vspace()

        if feloopy_info:
            
            import datetime
            now = datetime.datetime.now()
            date_str = now.strftime("Date: %Y-%m-%d")
            time_str = now.strftime("Time: %H:%M:%S")
            tline_text("FelooPy v0.2.8")
            empty_line()
            two_column(date_str, time_str)
            two_column(f"Interface: {self.interface_name}", f"Solver: {self.solver_name}")
            empty_line()
            bline()

        if sys_info:
            try:
                import psutil
                import cpuinfo
                import platform
                tline_text("System")
                empty_line()
                cpu_info = cpuinfo.get_cpu_info()["brand_raw"]
                cpu_cores = psutil.cpu_count(logical=False)
                cpu_threads = psutil.cpu_count(logical=True)
                ram_info = psutil.virtual_memory()
                ram_total = ram_info.total
                os_info = platform.system()
                os_version = platform.version()
                left_align(f"OS: {os_version} ({os_info})")
                left_align(f"CPU   Model: {cpu_info}")
                left_align(f"CPU   Cores: {cpu_cores}")
                left_align(f"CPU Threads: {cpu_threads}")
                try:
                    import GPUtil
                    gpus = GPUtil.getGPUs()
                    for gpu in gpus:
                        left_align(f"GPU   Model: {gpu.name}")
                        left_align(f"GPU    VRAM: {gpu.memoryTotal / 1024:.2f} GB")
                except:
                    pass
                left_align(f"SYSTEM  RAM: {ram_total / (1024 ** 3):.2f} GB")
            except:
                pass
            empty_line()
            bline()

        if model_info:
            tline_text("Model")
            empty_line()
            left_align(f"Name: {self.model_name}")
            list_three_column([
                ("Feature:         ", "Class:", "Total:"),
                ("Positive variable", self.pos_var_counter[0], self.pos_var_counter[1]),
                ("Binary variable  ", self.bin_var_counter[0], self.bin_var_counter[1]),
                ("Integer variable ", self.int_var_counter[0], self.int_var_counter[1]),
                ("Free variable    ", self.free_var_counter[0], self.free_var_counter[1]), 
                ("Total variables  ", self.tot_counter[0], self.tot_counter[1]), 
                ("Objective        ", "-", self.obj_counter[1]), 
                ("Constraint       ", self.con_counter[0], self.con_counter[1]) ])
            empty_line()
            bline()

        if sol_info:
            tline_text("Solve")
            empty_line()
            two_column(f"Method: {self.solution_method}", "Objective value")
            status_row_print(self.objectives_directions, status)
            if obj_values:
                if len(self.objectives_directions) != 1:
                    try:
                        solution_print(self.objectives_directions, status, self.get_obj(), self.get_payoff())
                    except:
                        left_align("Nothing found.")
                else:
                    solution_print(self.objectives_directions, status, self.get_obj())
            empty_line()
            bline()

        if metric_info:
            tline_text("Metric")
            empty_line()
            self.calculated_indicators = None
            try:
                self.get_indicators(ideal_pareto=ideal_pareto, ideal_point=ideal_point)
            except:
                pass
            metrics_print(self.objectives_directions, all_metrics, self.get_obj(), self.calculated_indicators, self.start, self.end)
            empty_line()
            bline()

        if dec_info:
            tline_text("Decision")
            empty_line()
            self.decision_information_print(status,show_tensors, show_detailed_tensors)
            empty_line()
            bline()

        if save is not None:
            sys.stdout.close()
            sys.stdout = stdout_origin

    def get_numpy_var(self, var_name):

        for i in self.VariablesDim.keys():
            if i==var_name:

                if self.VariablesDim[i] == 0:

                    output = self.get([i, (0,)])

                elif len(self.VariablesDim[i]) == 1:

                    output = np.zeros(shape=len(fix_dims(self.VariablesDim[i])[0]))

                    for k in fix_dims(self.VariablesDim[i])[0]:
                        
                        output[k] = self.get([i, (k,)])

                else:
                    output = np.zeros(shape=tuple([len(dim) for dim in fix_dims(self.VariablesDim[i])]))
                    for k in it.product(*tuple(fix_dims(self.VariablesDim[i]))):

                        output[k] = self.get([i, (*k,)])

        return output

    def healthy(self):
        try:
            status = self.get_status().lower()
            return ('optimal' in status or 'feasible' in status) and 'infeasible' not in status
        except:
            status = self.get_status()[0].lower()
            return ('feasible' in status or 'optimal' in status) and 'infeasible' not in status
        
    def decision_information_print(self, status, show_tensors, show_detailed_tensors, box_width=80):
        
        
        if show_detailed_tensors: show_tensors=True
        
        if not show_tensors:
        
            if type(status) == str:
                for i in self.VariablesDim.keys():
                    if self.VariablesDim[i] == 0:
                        if self.get([i, (0,)]) != 0:
                            print(f"│ {i} =", self.get([i, (0,)]), " " * (box_width - (len(f"│ {i} =") + len(str(self.get([i, (0,)])))) - 1) + "│")

                    elif len(self.VariablesDim[i]) == 1:
                        for k in fix_dims(self.VariablesDim[i])[0]:
                            if self.get([i, (k,)]) != 0:
                                print(f"│ {i}[{k}] =", self.get([i, (k,)]), " " * (box_width - (len(f"│ {i}[{k}] =") + len(str(self.get([i, (k,)])))) - 1) + "│")
                    else:
                        for k in it.product(*tuple(fix_dims(self.VariablesDim[i]))):
                            if self.get([i, (*k,)]) != 0:
                                print(f"│ {i}[{k}] =".replace("(", "").replace(")", ""), self.get([i, (*k,)]), " " * (box_width - (len(f"│ {i}[{k}] =".replace("(", "").replace(")", "")) + len(str(self.get([i, (*k,)])))) - 1) + "│")
            else:
                for i in self.VariablesDim.keys():
                    if self.VariablesDim[i] == 0:
                        if self.get_bound([i, (0,)])!=[0,0]:
                            print(f"│ {i} =", self.get_bound([i, (0,)]), " " * (box_width - (len(f"│ {i} =") + len(str(self.get_bound([i, (0,)])))) - 1) + "│")
                    elif len(self.VariablesDim[i]) == 1:
                        for k in fix_dims(self.VariablesDim[i])[0]:
                            if self.get_bound([i, (k,)])!= [0,0]:
                                print(f"│ {i}[{k}] =", self.get_bound([i, (k,)]), " " * (box_width - (len(f"│ {i}[{k}] =") + len(str(self.get_bound([i, (k,)])))) - 1) + "│")
                    else:
                        for k in it.product(*tuple(fix_dims(self.VariablesDim[i]))):
                            if self.get_bound([i, (*k,)]) != [0,0]:
                                print(f"│ {i}[{k}] =".replace("(", "").replace(")", ""), self.get_bound([i, (*k,)]), " " * (box_width - (len(f"│ {i}[{k}] =".replace("(", "").replace(")", "")) + len(str(self.get_bound([i, (*k,)])))) - 1) + "│")
    
        else:
        
            if show_detailed_tensors: np.set_printoptions(threshold=np.inf)
            
            for i in self.VariablesDim.keys():
                
                if type(status) == str:
    
                    numpy_var = self.get_numpy_var(i) 

                    if type(numpy_var)==np.ndarray:

                        numpy_str = np.array2string(numpy_var, separator=', ', prefix='│ ', style=str)
                        rows = numpy_str.split('\n')
                        first_row_len = len(rows[0])
                        for i, row in enumerate(rows):
                            if i == 0:
                                left_align(f"{i} = {row}")
                            else:
                                left_align(" "*(len(f"{i} =")-1)+row)
                    else:
                        left_align(f"{i} = {numpy_var}")
                                            
# Alternatives for defining this class:
            
construct = make_model = implementor = implement = Implement


WEIGHTING_ALGORITHMS = [
    ['ahp_method','pydecision'],
    ['fuzzy_ahp_method','pydecision'],
    ['bw_method','pydecision'],
    ['fuzzy_bw_method','pydecision'],
    ['cilos_method', 'pydecision'],
    ['critic_method', 'pydecision'],
    ['entropy_method', 'pydecision'],
    ['idocriw_method', 'pydecision'],
    ['merec_method', 'pydecision'],
    ['lp_method', 'feloopy'],
    ]

RANKING_ALGORITHMS = [
    ['aras_method', 'pydecision'],
    ['fuzzy_aras_method', 'pydecision'],
    ['borda_method', 'pydecision'],
    ['cocoso_method', 'pydecision'],
    ['codas_method', 'pydecision'],
    ['copeland_method', 'pydecision'],
    ['copras_method', 'pydecision'],
    ['fuzzy_copras_method', 'pydecision'],
    ['cradis_method', 'pydecision'],
    ['edas_method', 'pydecision'],
    ['fuzzy_edas_method', 'pydecision'],
    ['gra_method', 'pydecision'],
    ['mabac_method', 'pydecision'],
    ['macbeth_method', 'pydecision'],
    ['mairca_method', 'pydecision'],
    ['marcos_method', 'pydecision'],
    ['maut_method', 'pydecision'],
    ['moora_method', 'pydecision'],
    ['fuzzy_moora_method', 'pydecision'],
    ['moosra_method', 'pydecision'],
    ['multimoora_method', 'pydecision'],
    ['ocra_method', 'pydecision'],
    ['fuzzy_ocra_method', 'pydecision'],
    ['oreste_method', 'pydecision'],
    ['piv_method', 'pydecision'],
    ['promethee_ii', 'pydecision'],
    ['promethee_iv', 'pydecision'],
    ['promethee_vi', 'pydecision'],
    ['psi_method', 'pydecision'],
    ['regime_method', 'pydecision'],
    ['rov_method', 'pydecision'],
    ['saw_method', 'pydecision'],
    ['smart_method', 'pydecision'],
    ['spotis_method', 'pydecision'],
    ['todim_method', 'pydecision'],
    ['topsis_method', 'pydecision'],
    ['fuzzy_topsis_method', 'pydecision'],
    ['vikor_method', 'pydecision'],
    ['fuzzy_vikor_method', 'pydecision'],
    ['waspas_method', 'pydecision'],
    ['fuzzy_waspas_method', 'pydecision'],
    ['la_method', 'feloopy'],
    ]

SPECIAL_ALGORITHMS = [
    ['dematel_method', 'pydecision'],
    ['fuzzy_dematel_method', 'pydecision'],
    ['electre_i', 'pydecision'],
    ['electre_i_s', 'pydecision'],
    ['electre_i_v', 'pydecision'],
    ['electre_ii', 'pydecision'],
    ['electre_iii', 'pydecision'],
    ['electre_iv', 'pydecision'],
    ['electre_tri_b', 'pydecision'],
    ['promethee_i', 'pydecision'],
    ['promethee_iii', 'pydecision'],
    ['promethee_v', 'pydecision'],
    ['promethee_gaia', 'pydecision'],
    ['wings_method', 'pydecision'],
    ['cwdea_method', 'feloopy']
]

# Missing: SWOT, BOCR, ANP

class MADM:

    def __init__(self, solution_method, problem_name, interface_name):
        """
        Initializes an instance of MADM.

        Parameters:
        solution_method (str): The solution method to use.
        problem_name (str): The name of the problem.
        interface_name (str): The name of the interface.

        Returns:
        None
        """
        self.model_name = problem_name
        self.interface_name = 'pyDecision.algorithm' if interface_name == 'pydecision' else interface_name
        self.madam_method = solution_method

        if self.interface_name == 'pyDecision.algorithm':
            if "_method" not in solution_method and 'auto' not in solution_method and 'electre' not in solution_method and 'promethee' not in solution_method:
                self.madam_method = solution_method + "_method"
                from pyDecision.algorithm import ranking

            self.loaded_module = importlib.import_module(self.interface_name)

        if self.interface_name == 'feloopy':
            if "_method" not in solution_method and 'auto' not in solution_method and 'electre' not in solution_method and 'promethee' not in solution_method:
                self.madam_method = solution_method + "_method"

        if solution_method == 'auto':
            self.madam_method = 'auto'

        self.solver_options = dict()

        self.features = {
            'weights_found': False,
            'ranks_found': False,
            'inconsistency_found': False,
            'dpr_found': False,
            'dmr_found': False,
            'rpc_found': False,
            'rmc_found': False,
            'concordance_found': False,
            'discordance_found': False,
            'dominance_found': False,
            'kernel_found': False,
            'dominated_found': False,
            'global_concordance_found': False,
            'credibility_found': False,
            'dominance_s_found': False,
            'dominance_w_found': False,
            'd_rank_found': False,
            'a_rank_found': False,
            'n_rank_found': False,
            'p_rank_found': False,
            'classification_found': False,
            'selection_found': False
        }

    def add_criteria_set(self, index='', bound=None, step=1, to_list=False):
        """
        Adds a criteria set.

        Parameters:
        index (str): The index of the criteria set.
        bound (tuple): The range of the criteria set.
        step (int): The step size for the criteria set.
        to_list (bool): Whether to return the criteria set as a list or a set.

        Returns:
        set or list: The criteria set.
        """
        if bound is None and not index:
            raise ValueError('Either bound or index must be provided.')

        start, end = bound if bound else (0, len(index))
        criteria_set = [f'{index}{i}' for i in range(start, end, step)]

        return set(criteria_set) if not to_list else list(criteria_set)

    def add_alternatives_set(self, index='', bound=None, step=1, to_list=False):
        """
        Adds an alternatives set.

        Parameters:
        index (str): The index of the alternatives set.
        bound (tuple): The range of the alternatives set.
        step (int): The step size for the alternatives set.
        to_list (bool): Whether to return the alternatives set as a list or a set.

        Returns:
        set or list: The alternatives set.
        """
        if bound is None and not index:
            raise ValueError('Either bound or index must be provided.')

        start, end = bound if bound else (0, len(index))
        alternatives_set = [f'{index}{i}' for i in range(start, end, step)]

        self.features['number_of_alternatives'] = len(alternatives_set)
        
        return set(alternatives_set) if not to_list else list(alternatives_set)

    def add_dm(self, data):

        self.features['dm_defined'] = True
        self.decision_matrix = np.array(data)

        if self.madam_method != 'electre_tri_b':
            self.solver_options['dataset'] = self.decision_matrix
        else:
            self.solver_options['performance_matrix'] = self.decision_matrix

    def add_fcim(self, data):

        self.features['cim_defined'] = True
        self.influence_matrix = np.array(data)
        self.solver_options['dataset'] = self.influence_matrix

    def add_cim(self, data):

        self.features['cim_defined'] = True
        self.influence_matrix = np.array(data)
        self.solver_options['dataset'] = self.influence_matrix

    def add_bocv(self, data):
        
        self.features['bocv_defined'] = True
        self.best_to_others = np.array(data)
        self.solver_options['mic'] = self.best_to_others

    def add_owcv(self, data):

        self.features['owcv_defined'] = True
        self.others_to_worst = np.array(data)
        self.solver_options['lic'] = self.others_to_worst

    def add_fbocv(self, data):
        
        self.features['fbocv_defined'] = True
        self.best_to_others = data
        self.solver_options['mic'] = self.best_to_others

    def add_fowcv(self, data):

        self.features['fowcv_defined'] = True
        self.others_to_worst = data
        self.solver_options['lic'] = self.others_to_worst

    def add_fim(self, data):
        self.features['fim_defined'] = True
        self.fuzzy_influence_matrix = np.array(data)
        self.solver_options['dataset'] = self.fuzzy_influence_matrix

    def add_fdm(self, data):

        self.features['fdm_defined'] = True
        self.fuzzy_decision_matrix = np.array(data)
        self.solver_options['dataset'] = self.fuzzy_decision_matrix

    def add_wv_lb(self,data):
        self.features['wv_lb_defined'] = True
        self.solver_options['W_lower'] = np.array(data).tolist()

    def add_wv_ub(self,data):
        self.features['wv_ub_defined'] = True
        self.solver_options['W_upper'] = np.array(data)

    def add_wv(self,data):

        self.features['wv_defined'] = True
        self.weights = np.array(data)
        if self.madam_method not in ['electre_i','electre_i_s', 'electre_i_v', 'electre_ii', 'electre_iii', 'electre_tri_b', 'promethee_i','promethee_ii','promethee_iii', 'promethee_iv', 'promethee_v', 'promethee_gaia']:
            self.solver_options['weights'] = self.weights
        else:
            self.solver_options['W'] = self.weights

    def add_fwv(self,data):

        self.features['fwv_defined'] = True
        self.fuzzy_weights = data
        self.solver_options['weights'] = self.fuzzy_weights

    def add_bt(self, data):

        self.features['b_threshold_defined'] = True
        self.b_threshold = np.array(data).tolist()
        self.solver_options['B'] = self.b_threshold

    def add_grades(self, data):
        self.solver_options['grades'] = np.array(data)

    def add_lbt(self,data):

        self.features['lb_threshold_defined'] = True
        self.lb_threshold =  np.array(data) 
        if self.madam_method not in ['spotis_method']:
            self.solver_options['lower'] = self.lb_threshold
        if self.madam_method in ['spotis_method']:
            self.solver_options['s_min'] = self.lb_threshold
        
    def add_ubt(self,data):

        self.features['ub_threshold_defined'] = True
        self.ub_threshold =  np.array(data) 
        if self.madam_method not in ['spotis_method']:
            self.solver_options['upper'] = self.ub_threshold
        if self.madam_method in ['spotis_method']:
            self.solver_options['s_max'] = self.ub_threshold

    def add_qt(self,data):

        self.features['q_threshold_defined'] = True
        self.q_threshold =  np.array(data) 
        self.solver_options['Q'] = self.q_threshold

    def add_pt(self,data):

        self.features['p_threshold_defined'] = True
        self.p_threshold =  np.array(data) 
        self.solver_options['P'] = self.p_threshold

    def add_st(self,data):

        self.features['s_threshold_defined'] = True
        self.s_threshold =  np.array(data) 
        self.solver_options['S'] = self.s_threshold

    def add_vt(self,data):

        self.features['v_threshold_defined'] = True
        self.v_threshold =  np.array(data) 
        self.solver_options['V'] = self.v_threshold

    def add_uf(self,data):

        self.features['uf_defined'] = True
        self.utility_functions = data 
        if self.madam_method not in ['promethee_i', 'promethee_ii', 'promethee_iii', 'promethee_iv', 'promethee_v', 'promethee_vi', 'promethee_gaia']:
            self.solver_options['utility_functions'] = self.utility_functions
        else:
            self.solver_options['F'] = self.utility_functions

    def add_cpcm(self,data):

        self.features['cpm_defined'] = True
        self.criteria_pairwise_comparison_matrix = np.array(data)
        self.solver_options['dataset'] = self.criteria_pairwise_comparison_matrix

    def add_fcpcm(self,data):

        self.features['fcpcm_defined'] = True
        self.fuzzy_criteria_pairwise_comparison_matrix = np.array(data)
        self.solver_options['dataset'] = self.fuzzy_criteria_pairwise_comparison_matrix

    def add_apcm(self,data):

        self.features['apcm_defined'] = True
        self.alternatives_pairwise_comparison_matrix = np.array(data)
        self.solver_options['dataset'] = self.alternatives_pairwise_comparison_matrix

    def add_fapcm(self,data):

        self.features['fapm_defined'] = True
        self.fuzzy_alternatives_pairwise_comparison_matrix = np.array(data)
        self.solver_options['dataset'] = self.fuzzy_alternatives_pairwise_comparison_matrix

    def add_con_max_criteria(self,data):

        self.solver_options['criteria'] = data

    def add_con_cost_budget(self,cost, budget):

        self.solver_options['cost'] = cost
        self.solver_options['budget'] = budget

    def add_con_forbid_selection(self,selections):
        self.solver_options['forbidden'] = selections

    def sol(self, criteria_directions = [], solver_options=dict(), show_graph=None, show_log=None):

        if self.madam_method in ['promethee_ii', 'promethee_iv', 'promethee_vi']:
            self.solver_options['sort'] = False

        if self.madam_method in ['waspas_method']:
            if 'lambda_value' not in self.solver_options.keys():
                self.solver_options['lambda_value'] = 0.5

        if self.interface_name == 'pyDecision.algorithm':
            self.madam_algorithm = getattr(self.loaded_module, self.madam_method)
        else:

            if self.madam_method == 'cwdea_method':
                self.madam_algorithm = cwdea_method 

            if self.madam_method == 'lp_method':
                self.madam_algorithm = lp_method 

            if self.madam_method == 'la_method':
                self.madam_algorithm = la_method 

        self.solver_options.update(solver_options)

        if len(criteria_directions)!=0:
        
            self.solver_options['criterion_type'] = criteria_directions
            self.criteria_directions = criteria_directions

        self.auxiliary_solver_options = dict()
        if show_graph!=None:
            self.auxiliary_solver_options['graph'] = show_graph
        else:
            self.auxiliary_solver_options['graph'] = False
        if show_log!=None: 
            self.auxiliary_solver_options['verbose'] = show_log

        try:
            self.start = time.time()
            self.result =  self.madam_algorithm(**{**self.solver_options, **self.auxiliary_solver_options})
            self.finish = time.time()
        except:
            try:
                self.start = time.time()
                self.result =  self.madam_algorithm(**self.solver_options)
                self.finish = time.time()
            except:
                self.start = time.time()
                self.result =  self.madam_algorithm(**self.solver_options)
                self.finish = time.time()

        self.status = 'feasible (solved)'

        if  self.madam_method in np.array(WEIGHTING_ALGORITHMS)[:,0]:

            self.features['weights_found'] = True
            
            try:
                self.features['number_of_criteria'] = len(self.result[0])
            except:
                self.features['number_of_criteria'] = len(self.result)
                self.weights = self.result

            if self.madam_method in ['lp_method']:

                self.features['inconsistency_found'] = True
                self.weights = self.result[0]
                self.inconsistency = self.result[1]
                
            if self.madam_method in ['ahp_method']:

                self.features['inconsistency_found'] = True
                self.weights = self.result[0]
                self.inconsistency = self.result[1]

            if self.madam_method in ['fuzzy_ahp_method']:

                self.fuzzy_weights = self.result[0]
                self.weights = self.result[2]
                self.inconsistency = self.result[3]

            if self.madam_method in ['fuzzy_bw_method']:

                self.features['number_of_criteria'] = len(self.result[2])
                self.fuzzy_weights = self.result[2]
                self.weights = self.result[3]
                self.inconsistency = self.result[1]
                self.epsilon = self.result[0]
                self.features['inconsistency_found'] = True


        if  self.madam_method in np.array(RANKING_ALGORITHMS)[:,0]:

            self.features['ranks_found'] = True
            self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
            self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
            self.ranks = self.result

            if self.madam_method in ['promethee_vi']:
                self.features['ranks_found'] = True

            if self.madam_method in ['multimoora_method', 'waspas_method', 'fuzzy_waspas_method']:
                self.ranks = self.result[2]

            if self.madam_method in ['vikor_method', 'fuzzy_vikor_method']:
                self.ranks = self.result[3]

            if self.madam_method not in ['promethee_vi']:
                self.ranks = self.get_ranks()
            else:
                self.ranks = self.result[1]
                self.middle_ranks = self.get_ranks()
                self.ranks = self.result[2]
                self.upper_ranks =  self.get_ranks()
                self.ranks = self.result[0]
                self.lower_ranks =  self.get_ranks()
  
                self.ranks = np.array([self.lower_ranks, self.middle_ranks, self.upper_ranks ]).T

        if self.madam_method in np.array(SPECIAL_ALGORITHMS)[:,0]:

            if self.madam_method == 'cwdea_method':

                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.features['weights_found'] = True
                self.features['ranks_found'] = True
                self.ranks, self.weights = self.result
                self.ranks = self.get_ranks()

            if 'dematel' in self.madam_method:
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]

                self.features['weights_found'] = True
                self.features['dpr_found'] = True
                self.features['dmr_found'] = True
                self.D_plus_R, self.D_minus_R, self.weights = self.result

            if  self.madam_method in ['electre_i', 'electre_i_v']:
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.concordance, self.discordance, self.dominance, self.kernel, self.dominated = self.result
                self.kernel = [int(''.join(filter(str.isdigit, s)))-1 for s in self.kernel]
                self.dominated = [int(''.join(filter(str.isdigit, s)))-1 for s in self.dominated]
                self.features['concordance_found'] = True
                self.features['discordance_found'] = True
                self.features['dominance_found'] = True
                self.features['kernel_found'] = True
                self.features['dominated_found'] = True

            if self.madam_method == 'electre_i_s':
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.global_concordance, self.discordance, self.kernel, self.credibility, self.dominated = self.result
                self.kernel = [int(''.join(filter(str.isdigit, s)))-1 for s in self.kernel]
                self.dominated = [int(''.join(filter(str.isdigit, s)))-1 for s in self.dominated]
                self.features['global_concordance_found'] = True
                self.features['discordance_found'] = True
                self.features['kernel_found'] = True
                self.features['credibility_found'] = True
                self.features['dominated_found'] = True

            if self.madam_method == 'electre_ii':
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.concordance, self.discordance, self.dominance_s, self.dominance_w, self.rank_D, self.rank_A, self.rank_N, self.rank_P = self.result
                self.features['concordance_found'] = True
                self.features['discordance_found'] = True
                self.features['dominance_s_found'] = True
                self.features['dominance_w_found'] = True
                self.features['d_rank_found'] = True
                self.features['a_rank_found'] = True
                self.features['n_rank_found'] = True
                self.features['p_rank_found'] = True

                self.rank_D = [[int(''.join(filter(str.isdigit, s)))-1 for s in sd] for sd in self.rank_D]
                self.rank_A = [[int(''.join(filter(str.isdigit, s)))-1 for s in sd] for sd in self.rank_A]

            if self.madam_method == 'electre_iii':
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.global_concordance, self.credibility, self.rank_D, self.rank_A, self.rank_N, self.rank_P = self.result
                self.features['global_concordance_found'] = True
                self.features['credibility_found'] = True
                self.features['d_rank_found'] = True
                self.features['a_rank_found'] = True
                self.features['n_rank_found'] = True
                self.features['p_rank_found'] = True

                self.rank_D = [
                    int(item[1:]) if ';' not in item else [int(sub_item[1:]) for sub_item in item.split('; ')]
                    for item in  self.rank_D
                ]

                self.rank_A = [
                    int(item[1:]) if ';' not in item else [int(sub_item[1:]) for sub_item in item.split('; ')]
                    for item in  self.rank_A
                ]

            if self.madam_method == 'electre_iv':
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.credibility, self.rank_D, self.rank_A, self.rank_N, self.rank_P = self.result
                self.features['credibility_found'] = True
                self.features['d_rank_found'] = True
                self.features['a_rank_found'] = True
                self.features['n_rank_found'] = True
                self.features['p_rank_found'] = True

                self.rank_D = [
                    int(item[1:]) if ';' not in item else [int(sub_item[1:]) for sub_item in item.split('; ')]
                    for item in  self.rank_D
                ]

                self.rank_A = [
                    int(item[1:]) if ';' not in item else [int(sub_item[1:]) for sub_item in item.split('; ')]
                    for item in  self.rank_A
                ]

            if self.madam_method == 'electre_tri_b':
                self.features['number_of_criteria'] = self.solver_options['performance_matrix'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['performance_matrix'].shape[0]
                self.classification = self.result
                self.features['classification_found'] = True

            if self.madam_method == 'promethee_v':
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.selection = self.result
                self.features['selection_found'] = True

            if self.madam_method in ['promethee_i', 'promethee_iii']:
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['number_of_alternatives'] = self.solver_options['dataset'].shape[0]
                self.rank_P = self.result
                self.features['p_rank_found'] = True
            
            if self.madam_method in ['wings_method']:
                self.features['number_of_criteria'] = self.solver_options['dataset'].shape[1]
                self.features['weights_found'] = True
                self.features['rpc_found'] = True
                self.features['rmc_found'] = True

                self.R_plus_C, self.R_minus_C, self.weights = self.result
            
    def _generate_decision_info(self):

        tline_text('Decision')
        empty_line()

        if not self.show_tensor:

            if self.features['weights_found']:

                for i in range(self.features['number_of_criteria']):

                    if self.madam_method in ['fuzzy_ahp_method', 'fuzzy_bw_method']:
                        self.display_as_tensor(f'fw[{i}]', np.round(self.fuzzy_weights[i],self.output_decimals), self.show_detailed_tensors)
                    else:
                        self.display_as_tensor(f'w[{i}]', np.round(self.weights[i],self.output_decimals), self.show_detailed_tensors)

                if self.madam_method in ['fuzzy_bw_method']:
                    for i in range(self.features['number_of_criteria']):
                        self.display_as_tensor(f'w[{i}]', np.round(self.weights[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['rpc_found']:
                for i in range(self.features['number_of_criteria']):
                    self.display_as_tensor(f'rpc[{i}]', np.round(self.R_plus_C[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['rmc_found']:
                for i in range(self.features['number_of_criteria']):
                    self.display_as_tensor(f'rmc[{i}]', np.round(self.R_minus_C[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['ranks_found']:

                for i in range(len(self.ranks)):
                    self.display_as_tensor(f'r[{i}]', np.round(self.ranks[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['classification_found']:

                for i in range(self.features['number_of_alternatives']):
                    self.display_as_tensor(f'c[{i}]', np.round(self.classification[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['selection_found']:

                for i in range(self.features['number_of_alternatives']):
                    if self.selection[i,2] == 1:
                        self.display_as_tensor(f's[{int(self.selection[i,0])}]', np.round(self.selection[i,1],self.output_decimals), self.show_detailed_tensors)

            if self.features['dpr_found']:

                for i in range(self.features['number_of_criteria']):
                    self.display_as_tensor(f'dpr[{i}]', np.round(self.D_plus_R[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['dmr_found']:

                for i in range(self.features['number_of_criteria']):
                    self.display_as_tensor(f'dmr[{i}]', np.round(self.D_minus_R[i],self.output_decimals), self.show_detailed_tensors)

            if self.features['d_rank_found']:
                for i in range(len(self.rank_D)):
                    self.display_as_tensor(f'd_r[{i}]', self.rank_D[i], self.show_detailed_tensors)

            if self.features['a_rank_found']:
                for i in range(len(self.rank_A)):
                    self.display_as_tensor(f'a_r[{i}]', self.rank_A[i], self.show_detailed_tensors)

            if self.features['p_rank_found']:
                for i in range(len(self.rank_P)):
                    self.display_as_tensor(f'p_r[{i}]', self.rank_P[i], self.show_detailed_tensors)
        else:

            if self.features['weights_found']:

                if self.madam_method in ['fuzzy_ahp_method']:
                    self.display_as_tensor('fwv', np.round(self.fuzzy_weights,self.output_decimals), self.show_detailed_tensors)
                else:
                    self.display_as_tensor('wv', np.round(self.weights,self.output_decimals), self.show_detailed_tensors)

            if self.features['ranks_found']:

                if self.madam_method in ['fuzzy_aras_method']:
                    self.display_as_tensor('frv', np.round(self.fuzzy_ranks,self.output_decimals), self.show_detailed_tensors)
                else:
                    self.display_as_tensor('rv', np.round(self.ranks,self.output_decimals), self.show_detailed_tensors)

            if self.features['classification_found']:

                self.display_as_tensor(f'c', np.round(self.classification,self.output_decimals), self.show_detailed_tensors)

            if self.features['d_rank_found']:
                self.display_as_tensor(f'd_rv', self.rank_D, self.show_detailed_tensors)

            if self.features['a_rank_found']:
                self.display_as_tensor(f'a_rv', self.rank_A, self.show_detailed_tensors)

            if self.features['p_rank_found']:
                self.display_as_tensor(f'p_rv', self.rank_P, self.show_detailed_tensors)


        if self.features['global_concordance_found']:
            self.display_as_tensor('gcm', np.round(self.global_concordance,self.output_decimals), self.show_detailed_tensors)

        if self.features['concordance_found']:
            self.display_as_tensor('ccm', np.round(self.concordance,self.output_decimals), self.show_detailed_tensors)

        if self.features['discordance_found']:
            self.display_as_tensor('dcm', np.round(self.discordance,self.output_decimals), self.show_detailed_tensors)

        if self.features['credibility_found']:
            self.display_as_tensor('crm', np.round(self.credibility,self.output_decimals), self.show_detailed_tensors)

        if self.features['dominance_found']:
            self.display_as_tensor('dmm', np.round(self.dominance,self.output_decimals), self.show_detailed_tensors)

        if self.features['kernel_found']:
            self.display_as_tensor('kernel',  self.kernel, self.show_detailed_tensors)
            
        if self.features['dominated_found']:
            self.display_as_tensor('dominated', self.dominated, self.show_detailed_tensors)

        if self.features['dominance_s_found']:
            self.display_as_tensor('dmm_s', self.dominance_s, self.show_detailed_tensors)

        if self.features['dominance_w_found']:
            self.display_as_tensor('dmm_w', self.dominance_w, self.show_detailed_tensors)

        self.features['dominance_s_found'] = False
        self.features['dominance_w_found'] = False
        self.features['d_rank_found'] = False
        self.features['a_rank_found'] = False
        self.features['n_rank_found'] = False
        self.features['p_rank_found'] = False
        empty_line()
        bline()

    def _generate_metric_info(self):
        tline_text("Metric")
        empty_line()

        if self.features['inconsistency_found']:
            two_column('Inconsistency:', str(np.round(self.inconsistency,self.output_decimals)))
        
        import time
        elapsed_time_seconds = self.finish - self.start
        elapsed_time_microseconds = int(elapsed_time_seconds * 1_000_000)
        elapsed_time_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time_seconds))

        two_column('CPT (microseconds):', str(elapsed_time_microseconds))
        two_column('CPT (hour:min:sec):', elapsed_time_formatted)

        empty_line()
        bline()

    def get_numpy_var(self, input):

        if input == 'frv':
            return self.ranks
        
        if input == 'rv':
            return self.ranks

        if input == 'wv':
            return self.weights

        if input == 'fwv':
            return self.fuzzy_weights

        if input == 'dmrv':
            return self.D_minus_R

        if input == 'dprv':
            return self.D_plus_R

        if input == 'rmcv':
            return self.R_minus_C

        if input == 'rpcv':
            return self.R_plus_C
          
        if input in ['dominated']:
            return self.dominated
        
        if input in ['concordance', 'cmm']:
            return self.concordance

        if input in ['discordance', 'dcm']:
            return self.discordance

        if input in ['kernel']:
            return self.kernel
        
        if input in ['dominance', 'dmm']:
            return self.dominance
        
        if input in ['dominance_s', 'dmm_s']:
            return self.dominance_s

        if input in ['dominance_w', 'dmm_w']:
            return self.dominance_w
         
        if input in ['global_concordance', 'gcm']:
            return self.global_concordance

        if input in ['credibility', 'crm']:
            return self.credibility
    
        if input in ['rank_d', 'd_rv']:
            return self.rank_D

        if input in ['rank_a', 'a_rv']:
            return self.rank_A

        if input in ['classification', 'class', 'c']:
            return self.classification     
          
    def get_ranks_base(self):
        
        try:
            return np.array(self.ranks)[:,1]
        except: 
            return np.array(self.ranks)
        
    def get_ranks(self):

        if self.madam_method not in ['la_method']:

            if self.madam_method not in ['vikor_method', 'fuzzy_vikor_method']:

                try:
                    if self.madam_method not in ['borda_method', 'cradis_method', 'mairca_method', 'oreste_method', 'piv_method', 'spotis_method']:

                        return np.argsort(np.array(self.ranks)[:,1])[::-1]

                    else:
                        return np.argsort(np.array(self.ranks)[:,1])

                except:
                    if self.madam_method not in ['borda_method','cradis_method', 'mairca_method', 'oreste_method', 'piv_method', 'spotis_method']:
                        return np.argsort(np.array(self.ranks))[::-1]
                    else:
                        return np.argsort(np.array(self.ranks))

            else:

                return np.int64(np.array(self.ranks)[:,0])
            
        else:
            return self.ranks
        
    def get_status(self):
        return self.status

    def get_inconsistency(self):
        return self.inconsistency

    def get_weights(self):

        return self.weights
        
    def get_fuzzy_weights(self):

        return self.fuzzy_weights
        
    def get_crisp_weights(self):

        return self.crisp_weights
        
    def get_normalized_weights(self):
        
        return self.normalized_weights
    
    def report(self, all_metrics=False, feloopy_info=True, sys_info=False,
                        model_info=True, sol_info=True, metric_info=True,
                        ideal_pareto=None, ideal_point=None, show_tensors=False,
                        show_detailed_tensors=False, save=None, decimals = 4):

        self.show_tensor = show_tensors
        self.show_detailed_tensors = show_detailed_tensors

        self.output_decimals = 4

        if feloopy_info:
            self._generate_feloopy_info()

        if sys_info:
            self._generate_sys_info()

        if model_info:
            self._generate_model_info()

        if sol_info:
            self._generate_sol_info()

        if metric_info:
            self._generate_metric_info()

        self._generate_decision_info()

    def display_as_tensor(self, name, numpy_var, detailed):
        if detailed:
            np.set_printoptions(threshold=np.inf)

        if isinstance(numpy_var, np.ndarray):
            tensor_str = np.array2string(numpy_var, separator=', ', prefix='│ ') #Style argument deprecated.
            rows = tensor_str.split('\n')
            first_row_len = len(rows[0])
            for k, row in enumerate(rows):
                if k == 0:
                    left_align(f"{name} = {row}")
                else:
                    left_align(" " * (len(f"{name} =") - 1) + row)
        else:
            left_align(f"{name} = {numpy_var}")

    def _generate_feloopy_info(self):

        import datetime
        now = datetime.datetime.now()
        date_str = now.strftime("Date: %Y-%m-%d")
        time_str = now.strftime("Time: %H:%M:%S")

        tline_text("FelooPy v0.2.8")
        empty_line()
        two_column(date_str, time_str)

        if 'pydecision' in self.interface_name.lower():
            interface = 'pydecision'
            two_column(f"Interface: {interface}", f"Solver: {self.madam_method}")

        empty_line()
        bline()

    def _generate_sys_info(self):
        try:
            import psutil
            import cpuinfo
            tline_text("System")
            empty_line()
            cpu_info = cpuinfo.get_cpu_info()["brand_raw"]
            cpu_cores = psutil.cpu_count(logical=False)
            cpu_threads = psutil.cpu_count(logical=True)
            ram_info = psutil.virtual_memory()
            ram_total = ram_info.total
            os_info = platform.system()
            os_version = platform.version()
            left_align(f"OS: {os_version} ({os_info})")
            left_align(f"CPU   Model: {cpu_info}")
            left_align(f"CPU   Cores: {cpu_cores}")
            left_align(f"CPU Threads: {cpu_threads}")

            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    left_align(f"GPU   Model: {gpu.name}")
                    left_align(f"GPU    VRAM: {gpu.memoryTotal / 1024:.2f} GB")
            except:
                pass

            left_align(f"SYSTEM  RAM: {ram_total / (1024 ** 3):.2f} GB")
        except:
            pass

        empty_line()
        bline()

    def _generate_model_info(self):
        tline_text("Model")
        empty_line()
        left_align(f"Name: {self.model_name}")
        for i in self.features.keys():
            if 'defined' in i:
                left_align(i)

        for i in self.features.keys():
            if 'found' in i and self.features[i]=='True':
                left_align(i)

        try:
            two_column("Number of criteria:", str(self.features['number_of_criteria']))
        except:
            ""

        try:
            two_column("Number of alternatives:", str(self.features['number_of_alternatives']))
        except:
            ""

        empty_line()
        bline()

    def _generate_sol_info(self):

        tline_text("Solve")
        empty_line()
        left_align(f"Method: {self.madam_method}")
        left_align(f"Status: {self.status}")

        empty_line()
        bline()
    
madm = MADM