from core.errors import ErrorMessages
from models.service import Density, ConversionKoefficient

class Calculator:
    @staticmethod
    def calculate_density(
        loops: int,
        rows: int,
        height: float,
        width: float,
    ) -> Density:
        if loops <= 0 or rows <= 0 or height <= 0 or width <= 0:
            raise ValueError(ErrorMessages.INVALID_PARAMETERS)

        return Density(
            loops=loops / width,
            rows=rows / height,
        )
    
    @staticmethod
    def calculate_density_conversion(original_v: Density, target_v:Density) -> ConversionKoefficient:
        if original_v.loops <= 0 or original_v.rows <= 0 or target_v.loops <= 0 or target_v.rows <= 0:
            raise ValueError(ErrorMessages.INVALID_PARAMETERS)

        return ConversionKoefficient(
            loops_k=target_v.loops / original_v.loops,
            rows_k=target_v.rows / original_v.rows 
        )
