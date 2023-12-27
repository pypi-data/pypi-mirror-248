"""A package for Design of Experiments (DoE) and Design Space Exploration (DSE)"""

__version__ = "0.1.0"

from dataclasses import dataclass
from typing import Tuple, Optional, Union, List, Iterable, Dict
import random

from pyDOE2 import lhs


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


@dataclass
class Bounds:
    """A bounds object with a lower and upper bound."""
    lower: Union[float, int]
    upper: Union[float, int]

    def __init__(self, lower: Union[float, int], upper: Union[float, int]):
        if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
            raise TypeError("Bounds must be an int or float")
        self.lower = lower
        self.upper = upper


class VariableDefinition:
    """A variable with a name, bounds, and a default value.

    Parameters
    ----------
    name : str
        The name of the variable.
    bounds : Union[Tuple[float, float], Bounds]
        The lower and upper bounds of the variable.
    type : str, optional
        The type of the variable. Either "continuous" or "discrete".
    options : List[int, str], optional
        The options for the variable if it is discrete.
    """

    def __init__(self, name: str,
                 bounds: Union[Bounds, Iterable] = None,
                 type: str = "continuous",
                 options: Union[List[int], List[str], List[float], None] = None,
                 units: Optional[str] = None,
                 ):

        self.name = name

        if bounds:
            if isinstance(bounds, Bounds):
                self.bounds = bounds
            elif isiterable(bounds):
                self.bounds = Bounds(bounds[0], bounds[1])
            else:
                raise TypeError("bounds must be a Bounds object or an iterable with two elements")

        self.type = type
        self.options = options
        self.units = units

    def __repr__(self):
        return f"Variable(name={self.name}, bounds={self.bounds}, type={self.type})"

    def __str__(self):
        return self.name + ": " + str(self.bounds)

    def __eq__(self, other):
        if isinstance(other, VariableDefinition):
            return (self.name == other.name and self.bounds == other.bounds and
                    self.type == other.type and self.options == other.options and
                    self.units == other.units)
        return False


class Variable:
    """A variable instance with a name, value and units.

    Parameters
    ----------
    var_definition : VariableDefinition
        The type of variable it is.
    value : Union[float, int, str]
        The actual value of the variable."""

    def __init__(self, var_definition: VariableDefinition, value):
        self.value = value
        self.var_definition = var_definition
        self.validation()

    def validation(self):
        if not isinstance(self.value, (int, float, str)):
            raise TypeError("value must be an int, float or str")
        if self.var_definition.type == "discrete" and self.value not in self.var_definition.options:
            raise ValueError("value must be one of the options")
        if self.var_definition.type == "continuous" and not self.var_definition.bounds.lower <= self.value <= self.var_definition.bounds.upper:
            raise ValueError("value must be within the bounds")

    @property
    def name(self):
        return self.var_definition.name

    @property
    def units(self):
        return self.var_definition.units

    def __repr__(self):
        return f"Variable(name={self.name}, value={self.value}, units={self.units})"

    def __str__(self):
        return f"{self.name}: {self.value:.2f} {self.units}"

    def print_line(self, name_width=20, value_width=10):
        return f"{self.name:<{name_width}}: {self.value:>{value_width}.2f} {self.units}"


@dataclass
class PerformanceMetricDefinition:
    """A performance metric with a name, value and units."""

    name: str
    units: str


@dataclass
class PerformanceMetric:
    """A performance metric instance with a name, value and units."""

    metric_definition: PerformanceMetricDefinition
    value: float

    @property
    def name(self):
        return self.metric_definition.name

    @property
    def units(self):
        return self.metric_definition.units

    def __str__(self):
        return f"{self.name}: {self.value:.2f} {self.units}"


class DesignCase:
    """ A Design Case or Design Space sampling point.

    It contains a collection of Variable and PerformanceMetric objects.

    """

    def __init__(self, variables: List[Variable] = None, metrics: List[PerformanceMetric] = None):
        self._variables = {var.name: var for var in variables} if variables else {}
        self._metrics = {metric.name: metric for metric in metrics} if metrics else {}

    def __str__(self):
        max_length = max(
            max([len(var.name) for var in self._variables.values()]),
            max([len(metric.name) for metric in self._metrics.values()]),
        )  # TODO: indent this properly one day, so all the colons line up

        txt = "Variables:\n"
        for var in self._variables.values():
            txt += f"  {var}\n"
        txt += "Metrics:\n"
        for metric in self._metrics.values():
            txt += f"  {metric}\n"
        return txt

    def add_variable(self, variable: Variable):
        if not isinstance(variable, Variable):
            raise TypeError("variable must be a Variable object")
        if variable in self.variables:
            raise ValueError(f"Variable '{variable.name}' already exists.")
        self._variables[variable.name] = variable

    @property
    def variables(self):
        return self._variables.values()

    def add_metric(self, metric: PerformanceMetric):
        if not isinstance(metric, PerformanceMetric):
            raise TypeError("metric must be a PerformanceMetric object")
        if metric.name in self._metrics:
            raise ValueError(f"Metric '{metric.name}' already exists.")
        self._metrics[metric.name] = metric

    def __getitem__(self, item):
        if item in self._variables:
            return self._variables[item]
        if item in self._metrics:
            return self._metrics[item]
        raise KeyError(f"Item '{item}' not found.")


