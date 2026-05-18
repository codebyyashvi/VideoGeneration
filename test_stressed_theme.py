#!/usr/bin/env python3
"""Test the new stressed employee scenario theme"""

from layoffshield_guidelines import APPROVED_VIDEO_THEMES

print("=" * 80)
print("NEW THEME: STRESSED EMPLOYEE SCENARIO")
print("=" * 80)

theme = APPROVED_VIDEO_THEMES.get("stressed_employee_scenario", {})
print("\nTheme Title:", theme.get("theme"))
print("\nKey Messaging:")
for msg in theme.get("messaging", []):
    print(f"  • {msg}")

print("\nVisual Journey:")
for step in theme.get("journey", []):
    print(f"  → {step}")

print("\nDO:")
for do in theme.get("do", []):
    print(f"  ✓ {do}")

print("\nDON'T:")
for dont in theme.get("dont", []):
    print(f"  ✗ {dont}")

print(f"\nTone: {theme.get('tone')}")
print("\n" + "=" * 80)
print("✓ Stressed employee scenario is now available!")
print("✓ Use theme='stressed_employee_scenario' in video generation")
print("=" * 80)

# Now show all available themes
print("\nAll Available Themes:")
for theme_name in APPROVED_VIDEO_THEMES.keys():
    theme_title = APPROVED_VIDEO_THEMES[theme_name].get('theme', 'N/A')
    print(f"  • {theme_name}: '{theme_title}'")
