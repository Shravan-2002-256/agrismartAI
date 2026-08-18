"""
Irrigation Calculator Service
Calculates water requirements based on crop, soil, weather, and growth stage
"""
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class IrrigationCalculatorService:
    """
    AI-powered irrigation calculator
    Calculates optimal water requirements and scheduling
    """
    
    def __init__(self):
        # Crop water requirements (mm/day during peak growth)
        self.crop_water_requirements = {
            'rice': {'kc_initial': 1.05, 'kc_mid': 1.20, 'kc_end': 0.90, 'root_depth': 0.5},
            'wheat': {'kc_initial': 0.30, 'kc_mid': 1.15, 'kc_end': 0.40, 'root_depth': 1.5},
            'corn': {'kc_initial': 0.30, 'kc_mid': 1.20, 'kc_end': 0.60, 'root_depth': 1.5},
            'tomato': {'kc_initial': 0.60, 'kc_mid': 1.15, 'kc_end': 0.80, 'root_depth': 1.0},
            'potato': {'kc_initial': 0.50, 'kc_mid': 1.15, 'kc_end': 0.75, 'root_depth': 0.6},
            'cotton': {'kc_initial': 0.35, 'kc_mid': 1.15, 'kc_end': 0.70, 'root_depth': 1.5},
            'sugarcane': {'kc_initial': 0.40, 'kc_mid': 1.25, 'kc_end': 0.75, 'root_depth': 1.2},
            'banana': {'kc_initial': 0.50, 'kc_mid': 1.10, 'kc_end': 1.00, 'root_depth': 0.9},
            'onion': {'kc_initial': 0.70, 'kc_mid': 1.05, 'kc_end': 0.85, 'root_depth': 0.4},
            'cabbage': {'kc_initial': 0.70, 'kc_mid': 1.05, 'kc_end': 0.95, 'root_depth': 0.5},
        }
        
        # Soil water holding capacity (mm/m)
        self.soil_water_capacity = {
            'sandy': 60,
            'loamy': 140,
            'clay': 180,
            'silt': 150
        }
        
        logger.info(" Irrigation Calculator initialized")
    
    def calculate_et0(self, temperature: float, humidity: float, wind_speed: float = 2.0) -> float:
        """
        Calculate reference evapotranspiration (ET0) using simplified Penman-Monteith
        """
        # Simplified calculation for demo
        # Use abs() to prevent complex numbers when humidity > temperature
        temp_diff = abs(temperature - humidity)
        et0 = 0.0023 * (temperature + 17.8) * (temp_diff ** 0.5) * wind_speed
        return max(0, et0)
    
    def calculate_irrigation(
        self,
        crop_type: str,
        soil_type: str,
        area_acres: float,
        growth_stage: str,
        temperature: float,
        humidity: float,
        rainfall_last_week: float = 0,
        irrigation_efficiency: float = 0.75
    ) -> Dict:
        """
        Calculate irrigation requirements
        
        Args:
            crop_type: Type of crop
            soil_type: sandy/loamy/clay/silt
            area_acres: Field area in acres
            growth_stage: initial/development/mid/late
            temperature: Current temperature (°C)
            humidity: Current humidity (%)
            rainfall_last_week: Rainfall in last 7 days (mm)
            irrigation_efficiency: System efficiency (0-1)
        """
        try:
            crop_type = crop_type.lower()
            soil_type = soil_type.lower()
            
            # Validate inputs
            if irrigation_efficiency <= 0 or irrigation_efficiency > 1:
                logger.warning(f"Invalid irrigation_efficiency: {irrigation_efficiency}, using default 0.75")
                irrigation_efficiency = 0.75  # Default to 75% efficiency
            
            if area_acres <= 0:
                return {"success": False, "error": "Field area must be greater than 0"}
            
            if temperature < -10 or temperature > 60:
                return {"success": False, "error": "Temperature must be between -10°C and 60°C"}
            
            if humidity < 0 or humidity > 100:
                return {"success": False, "error": "Humidity must be between 0% and 100%"}
            
            # Get crop coefficients
            if crop_type not in self.crop_water_requirements:
                crop_type = 'tomato'  # default
            
            crop_data = self.crop_water_requirements[crop_type]
            
            # Select Kc based on growth stage
            stage_kc_map = {
                'initial': crop_data['kc_initial'],
                'development': (crop_data['kc_initial'] + crop_data['kc_mid']) / 2,
                'mid': crop_data['kc_mid'],
                'late': crop_data['kc_end']
            }
            kc = stage_kc_map.get(growth_stage, crop_data['kc_mid'])
            
            # Calculate ET0 (reference evapotranspiration)
            et0 = self.calculate_et0(temperature, humidity)
            
            # Calculate crop water requirement (ETc = ET0 × Kc)
            etc = et0 * kc  # mm/day
            
            # Ensure etc is not zero to avoid division by zero
            if etc <= 0:
                etc = 0.5  # Minimum value to prevent division errors
            
            # Weekly requirement
            weekly_requirement_mm = etc * 7
            
            # Adjust for rainfall
            effective_rainfall = rainfall_last_week * 0.8  # 80% efficiency
            net_requirement_mm = max(0, weekly_requirement_mm - effective_rainfall)
            
            # Convert to volume (cubic meters)
            area_m2 = area_acres * 4046.86  # 1 acre = 4046.86 m²
            water_volume_m3 = (net_requirement_mm / 1000) * area_m2
            water_volume_liters = water_volume_m3 * 1000
            
            # Account for irrigation efficiency
            actual_water_needed_m3 = water_volume_m3 / irrigation_efficiency
            actual_water_needed_liters = actual_water_needed_m3 * 1000
            
            # Soil water capacity and irrigation scheduling
            soil_capacity = self.soil_water_capacity.get(soil_type, 140)  # mm/m
            root_depth = crop_data['root_depth']  # meters
            
            # Available Water Capacity in root zone
            total_awc_mm = soil_capacity * root_depth
            
            # Management Allowed Depletion (MAD) - 50% for most crops
            mad_fraction = 0.5  # Allow 50% depletion before irrigating
            if crop_type in ['rice']:
                mad_fraction = 0.3  # More frequent for rice
            elif crop_type in ['cotton', 'sugarcane']:
                mad_fraction = 0.6  # Less frequent for hardy crops
            
            # Available water before irrigation needed
            allowed_depletion_mm = total_awc_mm * mad_fraction
            
            # Calculate irrigation frequency (days between irrigations)
            days_until_next = max(2, min(10, int(allowed_depletion_mm / etc)))
            # Constrain to practical range: 2-10 days
            
            # Per-irrigation application depth (replenish depleted water)
            per_irrigation_mm = etc * days_until_next
            per_irrigation_m3 = (per_irrigation_mm / 1000) * area_m2
            per_irrigation_liters = per_irrigation_m3 * 1000 / irrigation_efficiency
            
            # Generate schedule
            schedule = self._generate_schedule(days_until_next, per_irrigation_liters)
            
            return {
                "success": True,
                "crop_type": crop_type.capitalize(),
                "soil_type": soil_type.capitalize(),
                "growth_stage": growth_stage.capitalize(),
                "calculations": {
                    "et0_mm_per_day": round(et0, 2),
                    "crop_coefficient_kc": round(kc, 2),
                    "crop_water_requirement_mm_per_day": round(etc, 2),
                    "weekly_requirement_mm": round(weekly_requirement_mm, 2),
                    "effective_rainfall_mm": round(effective_rainfall, 2),
                    "net_water_needed_mm": round(net_requirement_mm, 2),
                    "water_volume_cubic_meters": round(actual_water_needed_m3, 2),
                    "water_volume_liters": round(actual_water_needed_liters, 2)
                },
                "recommendations": {
                    "irrigation_frequency_days": days_until_next,
                    "water_per_irrigation_liters": round(per_irrigation_liters, 2),
                    "water_per_irrigation_cubic_meters": round(per_irrigation_liters / 1000, 2),
                    "irrigation_depth_mm": round(per_irrigation_mm, 2),
                    "irrigation_efficiency_percent": int(irrigation_efficiency * 100)
                },
                "schedule": schedule,
                "tips": self._get_irrigation_tips(crop_type, soil_type, growth_stage)
            }
            
        except Exception as e:
            logger.error(f"Irrigation calculation error: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_schedule(self, frequency_days: int, water_per_irrigation: float) -> List[Dict]:
        """Generate 2-week irrigation schedule"""
        schedule = []
        for day in range(1, 15, frequency_days):
            schedule.append({
                "day": day,
                "water_liters": round(water_per_irrigation, 2),
                "morning_recommended": True,
                "notes": "Water early morning (6-8 AM) to reduce evaporation"
            })
        return schedule
    
    def _get_irrigation_tips(self, crop_type: str, soil_type: str, growth_stage: str) -> List[str]:
        """Get irrigation tips"""
        tips = [
            "Water early morning (6-8 AM) or evening (4-6 PM) to minimize evaporation",
            "Check soil moisture before irrigating - insert finger 2-3 inches deep",
            "Monitor plants for wilting signs, especially during midday"
        ]
        
        if soil_type == 'sandy':
            tips.append("Sandy soil drains quickly - irrigate more frequently with less water")
        elif soil_type == 'clay':
            tips.append("Clay soil holds water - irrigate less frequently but deeply")
        
        if growth_stage == 'initial':
            tips.append("Initial stage: Keep soil consistently moist for germination")
        elif growth_stage == 'mid':
            tips.append("Mid-season: Peak water demand - don't miss irrigations!")
        elif growth_stage == 'late':
            tips.append("Late stage: Reduce watering to improve quality and prepare for harvest")
        
        if crop_type in ['rice']:
            tips.append("Rice: Maintain 2-5 cm standing water during vegetative stage")
        elif crop_type in ['tomato', 'potato']:
            tips.append("Consistent moisture prevents blossom end rot and fruit cracking")
        
        return tips

# Global instance
irrigation_calculator = IrrigationCalculatorService()
