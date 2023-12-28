from _typeshed import Incomplete
from enot.quantization.calibration.functions import AsymmetricCalibrationFunction, SymmetricCalibrationFunction
from enot.quantization.utils.common import CalibrationMethod, QuantizationStrategy, QuantizationType, TensorInfo
from typing import Callable, Optional, Tuple, Union

__all__ = ['CALIBRATION_FUNCTION_FACTORY']

class CalibrationFunctionFactory:
    """Constructs calibration functions by QuantizationType."""
    def __init__(self) -> None: ...
    def register_builder(self, key: Tuple[QuantizationStrategy, CalibrationMethod], builder: Callable) -> None:
        """
        Registers builder for particular QuantizationStrategy and CalibrationMethod.

        Parameters
        ----------
        key : Tuple[QuantizationStrategy, CalibrationMethod]
            A key that identifies the builder.
        builder : Callable
            Callable object that will be built calibration function
            by quantization description and tensor description.

        """
    def create(self, quantization_type: QuantizationType, tensor_info: Optional[TensorInfo]) -> Union[SymmetricCalibrationFunction, AsymmetricCalibrationFunction]:
        """
        Creates calibration function by quantization description and tensor description.

        Parameters
        ----------
        quantization_type : QuantizationType
            Quantization description.
        tensor_info : Optional[TensorInfo]
            Description of the target tensor. Can be None in case of layerwise quantization.

        Returns
        -------
        Union[SymmetricCalibrationFunction, AsymmetricCalibrationFunction]
            Calibration function.

        """

CALIBRATION_FUNCTION_FACTORY: Incomplete
