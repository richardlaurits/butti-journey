"""
FPL Chip Status Extractor
==========================

Automatically fetches and parses chip status from FPL API.
Handles H1 vs H2 distinction correctly.

Usage:
    from chip_extractor import ChipExtractor
    status = ChipExtractor.get_chip_status(17490)
    print(status)
"""

import requests
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


class ChipType(Enum):
    """FPL Chip Types"""
    WILDCARD = "wildcard"
    BENCH_BOOST = "bboost"
    TRIPLE_CAPTAIN = "3xc"
    FREE_HIT = "freehit"


class Half(Enum):
    """FPL Season Halves"""
    H1 = "H1"  # GW1-19
    H2 = "H2"  # GW20-38


class ChipExtractor:
    """Extract and parse FPL chip status from API"""
    
    API_ENDPOINT = "https://fantasy.premierleague.com/api/entry/{team_id}/history/"
    ALL_CHIPS = [
        ChipType.WILDCARD.value,
        ChipType.BENCH_BOOST.value,
        ChipType.TRIPLE_CAPTAIN.value,
        ChipType.FREE_HIT.value
    ]
    
    CHIP_NAMES = {
        "wildcard": "Wildcard",
        "bboost": "Bench Boost",
        "3xc": "3x Captain",
        "freehit": "Free Hit"
    }
    
    @staticmethod
    def determine_half(gameweek: int) -> str:
        """
        Determine if a gameweek is in H1 or H2.
        
        Args:
            gameweek: Gameweek number (1-38)
            
        Returns:
            "H1" for GW1-19, "H2" for GW20-38
        """
        if gameweek <= 19:
            return Half.H1.value
        else:
            return Half.H2.value
    
    @staticmethod
    def get_chip_status(team_id: int, timeout: int = 10) -> Dict:
        """
        Fetch and parse chip status for a team.
        
        Args:
            team_id: FPL team ID
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with chip status breakdown:
            {
                "success": bool,
                "team_id": int,
                "used": {
                    "H1": [...],
                    "H2": [...]
                },
                "remaining": {
                    "H1": [...],
                    "H2": [...]
                },
                "summary": {...}
            }
        """
        try:
            url = ChipExtractor.API_ENDPOINT.format(team_id=team_id)
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            chips_array = data.get("chips", [])
            
            return ChipExtractor._parse_chips(team_id, chips_array)
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "team_id": team_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
        except Exception as e:
            return {
                "success": False,
                "team_id": team_id,
                "error": str(e),
                "error_type": "UnknownError"
            }
    
    @staticmethod
    def _parse_chips(team_id: int, chips_array: List[Dict]) -> Dict:
        """
        Parse chips array into structured format.
        
        Args:
            team_id: FPL team ID
            chips_array: List of used chips from API
            
        Returns:
            Structured chip status
        """
        used_chips = {Half.H1.value: [], Half.H2.value: []}
        
        # Parse used chips
        for chip in chips_array:
            chip_name = chip.get("name", "")
            gameweek = chip.get("event", 0)
            timestamp = chip.get("time", "")
            
            half = ChipExtractor.determine_half(gameweek)
            
            used_chips[half].append({
                "name": chip_name,
                "human_name": ChipExtractor.CHIP_NAMES.get(chip_name, chip_name),
                "gameweek": gameweek,
                "timestamp": timestamp
            })
        
        # Calculate remaining chips
        remaining_chips = {Half.H1.value: [], Half.H2.value: []}
        
        for half in [Half.H1.value, Half.H2.value]:
            used_names = {chip["name"] for chip in used_chips[half]}
            remaining_chips[half] = [
                {
                    "name": chip_name,
                    "human_name": ChipExtractor.CHIP_NAMES.get(chip_name, chip_name)
                }
                for chip_name in ChipExtractor.ALL_CHIPS
                if chip_name not in used_names
            ]
        
        return {
            "success": True,
            "team_id": team_id,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "used": used_chips,
            "remaining": remaining_chips,
            "summary": ChipExtractor._build_summary(used_chips, remaining_chips)
        }
    
    @staticmethod
    def _build_summary(used_chips: Dict, remaining_chips: Dict) -> Dict:
        """Build human-readable summary"""
        return {
            "H1": {
                "status": "Complete" if len(remaining_chips["H1"]) == 0 else "In Progress",
                "used_count": len(used_chips["H1"]),
                "remaining_count": len(remaining_chips["H1"]),
                "remaining_list": [c["human_name"] for c in remaining_chips["H1"]]
            },
            "H2": {
                "status": "Complete" if len(remaining_chips["H2"]) == 0 else "In Progress",
                "used_count": len(used_chips["H2"]),
                "remaining_count": len(remaining_chips["H2"]),
                "remaining_list": [c["human_name"] for c in remaining_chips["H2"]]
            },
            "overall": {
                "total_used": len(used_chips["H1"]) + len(used_chips["H2"]),
                "total_remaining": len(remaining_chips["H1"]) + len(remaining_chips["H2"])
            }
        }
    
    @staticmethod
    def format_output(status: Dict, format_type: str = "pretty") -> str:
        """
        Format chip status for display.
        
        Args:
            status: Chip status dictionary
            format_type: "pretty", "json", or "text"
            
        Returns:
            Formatted string
        """
        if not status.get("success", False):
            return f"❌ Error fetching chips: {status.get('error', 'Unknown error')}"
        
        if format_type == "json":
            return json.dumps(status, indent=2)
        
        elif format_type == "text":
            lines = [
                f"Team {status['team_id']} Chip Status",
                "=" * 40,
                "",
                "🏁 H1 (GW1-19):",
                f"  Status: {status['summary']['H1']['status']}",
                f"  Used: {status['summary']['H1']['used_count']}/4",
                f"  Remaining: {', '.join(status['summary']['H1']['remaining_list']) if status['summary']['H1']['remaining_list'] else 'None'}",
                "",
                "🏁 H2 (GW20-38):",
                f"  Status: {status['summary']['H2']['status']}",
                f"  Used: {status['summary']['H2']['used_count']}/4",
                f"  Remaining: {', '.join(status['summary']['H2']['remaining_list']) if status['summary']['H2']['remaining_list'] else 'None'}",
                "",
                "📊 Overall:",
                f"  Total Used: {status['summary']['overall']['total_used']}/8",
                f"  Total Remaining: {status['summary']['overall']['total_remaining']}/8"
            ]
            return "\n".join(lines)
        
        else:  # pretty format
            lines = [
                f"🎯 **Chip Status: Team {status['team_id']}**",
                "",
                "**H1 (GW1-19)** " + ("✅ Complete" if status['summary']['H1']['remaining_count'] == 0 else "🔄 In Progress"),
                f"├─ Used: {status['summary']['H1']['used_count']}/4",
                f"└─ Remaining: {', '.join(status['summary']['H1']['remaining_list']) if status['summary']['H1']['remaining_list'] else '❌ All used'}",
                "",
                "**H2 (GW20-38)** " + ("✅ Complete" if status['summary']['H2']['remaining_count'] == 0 else "🔄 In Progress"),
                f"├─ Used: {status['summary']['H2']['used_count']}/4",
                f"└─ Remaining: {', '.join(status['summary']['H2']['remaining_list']) if status['summary']['H2']['remaining_list'] else '❌ All used'}",
            ]
            return "\n".join(lines)


def main():
    """Example usage"""
    # Test with Team 17490 (Richard's team)
    team_id = 17490
    
    print(f"Fetching chip status for Team {team_id}...")
    status = ChipExtractor.get_chip_status(team_id)
    
    if status.get("success"):
        print("\n" + ChipExtractor.format_output(status, format_type="pretty"))
        print("\n" + ChipExtractor.format_output(status, format_type="text"))
    else:
        print(f"Error: {status.get('error')}")


if __name__ == "__main__":
    main()
