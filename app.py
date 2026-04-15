"""
English Dictionary Application – backed by a Radix Trie index.
Supports: add word, delete word, look up definition.
Each operation prints before/after snapshots of the trie.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
from radix_trie import RadixTrie

DATA_FILE = "dictionary_data.json"


# ────────────────────────────────────────────────────────────────────────────
#  Persistence helpers
# ────────────────────────────────────────────────────────────────────────────

def load_data(trie: RadixTrie) -> None:
    """Load saved words from JSON into the trie."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for word, definition in data.items():
            trie.insert(word, definition)
        print(f"[INFO] Loaded {len(data)} word(s) from '{DATA_FILE}'.\n")


def save_data(trie: RadixTrie) -> None:
    """Persist all words to JSON."""
    data = {word: definition for word, definition in trie.all_words()}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ────────────────────────────────────────────────────────────────────────────
#  Core operations  (each prints before / after trie snapshot)
# ────────────────────────────────────────────────────────────────────────────

def op_add(trie: RadixTrie, word: str, definition: str) -> None:
    print("\n" + "─" * 60)
    print(f"  OPERATION: ADD  »  '{word}'")
    print("─" * 60)

    print("\n[BEFORE]\n")
    print(trie.visualize())
    print()

    added = trie.insert(word, definition)

    print("[AFTER]\n")
    print(trie.visualize())
    print()

    if added:
        print(f"✔  Word '{word}' added successfully.")
    else:
        print(f"ℹ  Word '{word}' already existed – definition updated.")
    save_data(trie)


def op_delete(trie: RadixTrie, word: str) -> None:
    print("\n" + "─" * 60)
    print(f"  OPERATION: DELETE  »  '{word}'")
    print("─" * 60)

    # Check before attempting delete
    found = trie.search(word) is not None
    if not found:
        print(f"\n✘  Word '{word}' not found in dictionary. Nothing to delete.\n")
        return

    print("\n[BEFORE]\n")
    print(trie.visualize())
    print()

    trie.delete(word)

    print("[AFTER]\n")
    print(trie.visualize())
    print()
    print(f"✔  Word '{word}' deleted successfully.")
    save_data(trie)


def op_search(trie: RadixTrie, word: str) -> None:
    print("\n" + "─" * 60)
    print(f"  OPERATION: SEARCH  »  '{word}'")
    print("─" * 60)
    print()

    definition = trie.search(word)
    if definition:
        print(f"✔  FOUND: '{word}'")
        print(f"   Definition: {definition}")
    else:
        print(f"✘  '{word}' not found in dictionary.")
    print()


def op_list(trie: RadixTrie) -> None:
    words = trie.all_words()
    print("\n" + "─" * 60)
    print("  ALL WORDS IN DICTIONARY")
    print("─" * 60)
    if not words:
        print("  (empty)")
    for i, (w, d) in enumerate(words, 1):
        short_def = d[:60] + "…" if len(d) > 60 else d
        print(f"  {i:3}. {w:<20}  {short_def}")
    print(f"\n  Total: {len(words)} word(s)")
    print()


# ────────────────────────────────────────────────────────────────────────────
#  Interactive CLI
# ────────────────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════╗
║       English Dictionary (Radix-Trie)    ║
╠══════════════════════════════════════════╣
║  1. Add a word                           ║
║  2. Delete a word                        ║
║  3. Search / Look up a word              ║
║  4. List all words                       ║
║  5. Show trie structure                  ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝
"""


def run_cli():
    trie = RadixTrie()
    load_data(trie)

    while True:
        print(MENU)
        choice = input("  Your choice: ").strip()

        if choice == "1":
            word = input("  Enter word: ").strip()
            if not word:
                print("  Word cannot be empty.")
                continue
            definition = input("  Enter definition: ").strip()
            if not definition:
                print("  Definition cannot be empty.")
                continue
            op_add(trie, word, definition)

        elif choice == "2":
            word = input("  Enter word to delete: ").strip()
            if not word:
                print("  Word cannot be empty.")
                continue
            op_delete(trie, word)

        elif choice == "3":
            word = input("  Enter word to look up: ").strip()
            if not word:
                print("  Word cannot be empty.")
                continue
            op_search(trie, word)

        elif choice == "4":
            op_list(trie)

        elif choice == "5":
            print()
            print(trie.visualize())
            print()

        elif choice == "0":
            print("\n  Goodbye!\n")
            break

        else:
            print("  Invalid choice. Please try again.")


# ────────────────────────────────────────────────────────────────────────────
#  Demo run (non-interactive) – used for testing / README screenshots
# ────────────────────────────────────────────────────────────────────────────

def run_demo():
    print("=" * 60)
    print("  DEMO: English Dictionary backed by Radix-Trie")
    print("=" * 60)

    trie = RadixTrie()

    samples = [
        ("apple",   "A round fruit with red, yellow, or green skin."),
        ("apply",   "To make a formal request; to put into operation."),
        ("apt",     "Appropriate or suitable in the circumstances."),
        ("book",    "A written or printed work consisting of pages."),
        ("boost",   "Help or encourage (something) to increase."),
        ("byte",    "A unit of digital information, typically 8 bits."),
        ("python",  "A high-level programming language."),
        ("program", "A set of instructions for a computer."),
    ]

    for word, defi in samples:
        op_add(trie, word, defi)

    op_search(trie, "apply")
    op_search(trie, "boost")
    op_search(trie, "cat")   # not found

    op_delete(trie, "apt")
    op_delete(trie, "byte")

    op_list(trie)

    print("  Demo complete.")


# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        run_cli()