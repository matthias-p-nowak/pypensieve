print(f"starting " + __file__)
import pensieve
import tkinter as tk


def main():
    root = tk.Tk()
    pensieve.Pensieve(root, "root.window.main", "geometry")
    root.mainloop()


if __name__ == "__main__":
    main()
    print(f"exiting " + __file__)