class DoE:
    """A Design of Experiments (DoE) class.

    This class is used to generate a set of design cases (DesignCase objects) that can be used to run simulations.
    The design cases are generated using the Latin Hypercube Sampling (LHS) method.
    """

    def __init__(self, variables: List[VariableDefinition], n_designs: int = 0):
        self.variables = variables
        self.n_designs: int = n_designs
        self.design_cases = {i: DesignCase() for i in range(n_designs)}
        self._generate_design_cases()

    @property
    def metrics(self) -> List[PerformanceMetricDefinition]:
        """collects all the performance metrics from the design cases in a set"""
        metrics = set()
        for dc in self.design_cases.values():
            metrics.update(dc._metrics.keys())
        return list(metrics)

    @property
    def continuous_variables_definition(self) -> List[VariableDefinition]:
        """select the variable definitions that are continuous"""
        return list([var for var in self.variables if var.type == "continuous"])

    def sample_continuous(self) -> Dict[str, List[Variable]]:
        """get a sample from the continuous space using LHS"""

        # i am not passing every option of the lhs, but for the time being it is ok. Future update
        unitary_designs = lhs(n=len(self.continuous_variables_definition), samples=self.n_designs)
        # scale the unitary designs to the bounds of the variables

        for i, var in enumerate(self.continuous_variables_definition):
            for j, dc in self.design_cases.items():
                scaled_value = unitary_designs[j, i] * (var.bounds.upper - var.bounds.lower) + var.bounds.lower
                dc.add_variable(Variable(var, scaled_value))

    def generate_discrete_values(self, variable: VariableDefinition) -> None:
        """get a sample from the discrete space and get N samples randomly
        This is equivalent to a random sampling without replacement
        """

        # Your data list
        data = variable.options
        # The number of elements you want to sample
        num_samples = self.n_designs  # Replace with your desired sample size
        # Sampling with replacement
        samples = random.choices(data, k=num_samples)

        for sample, dc in zip(samples, self.design_cases.values()):
            dc.add_variable(Variable(variable, sample))

    def _generate_design_cases(self) -> None:
        """generate the design cases"""

        # generate the continuous variables
        self.sample_continuous()

        # generate the discrete variables
        for var in self.variables:
            if var.type == "discrete":
                self.generate_discrete_values(var)

    def to_csv(self, filename: str = "doe.csv", ndigits: int = 2, separator: str = ",") -> None:
        """write the design cases to a csv file

        Parameters
        ----------
        filename : str, optional
            The name of the file to write to.
        ndigits : int, optional
            The number of digits to round to.
        separator : str, optional
            The separator to use between values.

        """
        str_None = " "
        # get the header
        header = [var.name for var in self.variables] + [metric for metric in self.metrics]
        lines = []
        for design_case in self:
            values = []
            for item in header:
                try:
                    value = design_case[item].value
                    values.append(value)
                except KeyError:
                    values.append(None)
            lines.append(values)

        # write to file
        with open(filename, "w") as f:
            f.write(separator.join(header) + "\n")
            for line in lines:
                line_text = []
                for value in line:
                    if value is None:
                        line_text.append(str_None)
                    else:
                        try:
                            line_text.append(str(round(value, ndigits=ndigits)))
                        except TypeError:
                            line_text.append(str(value))

                f.write(separator.join(line_text) + "\n")

        # ensure that the columns are consistent with the header
        assert len(header) == len(values)

    def __len__(self):
        return len(self.design_cases)

    def __iter__(self):
        """Return an iterator over design cases."""
        return iter(self.design_cases.values())

    def __getitem__(self, index):
        """Return the design case at the given index."""
        return self.design_cases[index]

    def add_design_case(self, dc):
        """add a design case to the set of design cases"""
        if not isinstance(dc, DesignCase):
            raise TypeError("dc must be a DesignCase object")
        self.design_cases[len(self.design_cases)] = dc
        for variable in dc.variables:
            if variable.var_definition not in self.variables:
                self.variables.append(variable.var_definition)
