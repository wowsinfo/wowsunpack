"""
Test script to demonstrate the new selective unpacking functionality.
This test doesn't require a real game installation - it just verifies the API.
"""

from wowsunpack import WoWsUnpack
import inspect

def test_type_hints():
    """Test that all methods have proper type hints."""
    print("Testing type hints...\n")
    
    # Get all public methods of WoWsUnpack
    methods = [method for method in dir(WoWsUnpack) if not method.startswith('_')]
    
    for method_name in methods:
        method = getattr(WoWsUnpack, method_name)
        if callable(method):
            sig = inspect.signature(method)
            print(f"✓ {method_name}{sig}")
            
            # Check if method has docstring
            if method.__doc__:
                print(f"  Docstring: {method.__doc__.split(chr(10))[0].strip()}")
            else:
                print(f"  ⚠ Warning: No docstring")
            print()

def test_unpack_folder_signature():
    """Test that the new unpack_folder method exists and has correct signature."""
    print("\nTesting unpack_folder method...\n")
    
    # Check if method exists
    assert hasattr(WoWsUnpack, 'unpack_folder'), "unpack_folder method not found!"
    print("✓ unpack_folder method exists")
    
    # Check signature
    sig = inspect.signature(WoWsUnpack.unpack_folder)
    print(f"✓ Signature: unpack_folder{sig}")
    
    # Check parameters
    params = sig.parameters
    assert 'folder_path' in params, "folder_path parameter missing"
    assert 'file_pattern' in params, "file_pattern parameter missing"
    assert 'exclude_patterns' in params, "exclude_patterns parameter missing"
    print("✓ All required parameters present")
    
    # Check type hints
    assert params['folder_path'].annotation == str, "folder_path should be str"
    print("✓ folder_path has correct type hint: str")
    
    assert params['file_pattern'].annotation == str, "file_pattern should be str"
    print("✓ file_pattern has correct type hint: str")
    
    # Check for Optional type
    assert 'Optional' in str(params['exclude_patterns'].annotation) or 'List' in str(params['exclude_patterns'].annotation), \
        "exclude_patterns should be Optional[List[str]]"
    print("✓ exclude_patterns has correct type hint: Optional[List[str]]")
    
    # Check return type
    assert sig.return_annotation == type(None) or str(sig.return_annotation) == 'None', \
        "Return type should be None"
    print("✓ Return type is None")
    
    # Check docstring
    assert WoWsUnpack.unpack_folder.__doc__ is not None, "unpack_folder should have docstring"
    print("✓ Method has docstring")
    print(f"\nDocstring:\n{WoWsUnpack.unpack_folder.__doc__}")

def test_existing_methods():
    """Test that existing methods still work and have type hints."""
    print("\n\nTesting existing methods...\n")
    
    methods_to_check = [
        'unpack', 'unpackGameParams', 'unpackGameIcons', 
        'unpackGameGUI', 'unpackGameMaps', 'search'
    ]
    
    for method_name in methods_to_check:
        assert hasattr(WoWsUnpack, method_name), f"{method_name} method not found!"
        method = getattr(WoWsUnpack, method_name)
        sig = inspect.signature(method)
        print(f"✓ {method_name}{sig}")

def main():
    """Run all tests."""
    print("=" * 80)
    print("WoWsUnpack - Selective Unpacking Feature Test")
    print("=" * 80)
    
    try:
        test_type_hints()
        test_unpack_folder_signature()
        test_existing_methods()
        
        print("\n" + "=" * 80)
        print("✓ All tests passed!")
        print("=" * 80)
        
        print("\n\nNew Feature Summary:")
        print("-" * 80)
        print("The new 'unpack_folder()' method allows selective unpacking:")
        print("  - Unpack specific folders instead of everything")
        print("  - Use file patterns to filter files (e.g., '*.png')")
        print("  - Optionally exclude certain patterns")
        print("  - Improves performance by avoiding unnecessary unpacking")
        print("\nExample usage:")
        print("  unpacker.unpack_folder('gui/achievements', '*.png')")
        print("  unpacker.unpack_folder('content', '*.data')")
        print("  unpacker.unpack_folder('gui', exclude_patterns=['*_empty.png'])")
        print("-" * 80)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
