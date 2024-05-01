import multiprocessing as mp
from gpc_hardware.utils.puppeteer import ProcPipe


class A:
    def _init_(self) -> None:
        print(f"A_ini {mp.current_process().pid}")

    def do_the_thing(self, num: int) -> None:
        print(f"yes!! {num} {mp.current_process().pid}")


if __name__ == "__main__":
    print(f"main thread | {mp.current_process().pid}")
    a: ProcPipe[A] = ProcPipe(A)
    # NOTE in VSCode th following line actually gives nicer auto-completion
    # a: A = ProcPipe(A)
    for i in range(0, 100, 10):
        a.do_the_thing(i)