"""
Example script demonstrating the new selective unpacking feature.

This shows how to use the unpack_folder() method for performance-optimized
selective unpacking instead of extracting everything.
"""

from wowsunpack import WoWsUnpack

# Initialize with your game path
# Replace this with your actual World of Warships installation path
game_path = 'C:/Games/World_of_Warships'

# Create unpacker instance
# Note: This example won't actually run without a valid game path
# unpacker = WoWsUnpack(game_path)

print("=" * 80)
print("Selective Unpacking Examples")
print("=" * 80)

print("\n1. UNPACK ONLY ACHIEVEMENT ICONS")
print("-" * 80)
print("Instead of unpacking all GUI files, extract only achievement icons:")
print(">>> unpacker.unpack_folder('gui/achievements', '*.png')")
print("Benefits: Saves time, reduces disk usage, faster CI/CD")

print("\n2. UNPACK ONLY GAME PARAMETERS")
print("-" * 80)
print("Extract only .data files from content folder:")
print(">>> unpacker.unpack_folder('content', '*.data')")
print("Benefits: Get game params without icons/maps")

print("\n3. UNPACK SPECIFIC SHIP ICONS")
print("-" * 80)
print("Extract ship preview images:")
print(">>> unpacker.unpack_folder('gui/ship_previews', '*.png')")
print("Benefits: Only ship assets, nothing else")

print("\n4. UNPACK WITH EXCLUSIONS")
print("-" * 80)
print("Extract consumable icons but exclude empty placeholders:")
print(">>> unpacker.unpack_folder('gui/consumables', '*.png',")
print("...                        exclude_patterns=['*_empty.png', '*undefined.png'])")
print("Benefits: Filter out unwanted files")

print("\n5. UNPACK ENTIRE FOLDER")
print("-" * 80)
print("Extract all files from a specific folder:")
print(">>> unpacker.unpack_folder('gui/modernization_icons')")
print("Benefits: Cleaner than wild card patterns")

print("\n6. COMPARISON: OLD vs NEW")
print("-" * 80)
print("OLD WAY (slower, unpacks everything):")
print(">>> unpacker.unpackGameGUI()  # Unpacks ALL GUI files")
print("")
print("NEW WAY (faster, selective):")
print(">>> unpacker.unpack_folder('gui/achievements', '*.png')  # Only what you need")

print("\n7. USE CASE: AUTOMATION")
print("-" * 80)
print("For automation that only needs game parameters:")
print("""
# Old way: Unpack everything (slow)
unpacker.reset()
unpacker.unpackGameParams()
unpacker.unpackGameGUI()  # Not needed but was done anyway
unpacker.decodeGameParams()

# New way: Unpack only what's needed (fast)
unpacker.reset()
unpacker.unpack_folder('content', '*.data')  # Only game params
unpacker.decodeGameParams()
""")
print("Performance gain: Can be 5-10x faster depending on what you need!")

print("\n" + "=" * 80)
print("Full API Reference")
print("=" * 80)
print("""
def unpack_folder(
    folder_path: str,              # Folder to unpack (e.g., 'gui', 'content')
    file_pattern: str = '*',       # File pattern (e.g., '*.png', '*.data')
    exclude_patterns: Optional[List[str]] = None  # Patterns to exclude
) -> None

Common folder paths:
  - 'content' - Game parameters and data files
  - 'gui' - All GUI assets
  - 'gui/achievements' - Achievement icons
  - 'gui/ship_previews' - Ship preview images
  - 'gui/modernization_icons' - Upgrade/modernization icons
  - 'gui/consumables' - Consumable icons
  - 'gui/signal_flags' - Signal flag icons
  - 'gui/exteriors/camouflages' - Camouflage icons
  - 'gui/exteriors/permoflages' - Permanent camouflage icons
  - 'gui/crew_commander/skills' - Commander skill icons
  - 'spaces' - Game maps/environments

Common file patterns:
  - '*' - All files (default)
  - '*.png' - PNG images only
  - '*.jpg' - JPG images only
  - '*.data' - Data files only
  - 'icon_*' - Files starting with 'icon_'
  - '*achievement*' - Files containing 'achievement'
""")

print("\n" + "=" * 80)
print("For more information, see the README.md file")
print("=" * 80)
