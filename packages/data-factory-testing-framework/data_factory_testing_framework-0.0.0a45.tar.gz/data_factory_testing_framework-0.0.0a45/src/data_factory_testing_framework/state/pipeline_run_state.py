from typing import Any, Dict, List, Optional, Union

from data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import (
    VariableBeingEvaluatedDoesNotExistError,
)
from data_factory_testing_framework.exceptions.variable_does_not_exist_error import VariableDoesNotExistError
from data_factory_testing_framework.state.dependency_condition import DependencyCondition
from data_factory_testing_framework.state.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.state.run_parameter import RunParameter
from data_factory_testing_framework.state.run_state import RunState


class PipelineRunState(RunState):
    def __init__(
        self,
        parameters: Optional[List[RunParameter]] = None,
        variables: Optional[List[PipelineRunVariable]] = None,
        pipeline_activity_results: Optional[Dict[str, Any]] = None,
        iteration_item: str = None,
    ) -> None:
        """Represents the state of a pipeline run. Can be used to configure the state to validate certain pipeline conditions.

        Args:
            parameters: The global and regular parameters to be used for evaluating expressions.
            variables: The initial variables specification to use for the pipeline run.
            pipeline_activity_results: The results of previous activities to use for validating dependencyConditions and evaluating expressions
            (i.e. activity('activityName').output).
            iteration_item: The current item() of a ForEach activity.
        """
        if variables is None:
            variables = []

        if pipeline_activity_results is None:
            pipeline_activity_results = {}

        super().__init__(parameters)

        self.variables = variables
        self.pipeline_activity_results: Dict[str, Any] = pipeline_activity_results
        self.scoped_pipeline_activity_results: Dict[str, Any] = {}
        self.iteration_item = iteration_item
        self.return_values: Dict[str, Any] = {}

    def add_activity_result(self, activity_name: str, status: DependencyCondition, output: Any = None) -> None:  # noqa: ANN401
        """Registers the result of an activity to the pipeline run state.

        Args:
            activity_name: Name of the activity.
            status: Status of the activity.
            output: Output of the activity. (e.g. { "count": 1 } for activity('activityName').output.count)
        """
        self.pipeline_activity_results[activity_name] = {
            "status": status,
            "output": output,
        }
        self.scoped_pipeline_activity_results[activity_name] = {
            "status": status,
            "output": output,
        }

    def create_iteration_scope(self, iteration_item: str = None) -> "PipelineRunState":
        """Used to create a new scope for a ControlActivity like ForEach, If and Until activities.

        Args:
            iteration_item: The current item() of a ForEach activity.

        Returns:
            A new PipelineRunState with the scoped variables and activity results.
        """
        return PipelineRunState(
            self.parameters,
            self.variables,
            self.pipeline_activity_results,
            iteration_item,
        )

    def add_scoped_activity_results_from_scoped_state(self, scoped_state: "PipelineRunState") -> None:
        """Registers all the activity results of a childScope into the current state.

        Args:
            scoped_state: The scoped childState.
        """
        for result in scoped_state.pipeline_activity_results:
            self.pipeline_activity_results[result] = scoped_state.pipeline_activity_results[result]

    def try_get_scoped_activity_result_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Tries to get the activity result from the scoped state. Might be None if the activity was not executed in the scope.

        Args:
            name: Name of the activity.
        """
        return self.pipeline_activity_results[name] if name in self.pipeline_activity_results else None

    def set_variable(self, variable_name: str, value: Union[str, int, bool, float]) -> None:
        """Sets the value of a variable if it exists. Otherwise throws an exception.

        Args:
            variable_name: Name of the variable.
            value: New value of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                variable.value = value
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)

    def append_variable(self, variable_name: str, value: Union[str, int, bool, float]) -> None:
        """Appends a value to a variable if it exists and is an array. Otherwise, throws an exception.

        Args:
            variable_name: Name of the variable.
            value: Appended value of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                if not isinstance(variable.value, list):
                    raise ValueError(f"Variable {variable_name} is not an array.")

                variable.value.append(value)
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)

    def get_variable_by_name(self, variable_name: str) -> PipelineRunVariable:
        """Gets a variable by name. Throws an exception if the variable is not found.

        Args:
            variable_name: Name of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                return variable

        raise VariableDoesNotExistError(variable_name)

    def set_return_value(self, param: str, evaluated_value: Any) -> None:  # noqa: ANN401
        self.return_values[param] = evaluated_value
