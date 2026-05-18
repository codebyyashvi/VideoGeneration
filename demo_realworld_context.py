#!/usr/bin/env python3
"""
Demo: Real-World Layoff Context Integration
Shows how LayoffShield videos now include real-world data
"""

import asyncio
from layoff_news_fetcher import (
    fetch_layoff_trends,
    get_layoff_context_for_video,
    get_layoff_statistics,
)


async def main():
    print("\n" + "=" * 80)
    print("LAYOFFSHIELD VIDEO GENERATION - REAL-WORLD CONTEXT INTEGRATION")
    print("=" * 80)
    
    # 1. Show layoff statistics
    print("\n📊 CURRENT LAYOFF STATISTICS")
    print("-" * 80)
    stats = get_layoff_statistics()
    for key, value in stats.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    # 2. Show trends
    print("\n🔴 MAJOR TRENDS IN 2024-2025")
    print("-" * 80)
    trends = await fetch_layoff_trends()
    for i, trend in enumerate(trends.get("major_trends", [])[:5], 1):
        print(f"  {i}. {trend}")
    
    # 3. Show affected roles
    print("\n👥 MOST AFFECTED ROLES")
    print("-" * 80)
    print("  Most at risk:")
    for role in trends.get("most_affected_roles", [])[:4]:
        print(f"    ❌ {role}")
    
    print("\n  Safer roles:")
    for role in trends.get("least_affected_roles", [])[:4]:
        print(f"    ✅ {role}")
    
    # 4. Show affected industries
    print("\n🏢 AFFECTED INDUSTRIES")
    print("-" * 80)
    for industry in trends.get("affected_industries", []):
        print(f"  • {industry}")
    
    # 5. Show actionable insights
    print("\n💡 WHAT THIS MEANS FOR PROFESSIONALS")
    print("-" * 80)
    for insight in trends.get("actionable_insights_for_professionals", []):
        print(f"  ▶ {insight}")
    
    # 6. Show how this is used in videos
    print("\n🎬 HOW THIS CONTEXT IS USED IN VIDEO GENERATION")
    print("-" * 80)
    print("""
When generating a video with /generate-contextual:

1. AI model (Groq/LLaMA 3.3) receives:
   ✓ Your marketing topic (e.g., "Know your layoff risk")
   ✓ Theme instructions (e.g., "stressed_employee_scenario")
   ✓ REAL-WORLD CONTEXT (above data)

2. AI then creates a video prompt that:
   ✓ Addresses actual employee concerns
   ✓ References real market conditions
   ✓ Shows meaningful transformation
   ✓ Feels relevant to what employees are experiencing TODAY

3. Video result:
   ✓ Employee worried about layoffs (real concern) → 
   ✓ Opens LayoffShield and sees their risk score → 
   ✓ Gets clarity based on industry data → 
   ✓ Takes action (empowerment)
""")
    
    # 7. Show API endpoints
    print("\n🔌 NEW API ENDPOINTS AVAILABLE")
    print("-" * 80)
    print("""
  GET /layoff-trends
    → Returns current trends, affected roles, statistics
  
  GET /layoff-context
    → Returns full context for video generation
  
  GET /recommended-themes
    → Shows which themes are most relevant NOW
  
  POST /generate-contextual
    → Generate video WITH real-world context integrated
    → RECOMMENDED for meaningful, relevant videos
""")
    
    # 8. Example workflow
    print("\n📋 RECOMMENDED WORKFLOW")
    print("-" * 80)
    print("""
  1. GET /recommended-themes
     → See which themes are most relevant now
     
  2. GET /layoff-trends
     → Understand what employees are facing
     
  3. POST /generate-contextual
     {
       "topic": "Is my tech job at risk?",
       "theme": "stressed_employee_scenario"
     }
     → Generate contextual video
     
  4. Check status & publish
     → Video is compliance-checked AND context-aware
""")
    
    # 9. Key differences
    print("\n⚖️ OLD vs NEW")
    print("-" * 80)
    print("""
  OLD APPROACH:
    POST /generate
    {
      "topic": "Career readiness"
    }
    → Generic video about career skills
    
  NEW APPROACH:
    POST /generate-contextual
    {
      "topic": "Career readiness",
      "theme": "stressed_employee_scenario"
    }
    → Video that addresses REAL employee anxiety
    → Includes actual market data
    → Feels relevant to 2026 situation
    → Higher emotional impact
""")
    
    print("\n" + "=" * 80)
    print("✅ REAL-WORLD CONTEXT INTEGRATION COMPLETE")
    print("=" * 80)
    print("\nVideos are now:")
    print("  ✓ Compliance-compliant (all checks still enforced)")
    print("  ✓ Context-aware (includes real layoff data)")
    print("  ✓ Employee-relevant (addresses actual concerns)")
    print("  ✓ Emotionally resonant (meaningful transformation)")
    print("  ✓ Meaningful (rooted in real-world situation)")
    print("\nStart generating contextual videos with:")
    print("  POST /generate-contextual")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
