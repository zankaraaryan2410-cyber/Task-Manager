from colorama import Fore, Style, init
from storage import load_task, save_task
from Operations import (
    add_task, view_tasks, sort_by_priority,
    update_task, mark_done, remove_done, search_task
)

init(autoreset=True)

MENU = f"""
{Fore.CYAN}╔══════════════════════════════╗
║       TASK MANAGER           ║
╚══════════════════════════════╝{Style.RESET_ALL}
  {Fore.WHITE}1{Style.RESET_ALL} · View all tasks
  {Fore.WHITE}2{Style.RESET_ALL} · Add task
  {Fore.WHITE}3{Style.RESET_ALL} · Sort by priority
  {Fore.WHITE}4{Style.RESET_ALL} · Update task
  {Fore.WHITE}5{Style.RESET_ALL} · Mark task as Done
  {Fore.WHITE}6{Style.RESET_ALL} · Remove completed tasks
  {Fore.WHITE}7{Style.RESET_ALL} · Search task
  {Fore.RED}0{Style.RESET_ALL} · Exit
"""


def main():
    df = load_task()

    while True:
        print(MENU)
        choice = input("  Enter choice : ").strip()

        if   choice == "1": view_tasks(df)
        elif choice == "2": df = add_task(df);        save_task(df)
        elif choice == "3": sort_by_priority(df)
        elif choice == "4": df = update_task(df);     save_task(df)
        elif choice == "5": df = mark_done(df);       save_task(df)
        elif choice == "6": df = remove_done(df);     save_task(df)
        elif choice == "7": search_task(df)
        elif choice == "0":
            print(Fore.GREEN + "\n  Goodbye!\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "  Invalid choice. Try again." + Style.RESET_ALL)


if __name__ == "__main__":
    main()