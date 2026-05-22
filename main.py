import sys
from speech import wake_word_listener
from led import cleanup

if __name__ == "__main__":
    try:
        wake_word_listener()
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        cleanup()
        sys.exit(0)