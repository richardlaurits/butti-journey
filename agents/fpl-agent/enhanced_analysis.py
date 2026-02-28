#!/usr/bin/env python3
"""
FPL Analysis Agent - Enhanced Fantasy Football Analysis
Provides expert-level insights with sources, stats, and clear recommendations
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

AGENT_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/fpl-agent')
DATA_FILE = AGENT_DIR / 'richard_team.json'

# Richard's team structure (GW28)
RICHARD_TEAM = {
    "team_name": "FC MACCHIATO",
    "team_id": "17490",
    "current_gameweek": 28,
    "players": {
        "GK": ["Dúbravka"],  # Current
        "DEF": ["Virgil van Dijk", "Gabriel", "Guéhi"],  # Current
        "MID": ["Rice", "Bruno Fernandes", "Rayan", "Rogers"],  # Current
        "FWD": ["Haaland", "Thiago", "João Pedro"]  # Current
    }
}

# Expert recommendations based on current form, fixtures, and stats
EXPERT_ANALYSIS = {
    "sources": ["FPL Scout", "AllAboutFPL", "Brentford Official", "Statbunker"],
    
    "goalkeepers": {
        "current": "Dúbravka",
        "experts_say": {
            "Petrović": {
                "source": "FPL Scout Team",
                "stats": "2 clean sheets, 5 saves points, 4 bonus in last 4 matches",
                "fixture": "BOU - favorable",
                "recommendation": "HIGHER RANKED than Dúbravka"
            },
            "Kelleher": {
                "source": "AllAboutFPL",
                "stats": "Opponent Burnley has worst xG in league, Brentford 6th best xGA",
                "fixture": "BRE vs BUR - excellent",
                "recommendation": "BETTER FIXTURE than Dúbravka"
            }
        },
        "verdict": "UPGRADE - Dúbravka faces strong Brentford, not highly ranked"
    },
    
    "defenders": {
        "current": ["Virgil", "Gabriel", "Guéhi"],
        "experts_say": {
            "Van Dijk": {
                "source": "FPL Scout & AllAboutFPL",
                "stats": "28 points in last 2 GWs",
                "verdict": "KEEP - Form is elite"
            },
            "Gabriel": {
                "source": "FPL Scout Team",
                "verdict": "KEEP - Regular in both scout teams"
            },
            "Guéhi": {
                "source": "Multiple analysts",
                "concerns": ["Not mentioned in any scout teams", "Crystal Palace BLANK in GW31"],
                "verdict": "SELL - Poor value, blank coming"
            },
            "O'Reilly": {
                "source": "Scout recommendations",
                "stats": "Listed as DEF but plays MID, 3 goals in 2 matches, 360k+ new owners",
                "verdict": "TARGET - Hot property"
            },
            "Hill": {
                "source": "Trend reports",
                "stats": "5 straight returns, 3 assists in last 5 starts",
                "verdict": "TARGET - In form"
            }
        }
    },
    
    "midfielders": {
        "current": ["Rice", "Bruno Fernandes", "Rayan", "Rogers"],
        "experts_say": {
            "Bruno Fernandes": {
                "source": "Multiple scouts",
                "stats": "10+ points in all home matches under Carrick",
                "verdict": "KEEP - Elite captain option"
            },
            "Rayan": {
                "source": "Value picks",
                "stats": "2 goals, 1 assist in 4 appearances",
                "verdict": "KEEP - Bargain price"
            },
            "Rice": {
                "source": "Brentford article, AllAboutFPL",
                "concerns": ["Many transferring out ahead of GW31 blank"],
                "verdict": "SELL - Blank GW31"
            },
            "Rogers": {
                "source": "AllAboutFPL",
                "stats": "Blanks in 2 straight matches",
                "verdict": "SELL - Out of form"
            },
            "Mbeumo": {
                "source": "Scout recommendations",
                "stats": "Man United's highest point scorer since manager change",
                "verdict": "TARGET - In form"
            },
            "Wilson": {
                "source": "Ranked highly",
                "stats": "8 goals, 7 assists, 4 matches in a row vs bottom half teams",
                "verdict": "TARGET - Good fixtures"
            }
        }
    },
    
    "forwards": {
        "current": ["Haaland", "Thiago", "João Pedro"],
        "experts_say": {
            "Haaland": {
                "source": "Scout analysis",
                "stats": "Points in 4 straight matches after dry spell",
                "verdict": "KEEP - Form returning, captain material"
            },
            "Thiago": {
                "source": "Transfer trends",
                "stats": "Most bought forward, favorable fixtures vs Burnley & Bournemouth, five double-digit hauls",
                "verdict": "KEEP - Hot property"
            },
            "João Pedro": {
                "source": "Scout article",
                "concerns": ["Can be excluded from captain discussion", "Chelsea faces Arsenal this week"],
                "verdict": "SELL - Tough fixture"
            },
            "Ekitike": {
                "source": "Statbunker",
                "stats": "Most shots (17) and big chances (9) in last 6 GWs, plays West Ham at home",
                "verdict": "TARGET - Elite stats"
            }
        }
    }
}

# Captain recommendations
CAPTAIN_ANALYSIS = {
    "top_options": [
        {
            "player": "Bruno Fernandes",
            "reason": "10+ points in all home matches under Carrick",
            "confidence": "HIGH"
        },
        {
            "player": "Ekitike", 
            "reason": "Elite underlying stats (17 shots, 9 big chances), great fixture",
            "confidence": "HIGH"
        },
        {
            "player": "Haaland",
            "reason": "Returning to form, 4 straight matches with returns",
            "confidence": "MEDIUM"
        }
    ],
    "avoid": ["João Pedro", "Cole Palmer"]  # Chelsea vs Arsenal
}

# Blank GW31 warning
BLANK_GW31_WARNING = {
    "teams_blanking": ["Arsenal", "Wolves", "Man City", "Crystal Palace"],
    "richard_players_affected": ["Guéhi"],  # From current team
    "action_needed": "Transfer out Guéhi before GW31"
}

def format_expert_report():
    """Generate expert-level analysis report"""
    lines = []
    
    lines.append("⚽ **FPL EXPERT ANALYSIS - GW28**")
    lines.append("📊 Based on: FPL Scout, AllAboutFPL, Statbunker, Official Team News")
    lines.append("")
    lines.append("───")
    lines.append("")
    
    # GK Analysis
    lines.append("🧤 **MÅLVAKT**")
    lines.append(f"Din: **Dúbravka** vs Brentford (H)")
    lines.append("⚠️ **Problem:** Möter formstarkt Brentford, inte högt rankad av experter")
    lines.append("")
    lines.append("✅ **Experterna rekommenderar:**")
    lines.append("• **Petrović (BOU)** - FPL Scout Team: 2 nollor, 5 räddningspoäng, 4 bonus senaste 4 matcherna")
    lines.append("• **Kelleher (BRE)** - AllAboutFPL: Burnley har ligans sämsta xG, Brentford 6:e bäst xGA")
    lines.append("👉 **Rekommendation:** BYT till Petrović eller Kelleher")
    lines.append("")
    
    # DEF Analysis
    lines.append("🛡️ **FÖRSVAR**")
    lines.append("Dina: Virgil, Gabriel, **Guéhi**")
    lines.append("")
    lines.append("✅ **BEHÅLL:**")
    lines.append("• **Van Dijk** - 28 poäng senaste 2 omgångarna, i båda Scout-teamen")
    lines.append("• **Gabriel** - Regular i scout-elvor")
    lines.append("")
    lines.append("❌ **SÄLJ:**")
    lines.append("• **Guéhi** - Inte med i några scout-team, Crystal Palace BLANK i GW31")
    lines.append("")
    lines.append("🎯 **TARGETS:**")
    lines.append("• **O'Reilly (MCI)** - Listad som back men spelar mittfält, 3 mål på 2 matcher, 360k+ nya ägare")
    lines.append("• **Hill (BOU)** - 5 raka returns, 3 assists senaste 5 starterna")
    lines.append("")
    
    # MID Analysis
    lines.append("🎮 **MITTFÄLT**")
    lines.append("Dina: **Rice**, Bruno, Rayan, **Rogers**")
    lines.append("")
    lines.append("✅ **BEHÅLL:**")
    lines.append("• **Bruno Fernandes** - 10+ poäng i ALLA hemmamatcher under Carrick, kaptenkandidat")
    lines.append("• **Rayan** - 2 mål, 1 assist på 4 matcher, bra värde")
    lines.append("")
    lines.append("❌ **SÄLJ:**")
    lines.append("• **Rice** - Många byter ut inför GW31 blank (Brentford article)")
    lines.append("• **Rogers** - Blankat i 2 raka matcher (AllAboutFPL)")
    lines.append("")
    lines.append("🎯 **TARGETS:**")
    lines.append("• **Mbeumo** - Uniteds högst poänggivande spelare sedan tränarbytet")
    lines.append("• **Wilson** - 8 mål, 7 assists, 4 matcher i rad mot bottenteam")
    lines.append("")
    
    # FWD Analysis
    lines.append("⚽ **ANFALL**")
    lines.append("Dina: Haaland, Thiago, **João Pedro**")
    lines.append("")
    lines.append("✅ **BEHÅLL:**")
    lines.append("• **Haaland** - Poäng i 4 raka matcher efter torrperiod, kaptenmaterial")
    lines.append("• **Thiago** - Mest köpta forwarden, 5 tvåsiffriga hauls, bra matcher")
    lines.append("")
    lines.append("❌ **SÄLJ:**")
    lines.append("• **João Pedro** - Chelsea möter Arsenal, Scout utesluter från kapten-diskussion")
    lines.append("")
    lines.append("🎯 **TARGET:**")
    lines.append("• **Ekitike (LIV)** - Flest avslut (17) och big chances (9) senaste 6 omgångarna, möter West Ham hemma")
    lines.append("")
    
    # Summary table
    lines.append("───")
    lines.append("")
    lines.append("📋 **SAMMANFATTNING**")
    lines.append("")
    lines.append("| Position | Behåll | Sälj | Target |")
    lines.append("|----------|--------|------|--------|")
    lines.append("| GK | - | Dúbravka | Petrović, Kelleher |")
    lines.append("| DEF | Van Dijk, Gabriel | Guéhi | O'Reilly, Hill |")
    lines.append("| MID | Bruno, Rayan | Rice, Rogers | Mbeumo, Wilson |")
    lines.append("| FWD | Haaland, Thiago | João Pedro | Ekitike |")
    lines.append("")
    
    # Captain
    lines.append("©️ **KAPTEN**")
    lines.append("1. **Bruno Fernandes** - Högst confidence (10+ poäng hemma under Carrick)")
    lines.append("2. **Ekitike** - Elite stats, bra fixture")
    lines.append("3. **Haaland** - Formen tillbaka")
    lines.append("")
    
    # GW31 warning
    lines.append("⚠️ **VIKTIGT: GW31 BLANK**")
    lines.append("Dessa lag spelar inte: Arsenal, Wolves, Man City, Crystal Palace")
    lines.append("**Du har: Guéhi** - Sälj innan GW31!")
    lines.append("")
    
    lines.append("💡 **Din elva är konkurrenskraftig men saknar flera key picks. Prioritera att sälja Guéhi, Rice, Rogers och João Pedro.")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(format_expert_report())
