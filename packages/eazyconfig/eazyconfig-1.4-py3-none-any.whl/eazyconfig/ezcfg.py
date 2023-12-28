import re
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List, Tuple
from .assets import trim_path_string
from colorama import just_fix_windows_console
from abc import ABC, abstractmethod
just_fix_windows_console()


class BaseEzConfig(ABC):
    def __init__(self, path_config_file: Path|str, float_vars=None, int_vars=None, comma_sep_vars=None, boolean_vars=None):
        self.path_config_file = path_config_file
        self.float_vars = float_vars
        self.int_vars = int_vars
        self.comma_sep_vars = comma_sep_vars
        self.boolean_vars = boolean_vars
        self.parameters = {}

    @abstractmethod
    def _prepare_input_params(self) -> None: ...
        
    @abstractmethod
    def get_params(self) -> Dict:...

    def _handle_float(self, key: str, var: str) -> None:
        try:
            self.parameters[key] = float(var)
        except Exception as e:
            raise RuntimeError(f"Provide a float {self.float_vars}", e) 

    def _handle_int(self, key: str, var: str) -> None:
        try:
            self.parameters[key] = int(var)
        except Exception as e:
            raise RuntimeError(f"Provide an integer {self.float_vars}", e)

    def _handle_bool(self, key: str, var: str) -> None:
        try:
            self.parameters[key] = eval(var.capitalize())
        except Exception as e:
            raise RuntimeError(f"Provide a number {self.float_vars}") from e  
        
    def _handle_comma_sep(self, key: str, var: str) -> None:
        try:
            separated_values = var.split(",")
            separated_values = [x.strip() for x in separated_values if x.strip()]
            self.parameters[key] = separated_values
        except Exception as e:
            raise RuntimeError("Unexpected error in converting comma-separated str to list of str", e)


class Configure(BaseEzConfig):
    def __init__(
        self,
        config_settings: Dict,
        path_config_file: str | Path,
        float_vars: List[str] = None,
        int_vars: List[str] = None,
        comma_sep_vars: List[str] = None,
        boolean_vars: List[str] = None,
        mandatory_vars: List[str] = None,
        optional_vars: List[str] = None
    ) -> None:
        """
        Structure of the config file:\n
        [header] \n
        params = \n

        @config_settings: 
        Dictionary of which the keys are the headers and associated values are the parameters: List | Tuple
        @path_config_file:
        Pathname of the config file
        @float_vars
        List of the variables that are supposed to be float
        @mandatory_vars
        Variables whose existence in the config file are mandatory. Default all variables are mandatory
        """
        super().__init__(
            path_config_file=path_config_file, 
            float_vars=float_vars, 
            int_vars=int_vars, 
            comma_sep_vars=comma_sep_vars,
            boolean_vars=boolean_vars
        )
        self.config_settings = config_settings
        self.mandatory_vars = mandatory_vars
        self.optional_vars = optional_vars

    def _check_mandatory_or_optional(self, variable: str, variable_name: str) -> None:
        try:
            if self.optional_vars is None:
                if self.mandatory_vars is None:
                    if not variable:
                        raise ValueError(f"Please provide information for {variable_name}\n")
                else:
                    if variable_name in self.mandatory_vars and not variable:
                        raise ValueError(f"Please provide information for {variable_name}\n")
            else:
                if not variable and variable_name not in self.optional_vars:
                    raise ValueError(f"Please provide information for {variable_name}\n")
             
        except Exception as e:
            raise RuntimeError("Failed to check if the variable is mandaotry or optional", e)

    def _fetch_vars_from_cfgfile(self, config: ConfigParser) -> None:
        for header, variables_names in self.config_settings.items():
            for variable_name in variables_names:
                variable = config.get(header, variable_name).strip()
                self._check_mandatory_or_optional(variable, variable_name)

                if self.float_vars is not None and variable_name in self.float_vars:
                    self._handle_float(variable_name, variable) 
                    continue

                if self.boolean_vars is not None and variable_name in self.boolean_vars:
                    self._handle_bool(variable_name, variable) 
                    continue

                if self.int_vars is not None and variable_name in self.int_vars:
                    self._handle_int(variable_name, variable) 
                    continue

                if self.comma_sep_vars is not None and variable_name in self.comma_sep_vars:
                    self._handle_comma_sep(variable_name, variable)
                    continue
                self.parameters[variable_name] = trim_path_string(variable)
    
    def _prepare_input_params(self) -> None:
        try:
            config = ConfigParser()
            config.read(self.path_config_file)
            self._fetch_vars_from_cfgfile(config)

        except Exception as e:
            raise RuntimeError(f"Failed to extract input parameters\n", e)

    def get_params(self) -> Dict:
        self._prepare_input_params()
        return self.parameters


class ConfigureText(BaseEzConfig):
    def __init__(
        self,
        path_config_file: str | Path,
        mandatory_vars: List[str] = None,
        float_vars: List[str] = None,
        int_vars: List[str] = None,
        comma_sep_vars: List[str] = None,
        boolean_vars: List[str] = None,
    ) -> None:
        """
        This class is to prepare the inputs without the conventional .cfg file (no headers)
        The parameters and the value should be separated by "="
        "#" counts as comments in the text file and will NOT be processed

        @mandatory_vars: If not specified, all the variables will be mandatory
        """
        super().__init__(path_config_file=path_config_file, float_vars=float_vars, int_vars=int_vars, comma_sep_vars=comma_sep_vars)
        self.mandatory_vars = mandatory_vars
        self.boolean_vars = boolean_vars

    def _extract_key_var(self, line: str) -> Tuple[str, str]:
        try:
            key, var = line.strip().replace('"', '').replace("'", "").split("=")
            return key.strip(), var.strip() 
        except Exception as e:
            raise Exception("Failed to extract key and variable from each line", e)

    def _check_mandatory_vars(self, var: str, key: str) -> None:
        if self.mandatory_vars is None and not var:
            raise ValueError(f"All variables are mandatory! Make sure you provide value for {key}")

        if self.mandatory_vars and key in self.mandatory_vars and not var:
            raise ValueError(f"Make sure you provide information for {key}")         
    
    def _prepare_input_params(self) -> Dict:
        try:
            with open(self.path_config_file, "r") as f:
                for line in f:
                    if not re.search(r"^#", line) and line.strip():
                        key, var = self._extract_key_var(line=line)
                        self._check_mandatory_vars(var, key)

                        if self.float_vars is not None and key in self.float_vars:
                            self._handle_float(key, var)
                            continue

                        if self.boolean_vars is not None and key in self.boolean_vars:
                            self._handle_bool(key, var)
                            continue
                        
                        if self.int_vars is not None and key in self.int_vars:
                            self._handle_int(key, var) 
                            continue
                        
                        if self.comma_sep_vars is not None and key in self.comma_sep_vars:
                            self._handle_comma_sep(key, var)
                            continue

                        self.parameters[key] = var

            if not self.parameters:
                raise ValueError("Please provide all the required information\n")

        except Exception as e:
            raise RuntimeError("Failed to extract input parameters") from e

    def get_params(self) -> Dict:
        self._prepare_input_params()
        return self.parameters