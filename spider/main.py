"""爬题模块"""
from InitProblems import init_problems_multithreading
from initOJs import init_remote_ojs


def main():
    init_remote_ojs()
    init_problems_multithreading()


if __name__ == '__main__':
    main()
