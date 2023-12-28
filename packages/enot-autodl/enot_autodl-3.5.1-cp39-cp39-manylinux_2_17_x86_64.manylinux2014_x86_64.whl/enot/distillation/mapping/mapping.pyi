from typing import Any, List, NamedTuple, Tuple

__all__ = ['Mapping']

class Mapping:
    """Mapping between modules of teacher and student models."""
    class _Mapping(NamedTuple):
        teacher_module: Mappable
        student_module: Mappable
        payload: Any
    def __init__(self, teacher: Module, student: Module) -> None:
        """
        Parameters
        ----------
        teacher : Module
            Teacher module.
        student : Module
            Student module.

        """
    def add(self, teacher_module: Mappable, student_module: Mappable, payload: Any = None) -> None:
        """
        Add pair to mapping.

        Parameters
        ----------
        teacher_module : Mappable
            Teacher module which will be associated with student module.
        student_module : Mappable
            Student module which will be associated with teacher module.
        payload : Any
            Payload, default value is None.

        """
    def apply(self) -> Tuple[Module, Module]:
        """Apply mapping."""
    def revert(self) -> Tuple[Module, Module]:
        """Revert all changes."""
    @property
    def teacher(self) -> Module: ...
    @property
    def student(self) -> Module: ...
    def payload(self) -> List[Any]:
        """Payload, order is preserved."""
